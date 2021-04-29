# alt_article

A Flask application to recommend alternative news articles using a preprocessed dataset.

The pipeline to process the article data can be found at: 
https://colab.research.google.com/drive/18AEcfJKpftjEWO5Oc1_LisQV1DM2E9Ww?usp=sharing.

The model used to analyse sentiment can be found at:
https://colab.research.google.com/drive/1aRL4xfylNlhU9ICenthmfTYizkjkvhkm?usp=sharing

This application in a notebook form can be found at:
https://colab.research.google.com/drive/1-yI-tPEWy-EWbhV7o00K3neOPH2L3VOP?usp=sharing

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

## Run unit tests:

```
python -m unittest
```

## Test Response Times

```
python response_test.py
```

## Test the endpoints

### Get article by index
Note: Article index must be within the bounds of the dataset.
```
curl http://127.0.0.1:5000/by_index/10000
```

### Get article by title
Note: Article title should be encoded for use in URL.

```
curl http://127.0.0.1:5000/by_title/Oklahoma%20prison%20officials%20say%20cellphone%20jamming%20would%20help
```
