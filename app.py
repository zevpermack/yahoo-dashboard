import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import os
from constants import CURRENT_MANAGERS, BATTER_STATS, PITCHER_STATS
from supabase import create_client
from dotenv import load_dotenv
import json


def handler(event, context):

    load_dotenv()

    # Authenticate with the Yahoo API
    access_token = os.getenv("ACCESS_TOKEN")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    guid = os.getenv("GUID")
    if guid == "null":
        guid = None
    refresh_token = os.getenv("REFRESH_TOKEN")
    token_time = float(os.getenv("TOKEN_TIME"))
    token_type = os.getenv("TOKEN_TYPE")

    # Initialize the db variable
    db = None

    # Connect to the Supabase database
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    db = create_client(url, key)

    # Suppress yahoo_oauth log messages unless there's an error
    logging.getLogger("yahoo_oauth").setLevel(logging.ERROR)

    if os.getenv("AWS_EXECUTION_ENV") != "None":
        file_path = "/tmp/secrets.json"
    else:
        file_path = "secrets.json"  # Adjust this path as needed

    with open(file_path, "w") as f:
        json.dump(
            {
                "access_token": access_token,
                "consumer_key": consumer_key,
                "consumer_secret": consumer_secret,
                "guid": guid,
                "token_time": token_time,
                "refresh_token": refresh_token,
                "token_type": token_type,
            },
            f,
        )

    oauth = OAuth2(
        consumer_key,
        consumer_secret,
        access_token=access_token,
        token_time=token_time,
        refresh_token=refresh_token,
        token_type=token_type,
    )

    # Use the oauth object to create a League object
    this_years_league = yfa.League(oauth, "431.l.51071")
    # last_years_league = yfa.League(oauth, "422.l.115216")

    # Get the league standings
    standings = this_years_league.standings()
    print(standings)

    team_stats_table = db.table("team_stats")

    response = team_stats_table.select("*").execute()
    initial_count = len(response.data)

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

    response = team_stats_table.select("*").execute()
    final_count = len(response.data)

    result = f"Initial count: {initial_count}, Final count: {final_count}"
    return {"statusCode": 200, "body": result}

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


if __name__ == "__main__":
    handler(None, None)
