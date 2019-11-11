from sklearn.feature_extraction.text import CountVectorizer
import levenshtein as lvs
import os, re

files_dir = "files"
out_dir = "results"

#configurable parameteres. Play with them and see how they affect the final result
# max levenshtein distance from the target word (erlebnis or erfahrung) that a
# book's word must have in order to be considere valid
max_levenshtein = 2
# max difference in length for a word to be eligible to be a levenshtein word
# of the target one
max_length_difference = 2

# for each target word, specify all the possible forms that it may assume. This is
# to tackle OCR errors
similar_words = {
	"erlebnis": ["erleben", "erfahrang"],
	"erfahrung": ["erfahren"],
}
# all the following words will be ignored no matter what
ignore_words = [
	"word1", "word2", "..."
]

# we will use this module to preprocess and clean text, and transform it into a
# list of words
cv = CountVectorizer(stop_words=None, analyzer='word')
analyzer = cv.build_analyzer()

# process all files one at a time
for input_file in os.listdir(files_dir):
	# skip files that are not .txt
	if not input_file.endswith(".txt"):
		continue

	# display the current file
	print("[{}]".format(input_file))

	# open the file and load its content in memory
	with open(os.path.join(files_dir,input_file), "r", encoding="utf-8") as f:
		text = f.read()

	# remove new lines
	text = re.sub('\\n', '', text)
	# remove series of two or more spaces/tabs
	text = re.sub('[\t\s]{2,}', ' ', text)
	# remove words that were previously separated by a newline
	text = re.sub('- ', '', text)
	# remove numbers
	text = re.sub('[0-9]{1,}', '', text)

	# transform the file content into a list of word
	book_words = analyzer(text)

	# iterate over target words
	for desired_word, similar_words in similar_words.items():
		#initialize number of matches to zero
		exact_match = 0
		partial_match = 0
		# keep track of the words considered valid according to levenshtein
		# distance. This is useful to detect and ignore noise words by speci-
		# fying them in the list of ignored_words
		levenshtein_words = set()

		# iterate over the list of book words and process them one at a time
		for w in book_words:
			# skip the word if contained in the list of ignored ones
			if w in ignore_words:
				continue
			# if thw word is the target one, this is an exact match
			if w == desired_word:
				exact_match += 1
			else:
				# otherwise, check if the word is one of the similar ones
				match = False
				for sw in similar_words:
					if w == sw:
						# consider matches with similar words as exact matches
						exact_match += 1
						match = True

				# if the current word does not match either with the target word
				# or with the simiral ones, test its levenshtein distance
				if not match:
					diff = len(w) - len(desired_word)
					if len(w) > len(desired_word):
						# check all possible subwords of the current word
						for i in range(diff+1):
							if w[i:] == desired_word:
								# check whether the target word is a subword
								# of the current one
								exact_match += 1
								levenshtein_words.add("[{}]".format(w))
							else:
								# otherwise, check whether any subword of the current
								# word is a levenshtein word of the target
								if lvs.levenshtein_distance(w[i:],desired_word) <= max_levenshtein:
									partial_match += 1
									levenshtein_words.add("[{}]".format(w))
					# check whether the current word is a levenshtein word of the
					# target one, only if their difference in length is below the
					# specified threshold
					if diff <= max_length_difference:
						if lvs.levenshtein_distance(w,desired_word) <= max_levenshtein:
							partial_match += 1
							levenshtein_words.add(w)

		output_file = input_file.replace(".txt", ".csv")
		if os.path.exists(os.path.join("results", output_file)):
			file_exists = True
		else:
			file_exists = False
		with open(os.path.join(out_dir,output_file), "a", encoding="utf-8") as out_file:
			# write the file heading
			if not file_exists:
				out_file.write("parola,libro,occorrenze,occorrenze_parziali\n")
			# write the target word, the file analyzed and the number of exact and partial matches
			out_file.write("{},{},{},{}\n".format(desired_word,input_file,exact_match,partial_match))

		# for each input file (= book), also write all the levenshtein words that
		# have been found. Useful for tuning the script parameters
		with open(os.path.join(out_dir,input_file.replace(".txt", "_{}_levenshtein_words.txt".format(desired_word))), "w", encoding="utf-8") as out_file:
			for w in levenshtein_words:
				out_file.write(str(w)+"\n")
