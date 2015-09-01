__author__ = 'fxechappe'
import time, sys, requests, json, inspect, sqlite3

url = "https://api.github.com/"
OK = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


"""
UTILS FUNCTIONS
"""


def br(v):
    """
    prints loading points
    :param v:
    :return:
    """
    if v == 's':
        for i in range(18):
            print("."),
            time.sleep(0.07)
            sys.stdout.flush()
    else:
        for i in range(18):
            print("."),
    print("\n")


def lno():
    """
    Returns the current line number in our program
    :return:
    """
    return "l." + str(inspect.currentframe().f_back.f_lno) + "-"


def ppj(j):
    """
    prints a prettified output for json in console
    :param j:
    :return:
    """
    print(json.dumps(j, sort_keys=True, indent=2, separators=(',', ': ')))


def welcome():
    welcome_msg = """
        ###################################
        ############ REPO LOOKUP ##########
        ###################################
        """
    print(welcome_msg)


def bye():
    welcome_msg = """
        ###################################
        ###################################
        ###################################
        """
    print(welcome_msg)
    sys.exit()


def set_db():
    """
    sets db, create db and tables if not exist
    """
    db = sqlite3.connect('db/repo_lookup.db')
    db.execute("CREATE TABLE if not exists member (id INTEGER PRIMARY KEY, name char(100) NOT NULL, repos INTEGER, created_at DATETIME, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    db.execute('CREATE UNIQUE INDEX if not exists "uniq name" ON "member" ("name")')
    db.execute("CREATE TABLE if not exists org (id INTEGER PRIMARY KEY, name char(100) UNIQUE NOT NULL, created_at DATETIME, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    # db.execute("CREATE TABLE if not exists repo (id INTEGER PRIMARY KEY, name char(100) NOT NULL, created_at DATETIME, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    # db.execute("CREATE TABLE if not exists team (id INTEGER PRIMARY KEY, org_id INTEGER, name char(100) NOT NULL, created_at DATETIME, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    # db.execute("CREATE TABLE if not exists team_member (member_id INTEGER, team_id INTEGER, created_at DATETIME, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    # db.execute('CREATE UNIQUE INDEX if not exists "uniq" ON "team" ("org_id", "name")')
    db.commit()
    return db

"""
GITHUB API FUNCTIONS
"""


def get_org(org_name, creds):
    """
    gets org's datas
    :param org_name:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "orgs/" + org_name, auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return r.json


def get_org_repos(org_name, creds):
    """
    gets org's repositories number
    :param org_name:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "orgs/" + org_name + "/repos", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return r.json


def get_org_teams(org_name, creds):
    """
    gets org's teams
    :param org_name:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "orgs/" + org_name + "/teams", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return r.json


def get_team_repos(team_id, creds):
    """
    gets number of repos for a given team
    :param team_id:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "teams/" + str(team_id) + "/repos", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return len(r.json)


def get_team_members(team_id, creds):
    """
    gets members of a given team
    :param team_id:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "teams/" + str(team_id) + "/members", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return r.json


def get_org_members(org_name, creds):
    """
    gets members of a given org
    :param org_name:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "orgs/" + org_name + "/members", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return r.json


def get_member_repos(login, creds):
    """
    gets repos for a given member
    :param login:
    :param creds:
    :return:
    """
    try:
        r = requests.get(url + "users/" + login + "/repos", auth=(creds[1], creds[2]))
    except Exception as e:
        print(FAIL + lno() + str(e))
        sys.exit()
    try:
        print(FAIL + str(r.json['message']))
        return False
    except Exception as e:
        return len(r.json)
