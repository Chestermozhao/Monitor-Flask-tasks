```
_____ _           _          ____     _                       _____ _                        
|  ___| | __ _ ___| | __     / ___|___| | ___ _ __ _   _      |  ___| | _____      _____ _ __ 
| |_  | |/ _` / __| |/ /____| |   / _ \ |/ _ \ '__| | | |_____| |_  | |/ _ \ \ /\ / / _ \ '__|
|  _| | | (_| \__ \   <_____| |__|  __/ |  __/ |  | |_| |_____|  _| | | (_) \ V  V /  __/ |   
|_|   |_|\__,_|___/_|\_\     \____\___|_|\___|_|   \__, |     |_|   |_|\___/ \_/\_/ \___|_|   
                                                   |___/                                      						   
```
---
# Project description
Flask-Celery-Flower is the project for practicing building async tasks and monitoring broker queue wieh Flower.

---
# Quick Start

## Prerequisite
- Python 3.8

## Development

#### Initial venv

```shell
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### Init git pre-commit

```
pre-commit install
```

#### Create .env file

```shell
# The valid environment variables need be completed with your email configuration
cp env.example .env
```

## Development Run flask server

Run develop

```
python celery_flask_demo/celery_flask.py
```

## celery worker

Init celery worker
```
cd celery_flask_demo
celery -A celery_flask.celery worker --loglevel=INFO
```

## flower dashboard

Configure flower dashboard to monitor redis broker status
```
cd celery_flask_demo
flower -A celery_flask.celery --broker=redis://localhost:6379/0
```
