import unittest
from aan import *


class test_notebook(unittest.TestCase):

  def test_contains_topic(self):
    input_topic = ["Donald Trump", "Trump"]
    input_alternative_topic = ["Donald Trump"]
    expected = True

    self.assertEqual(contains_topic(input_alternative_topic, input_topic), expected)

  def test_not_contains_topic(self):
    input_topic = ["Donald Trump", "Trump"]
    input_alternative_topic = ["Obama"]
    expected = False

    self.assertEqual(contains_topic(input_alternative_topic, input_topic), expected)

  def test_entity_string(self):
    input = ["Donald Trump", "Trump", "Obama", "Donald Trump", "Pelosi"]
    input_threshold = 3
    expected = "Donald Trump Donald Trump Trump Obama"

    self.assertEqual(entity_string(input, input_threshold), expected)

  def test_find_similarities(self):

    input = ['Donald Trump', 'Donald Trump', 'Trump', 'Obama']

    input_same = ['Donald Trump', 'Donald Trump', 'Trump', 'Obama']
    expected_same = 1.0

    input_similar = ['Donald Trump', 'Donald Trump', 'Obama', 'Pelosi']
    expected_similar = lambda similarity: 0.0 < similarity < 1.0

    input_different = ['Pelosi', 'Pelosi', 'Capitol', 'Whitehouse']
    expected_different = 0.0

    self.assertEqual(find_similarity(input_same, input), expected_same)

    self.assertTrue(expected_similar(find_similarity(input_similar, input)))

    self.assertEqual(find_similarity(input_different, input), expected_different)

  def test_find_balance(self):

    input_sentiment = 3.12
    input_alternative_sentiment = -3.07
    expected = 0.025

    self.assertEqual(find_balance(input_alternative_sentiment, input_sentiment), expected)