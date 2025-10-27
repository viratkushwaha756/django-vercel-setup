@echo off
echo Activating Virtual Environment...
call venv\Scripts\activate.bat
echo Virtual Environment Activated!
echo.
echo To run the Django server: python manage.py runserver
echo To deactivate: deactivate
echo.
cmd /k
