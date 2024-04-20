import json
import logging
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from datetime import datetime
from db_connection import db
import os

# Suppress yahoo_oauth log messages unless there's an error
logging.getLogger('yahoo_oauth').setLevel(logging.ERROR)

# CONSTANTS LAST YEAR
TEAM_NAMES = ['AAA Chiefs', "Jordan's World-Class Team", 'AA Chiefs', 'The Toronto Blue Jays', 'Laurie’s Permacks', 'Riber Hites Kardenles']
TEAM_IDS= ['422.l.115216.t.1', '422.l.115216.t.2', '422.l.115216.t.3', '422.l.115216.t.4', '422.l.115216.t.5', '422.l.115216.t.6']
# Authenticate with the Yahoo API
oauth = OAuth2(None, None, from_file=os.path.join('config', 'oauth2.json'))

# Use the oauth object to create a League object
this_years_league = yfa.League(oauth, '431.l.51071')
last_years_league = yfa.League(oauth, '422.l.115216')

# Get the league standings and pretty-print them
standings = this_years_league.standings()
print("THIS IS STANDINGS")
print(json.dumps(standings, indent=4))

teams = this_years_league.teams()
for team in teams:
  print(team)


# Get the team object
team = this_years_league.to_team(TEAM_IDS[0])

# Specify the date
date = datetime(2023, 9, 4)

# Get the team's roster for the specified date
# We can't do this because MLB doesn't let you check rosters for past dates
# We should probably start our own DB that keeps the historical records
# roster = team.roster(date)

# Print the roster
# print(f"Roster on {date}: {roster}")
team_names = []

# # print the team names
for team in standings:
  team_names.append(team['name'])
print("this is team_names", team_names)

# #Get team key
team_key = this_years_league.team_key()
print('team key: ', team_key)

# # get team object
team = this_years_league.to_team(team_key)
print("team: ", team)

# #get team stuff
roster = team.roster()
# print("roster: ", roster)
