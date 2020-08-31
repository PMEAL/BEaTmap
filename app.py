import texts
import beatmap as bt
import pandas as pd
import numpy as np
import scipy as sp
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams
from stateful import *
import altair as alt


st.set_option('deprecation.showfileUploaderEncoding', False)
rcParams["axes.formatter.limits"] = 0, 0
rcParams['font.sans-serif'] = [
    'Lucida Sans Unicode', 'Lucida Grande', 'DejaVu Sans', 'Tahoma'
]


def main():
    state = _get_state()
    pages = {
        "About": page_about,
        "BEaTmap Analysis": page_beatmap,
        "Supplimental Analysis": page_supplimental,
        # "References": page_references
    }

    st.sidebar.title(":maple_leaf: BEaTmap")
    st.sidebar.markdown(texts.intro_sidebar)
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks w/ widgets, must be called at the end the app
    state.sync()


def page_about(state):
    r"""BEaTmap quick summary"""
    st.markdown("# :maple_leaf: BEaTmap")
    st.markdown(texts.intro)
    st.markdown("# :duck: Getting started")
    st.markdown(texts.getting_started)
    st.markdown("# :books: References")
    st.markdown(texts.references)


def page_beatmap(state):
    r"""File uploader widget"""
    st.markdown("# :maple_leaf: BEaTmap Analysis")
    st.markdown("## :file_folder: Upload isotherm data")
    st.markdown(texts.upload_instruction)
    state.uploaded_file = st.file_uploader(
        label="Upload a CSV file", type="csv"
    )
    upload_success = st.empty()
    st.markdown("### Adsorbate area")
    st.markdown(texts.area_instruction)
    state.a_o = st.number_input(
        label="Enter adsorbate cross-sectional area (Angstrom per molecule)",
        value=state.a_o or 16.2
    )
    if state.uploaded_file and state.a_o:
        upload_success.success("File uploaded!")
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(state.uploaded_file, state.a_o)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        experimental_data_plot(state.isotherm_data)

    st.markdown("## :wrench: Settings")
    st.markdown("## Model assumptions")
    try:
        state.check_values = [value for value in state.checks]
    except TypeError:
        state.check_values = [True] * 5
    state.checks = [
        st.checkbox(
            label=texts.checks[i], value=state.check_values[i]
        ) for i in range(5)
    ]
    state.points = st.slider(
        label="Minimum number of points",
        min_value=2,
        max_value=27,
        value=state.points
    )
    st.markdown("## BET calculation criteria")
    options = ["Minimum error", "Maximum data points"]
    state.criterion = st.radio(
        label="Select the BET calculation criteria:",
        options=options,
        index=options.index(state.criterion) if state.criterion else 0
    )
    if state.criterion == "Minimum error":
        state.criterion_str = "error"
    else:
        state.criterion_str = "points"

    st.markdown("## :straight_ruler:BET analysis")
    # Bypass calculations if no data is found
    if not state.bet_results:
        st.error("You need to upload isotherm data first!")
        return
    state.mask_results = bt.core.rouq_mask(
        intercept=state.bet_results.intercept,
        iso_df=state.bet_results.iso_df,
        nm=state.bet_results.nm,
        slope=state.bet_results.slope,
        check1=state.checks[0],
        check2=state.checks[1],
        check3=state.checks[2],
        check4=state.checks[3],
        check5=state.checks[4],
        points=state.points
    )
    ssa_answer = bt.core.ssa_answer(
        state.bet_results, state.mask_results, state.criterion_str
    )
    st.success(f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")
    # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
    st.markdown(r"## Specific surface area heatmap")
    st.markdown(texts.ssa_instruction)
    plot_ssa_heatmap(state.bet_results, state.mask_results)
    st.markdown(r"## BET plot")
    bet_plot(state.bet_results, state.mask_results, ssa_answer)


def page_supplimental(state):
    r"""Supplimental analysis"""
    st.markdown("# :chart_with_upwards_trend: Supplimental analysis")
    # Bypass calculations if no data is found
    if not state.bet_results:
        st.error("You need to upload isotherm data first!")
        return
    ssa_table, c_table, ssa_ssd, c_std = bt.vis.dataframe_tables(
        state.bet_results, state.mask_results
    )
    ssa_table.set_index(' ', inplace=True)
    c_table.set_index(' ', inplace=True)
    st.markdown("## Specific surface area")
    st.success(f"Standard deviation of specific surface area: **{ssa_ssd:.3f}** $m^2/g$")
    st.write(ssa_table)
    st.markdown("## BET constant (C)")
    st.success(f"Standard deviation of BET constant (C): **{c_std:.3f}**")
    st.write(c_table)
    st.markdown("## Isotherm combination plot")
    st.markdown(texts.iso_combo_instruction)
    iso_combo_plot(state.bet_results, state.mask_results)
    st.markdown("## BET minimum and maxium error plot")
    st.markdown(texts.bet_combo_instruction)
    bet_combo_plot(state.bet_results, state.mask_results)
    st.markdown("## Error heatmap")
    st.markdown(texts.err_instruction)
    plot_err_heatmap(state.bet_results, state.mask_results)



def page_references(state):
    r"""References used in BEaTmap"""
    st.markdown("# :books: References")
    st.markdown(texts.references)


@st.cache(allow_output_mutation=True)
def fetch_isotherm_data(uploaded_file, a_o):
    r"""Extracts and returns isotherm data given a .csv file (or buffer)"""
    isotherm_data = bt.io.import_data(uploaded_file, info="test", a_o=a_o)
    return isotherm_data


@st.cache(allow_output_mutation=False)
def fetch_bet_results(isotherm_data):
    r"""Analyzes isotherm data and returns results as a named tuple"""
    bet_results = bt.core.bet(
        isotherm_data.iso_df,
        isotherm_data.a_o,
        isotherm_data.info
    )
    return bet_results


# def plot_isotherm_data(isotherm_data):
#     r"""Plot BET experimental isotherm data"""
#     source = pd.DataFrame(
#         {
#             "P/Po": isotherm_data.iso_df.relp,
#             "n (mol/g)": isotherm_data.iso_df.n
#         }
#     )
#     temp = alt.Chart(source).mark_point().encode(
#         y=alt.Y("n (mol/g)", axis=alt.Axis(format='~e', tickCount=len(source)/4)),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1'))
#     ).configure_view(
#         strokeWidth = 0
#     ).configure_mark(
#         opacity=0.7
#     ).configure_axis(
#         labelFontSize=20,
#         titleFontSize=20,
#         grid=False
#     ).properties(
#         title="Experimental isotherm data",
#         height=600,
#         width=600
#     ).configure_title(
#         fontSize=24
#     )
#     st.altair_chart(temp, use_container_width=True)


def plot_ssa_heatmap(bet_results, mask_results):
    r"""Plot SSA heatmap"""
    x, y = np.meshgrid(bet_results.iso_df.relp, bet_results.iso_df.relp)
    axis_values = bet_results.iso_df.relp.values.tolist()
    temp = np.round(bet_results.ssa.copy(),2)
    temp[mask_results.mask] = 0
    dmin = np.amin(temp[~mask_results.mask])
    dmax = np.amax(temp[~mask_results.mask])
    source = pd.DataFrame(
        {
            "Start relative pressure": x.ravel(),
            "End relative pressure": y.ravel(),
            "SSA": temp.ravel()
        }
    )
    hmap = alt.Chart(source).mark_rect(stroke='gray', strokeWidth=0.5).encode(
        x=alt.X(
            "Start relative pressure:O",
            sort=alt.EncodingSortField(
                "Start relative pressure",
                order="ascending",
            ),
            axis=alt.Axis(tickCount=10, labelSeparation=10, tickMinStep=1)
        ),
        y=alt.Y(
            "End relative pressure:O",
            sort=alt.EncodingSortField(
                "End relative pressure",
                order="descending"
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=10)
        ),
        color=alt.Color("SSA:Q", scale=alt.Scale(domain=[dmin, dmax], scheme="Greens")),
        # color=alt.Color('z:Q', scale=alt.Scale(range=["white", "green"]))
        tooltip=['SSA','Start relative pressure', 'End relative pressure']
    ).configure_view(
        strokeWidth = 0
    ).configure_scale(
        bandPaddingInner=0.15
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20,
        domainColor='white'
    ).properties(
        title="Specific surface area [m^2/g]",
    ).configure_title(
        fontSize=24
    ).configure_legend(
        padding=10,
        strokeColor='white',
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=20,
        gradientLength=250,
        tickCount=5,
        offset=40
    ).interactive()

    st.altair_chart(hmap)

def plot_err_heatmap(bet_results, mask_results):
    r"""Plot Error heatmap"""
    x, y = np.meshgrid(bet_results.iso_df.relp, bet_results.iso_df.relp)
    axis_values = bet_results.iso_df.relp.values.tolist()
    temp = np.round(bet_results.err.copy(), 2)
    temp[mask_results.mask] = 0
    dmin = np.amin(temp[~mask_results.mask])
    dmax = np.amax(temp[~mask_results.mask])
    source = pd.DataFrame(
        {
            "Start relative pressure": x.ravel(),
            "End relative pressure": y.ravel(),
            "Error": temp.ravel()
        }
    )
    hmap = alt.Chart(source).mark_rect(stroke='gray', strokeWidth=0.5).encode(
        x=alt.X(
            "Start relative pressure:O",
            sort=alt.EncodingSortField(
                "Start relative pressure",
                order="ascending",
            ),
            axis=alt.Axis(tickCount=10, labelSeparation=10, tickMinStep=1)
        ),
        y=alt.Y(
            "End relative pressure:O",
            sort=alt.EncodingSortField(
                "End relative pressure",
                order="descending"
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=10)
        ),
        color=alt.Color("Error:Q", scale=alt.Scale(domain=[dmin, dmax], scheme="Greys")),
        # color=alt.Color('Error:Q', scale=alt.Scale(range=["white", "green"]))
        tooltip=['Error','Start relative pressure', 'End relative pressure']
    ).configure_view(
        strokeWidth = 0
    ).configure_scale(
        bandPaddingInner=0.15
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20,
        domainColor = 'white'
    ).properties(
        title="Error",
    ).configure_title(
        fontSize=24
    ).configure_legend(
        padding=10,
        strokeColor='white',
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=20,
        gradientLength=250,
        tickCount=5,
        offset=40
    )
    st.altair_chart(hmap)

# def plot_isotherm_combo(bet_results, mask_results):
#     r"""Plot BET experimental isotherm data"""
    
#     mask = mask_results.mask

#     if mask.all() == True:
#         print('No valid relative pressure ranges. BET isotherm \
# combo plot not created.')
#         return
    
#     df = bet_results.iso_df
#     nm = np.ma.array(bet_results.nm, mask=mask)
#     c = np.ma.array(bet_results.c, mask=mask)
#     err = np.ma.array(bet_results.err, mask=mask)

#     err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)
#     c_min_err = c[err_min_idx[0], err_min_idx[1]]

#     nnm_min = nm[err_min_idx[0], err_min_idx[1]]
#     ppo = np.arange(0, .9001, .001)
#     synth_min = 1 / (1 - ppo) - 1 / (1 + (c_min_err - 1) * ppo)
#     expnnm_min = df.n / nnm_min
    
#     err_min_i = int(err_min_idx[0] + 1)
#     err_min_j = int(err_min_idx[1])
#     expnnm_min_used = expnnm_min[err_min_j:err_min_i]
#     ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]
    
#     model_source = pd.DataFrame(
#         {
#             "P/Po": ppo,
#             "n (mol/g)": synth_min
#         }
#     )
#     model = alt.Chart(model_source).mark_line().encode(
#         y=alt.Y("n (mol/g)"),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1')))
    
#     experimental_source = pd.DataFrame(
#         {
#             "P/Po": bet_results.iso_df.relp,
#             "n (mol/g)": expnnm_min
#         }
#     )
#     experimental = alt.Chart(experimental_source).mark_point().encode(
#         y=alt.Y("n (mol/g)"),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1')))
    
#     experimental_used_source = pd.DataFrame(
#         {
#             "P/Po": ppo_expnnm_min_used,
#             "n (mol/g)": expnnm_min_used
#         }
#     )
#     experimental_used = alt.Chart(experimental_used_source).mark_point().encode(
#         y=alt.Y("n (mol/g)"),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1')))
    
#     st.altair_chart(model+experimental+experimental_used, use_container_width=True)
    
# def plot_bet_combo_plot(bet_results, mask_results):
#     mask = mask_results.mask

#     if mask.all() == True:
#         print('No valid relative pressure ranges. BET combo plot not created.')
#     return

#     df = bet_results.iso_df
#     err = np.ma.array(bet_results.err, mask=mask)

#     err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)

#     min_start = int(err_min_idx[1])
#     min_stop = int(err_min_idx[0])
#     max_start = int(err_max_idx[1])
#     max_stop = int(err_max_idx[0])

#     slope, intercept, r_val, p_value, std_err =\
#         sp.stats.linregress(df.relp[min_start: min_stop + 1],
#                             df.bet[min_start:min_stop + 1])

#     min_liney = np.zeros(2)
#     min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
#     min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
#     min_linex = np.zeros(2)
#     min_linex[0] = df.relp[min_start] - .01
#     min_linex[1] = df.relp[min_stop] + .01

#     slope_max, intercept_max, r_value_max, p_value_max, std_err_max = \
#         sp.stats.linregress(df.relp[max_start: max_stop + 1],
#                             df.bet[max_start: max_stop + 1])
#     max_liney = np.zeros(2)
#     max_liney[0] = slope_max * (df.relp[max_start] - .01) + intercept_max
#     max_liney[1] = slope_max * (df.relp[max_stop] + .01) + intercept_max
#     max_linex = np.zeros(2)
#     max_linex[0] = df.relp[max_start] - .01
#     max_linex[1] = df.relp[max_stop] + .01
    
#     minline_source = pd.DataFrame(
#         {
#             "P/Po": min_linex,
#             "n (mol/g)": min_liney
#         }
#     )
#     model = alt.Chart(model_source).mark_line().encode(
#         y=alt.Y("n (mol/g)"),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1')))
    
#     maxline_source = pd.DataFrame(
#         {
#             "P/Po": max_linex,
#             "n (mol/g)": max_liney
#         }
#     )
#     model = alt.Chart(model_source).mark_line().encode(
#         y=alt.Y("n (mol/g)"),
#         x=alt.X("P/Po", axis=alt.Axis(format='.1')))

def experimental_data_plot(isotherm_data):
    """Creates a scatter plot of experimental data.

    Typical isotherm presentation where
    x-axis is relative pressure, y-axis is specific amount adsorbed.

    Parameters
    ----------
    isotherm_data : namedtuple
        The isotherm_data.iso_df element is used to
        create a plot of isotherm data.

    save_file : boolean
        When save_file=True a .png of the figure is created in the
        working directory.

    Returns
    -------

    """

    df = isotherm_data.iso_df
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, df['n'].iloc[-1] * 1.05)
    ax.set_title('Experimental Isotherm')
    ax.set_ylabel('n [mol/g]')
    ax.set_xlabel('P/Po')
    ax.ticklabel_format(style='plain')
    ax.grid(b=True, which='major', color='gray', linestyle=':')
    ax.plot(df.relp, df.n, c='k', marker='o', markerfacecolor="w", linewidth=0)
    plt.show()
    st.pyplot()
    return

