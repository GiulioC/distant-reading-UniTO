import pyLDAvis.sklearn
import numpy as np
import re

def match_right_text(r_text, n):
	regex = ""
	for _ in range(n):
		regex = regex + "[^\)]*\)"
	match = re.match(regex, r_text)
	txt = match.group()

	open_p = txt[:-1].count("(")
	closed_p = txt[:-1].count(")")

	if open_p > closed_p:
		inner_txt, inner_end = match_right_text(r_text[match.span()[1]+1:], (open_p-closed_p))
		return txt + inner_txt, match.span()[1]+inner_end
	else:
		return txt, match.span()[1]

def extract_parenthesis_groups(book_text):
	docs = []
	while True:
		m = re.search("\([^\)]{5,}\)", book_text)

		if m is None:
			break

		span = m.span()
		start = span[0]
		end = span[1]
		group = m.group()

		group_p = group
		open_p = group_p[1:-1].count("(")
		closed_p = group_p[1:-1].count(")")

		if open_p > closed_p:
			try:
				right_text, extended_end = match_right_text(book_text[end+1:],open_p-closed_p)
				p_text = group + " " + right_text
				end = end + extended_end
			except AttributeError:
				p_text = group
		else:
			p_text = group

		docs.append(p_text)
		book_text = book_text[end:]
	return docs

def extract_parenthesis_groups_v2(book_text):
	docs = []
	tmp_text = book_text
	while True:
		match = False
		for match in re.finditer("\([^\(\)]*\)", tmp_text):
			docs.append(match.group())
			match = True

		tmp_text = re.sub("\([^\(\)]*\)", "", tmp_text)

		if not match:
			return docs

def feed_data(data, transformer, min_word_length, min_words_doc):
	for doc in data:
		t_data = [w for w in transformer(doc) if len(w) >= min_word_length]
		if len(t_data) >= min_words_doc:
			yield ' '.join(t_data)

def visualize_lda(lda_model, TDmatrix, vectorizer, sort_t, path):
	panel = pyLDAvis.sklearn.prepare(lda_model, TDmatrix, vectorizer, mds='tsne', sort_topics=sort_t)
	pyLDAvis.save_html(panel, path)
