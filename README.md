python -m venv .venv

.venv\Scripts\activate

.venv\Scripts\deactivate

python -m pip install -r requirement.txt #install all modules at once (specifically used in venv)

pip show <package-name> #to get the version of the module installed



run fast api
uvicorn main:app --reload

CTL + C to stop or from right side panel, right click terminal and close


use sqlite from CMD
go to db file.. app/data/genesis_db
sqlite3 genesis.db

Command	Description
.tables	Show all tables in the database
.schema	Show schema (table structure)
SELECT * FROM user;	Query a table
.exit or .quit	Exit SQLite prompt
.headers on	Show column names in query results
.mode column	Pretty-print tabular results