from python:3.7

workdir /app
copy requirements.txt requirements.txt
run pip install -r requirements.txt
copy . .
copy ./python_pb /python_pb
env PYTHONPATH /app
cmd [ "gunicorn", "-c", "gunicorn_conf.py", "--reload", "http_server:app" ]
