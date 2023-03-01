import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2.rinterface_lib.callbacks
import pandas as pd

# Redirect R output since this prints a lot of messages
rpy2.rinterface_lib.callbacks.consolewrite_print = lambda *args: None
rpy2.rinterface_lib.callbacks.consolewrite_warnerror = lambda *args: None

# Use devtools to install the nwslR package from GitHub
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
    """Run the specified method (with optional args) in R."""

    return robjects.r(
        """
        data <- {method}({formatted_args})
        types <- sapply(data, class)
        list(data, types)
        """.format(
            method=method,
            formatted_args=",".join(
                map(lambda x: "'" + x[0] + "'='" + x[1] + "'", args.items())
            ),
        )
    )


def load_matches():
    """All matches from 2016-present with information and match IDs."""
    return _convert_and_fix_types(_run_query("load_matches"))


def load_players():
    """All players rostered from 2016-present with information and player IDs."""
    return _convert_and_fix_types(_run_query("load_players"))


def load_teams():
    """All teams active from 2016-present with information and team IDs"""
    return _convert_and_fix_types(_run_query("load_teams"))


def load_metrics():
    """All metrics available from scrapers with definitions.

    Not all metrics are available for all players/matches/teams/etc.
    """
    return _convert_and_fix_types(_run_query("load_metrics"))


def load_team_season_stats(team_id, season):
    """Loads team level stats for a team/season."""
    return _convert_and_fix_types(
        _run_query("load_team_season_stats", {"team_id": team_id, "season": season})
    )


def load_player_season_stats(team_id, season):
    """Loads player level stats for a team/season."""
    return _convert_and_fix_types(
        _run_query("load_player_season_stats", {"team_id": team_id, "season": season})
    )


def load_team_match_stats(match_id):
    """Loads team level stats for a given match."""
    return _convert_and_fix_types(
        _run_query("load_team_match_stats", {"match_id": match_id})
    )


def load_player_match_stats(match_id):
    """Loads player level stats for a given match."""
    return _convert_and_fix_types(
        _run_query("load_player_match_stats", {"match_id": match_id})
    )