def bet_plot(bet_results, mask_results, ssa_answer):
    mask = mask_results.mask

    if mask.all() == True:
        print('No valid relative pressure ranges. BET combo plot not created.')
        return

    df = bet_results.iso_df

    value_index = bt.utils.index_of_value(bet_results.ssa, ssa_answer)
    data_start = int(value_index[1])
    data_stop = int(value_index[0])

    slope, intercept, r_val, p_value, std_err =\
    sp.stats.linregress(df.relp[data_start: data_stop + 1],
                        df.bet[data_start:data_stop + 1])

    liney = np.zeros(2)
    liney[0] = slope * (0) + intercept
    liney[1] = slope * (df.relp[data_stop] + .01) + intercept
    linex = np.zeros(2)
    linex[0] = 0
    linex[1] = df.relp[data_stop] + .01
    
    figure, ax = plt.subplots(1, figsize=(10, 10))

    ax.set_title('BET Plot')
    ax.set_xlim(0, linex[1])
    ax.set_ylabel('1/[n(P/Po-1)]')
    ax.set_ylim(0, liney[1]*1.1)
    ax.set_xlabel('P/Po')
    ax.ticklabel_format(style='plain')
    ax.grid(b=True, which='major', color='gray', linestyle='-')
    ax.plot(df.relp[data_start:data_stop + 1], df.bet[data_start:data_stop + 1],
             label='Experimental Data', c='grey', marker='o',
             linewidth=0, fillstyle='none')
    ax.plot(linex, liney, color='black',
             label='Linear Regression')
    ax.legend(loc='upper left', framealpha=1)
    ax.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                % (slope, intercept, r_val),
                bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                textcoords='axes fraction', xytext=(.695, .017),
                xy=(df.relp[data_stop], df.bet[data_start]), size=11)
    plt.show()
    st.pyplot()
    return

