import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import os
from constants import CURRENT_MANAGERS, BATTER_STATS, PITCHER_STATS
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timezone


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

    oauth = OAuth2(
        consumer_key,
        consumer_secret,
        store_file=False,
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

    try:
        response = team_stats_table.select("*").execute()
    except Exception as e:
        print(e)
    initial_count = len(response.data)

    # Get today's date in UTC
    today = datetime.now(timezone.utc).date()

    # Check if the first response has any entries from today's date
    for entry in response.data:
        # Parse the 'created_at' timestamp into a datetime object and convert it to a date
        entry_date = datetime.strptime(
            entry["created_at"], "%Y-%m-%dT%H:%M:%S.%f+00:00"
        ).date()
        if (
            entry_date.year == today.year
            and entry_date.month == today.month
            and entry_date.day == today.day
        ):
            return {"statusCode": 200, "body": "Entry from today's date already exists"}

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

    try:
        response = team_stats_table.select("*").execute()
    except Exception as e:
        print(e)
    final_count = len(response.data)

    result = f"Initial count: {initial_count}, Final count: {final_count}"
    return {"statusCode": 200, "body": result}


if __name__ == "__main__":
    handler(None, None)
