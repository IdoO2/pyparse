#!/bin/bash
# Builds database structure for pyparse plugin
# This db is mostly use for development and debugging
# In production it's strongly recommanded to use an in memory db.

db_file="db-symbol" # database default name

if [ -f $db_file ]
then
  echo "delete previous $db_file"
  rm $db_file
fi

sqlite3 -echo $db_file < struct.sql # build a new db using struct.sql