def bet_combo_plot(bet_results, mask_results):
    """Creates two BET plots, for the minimum and maxium error data sets.

    Only datapoints in the minimum and maximum error data sets are plotted.
    Equation for best fit line and corresponding R value are annotated on plots
    Image is 2 by 1, two BET plots arranged horizontally in one image.

    Parameters
    ----------

    bet_results : namedtuple
        Namedtuple where the bet_results.iso_df element is used to
        create a plot of isotherm BET values.

    mask_results : namedtuple
        The mask_results.mask element is used to mask the BET results so that
        only valid results are displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    Returns
    -------

    """

    mask = mask_results.mask

    if mask.all() == True:
        print('No valid relative pressure ranges. BET combo plot not created.')
        return

    df = bet_results.iso_df
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_val, p_value, std_err =\
        sp.stats.linregress(df.relp[min_start: min_stop + 1],
                            df.bet[min_start:min_stop + 1])

    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - .01
    min_linex[1] = df.relp[min_stop] + .01

    slope_max, intercept_max, r_value_max, p_value_max, std_err_max = \
        sp.stats.linregress(df.relp[max_start: max_stop + 1],
                            df.bet[max_start: max_stop + 1])
    max_liney = np.zeros(2)
    max_liney[0] = slope_max * (df.relp[max_start] - .01) + intercept_max
    max_liney[1] = slope_max * (df.relp[max_stop] + .01) + intercept_max
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - .01
    max_linex[1] = df.relp[max_stop] + .01

    figure, ax = plt.subplots(1, figsize=(10, 10))

    ax.set_title('BET Plot')
    ax.set_xlim(0, max(min_linex[1], max_linex[1])*1.1)
    ax.set_ylabel('1/[n(P/Po-1)]')
    ax.set_ylim(0, max(min_liney[1]*1.1, max_liney[1]*1.1))
    ax.set_xlabel('P/Po')
    ax.ticklabel_format(style='plain')
    ax.grid(b=True, which='major', color='gray', linestyle='-')
    ax.plot(df.relp[min_start:min_stop + 1], df.bet[min_start:min_stop + 1],
             label='Min Error Experimental Data', c='grey', marker='o',
             linewidth=0, fillstyle='none')
    ax.plot(min_linex, min_liney, color='black',
             label='Min Error Linear Regression')
    ax.plot(df.relp[max_start:max_stop + 1], df.bet[max_start:max_stop + 1],
             label='Max Error Experimental Data', c='grey', marker='x',
             linewidth=0)
    ax.plot(max_linex, max_liney, color='black', linestyle='--',
             label='Max Error Linear Regression')
    ax.legend(loc='upper left', framealpha=1)
    ax.annotate('Min Error Linear Regression: \nm = %.3f \nb = %.3f \nR = \
%.3f \n\nMax Error Linear Regression: \nm = %.3f \nb = %.3f \
\nR = %.3f' % (slope, intercept, r_val, slope_max, intercept_max, r_value_max),
                bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                textcoords='axes fraction', xytext=(.695, .017),
                xy=(df.relp[min_stop], df.bet[min_start]), size=11)
    plt.show()
    st.pyplot()
    return


