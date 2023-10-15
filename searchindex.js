Search.setIndex({"docnames": ["advanced_usage", "basic_usage", "index", "installation", "modules/generated/beatmap.core", "modules/generated/beatmap.core.bet", "modules/generated/beatmap.core.check_absorbed_amount", "modules/generated/beatmap.core.check_enough_datapoints", "modules/generated/beatmap.core.check_pressure_consistency", "modules/generated/beatmap.core.check_pressure_increasing", "modules/generated/beatmap.core.check_y_intercept_positive", "modules/generated/beatmap.core.rouq_mask", "modules/generated/beatmap.core.run_beatmap", "modules/generated/beatmap.core.single_point_bet", "modules/generated/beatmap.core.ssa_answer", "modules/generated/beatmap.io", "modules/generated/beatmap.io.export_processed_data", "modules/generated/beatmap.io.export_raw_data", "modules/generated/beatmap.io.import_data", "modules/generated/beatmap.io.import_list_data", "modules/generated/beatmap.utils", "modules/generated/beatmap.utils.find_package_root", "modules/generated/beatmap.utils.get_fixtures_path", "modules/generated/beatmap.utils.get_logger", "modules/generated/beatmap.utils.index_of_value", "modules/generated/beatmap.utils.lin_interp", "modules/generated/beatmap.utils.max_min", "modules/generated/beatmap.vis", "modules/generated/beatmap.vis.ascii_tables", "modules/generated/beatmap.vis.bet_combo_plot", "modules/generated/beatmap.vis.dataframe_tables", "modules/generated/beatmap.vis.err_heatmap", "modules/generated/beatmap.vis.experimental_data_plot", "modules/generated/beatmap.vis.iso_combo_plot", "modules/generated/beatmap.vis.ssa_heatmap", "modules/index", "streamlit", "user_guide"], "filenames": ["advanced_usage.md", "basic_usage.md", "index.rst", "installation.md", "modules/generated/beatmap.core.rst", "modules/generated/beatmap.core.bet.rst", "modules/generated/beatmap.core.check_absorbed_amount.rst", "modules/generated/beatmap.core.check_enough_datapoints.rst", "modules/generated/beatmap.core.check_pressure_consistency.rst", "modules/generated/beatmap.core.check_pressure_increasing.rst", "modules/generated/beatmap.core.check_y_intercept_positive.rst", "modules/generated/beatmap.core.rouq_mask.rst", "modules/generated/beatmap.core.run_beatmap.rst", "modules/generated/beatmap.core.single_point_bet.rst", "modules/generated/beatmap.core.ssa_answer.rst", "modules/generated/beatmap.io.rst", "modules/generated/beatmap.io.export_processed_data.rst", "modules/generated/beatmap.io.export_raw_data.rst", "modules/generated/beatmap.io.import_data.rst", "modules/generated/beatmap.io.import_list_data.rst", "modules/generated/beatmap.utils.rst", "modules/generated/beatmap.utils.find_package_root.rst", "modules/generated/beatmap.utils.get_fixtures_path.rst", "modules/generated/beatmap.utils.get_logger.rst", "modules/generated/beatmap.utils.index_of_value.rst", "modules/generated/beatmap.utils.lin_interp.rst", "modules/generated/beatmap.utils.max_min.rst", "modules/generated/beatmap.vis.rst", "modules/generated/beatmap.vis.ascii_tables.rst", "modules/generated/beatmap.vis.bet_combo_plot.rst", "modules/generated/beatmap.vis.dataframe_tables.rst", "modules/generated/beatmap.vis.err_heatmap.rst", "modules/generated/beatmap.vis.experimental_data_plot.rst", "modules/generated/beatmap.vis.iso_combo_plot.rst", "modules/generated/beatmap.vis.ssa_heatmap.rst", "modules/index.rst", "streamlit.rst", "user_guide.rst"], "titles": ["Advanced Usage", "Basic Usage", "BEaTmap: BET Analysis Tool", "Installation", "core", "bet", "check_absorbed_amount", "check_enough_datapoints", "check_pressure_consistency", "check_pressure_increasing", "check_y_intercept_positive", "rouq_mask", "run_beatmap", "single_point_bet", "ssa_answer", "io", "export_processed_data", "export_raw_data", "import_data", "import_list_data", "utils", "find_package_root", "get_fixtures_path", "get_logger", "index_of_value", "lin_interp", "max_min", "vis", "ascii_tables", "bet_combo_plot", "dataframe_tables", "err_heatmap", "experimental_data_plot", "iso_combo_plot", "ssa_heatmap", "API Reference", "Web App", "User Guide"], "terms": {"altern": 0, "you": [0, 1, 3, 24, 37], "can": [0, 3, 5, 11, 12, 13, 37], "us": [0, 1, 2, 3, 5, 6, 11, 12, 13, 14, 17, 18, 20, 29, 31, 32, 33, 34, 36, 37], "individu": [0, 5, 11, 37], "function": [0, 1, 3, 4, 5, 11, 12, 15, 20, 27, 37], "beatmap": [0, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37], "perform": [0, 1, 4, 5, 13], "evalu": [0, 1, 2, 11], "thi": [0, 5, 6, 8, 9, 10, 11, 12, 13, 36, 37], "allow": [0, 1, 2], "user": [0, 1, 2, 12, 14, 19], "access": [0, 1], "more": [0, 12, 37], "": [0, 1, 10, 37], "custom": 0, "The": [0, 1, 2, 3, 8, 11, 12, 16, 18, 25, 29, 31, 32, 33, 34, 37], "import_data": 0, "isotherm": [0, 2, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 19, 28, 29, 30, 31, 32, 33, 35], "data": [0, 1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 25, 27, 28, 29, 30, 31, 32, 33], "from": [0, 2, 8, 14, 18, 28, 30], "csv": [0, 1, 12, 16, 17, 18], "file": [0, 1, 5, 12, 16, 17, 18, 19], "where": [0, 2, 5, 6, 7, 8, 9, 10, 11, 12, 28, 29, 30, 32, 33], "first": [0, 5, 13, 18], "column": [0, 18], "i": [0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 16, 17, 18, 24, 26, 29, 31, 32, 33, 34, 35, 36, 37], "rel": [0, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 32, 33], "pressur": [0, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 25, 32, 33], "second": [0, 8, 18], "amount": [0, 5, 6, 8, 11, 12, 13, 18, 19, 25, 32], "adsorb": [0, 1, 5, 6, 8, 12, 13, 17, 18, 19, 25, 32], "return": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 22, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 37], "name": [0, 1, 5, 11, 12, 13, 14, 18, 19, 23, 31, 33, 34], "tupl": [0, 5, 11, 13, 14, 33], "entri": 0, "datafram": [0, 5, 6, 7, 8, 9, 11, 13, 17, 18, 19, 25, 28, 30], "2nd": 0, "4th": [0, 5], "field": [0, 11, 13, 17, 18, 19, 28, 30], "ar": [0, 2, 5, 8, 11, 12, 13, 17, 18, 19, 26, 28, 29, 30, 31, 33, 34], "cross": [0, 1, 5, 12, 13, 18, 19], "section": [0, 1, 5, 12, 13, 18, 19], "area": [0, 1, 2, 5, 12, 13, 14, 18, 19, 28, 30, 34], "inform": [0, 1, 3, 5, 12, 13, 16, 17, 18, 19, 37], "about": [0, 1, 3, 12], "path": [0, 1, 3, 12, 18, 19, 22], "respect": [0, 12], "index": [0, 5, 24, 26], "element": [0, 5, 28, 29, 30, 31, 32, 33, 34], "order": [0, 5], "prioriti": [0, 5], "other": [0, 5, 19], "given": [0, 5, 23], "bt": [0, 1], "matplotlib": [0, 1, 29, 33], "pylot": [0, 1], "plt": [0, 1], "next": [0, 1], "line": [0, 1, 29], "might": [0, 1], "break": [0, 1, 3], "don": [0, 1], "t": [0, 1, 9], "have": [0, 1, 2, 3, 36], "fixtur": [0, 1, 22], "folder": [0, 1, 3], "fpath": [0, 1], "util": [0, 1, 2, 21, 22, 23, 24, 25, 26], "get_fixtures_path": [0, 1], "vulcan_chex": [0, 1], "isotherm_data": [0, 5, 17, 18, 19, 32], "io": [0, 16, 17, 18, 19], "info": [0, 1, 5, 12, 17, 18, 19], "chex": [0, 1], "vulcan": [0, 1], "a_o": [0, 1, 5, 12, 13, 18, 19], "39": [0, 1], "everi": 0, "rang": [0, 2, 5, 6, 7, 8, 9, 10, 12, 13, 14, 28, 30, 33, 35], "within": [0, 8], "accept": [0, 5, 11], "store": [0, 5, 13], "creat": [0, 3, 12, 28, 29, 30, 31, 32, 33, 34, 36], "rather": [0, 5, 11], "than": [0, 5, 7, 11, 12], "pass": [0, 5, 8, 11, 12, 24], "paramet": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34], "output": [0, 5, 11, 12], "contain": [0, 4, 5, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 27, 28, 29, 30, 33], "well": 0, "raw": [0, 17, 25], "etc": 0, "again": 0, "bet_result": [0, 5, 11, 13, 14, 16, 17, 28, 29, 30, 31, 33, 34], "core": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "iso_df": [0, 5, 11, 17, 28, 29, 30, 32, 33], "mask": [0, 2, 11, 14, 28, 29, 30, 31, 33, 34], "out": 0, "invalid": [0, 2, 11, 12, 28, 30], "rouq_mask": [0, 14], "numpi": 0, "arrai": [0, 5, 6, 7, 8, 9, 10, 11, 13, 14, 24, 26], "correspond": [0, 5, 6, 7, 8, 9, 10, 11, 13, 14, 25, 31, 34], "each": [0, 11], "criterion": [0, 12, 14], "mask_result": [0, 14, 28, 29, 30, 31, 33, 34], "intercept": [0, 5, 8, 10, 11, 12], "nm": [0, 5, 6, 8, 11, 13, 33], "slope": [0, 5, 8, 11], "enforce_y_intercept_posit": [0, 1, 11, 12], "true": [0, 1, 11, 12, 29, 31, 32, 33, 34], "enforce_pressure_increas": [0, 1, 11, 12], "enforce_absorbed_amount": [0, 1, 11, 12], "enforce_relative_pressur": [0, 1, 11, 12], "enforce_enough_datapoint": [0, 1, 11, 12], "min_num_point": [0, 1, 11, 12, 16], "5": [0, 1, 7, 11, 12, 16], "heatmap": [0, 2, 12, 31, 34], "specif": [0, 5, 6, 8, 12, 13, 14, 18, 25, 28, 30, 32, 34], "surfac": [0, 2, 5, 12, 13, 14, 28, 30, 34], "valu": [0, 5, 6, 7, 8, 10, 11, 12, 13, 14, 19, 24, 25, 26, 28, 29, 30, 31, 34], "visual": [0, 2, 27], "concept": 0, "central": 0, "idea": 0, "ssa_heatmap": 0, "requir": [0, 7, 13, 16, 17, 18, 19], "produc": [0, 1], "figur": [0, 1, 12, 29, 31, 32, 33, 34], "plot": [0, 5, 10, 29, 32, 33, 37], "experiment": [0, 5, 6, 7, 8, 9, 11, 13, 16, 19, 28, 30, 31, 32], "model": 0, "manner": 0, "see": 0, "document": 0, "full": 0, "summari": [0, 28, 30], "vi": [0, 28, 29, 30, 31, 32, 33, 34], "iso_combo_plot": 0, "save_fil": [0, 29, 31, 32, 33, 34], "v": 0, "It": [0, 1], "desir": 0, "spreadsheet": 0, "all": [0, 1, 2, 5, 11, 12, 13, 16, 17, 18, 19, 26, 28, 30], "sheet": 0, "save": [0, 12, 16, 17], "parent": [0, 12, 16, 17], "directori": [0, 12, 16, 17, 22, 29, 31, 32, 33, 34], "export_processed_data": 0, "an": [1, 2, 13, 24, 26, 33], "envelop": [1, 37], "import": [1, 5, 6, 7, 8, 9, 18, 19], "bet": [1, 4, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19, 28, 29, 30, 31, 33, 35, 37], "analysi": [1, 4, 5, 6, 7, 13, 16, 17, 18, 19, 28, 30, 37], "rouquerol": [1, 2, 28, 30], "criteria": [1, 2, 12, 14, 28, 30], "ha": [1, 2], "been": 1, "built": [1, 12], "later": [1, 12], "export": [1, 12, 16, 17], "squar": [1, 5, 12, 13, 18], "angstrom": [1, 5, 12, 13, 18], "need": 1, "specifi": [1, 12, 14], "much": 1, "one": [1, 2, 11, 19], "rouq_criteria": 1, "aux_param": 1, "save_figur": [1, 12], "export_data": [1, 12], "fals": [1, 12, 32], "ssa_gradi": [1, 12], "green": [1, 12, 34], "err_gradi": [1, 12], "grei": [1, 12, 31], "result": [1, 2, 5, 8, 11, 12, 13, 27, 28, 29, 30, 31, 33, 34, 37], "run_beatmap": 1, "ssa_criterion": [1, 12], "error": [1, 5, 12, 14, 28, 29, 30, 31, 33], "obtain": 2, "porou": 2, "sampl": 2, "interpret": 2, "ga": 2, "adsorpt": [2, 6, 7, 8, 9], "veri": 2, "wide": 2, "done": 2, "theori": 2, "develop": 2, "brunauer": 2, "emmett": 2, "teller": 2, "1950": 2, "beat": 2, "so": [2, 29, 31, 33, 34], "commonli": 2, "place": 2, "acronym": 2, "synonym": 2, "wa": 2, "deriv": 2, "sever": 2, "assumpt": 2, "must": [2, 8, 12, 31, 34], "met": 2, "predict": 2, "valid": [2, 7, 11, 12, 14, 16, 28, 29, 30, 31, 33, 34, 35], "et": 2, "al": 2, "put": 2, "forth": 2, "whether": 2, "adsoprt": [2, 16, 17, 18, 19], "meet": 2, "appli": [2, 8, 12, 28, 30], "elimin": 2, "do": [2, 8], "adher": 2, "provid": [2, 12, 19], "quick": [2, 36], "comprehens": 2, "represent": 2, "conceptul": 2, "vizual": 2, "instal": 2, "guid": [2, 3], "web": 2, "app": 2, "api": 2, "refer": [2, 3], "depend": 3, "heavili": 3, "scipi": 3, "stack": 3, "best": [3, 29], "wai": 3, "get": [3, 23], "fulli": 3, "environ": 3, "anaconda": 3, "python": 3, "distribut": 3, "Be": 3, "sure": 3, "3": [3, 5], "9": [3, 5], "version": 3, "onc": 3, "ve": 3, "your": 3, "choic": 3, "type": 3, "enter": 3, "follow": 3, "termin": 3, "unix": 3, "base": [3, 36], "machin": 3, "command": 3, "prompt": [3, 12], "window": [3, 36], "pip": 3, "note": 3, "conda": 3, "usual": 3, "automat": [3, 37], "initi": 3, "On": 3, "should": 3, "shortcut": 3, "start": [3, 5], "menu": 3, "which": [3, 12], "basic": [3, 37], "point": [3, 5, 6, 7, 11, 12, 13, 14, 16, 25, 33], "while": 3, "recommend": 3, "new": 3, "avoid": 3, "accident": 3, "If": [3, 11, 12, 26, 37], "think": 3, "mai": 3, "interest": 3, "contribut": 3, "wish": [3, 24], "both": 3, "edit": 3, "sourc": 3, "code": 3, "clone": 3, "repositori": [3, 37], "local": 3, "e": 3, "root": 3, "For": [3, 24, 26], "contributor": 3, "arg": [5, 11], "ani": [5, 12], "less": [5, 7], "end": 5, "written": [5, 17], "eg": [5, 12], "indici": [5, 13], "begin": 5, "10th": 5, "float": [5, 12, 14, 18, 19, 25, 26, 28, 30], "str": [5, 12, 14, 17, 18, 19, 21, 23, 34], "namedtupl": [5, 11, 13, 16, 17, 18, 19, 28, 29, 30, 31, 32, 34], "ndarrai": [5, 6, 7, 8, 9, 10, 11, 13, 28, 30], "2d": [5, 6, 8, 10, 11, 13, 24, 26], "trendlin": 5, "last": [5, 13], "datapoint": [5, 12, 13, 29], "monolay": [5, 6, 8, 11, 12, 13, 33], "mol": [5, 13, 18, 19], "g": [5, 13, 18, 19], "ssa": [5, 12, 13, 14, 28, 30, 34], "m": [5, 13], "2": [5, 12, 13], "c": [5, 28, 30], "constant": [5, 28, 30], "err": [5, 28, 30, 31], "averag": [5, 28, 30, 31], "between": [5, 12, 13, 25, 31], "theoret": [5, 12, 31], "r": 5, "num_pt": 5, "number": [5, 7, 11, 12, 14, 16], "per": [5, 12, 19], "string": [5, 18, 19, 31], "df": [6, 7, 8, 9, 13, 25], "check": [6, 7, 8, 9, 10, 11, 13], "coordin": [6, 8], "unit": [6, 8, 19], "mole": [6, 8], "gram": [6, 8, 19], "1": [6, 7, 8, 9, 10, 11, 24, 26, 33], "0": [6, 7, 8, 9, 10, 11, 24, 26, 31], "includ": 6, "n": [6, 8, 9, 12, 18, 19, 25, 33], "ie": [6, 8, 9, 10], "fail": [6, 8, 9, 10, 11], "minimum": [7, 11, 12, 14, 16, 26, 29, 33, 34], "int": [7, 11, 12, 16], "consid": [7, 11, 12, 16], "default": [7, 12, 14, 16, 31], "consist": [8, 9, 35], "found": 8, "linear": [8, 9, 10], "interpol": [8, 25], "experiement": 8, "A": [8, 12], "set": [8, 12, 13, 29], "equat": [8, 29], "solv": 8, "two": [8, 18, 19, 25], "compar": 8, "agre": 8, "10": [8, 12], "regress": [8, 10], "relev": [8, 13, 17, 18, 19, 28, 30], "y": [8, 10, 12, 32], "p": [9, 12, 35], "po": [9, 12], "aka": 9, "check2": [9, 11, 12], "increas": 9, "necessari": [9, 12], "condit": 9, "dataset": 9, "isn": 9, "posit": 10, "neg": [10, 12], "zero": 10, "call": [11, 37], "combin": 11, "rouqerol": 11, "check1": [11, 12], "check3": [11, 12], "check4": [11, 12], "bool": [11, 12, 29, 34], "otherwis": 11, "skip": 11, "enforce_absorbed_amount_valid": 11, "enforce_relative_pressure_valid": 11, "interv": [11, 16], "select": [11, 12], "maskedarrai": [11, 28, 30], "object": [11, 28, 29, 30, 33], "check5": [11, 12], "none": [12, 16, 17, 18, 19, 31, 32, 34], "singl": [12, 13, 14], "execut": [12, 37], "algorithim": 12, "friendli": 12, "possibl": 12, "Or": 12, "left": 12, "empti": 12, "input": 12, "them": 12, "myfil": 12, "nitrogen": 12, "carbon": 12, "16": 12, "In": 12, "case": 12, "former": 12, "through": [12, 37], "promt": 12, "consol": 12, "addit": 12, "roquerol": 12, "defin": [12, 14], "reason": 12, "decreas": 12, "fall": 12, "outsid": 12, "disagr": 12, "actual": 12, "coverag": 12, "occur": [12, 33], "fewer": 12, "png": [12, 29, 31, 32, 33, 34], "answer": [12, 14, 34], "lowest": [12, 14], "most": [12, 14, 24], "color": [12, 31, 34], "gradient": [12, 31, 34], "vaild": [12, 31, 34], "seaborn": [12, 31, 34], "packag": [12, 31, 34], "agreement": 13, "also": 13, "raw_data": 13, "flaot": 13, "molecul": [13, 18], "singlept_result": 13, "log": 14, "maximum": [14, 26, 29, 31, 34], "remov": 14, "invaid": 14, "consider": 14, "final": 14, "either": [14, 37], "max": [14, 26], "min": [14, 26], "ssa_an": 14, "read": 15, "write": 15, "process": [16, 37], "format": [18, 28, 37], "expect": 18, "tabl": [18, 28, 37], "being": 18, "buffer": 18, "short": 18, "descript": 18, "identifi": 18, "iso_data": [18, 19], "relp": [19, 25, 28, 30], "list": 19, "helper": 20, "throughout": 20, "librari": 20, "package_nam": 21, "logger": 23, "find": [24, 25, 26], "similar": 24, "numer": 24, "idx": 24, "j": [24, 26], "val": 25, "linerarli": 25, "design": 25, "some": 25, "realtaiv": 25, "interp_v": 25, "multipl": 26, "exist": 26, "max_idx": 26, "min_idx": 26, "print": 28, "ascii": 28, "prettyt": 28, "highlight": [28, 30], "high": [28, 30], "low": [28, 30], "table2": 28, "ssa_std": [28, 30], "atandard": [28, 30], "deviat": [28, 30], "c_std": [28, 30], "standard": [28, 30], "maxium": 29, "onli": [29, 31, 33, 34], "fit": 29, "r2": 29, "annot": 29, "displai": [29, 31, 33, 34], "when": [29, 31, 32, 33, 34], "work": [29, 31, 32, 33, 34], "ax": [29, 33], "popul": 30, "panda": 30, "summar": 30, "ssa_tabl": 30, "c_tabl": 30, "shade": [31, 34], "normal": [31, 34], "white": 31, "black": 31, "boolean": [31, 32, 33], "scatter": 32, "typic": 32, "present": 32, "x": 32, "axi": 32, "imag": 33, "same": 33, "load": 33, "sa": 34, "four": 35, "main": 35, "modul": 35, "tool": 35, "determin": 35, "p0": 35, "we": 36, "gui": 36, "streamlit": 36, "host": 36, "server": 36, "avail": 36, "here": [36, 37], "give": 36, "try": 36, "embed": 36, "below": 36, "nbsp": 36, "whole": 37, "form": 37, "yourself": 37, "latter": 37, "want": 37, "control": 37, "over": 37, "possibli": 37, "further": 37, "prefer": 37, "go": 37, "ipython": 37, "notebook": 37, "github": 37, "click": 37, "view": 37, "usag": 37, "advanc": 37}, "objects": {"": [[35, 0, 0, "-", "beatmap"]], "beatmap": [[4, 0, 0, "-", "core"], [15, 0, 0, "-", "io"], [20, 0, 0, "-", "utils"], [27, 0, 0, "-", "vis"]], "beatmap.core": [[5, 1, 1, "", "bet"], [6, 1, 1, "", "check_absorbed_amount"], [7, 1, 1, "", "check_enough_datapoints"], [8, 1, 1, "", "check_pressure_consistency"], [9, 1, 1, "", "check_pressure_increasing"], [10, 1, 1, "", "check_y_intercept_positive"], [11, 1, 1, "", "rouq_mask"], [12, 1, 1, "", "run_beatmap"], [13, 1, 1, "", "single_point_bet"], [14, 1, 1, "", "ssa_answer"]], "beatmap.io": [[16, 1, 1, "", "export_processed_data"], [17, 1, 1, "", "export_raw_data"], [18, 1, 1, "", "import_data"], [19, 1, 1, "", "import_list_data"]], "beatmap.utils": [[21, 1, 1, "", "find_package_root"], [22, 1, 1, "", "get_fixtures_path"], [23, 1, 1, "", "get_logger"], [24, 1, 1, "", "index_of_value"], [25, 1, 1, "", "lin_interp"], [26, 1, 1, "", "max_min"]], "beatmap.vis": [[28, 1, 1, "", "ascii_tables"], [29, 1, 1, "", "bet_combo_plot"], [30, 1, 1, "", "dataframe_tables"], [31, 1, 1, "", "err_heatmap"], [32, 1, 1, "", "experimental_data_plot"], [33, 1, 1, "", "iso_combo_plot"], [34, 1, 1, "", "ssa_heatmap"]]}, "objtypes": {"0": "py:module", "1": "py:function"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "function", "Python function"]}, "titleterms": {"advanc": 0, "usag": [0, 1], "import": 0, "dataset": 0, "bet": [0, 2, 5], "analysi": [0, 2], "rouquerol": 0, "criteria": 0, "supplementari": 0, "export": 0, "result": 0, "basic": 1, "beatmap": 2, "tool": 2, "what": 2, "i": 2, "content": [2, 35], "instal": 3, "core": 4, "check_absorbed_amount": 6, "check_enough_datapoint": 7, "check_pressure_consist": 8, "check_pressure_increas": 9, "check_y_intercept_posit": 10, "rouq_mask": 11, "run_beatmap": 12, "single_point_bet": 13, "ssa_answ": 14, "io": 15, "export_processed_data": 16, "export_raw_data": 17, "import_data": 18, "import_list_data": 19, "util": 20, "find_package_root": 21, "get_fixtures_path": 22, "get_logg": 23, "index_of_valu": 24, "lin_interp": 25, "max_min": 26, "vi": 27, "ascii_t": 28, "bet_combo_plot": 29, "dataframe_t": 30, "err_heatmap": 31, "experimental_data_plot": 32, "iso_combo_plot": 33, "ssa_heatmap": 34, "api": 35, "refer": 35, "web": 36, "app": 36, "user": 37, "guid": 37}, "envversion": {"sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx": 60}, "alltitles": {"Advanced Usage": [[0, "advanced-usage"]], "Import the dataset": [[0, "import-the-dataset"]], "BET analysis": [[0, "bet-analysis"]], "Rouquerol criteria": [[0, "rouquerol-criteria"]], "Supplementary analysis": [[0, "supplementary-analysis"]], "Export the results": [[0, "export-the-results"]], "Basic Usage": [[1, "basic-usage"]], "BEaTmap: BET Analysis Tool": [[2, "beatmap-bet-analysis-tool"]], "What is BEaTmap?": [[2, "what-is-beatmap"]], "Contents": [[2, "contents"], [35, "module-beatmap"]], "Installation": [[3, "installation"]], "core": [[4, "module-beatmap.core"], [4, "id1"]], "bet": [[5, "bet"]], "check_absorbed_amount": [[6, "check-absorbed-amount"]], "check_enough_datapoints": [[7, "check-enough-datapoints"]], "check_pressure_consistency": [[8, "check-pressure-consistency"]], "check_pressure_increasing": [[9, "check-pressure-increasing"]], "check_y_intercept_positive": [[10, "check-y-intercept-positive"]], "rouq_mask": [[11, "rouq-mask"]], "run_beatmap": [[12, "run-beatmap"]], "single_point_bet": [[13, "single-point-bet"]], "ssa_answer": [[14, "ssa-answer"]], "io": [[15, "module-beatmap.io"], [15, "id1"]], "export_processed_data": [[16, "export-processed-data"]], "export_raw_data": [[17, "export-raw-data"]], "import_data": [[18, "import-data"]], "import_list_data": [[19, "import-list-data"]], "utils": [[20, "module-beatmap.utils"], [20, "id1"]], "find_package_root": [[21, "find-package-root"]], "get_fixtures_path": [[22, "get-fixtures-path"]], "get_logger": [[23, "get-logger"]], "index_of_value": [[24, "index-of-value"]], "lin_interp": [[25, "lin-interp"]], "max_min": [[26, "max-min"]], "vis": [[27, "module-beatmap.vis"], [27, "id1"]], "ascii_tables": [[28, "ascii-tables"]], "bet_combo_plot": [[29, "bet-combo-plot"]], "dataframe_tables": [[30, "dataframe-tables"]], "err_heatmap": [[31, "err-heatmap"]], "experimental_data_plot": [[32, "experimental-data-plot"]], "iso_combo_plot": [[33, "iso-combo-plot"]], "ssa_heatmap": [[34, "ssa-heatmap"]], "API Reference": [[35, "api-reference"]], "Web App": [[36, "web-app"]], "User Guide": [[37, "user-guide"]]}, "indexentries": {"beatmap.core": [[4, "module-beatmap.core"]], "module": [[4, "module-beatmap.core"], [15, "module-beatmap.io"], [20, "module-beatmap.utils"], [27, "module-beatmap.vis"], [35, "module-beatmap"]], "bet() (in module beatmap.core)": [[5, "beatmap.core.bet"]], "check_absorbed_amount() (in module beatmap.core)": [[6, "beatmap.core.check_absorbed_amount"]], "check_enough_datapoints() (in module beatmap.core)": [[7, "beatmap.core.check_enough_datapoints"]], "check_pressure_consistency() (in module beatmap.core)": [[8, "beatmap.core.check_pressure_consistency"]], "check_pressure_increasing() (in module beatmap.core)": [[9, "beatmap.core.check_pressure_increasing"]], "check_y_intercept_positive() (in module beatmap.core)": [[10, "beatmap.core.check_y_intercept_positive"]], "rouq_mask() (in module beatmap.core)": [[11, "beatmap.core.rouq_mask"]], "run_beatmap() (in module beatmap.core)": [[12, "beatmap.core.run_beatmap"]], "single_point_bet() (in module beatmap.core)": [[13, "beatmap.core.single_point_bet"]], "ssa_answer() (in module beatmap.core)": [[14, "beatmap.core.ssa_answer"]], "beatmap.io": [[15, "module-beatmap.io"]], "export_processed_data() (in module beatmap.io)": [[16, "beatmap.io.export_processed_data"]], "export_raw_data() (in module beatmap.io)": [[17, "beatmap.io.export_raw_data"]], "import_data() (in module beatmap.io)": [[18, "beatmap.io.import_data"]], "import_list_data() (in module beatmap.io)": [[19, "beatmap.io.import_list_data"]], "beatmap.utils": [[20, "module-beatmap.utils"]], "find_package_root() (in module beatmap.utils)": [[21, "beatmap.utils.find_package_root"]], "get_fixtures_path() (in module beatmap.utils)": [[22, "beatmap.utils.get_fixtures_path"]], "get_logger() (in module beatmap.utils)": [[23, "beatmap.utils.get_logger"]], "index_of_value() (in module beatmap.utils)": [[24, "beatmap.utils.index_of_value"]], "lin_interp() (in module beatmap.utils)": [[25, "beatmap.utils.lin_interp"]], "max_min() (in module beatmap.utils)": [[26, "beatmap.utils.max_min"]], "beatmap.vis": [[27, "module-beatmap.vis"]], "ascii_tables() (in module beatmap.vis)": [[28, "beatmap.vis.ascii_tables"]], "bet_combo_plot() (in module beatmap.vis)": [[29, "beatmap.vis.bet_combo_plot"]], "dataframe_tables() (in module beatmap.vis)": [[30, "beatmap.vis.dataframe_tables"]], "err_heatmap() (in module beatmap.vis)": [[31, "beatmap.vis.err_heatmap"]], "experimental_data_plot() (in module beatmap.vis)": [[32, "beatmap.vis.experimental_data_plot"]], "iso_combo_plot() (in module beatmap.vis)": [[33, "beatmap.vis.iso_combo_plot"]], "ssa_heatmap() (in module beatmap.vis)": [[34, "beatmap.vis.ssa_heatmap"]], "beatmap": [[35, "module-beatmap"]]}})