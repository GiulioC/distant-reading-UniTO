from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import re, os, sys
import numpy as np
import textract
import utils

files_dir = "files"
n_features = 2000
n_topics = 20
w_threshold = 4
d_threshold = 5

manual_stopwords = [
	"word1", "word2", "..."
]

documents = []
for file in os.listdir(files_dir):
	if file.endswith(".docx") or file.endswith(".txt"):
		os.rename(
			os.path.join(files_dir, file),
			os.path.join(files_dir, '_'.join(file.split()))
		)
for file in os.listdir(files_dir):
	if file.endswith(".docx"):
		text = textract.process(os.path.join(files_dir,file), extension='docx').decode('utf-8')
	elif file.endswith(".txt"):
		with open(os.path.join(files_dir,file), "r") as f:
			text = f.read()
	else:
		continue

	print("[{}]".format(file))

	text = re.sub('\\n', '', text)
	text = re.sub('[\t\s]{2,}', ' ', text)
	text = re.sub('- ', '', text)
	text = re.sub('[0-9]{1,}', '', text)

	documents.extend(utils.extract_parenthesis_groups_v2(text))
	print(len(documents), "Total documents\n")

print("DOCUMENTS:",len(documents))
print("AVG CHARS: ",np.mean([len(d) for d in documents]))
print("MIN CHARS: ",np.min([len(d) for d in documents]))
print("MAX CHARS: ",np.max([len(d) for d in documents]))
print("AVG WORDS: ",np.mean([len(d.split()) for d in documents]))
print("MIN WORDS: ",np.min([len(d.split()) for d in documents]))
print("MAX WORDS: ",np.max([len(d.split()) for d in documents]))

cv = CountVectorizer(
	stop_words=set(list(stopwords)+manual_stopwords),
	analyzer='word',
    min_df=0.0,
    max_df=0.8,
	max_features=n_features
)
analyzer = cv.build_analyzer()

TDmat = cv.fit_transform(utils.feed_data(documents, analyzer, w_threshold, d_threshold))
lda = LatentDirichletAllocation(n_components=n_topics)
lda.fit_transform(TDmat)
utils.visualize_lda(lda, TDmat, cv, True, "lda_{}_{}.html".format(n_topics, n_features))
