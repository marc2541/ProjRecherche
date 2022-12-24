import urllib.request
import spacy
import os
import time
import re
import random
import time
from PyPDF2 import PdfReader
from scholarly import scholarly

directory1 = "./texts"
directory2 = "./pdfs"

keywords = ["Machine", "Learning"]
search_query = scholarly.search_pubs("+".join(keywords))

articles = [(next(search_query)) for i in range(1)]

for article in articles:
    art = scholarly.fill(article)
    pdf_url = art['eprint_url']
    numart = str(articles.index(article))

    if pdf_url:
        #download pdf

            urllib.request.urlretrieve(pdf_url, directory2 + "/" + numart + ".pdf")


            pdf = PdfReader(directory2 + "/" + numart + ".pdf")
            munberpages = len(pdf.pages)
            page = pdf.pages[munberpages-1]
            text = page.extract_text()

            with open(directory1 + "/text"+ numart + ".txt", "a") as f:
                f.write(text)

            print("The files should be created")
    else:
        print("No pdf found for aritcle " + numart)