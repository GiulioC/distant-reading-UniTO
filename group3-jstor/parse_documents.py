import pandas as pd
import os
import re

files_dir = "files"
out_dir = "results"

d = {
	"document-name":[],
	"article-type":[],
	"publisher-name":[],
	"journal-title":[],
	"article-id":[],
	"doi":[],
	"subject":[],
	"article-title":[],
	"author(s)":[],
	"date":[],
	"volume":[],
	"issue":[],
	"fpage":[],
	"lpage":[],
	"language":[],
	"footnote":[],
	"abstract":[]
}

for mental_exp in os.listdir(files_dir):
	metadata_dir = os.path.join(files_dir, mental_exp, "metadata")
	for doc in os.listdir(metadata_dir):
		if not doc.endswith(".txt"):
			continue

		print("[{}][{}]".format(metadata_dir,doc))

		with open(os.path.join(metadata_dir,doc), "r") as f:
			text = f.read()

		article_type = (re.search("article-type=\"[^\"]*\"", text).group().split('"')[1])
		try:
			publisher_name = (re.search("publisher-name\">.*<publisher-name>", text).group()[:-1].split(">")[1])
		except AttributeError:
			publisher_name = (re.search("publisher-name>[^<]*<", text).group()[:-1].split(">")[1])
		journal_title = (re.search("journal-title>[^<]*<", text).group()[:-1].split(">")[1])
		try:
			doc_id = (re.search("jstor-stable\">[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			doc_id = (re.search("<article-id[^>]*>[^<]*</article-id>", text).group()[:-1].split(">")[1].split("<")[0])
		try:
			doi = (re.search("doi\">[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			doi = ""
		try:
			subject = (re.search("subject>[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			subject = ""
		try:
			article_match_start = text.find("<article-title>")
			article_match_end = text.find("</article-title>")
			if article_match_start == -1 or article_match_end == -1:
				article_title = ""
			else:
				article_title = text[article_match_start+15:article_match_end]
		except AttributeError:
			article_title = ""

		author_names = []
		for match in re.finditer("<contrib[^>]*>\s*<string-name[^>]*>\s*<given-names>.*\s*<surname>.*\s*<\/string-name>\s*<\/contrib>", text):
			author_text = match.group()
			author_name = re.search("<given-names>[^<]*<", author_text).group()[:-1].split(">")[1]
			author_surname = re.search("surname>[^<]*<", author_text).group()[:-1].split(">")[1]
			author_names.append("{} {}".format(author_name, author_surname))
		author_names = ", ".join(author_names) if len(author_names) > 0 else ""

		try:
			date_block = re.search("<pub-date[^>]*>\s*<day.*\s*<month.*\s*<year.*", text).group()
			day = re.search("<day[^>]*>[^<]*<", date_block).group()[:-1].split(">")[1]
			month = re.search("<month[^>]*>[^<]*<", date_block).group()[:-1].split(">")[1]
			year = re.search("<year[^>]*>[^<]*<", date_block).group()[:-1].split(">")[1]
			date = year
		except AttributeError:
			try:
				date_block = re.search("<pub-date[^>]*>\s*(<month.*\s*)?<year.*\s*(<string-date.*)?", text).group()
				if "string-date" in date_block:
					date = re.search("<string-date[^>]*>[^<]*<", date_block).group()[:-1].split(">")[1]
					date = re.sub('[^0-9]','',date)
				elif "year" in date_block:
					date = re.search("<year[^>]*>[^<]*<", date_block).group()[:-1].split(">")[1]
				else:
					date = ""
			except AttributeError:
				date = ""

		try:
			volume = (re.search("<volume[^>]*>[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			volume = ""
		try:
			issue = (re.search("<issue[^>]*>[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			issue = ""
		try:
			fpage = (re.search("fpage>[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			fpage = ""
		try:
			lpage = (re.search("lpage>[^<]*<", text).group()[:-1].split(">")[1])
		except AttributeError:
			lpage = ""
		lang = (re.search("lang</meta-name>[\s\n]*<meta-value>[^<]*<", text).group()[:-1].split(">")[-1].split("<")[0])
		try:
			footnote = re.search("<fn id=\"[^\"]*\">[\s\n]*<label>[^<]*</label>[\s\n]*.*", text).group().split("<p>")[1].split("</p>")[0]
			footnote = re.sub("<[^>]*>", " ", footnote)
		except AttributeError:
			footnote = ""
		try:
			abstract_group = re.search("<abstract>\s*.*\s*</abstract>", text).group()
			abstract = re.search("<p>.*</p>", abstract_group).group()[3:-4]
		except AttributeError:
			abstract = ""

		d["document-name"].append(doc)
		d["article-type"].append(article_type)
		d["publisher-name"].append(publisher_name)
		d["journal-title"].append(journal_title)
		d["article-id"].append(doc_id)
		d["doi"].append(doi)
		d["subject"].append(subject)
		d["article-title"].append(article_title)
		d["author(s)"].append(author_names)
		d["date"].append(date)
		d["volume"].append(volume)
		d["issue"].append(issue)
		d["fpage"].append(fpage)
		d["lpage"].append(lpage)
		d["language"].append(lang)
		d["footnote"].append(footnote)
		d["abstract"].append(abstract)

	df = pd.DataFrame(d)
	df.to_csv(os.path.join(out_dir,"{}.csv".format(mental_exp)), index=None)