def iso_combo_plot(bet_results, mask_results):
    """Creates an image displaying the relative pressure range with minimum
    error and the BET isotherm on the same plot. The point where n/nm = 1 is
    is the point where the BET monolayer loading is achieved.

    Parameters
    ----------

    bet_results : named tuple
        The bet_results.iso_df element is used to
        create a plot of isotherm data.

    mask_results : named tuple
        The mask_results.mask element is used to mask the BET results so that
        only valid results are displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    Returns
    -------

    """

    mask = mask_results.mask

    if mask.all() == True:
        print('No valid relative pressure ranges. BET isotherm \
combo plot not created.')
        return

    df = bet_results.iso_df
    nm = np.ma.array(bet_results.nm, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)
    c_min_err = c[err_min_idx[0], err_min_idx[1]]

    nnm_min = nm[err_min_idx[0], err_min_idx[1]]
    ppo = np.arange(0, .9001, .001)
    synth_min = 1 / (1 - ppo) - 1 / (1 + (c_min_err - 1) * ppo)
    expnnm_min = df.n / nnm_min
    err_min_i = int(err_min_idx[0] + 1)
    err_min_j = int(err_min_idx[1])
    expnnm_min_used = expnnm_min[err_min_j:err_min_i]
    ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]

    f, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax.set_title('BET Isotherm and Experimental data')
    ax.set_ylim(0, synth_min[-2]+1)
    ax.set_xlim(0, 1)
    ax.set_ylabel('n/nm')
    ax.set_xlabel('P/Po')
    ax.ticklabel_format(style='plain')
    ax.grid(b=True, which='major', color='gray', linestyle='-')
    ax.plot(ppo, synth_min, linestyle='-', linewidth=1, c='black',
             label='Theoretical isotherm', marker='')
    ax.plot(ppo_expnnm_min_used, expnnm_min_used, c='gray',
             label='Experimental isotherm - used data',
             marker='o', linewidth=0)
    ax.plot(df.relp, expnnm_min, c='grey', fillstyle='none',
             label='Experimental isotherm', marker='o', linewidth=0)
    ax.plot([0, 1], [1, 1], c='grey', linestyle='--',
             linewidth=1, marker='')
    ax.legend(loc='upper left', framealpha=1)

    plt.show()
    st.pyplot()
    return


