#!/bin/bash
python ANNA/manage.py migrate
echo 'server start'
python ANNA/manage.py runserver