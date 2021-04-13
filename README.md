# alt_article

A Flask application to recommend alternative news articles using a preprocessed dataset.

## Setup venv and install requirements:

```
python -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt
```

## Run flask app:

```
export FLASK_APP=main.py

# Activate debugging mode
export FLASK_ENV=development

flask run
```