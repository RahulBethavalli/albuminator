#!/bin/sh

exec gunicorn -b :8000 --access-logfile - --error-logfile - --timeout 60000 server:app
