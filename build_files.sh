#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
echo "Build completed successfully!"
