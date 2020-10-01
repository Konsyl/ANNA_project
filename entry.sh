#!/bin/bash
python ANNA/manage.py migrate
echo 'server start'
python ANNA/manage.py runserver 0.0.0.0:8000