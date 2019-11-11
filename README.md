Distant Reading Course UniTO
======
This is the public repository for the python scripts that have been used in a brief series of technical lessons that I held for the Course <i>Distant reading in the history of ideas</i> with professor Paolo Tripodi.

There are three folders, one for each group of students and corresponding topic of research, plus a folder for an experiment requested by the professor for personal use.

Group 1 - Cavell
-----
The goal of this group is to study the books from Stanley Cavell by extracting all the text inside round brackets and analyze its features using a technique based on topic modeling.

Original books are in PDF and need to be converted in a textual format
```
python3 text_ocr.py
```

Now we can run topic modeling
```
python3 topic_modeling.py
```

Group 2 - Kant Studien
-----
The goal is to analyze the publications in the Kant Studien and explore the usage of two words that mean <i>Experience</i>: <b>Erlebnis</b> and <b>Erfahrung</b>. The hypothesis of the students is that the usage and frequency of these two words changed during the years.

Again, books are in PDF and need to be converted in a textual format
```
python3 text_ocr.py
```

Now we can search for the occurrences of the two words:
```
python3 search_words.py
```

Group 3 - JSTOR
-----
The students from this group wanted to collect the metadata from a series of journal articles about the so called <i>Mental Experiments</i>, and at the same time explore how the usage of certain words changed during the years within a specific mental experiment.

To collect data and generate years statistics, run:
```
python3 parse_documents.py
```

Wittgenstein - JSTOR
-----
In this case the Professor is only interested in collecting the metadata from a JSTOR dump of journal articles.

Collect metadata by running:
```
python3 parse_documents.py
```
