#!/usr/bin/env bash

# Let the db start
python3 ./backend_pre_start.py
# Run migrations
alembic upgrade head
# Create initial data in db
python3 ./initial_data.py
