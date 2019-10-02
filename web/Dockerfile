from python:3.7

workdir /app
copy requirements.txt requirements.txt
run pip install -r requirements.txt
copy . .
env PYTHONPATH /app
cmd [ "gunicorn", "-c", "gunicorn_conf.py", "--reload", "server:app" ]
