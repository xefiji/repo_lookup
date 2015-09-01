__author__ = 'fxechappe'
import sqlite3, sys
from functions import *
from datetime import date, datetime

db = set_db()

if len(sys.argv) != 4:
    print('missing parameter')
    sys.exit()
else:
    org_name = sys.argv[1]
    username= sys.argv[2]
    password = sys.argv[3]
    creds = [org_name, username, password]

# getting org
org = get_org(org_name, creds)
if not org:
    sys.exit()

t = (org['name'], datetime.now())
try:
    db.execute('INSERT OR IGNORE INTO org(name, created_at) VALUES(?,?)', t)
    db.commit()
except Exception as e:
    print(lno() + str(e))
    sys.exit()

# getting members
members = get_org_members(org_name, creds)
if not org:
    print('No members, wtf ?')
    sys.exit()

for member in members:
    total_repos = get_member_repos(member['login'], creds)
    # insert
    try:
        t = (member['login'], total_repos, datetime.now())
        db.execute('INSERT OR IGNORE INTO member(name, repos, created_at) VALUES(?,?,?)', t)
        db.commit()
    except Exception as e:
        print(lno() + str(e))
        sys.exit()

    # update (in 2 times coz no "on duplicate key" clause in sqlite ??)
    try:
        t = (total_repos, member['login'])
        db.execute('UPDATE member SET repos = ? WHERE name = ?', t)
        db.commit()
    except Exception as e:
        print(lno() + str(e))
        sys.exit()


"""
# TODO push org, team and repos in database
# TODO adds join table (org_has_team, team_has_member, member_hash_repo)
# BELOW: not tested code

try:
    ret = db.execute("SELECT last_insert_rowid()")
except Exception as e:
    print(lno() + str(e))
    sys.exit()

last_id = ret.fetchone()[0]

if last_id == 0:
    try:
        ret = db.execute('SELECT id FROM org WHERE name = ?', (org['name'], ))
    except Exception as e:
        print(lno() + str(e))
        sys.exit()
    org_id = ret.fetchone()[0]
else:
    org_id = last_id

# getting org's teams
teams = get_org_teams(org_name, creds)
if not teams:
    sys.exit()

sql = "INSERT OR IGNORE INTO team(org_id, name, created_at) VALUES "
datas = ()
for team in teams:
    sql += "(?,?,?),"
    datas += org_id, team['name'], datetime.now()

    # getting team's membres
    team_members = get_team_members(team['id'], creds)
    ppj(team_members)

    sql_members = "INSERT OR IGNORE INTO member(name, repos, created_at) VALUES "
    data_members = ()
    for member in team_members:
        sql_members += "(?,?,?),"
        member['total_repos'] = get_member_repos(member['login'], creds)
        data_members += member['login'], member['total_repos'], datetime.now()
try:
    ret = db.execute(sql[:-1], datas)
    db.commit()
except Exception as e:
    print(lno() + str(e))
    sys.exit()
"""






