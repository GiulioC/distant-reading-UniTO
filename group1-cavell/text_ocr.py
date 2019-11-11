from sklearn.feature_extraction.text import CountVectorizer
import textract
import os

files_dir = "files"

# read all the .pdf and files one at a time
for pdf_file in os.listdir(files_dir):
	# skip files that are not pdf
	if not pdf_file.endswith(".pdf"):
		continue

	# if the current file has already a corresponding ocr version then skip it
	if os.path.exists(os.path.join(files_dir,pdf_file.replace(".pdf", ".txt"))):
		continue

	# display current pdf file
	print(pdf_file)

	# run OCR to convert .pdf file into .txt (takes a while)
	text = textract.process(
		os.path.join(files_dir,pdf_file),
		extension="pdf",
		method='tesseract'
	).decode('utf-8')

	# save the content of the .pdf to a new .txt file to be used later
	with open(os.path.join(files_dir,pdf_file.replace(".pdf", ".txt")), "w") as f:
		f.write(text)
