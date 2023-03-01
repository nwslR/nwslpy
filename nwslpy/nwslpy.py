import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2.rinterface_lib.callbacks
import pandas as pd

# Redirect R output
rpy2.rinterface_lib.callbacks.consolewrite_print = lambda *args: None
rpy2.rinterface_lib.callbacks.consolewrite_warnerror = lambda *args: None

# Initialization needed for all requests
utils = rpackages.importr("utils")
utils.install_packages("devtools")
devtools = rpackages.importr("devtools")
devtools.install_github("nwslR/nwslR")
rpackages.importr("nwslR")


def _convert_and_fix_types(res):
    """Converts the raw output from rpy2 into Python types."""

    df = pandas2ri.rpy2py(res[0])
    types = (
        pandas2ri.rpy2py(res[1])
        if type(res[1]) == robjects.vectors.StrVector
        else [pandas2ri.rpy2py(x)[0] for x in res[1]]
    )
    for i, (col, t) in enumerate(zip(df.columns, types)):
        if "_pct" in col or "_accuracy" in col:
            df[col] = df[col].astype(float)
        elif t == "numeric":
            df[col] = df[col].astype("Int64")
        elif t == "logical":
            df[col] = df[col].astype(bool)
        elif t == "hms":
            df[col] = pd.to_datetime(df[col], unit="s").dt.time
        elif t == "Date":
            df[col] = pd.to_datetime(df[col], unit="d")
    return df


def _run_query(method, args={}):

    return robjects.r(
        """
        data <- {method}({formatted_args})
        types <- sapply(data, class)
        list(data, types)
        """.format(
            method=method,
            formatted_args=",".join(
                list(map(lambda x: "'" + x[0] + "'='" + x[1] + "'", args.items())))
        )
    )


def load_matches():
    return _convert_and_fix_types(_run_query("load_matches"))


def load_players():
    return _convert_and_fix_types(_run_query("load_players"))


def load_teams():
    return _convert_and_fix_types(_run_query("load_teams"))


def load_metrics():
    return _convert_and_fix_types(_run_query("load_metrics"))


def load_team_season_stats(team_id, season):
    return _convert_and_fix_types(
        _run_query("load_team_season_stats", {
                   "team_id": team_id, "season": season})
    )


def load_player_season_stats(team_id, season):
    return _convert_and_fix_types(
        _run_query("load_player_season_stats", {
                   "team_id": team_id, "season": season})
    )


def load_team_match_stats(match_id):
    return _convert_and_fix_types(_run_query("load_team_match_stats", {"match_id": match_id}))


def load_player_match_stats(match_id):
    return _convert_and_fix_types(_run_query("load_player_match_stats", {"match_id": match_id}))
