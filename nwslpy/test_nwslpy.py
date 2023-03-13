import unittest
import nwslpy


class TestNWSLPY(unittest.TestCase):
    def test_matches(self):
        matches = nwslpy.load_matches()
        self.assertTrue(
            "angel-city-fc-vs-north-carolina-courage-2022-04-29" in matches.index
        )

    def test_players(self):
        players = nwslpy.load_players()
        self.assertTrue("M. Rapinoe" in players["player_match_name"].values)

    def test_teams(self):
        teams = nwslpy.load_teams()
        self.assertTrue("Washington Spirit" in teams["team_name"].values)

    def test_metrics(self):
        metrics = nwslpy.load_metrics()
        print(metrics)
        self.assertTrue("goals" in metrics.index)


if __name__ == "__main__":
    unittest.main()
