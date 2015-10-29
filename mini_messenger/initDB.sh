#/bin/bash
rm data.db
sqlite3 data.db < "CS166_Project/sql/src/create_tables.sql"
sqlite3 data.db < "import.sql"
