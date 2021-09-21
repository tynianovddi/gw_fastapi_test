#!/bin/bash

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./initial_data_setup.py