# # BEaTmap quick summary
# intro_state = st.sidebar.radio(
#     label="BEaTmap quick summary",
#     options=("Show app info", "Hide app info"),
#     index=0
# )

# st.markdown("# BEaTmap")
# if intro_state == "Show app info":
#     st.markdown(texts.intro)

# # File uploader widget
# st.sidebar.markdown("# Upload isotherm data")
# uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
# st.sidebar.success("Uploaded!")

# # Fetch and analyze the uploaded data
# isotherm_data = fetch_isotherm_data(uploaded_file)
# bet_results = fetch_bet_results(isotherm_data)

# # Visualize isotherm data
# st.sidebar.markdown("# Plot isotherm data")
# plot_isotherm_state = st.sidebar.radio(
#     label="Take a quick look at your data", options=("Show", "Hide"), index=1
# )

# if plot_isotherm_state == "Show":
#     st.markdown("## Isotherm data")
#     plot_bet_data(isotherm_data)

# # Model assumptions and settings
# st.sidebar.markdown("# Settings")
# settings_state = st.sidebar.radio(
#     label="Assumptions considered in the model.",
#     options=("Show settings", "Hide settings"),
#     index=1
# )

# if settings_state == "Show settings":
#     st.markdown("## Settings")
#     st.markdown("### Model assumptions")
#     checks = [st.checkbox(label=texts.checks[i], value=True) for i in range(5)]
#     points = st.slider(
#         label="Minimum number of points", min_value=2, max_value=27, value=5
#     )
#     st.markdown("### BET calculation criteria")
#     criterion = st.radio(
#         label="Select the BET calculation criteria:",
#         options=("Minimum error", "Maximum data points")
#     )
#     criterion = "error" if "error" in criterion else "points"

#     mask_results = bt.core.rouq_mask(
#         intercept=bet_results.intercept,
#         iso_df=bet_results.iso_df,
#         nm=bet_results.nm,
#         slope=bet_results.slope,
#         check1=checks[0],
#         check2=checks[1],
#         check3=checks[2],
#         check4=checks[3],
#         check5=checks[4],
#         points=points
#     )

# ssa_answer = bt.core.ssa_answer(bet_results, mask_results, criterion)
# st.success( f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")
# # plot_ssa_heatmap(bet_results, mask_results)

# state = _get_state()
# pages = {
#     "Settings": page_settings,
#     "Analysis": page_dashboard,
# }

# st.sidebar.title(":floppy_disk: Page states")
# page = st.sidebar.radio("Select your page", tuple(pages.keys()))

# # Display the selected page with the session state
# pages[page](state)

# # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
# state.sync()


if __name__ == "__main__":
    main()
