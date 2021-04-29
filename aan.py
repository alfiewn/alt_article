from collections import Counter
from itertools import starmap

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

valid_article_df = None

def load_article_df():
  global valid_article_df
  valid_article_df = pd.read_csv('./articles_w_sentiment.csv', delimiter='\t')

def contains_topic(other_topics, input_article_topic):
  for topic in other_topics:
    if topic in input_article_topic:
      return True
  return False

def entity_string(entities, n=10):
  top_entities = Counter(entities).most_common(n)
  entity_string = ""
  for entityTuple in top_entities:
    repeats = entityTuple[1]
    entity = entityTuple[0]
    for i in range(repeats):
      entity_string = entity_string + " " + entity
  return entity_string.lstrip()

def find_similarity(input_entities, alternative_entities):

  input_entities_string = entity_string(input_entities)
  alternative_entites_string = entity_string(alternative_entities)

  vector = CountVectorizer().fit_transform([input_entities_string, alternative_entites_string])
  return cosine_similarity(vector[0:1], vector).flatten()[1]

def find_balance(input_article_sentiment, alternative_sentiment):
  return round((alternative_sentiment + input_article_sentiment)/2, 3)

def find_ranking(similarity_ranking, sentiment_ranking):
  return similarity_ranking + sentiment_ranking


def get_by_title(title):
  index = valid_article_df[valid_article_df['title'].str.strip()==(title)].index
  return (False, {"error": f"No article found with title: {title}"}) if index.empty else get_by_index(index[0])

def get_by_index(input_article_index):
  input_article_body = valid_article_df['body'][input_article_index]
  input_article_url = valid_article_df['url'][input_article_index]

  input_article_topic = eval(valid_article_df['topic'][input_article_index])
  input_article_entities = eval(valid_article_df['entities'][input_article_index])
  input_article_sentiment = eval(valid_article_df['sentiment'][input_article_index])[0]


  matching_article_df = valid_article_df.loc[valid_article_df['topic'].apply(lambda alternative_topic: contains_topic(eval(alternative_topic), input_article_topic))]

  matching_article_df = matching_article_df.drop([input_article_index])

  matching_entities = matching_article_df['entities']
  matching_article_df['similarity'] = matching_entities.map(lambda alternative_entities: find_similarity(eval(alternative_entities), input_article_entities))

  matching_sentiments = matching_article_df['sentiment']
  matching_article_df['sentiment_balance'] = matching_sentiments.map(lambda alternative_sentiment: find_balance(eval(alternative_sentiment)[0], input_article_sentiment))

  rankings = list(range(0, len(matching_article_df)))

  by_similarity = matching_article_df.sort_values(
      by='similarity', 
      ascending=False,
      key=abs
      )

  by_similarity['similarity_rank'] = rankings

  by_sentiment_balance = by_similarity.sort_values(
      by='sentiment_balance', 
      ascending=True,
      key=abs
      )

  by_sentiment_balance['balance_rank'] = rankings

  similarity_rankings = by_sentiment_balance['similarity_rank']

  by_sentiment_balance['optimised'] = list(starmap(find_ranking, zip(similarity_rankings, rankings)))

  alternative_article = None if len(by_sentiment_balance) == 0 else by_sentiment_balance.sort_values(
      by='optimised', 
      ascending=True
      ).iloc(0)

  if not alternative_article:
    return (False, {"error": "Failed to find a valid alternative article"})
  else:
    return (True, {
              "input_body": input_article_body,
              "input_url": input_article_url,
              "input_sentiment": input_article_sentiment,
              "alternative_body": alternative_article[0]['body'],
              "alternative_url": alternative_article[0]['url'],
              "alternative_sentiment": eval(alternative_article[0]['sentiment'])[0],
              "similarity": alternative_article[0]['similarity'],
              "sentiment_balance": alternative_article[0]['sentiment_balance']
    })
