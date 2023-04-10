import pandas as pd

TYPES = {"kickoff": "datetime", "time": "time", "last_updated": "date"}


def _fix_types(df):
    """Coerce types for certain columns."""
    for col in df.columns:
        if col in TYPES.keys():
            t = TYPES[col]
            if t == "datetime":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif t == "date":
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
            elif t == "time":
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.time

    return df


def load_matches():
    """All matches from 2016-present with information and match IDs."""
    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/key_tables/matches.csv",
            index_col=0,
        )
    )


def load_players():
    """All players rostered from 2016-present with information and player IDs."""
    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/key_tables/players.csv",
            index_col=0,
        )
    )


def load_teams():
    """All teams active from 2016-present with information and team IDs"""
    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/key_tables/teams.csv",
            index_col=0,
        )
    )


def load_metrics():
    """All metrics available from scrapers with definitions.

    Not all metrics are available for all players/matches/teams/etc.
    """
    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/key_tables/metrics.csv",
            index_col=0,
        )
    )


available_teams = list(load_teams()["team_abbreviation"])
available_seasons = list(load_matches()["season"].unique())


def load_team_season_stats(team_id, season):
    """Loads team level stats for a team/season."""

    if team_id not in available_teams:
        raise Exception("Error: Team must be one of: " + str(available_teams))

    if season not in available_seasons:
        raise Exception("Error: Season must be one of: " + str(available_seasons))

    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/team_season_summaries/{0}_{1}.csv".format(
                team_id, season
            )
        )
    )


def load_player_season_stats(team_id, season):
    """Loads player level stats for a team/season."""

    if team_id not in available_teams:
        raise Exception("Error: Team must be one of: " + str(available_teams))

    if season not in available_seasons:
        raise Exception("Error: Season must be one of: " + str(available_seasons))

    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/player_season_summaries/{0}_{1}.csv".format(
                team_id, season
            )
        )
    )


def load_team_match_stats(match_id):
    """Loads team level stats for a given match."""
    matches = load_matches()
    if match_id not in matches.index:
        raise Exception(
            "Error: Match does not exist! Please make sure you are using the correct Match ID."
        )

    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/team_match_summaries/{0}.csv".format(
                match_id
            )
        )
    )


def load_player_match_stats(match_id):
    """Loads player level stats for a given match."""
    matches = load_matches()
    if match_id not in matches.index:
        raise Exception(
            "Error: Match does not exist! Please make sure you are using the correct Match ID."
        )

    return _fix_types(
        pd.read_csv(
            "https://github.com/nwslR/nwsldata/releases/download/player_match_summaries/{0}.csv".format(
                match_id
            )
        )
    )
