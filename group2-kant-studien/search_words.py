from sklearn.feature_extraction.text import CountVectorizer
import levenshtein as lvs
import os

files_dir = "files"
out_dir = "results"
max_levenshtein = 2

words_dict = {
	"italien": ["Italienisch"]
}

cv = CountVectorizer(stop_words=None, analyzer='word')
analyzer = cv.build_analyzer()

for input_file in os.listdir(files_dir):
	if not input_file.endswith(".txt"):
		continue

	print("[{}]".format(input_file))

	text = ""
	with open(os.path.join(files_dir,input_file), "r", encoding="utf-8") as f:
		text = f.read()

	book_words = analyzer(text)

	for desired_word, similar_words in words_dict.items():
		exact_match = 0
		partial_match = 0
		levenshtein_words = set()

		for w in book_words:
			if w == desired_word:
				exact_match += 1
			else:
				match = False
				for sw in similar_words:
					if w == sw:
						exact_match += 1
						match = True

				if not match:
					if lvs.levenshtein_distance(w,desired_word) <= max_levenshtein:
						partial_match += 1
						levenshtein_words.add(w)

		output_file = input_file.replace(".txt", ".csv")
		if os.path.exists(os.path.join("results", output_file)):
			file_exists = True
		else:
			file_exists = False
		with open(os.path.join(out_dir,output_file), "a") as out_file:
			if not file_exists:
				out_file.write("parola,libro,occorrenze,occorrenze_parziali\n")
			out_file.write("{},{},{},{}\n".format(desired_word,input_file,exact_match,partial_match))

		with open(os.path.join(out_dir,input_file.replace(".txt", "_{}_levenshtein_words.txt".format(desired_word))), "w") as out_file:
			for w in levenshtein_words:
				out_file.write(str(w)+"\n")
