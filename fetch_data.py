import json
import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from datetime import datetime
from db_connection import db
import os
from constants import CURRENT_MANAGERS, BATTER_STATS, PITCHER_STATS
import sys


def lambda_handler(event, context):
    # Suppress yahoo_oauth log messages unless there's an error
    logging.getLogger("yahoo_oauth").setLevel(logging.ERROR)

    # Authenticate with the Yahoo API
    oauth = OAuth2(None, None, from_file=os.path.join("config", "oauth2.json"))

    # Use the oauth object to create a League object
    this_years_league = yfa.League(oauth, "431.l.51071")
    # last_years_league = yfa.League(oauth, "422.l.115216")

    # Get the league standings
    standings = this_years_league.standings()
    print(standings)

    team_stats_table = db.table("team_stats")

    for team_stats in standings:
        team_key = team_stats["team_key"]
        team_stats_table.upsert(
            {
                "team_key": team_key,
                "rank": team_stats["rank"],
                "points_for": team_stats["points_for"],
                "points_change": team_stats["points_change"],
                "points_back": team_stats["points_back"],
            }
        ).execute()

    # # Insert today's stats
    # db.table("team_stats").insert(
    #     {
    #         "team_key": team["team_key"],
    #         "date": datetime.date.today(),
    #         "rank": team["rank"],
    #         "points_for": team["points_for"],
    #         "points_change": team["points_change"],
    #         "points_back": team["points_back"],
    #     }
    # )
    # Get the team object
    # for manager in CURRENT_MANAGERS:
    #     team = this_years_league.to_team(CURRENT_MANAGERS[manager]["team_key"])
    #     roster = team.roster()
    #     for player in roster:
    #         player_id = player["player_id"]
    #         player_stats = this_years_league.player_stats(player_id, "date")
    #         print(player_stats)
    #         break
    # print(team.roster)
    # this_years_league.player_details("12562")
    # print(this_years_league.player_stats("12562", "date"))
    # this_years_league.stat_categories()
    # print(datetime.now().date())

    # Get the team's roster for the specified date
    # We can't do this because MLB doesn't let you check rosters for past dates
    # We should probably start our own DB that keeps the historical records
    # roster = team.roster()
    # print(roster)
