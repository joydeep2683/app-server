# app-server
To Run app-server -
```
pip install virtualenv
virtualenv .venv -p /opt/homebrew/bin/python3.12
[Use brew to install python3.12 if not installed]
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
[Ask for .env file]
python manage.py runserver
```
