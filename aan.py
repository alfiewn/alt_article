import pandas as pd
import numpy as np

from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

valid_article_df = None

def in_memory(df):
  global valid_article_df
  valid_article_df = df

def contains_topic(other_topics, input_article_topic):
  other_topics = eval(other_topics)
  for topic in other_topics:
    if topic in input_article_topic:
      return True
  return False

def entity_string(entities, n):
  top_entities = Counter(entities).most_common(n)
  entityString = ""
  for entityTuple in top_entities:
    repeats = entityTuple[1]
    entity = entityTuple[0]
    for i in range(repeats):
      entityString = entityString + " " + entity
  return entityString

def find_similarities(entities, input_article_entities):
  similarities = []
  for entity_list in entities:
    to_compare = entity_string(eval(entity_list), 10)

    vector = CountVectorizer().fit_transform([input_article_entities, to_compare])

    score = cosine_similarity(vector[0:1], vector).flatten()[1]
    
    similarities.append(score)

  return similarities

def get_sentiment_balances(sentiments, input_article_sentiment):
  sentiment_balances = []
  for sentiment in sentiments:
    sentiment_balance = abs(eval(sentiment)[0] + input_article_sentiment)
    sentiment_balances.append(sentiment_balance)
  return sentiment_balances

def get_alternative_article(input_article_index):
    
  # valid_article_df = pd.read_csv('./articles_w_sentiment.csv', delimiter='\t')

  input_article_body = valid_article_df['body'][input_article_index]
  input_article_url = valid_article_df['url'][input_article_index]

  input_article_topic = eval(valid_article_df['topic'][input_article_index])
  input_article_entities = eval(valid_article_df['entities'][input_article_index])
  input_article_sentiment = eval(valid_article_df['sentiment'][input_article_index])[0]


  matching_article_df = valid_article_df.loc[valid_article_df['topic'].apply(lambda topics: contains_topic(topics, input_article_topic))]

  matching_article_df = matching_article_df.drop([input_article_index])

  matching_entities = matching_article_df['entities']
  matching_article_df['similarity'] = find_similarities(matching_entities, entity_string(input_article_entities, 10))

  matching_sentiments = matching_article_df['sentiment']
  matching_article_df['sentiment_balance'] = get_sentiment_balances(matching_sentiments, input_article_sentiment)

  rankings = list(range(0, len(matching_article_df)))

  by_similarity = matching_article_df.sort_values(
      by='similarity', 
      ascending=False
      ).drop(['nid', 'category', 'abstract'], axis=1)

  by_similarity['similarity_rank'] = rankings

  by_sentiment_balance = by_similarity.sort_values(
      by='sentiment_balance', 
      ascending=True
      )

  by_sentiment_balance['balance_rank'] = rankings

  similarity_rankings = by_sentiment_balance['similarity_rank']

  optimised_rankings = []
  for similarity, sentiment in zip(similarity_rankings, rankings):
      optimised_rankings.append(similarity + sentiment)

  by_sentiment_balance['optimised'] = optimised_rankings


  alternative_article = None if len(by_sentiment_balance) == 0 else by_sentiment_balance.sort_values(
      by='optimised', 
      ascending=True
      ).iloc(0)

  if not alternative_article:
    return None
  else:
    return {
              "input_body": input_article_body,
              "input_url": input_article_url,
              "input_sentiment": input_article_sentiment,
              "alternative_body": alternative_article[0]['body'],
              "alternative_url": alternative_article[0]['url'],
              "alternative_sentiment": eval(alternative_article[0]['sentiment'])[0],
              "similarity": alternative_article[0]['similarity'],
              "sentiment_balance": alternative_article[0]['sentiment_balance']
    } 