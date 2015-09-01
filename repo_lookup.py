__author__ = 'fxechappe'

from functions import *
import sys, getpass
from terminaltables import AsciiTable
from colorclass import Color, Windows

# welcome message
welcome()

# prompt cnx vars
org_name = str(raw_input(">>>Org name ?\n"))
username = str(raw_input(">>>User name ?\n"))
password = str(getpass.getpass(">>>Password ?\n"))

creds = [org_name, username, password]

# output
br("f")
print("Looking for repo for org **{}**".format(org_name.upper()))
br("s")

# getting org
org = get_org(org_name, creds)
if not org:
    sys.exit()

# getting org's repos
org_repos = get_org_repos(org_name, creds)
if not org_repos:
    sys.exit()

if org_repos == 0:
    print(WARNING + "No repo found!" + ENDC)
    print("exiting -> []")
    sys.exit()

# getting org's teams
teams = get_org_teams(org_name, creds)
if not teams:
    sys.exit()

if len(teams) == 0:
    print(WARNING + "No team found!" + ENDC)
    print("exiting -> []")
    sys.exit()

# output
print(OK + ("{} teams found!".format(len(teams)) + ENDC + "\n"))

# final datas dict construction
team_datas = []
for team in teams:

    # getting number of team's repos
    team_repos = get_team_repos(team['id'], creds)

    # getting team's membres
    team_members = get_team_members(team['id'], creds)

     # getting members repos
    for member in team_members:
        member['total_repos'] = get_member_repos(member['login'], creds)

    try:
        team_datas.append({'name': team['name'], 'total_repos': team_repos, 'members': team_members})
    except:
        pass

# table to display
table_datas = []
headers = ["TEAMS:"]
t_repos = ["REPOS:"]
t_members = ["MEMBERS(repos):"]
for t in team_datas:

    # headers
    headers.append(str(t['name']).upper())

    # members
    m = ""
    for member in t['members']:
        m += member['login'] + "(" + str(member['total_repos']) + ")" + "\n"
    t_members.append(m)

    # total repos
    t_repos.append(str(t['total_repos']))


table_datas.append(headers)
table_datas.append(t_members)
table_datas.append(t_repos)

table = AsciiTable(table_datas, org_name.upper() + " - Total: " + str(org_repos) + " different repos")
table.inner_row_border = True
print(table.table)

bye()