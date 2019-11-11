import pyLDAvis.sklearn
import numpy as np
import re

# given a document (= book) consisting in a single string, extracts all the text
# enclosed in round brackets and returns a list of document, where each document
# consists in a group of words that were previously part of the same bracket group
def extract_parenthesis_groups(book_text, n_chars):
	docs = []
	tmp_text = book_text
	while True:
		match = False
		for match in re.finditer("\([^\(\)]*\)", tmp_text):
			start, end = match.span()
			docs.append(tmp_text[start-n_chars:end+n_chars])
			match = True

		tmp_text = re.sub("\([^\(\)]*\)", "", tmp_text)

		if not match:
			return docs

# passes the text to the vectorizer that will transform it into numbers, and applies
# the filters for word and document lenght
def feed_data(data, transformer, min_word_length, min_words_doc):
	for doc in data:
		t_data = [w for w in transformer(doc) if len(w) >= min_word_length]
		if len(t_data) >= min_words_doc:
			yield ' '.join(t_data)

# computes the TopicModeling visualization and saved it on the file system
def visualize_lda(lda_model, TDmatrix, vectorizer, sort_t, path):
	panel = pyLDAvis.sklearn.prepare(lda_model, TDmatrix, vectorizer, mds='tsne', sort_topics=sort_t)
	pyLDAvis.save_html(panel, path)
