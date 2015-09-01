# repo_lookup

### repo_lookup.py
*cli script that will prompt for *organization*, *github username* and *github password*
*will look for all team, members and repositories
*will fetch them in a pretty table
*`python repo_lookup.py`, and that's it

### cron.py
*cli cron script to be executed in crontab
*gets all members and repositories and push them in a sqlite db
*`python cron.py <organization> <github username> <github password>`

### functions.py
*generalistic functions (display, db cnx, etc.)
*github api wrappers and error handling
