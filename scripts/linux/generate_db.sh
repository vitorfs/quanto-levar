#!/bin/bash

cd ../..

rm db.sqlite3 
python manage.py syncdb
