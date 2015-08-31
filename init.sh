#!/bin/bash
# Builds database structure for pyparse plugin
# This db is mostly use for development and debugging
# In production it's strongly recommanded to use an in memory db.

WORKING_DIR=`pwd`
DB_DIR=$WORKING_DIR'/src/parser/db'
STRUCT=$DB_DIR'/struct.sql'
DB_FILE=$DB_DIR'/db-symbol' # database default name

if [ -f $DB_FILE ]
then
  echo "delete previous $DB_FILE"
  rm $DB_FILE
fi

sqlite3 -echo $DB_FILE < $STRUCT # build a new db using struct.sql
