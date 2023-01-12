#!/bin/bash

# check if the database file exists
if [ ! -f data/links.sqlite ]; then
    # initialize the database
    sqlite3 data/links.sqlite < init/schema.sql
    echo "Database initialized"
else
    echo "Database already exists"
fi
