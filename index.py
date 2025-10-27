# index.py
from fruitables.wsgi import application

# Vercel expects a callable named `app`
app = application
