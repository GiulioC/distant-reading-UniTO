from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import re, os, sys
import numpy as np
import utils

files_dir = "files"

#configurable parameteres. Play with them and see how they affect the final result
# number of different words to consider. The model will use n_features most frequent words
n_features = 2000
# number of topics to derive from the documents
n_topics = 20
# minimun lenght of the words. All those with length < w_threshold will be ignored
w_threshold = 4
# minimum number of words to consider a document valid. Those with less than
# d_threshold words will be ignored
d_threshold = 5
# how much charactes outside the brackets to include when extracting bracketed text
num_characters_around_brackets = 0
# fill this list with all the words you want to ignore
manual_stopwords = [
	"word1", "word2", "..."
]

documents = []
# read one file at a time from the file system
for file in os.listdir(files_dir):
	# skip all files that are not in .txt format
	if not file.endswith(".txt"):
		continue
	# remove whitespaces from files' names
	os.rename(
		os.path.join(files_dir, file),
		os.path.join(files_dir, '_'.join(file.split()))
	)
	# open the file and load its content in memory
	with open(os.path.join(files_dir,file), "r", encoding="utf-8") as f:
		text = f.read()

	# display the file we are currently working on
	print("[{}]".format(file))

	# remove new lines
	text = re.sub('\\n', '', text)
	# remove series of two or more spaces/tabs
	text = re.sub('[\t\s]{2,}', ' ', text)
	# remove words that were previously separated by a newline
	text = re.sub('- ', '', text)
	# remove numbers
	text = re.sub('[0-9]{1,}', '', text)

	# extract all the text inside of two round brackects and consider each of them
	# as a single document
	documents.extend(utils.extract_parenthesis_groups(text, num_characters_around_brackets))
	# display the total number of documents found in the current file
	print(len(documents), "Total documents\n")

# display some statistics about the documents
print("DOCUMENTS:",len(documents)) #total number
print("AVG CHARS: ",np.mean([len(d) for d in documents])) #average length (in characters)
print("MIN CHARS: ",np.min([len(d) for d in documents])) #minimum length (in characters)
print("MAX CHARS: ",np.max([len(d) for d in documents])) #maximum length (in characters)
print("AVG WORDS: ",np.mean([len(d.split()) for d in documents])) #average length (in words)
print("MIN WORDS: ",np.min([len(d.split()) for d in documents])) #minimum length (in words)
print("MAX WORDS: ",np.max([len(d.split()) for d in documents])) #maximum length (in words)

# this is the module that transforms textual data into numbers. This is needed
# because TopicModeling algorithm expects a list of numbers rather than a list
# of words
cv = CountVectorizer(
	stop_words=set(list(stopwords)+manual_stopwords),
	analyzer='word',
    min_df=0.0,
    max_df=0.8,
	max_features=n_features
)
# this will handle text preprocessing
analyzer = cv.build_analyzer()

# transform the list of documents into a big matrix of numbers (rows: documents,
# columns: n_features distinct words)
TDmat = cv.fit_transform(utils.feed_data(documents, analyzer, w_threshold, d_threshold))
# instantiate the TopicModeling algorithm
lda = LatentDirichletAllocation(n_components=n_topics)
# train the algorithm of the transformed documents
lda.fit_transform(TDmat)
# visualize the result in a handy way
utils.visualize_lda(lda, TDmat, cv, True, "lda_{}_{}.html".format(n_topics, n_features))
