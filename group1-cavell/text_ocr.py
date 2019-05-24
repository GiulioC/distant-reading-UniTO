from sklearn.feature_extraction.text import CountVectorizer
import textract
import magic
import os

files_dir = "files"

for pdf_file in os.listdir(files_dir):
	if not pdf_file.endswith(".pdf"):
		continue

	if os.path.exists(os.path.join(files_dir,pdf_file.replace(".pdf", ".txt"))):
		continue

	print(pdf_file)

	file_type = str(magic.from_file(os.path.join(files_dir,pdf_file)))

	if file_type.startswith("PDF"):
		ext = "pdf"

	text = textract.process(
		os.path.join(files_dir,pdf_file),
		extension=ext,
		method='tesseract'
	).decode('utf-8')

	with open(os.path.join(files_dir,pdf_file.replace(".pdf", ".txt")), "w") as f:
		f.write(text)
