import urllib.request
import spacy
import time
import random
import time
from PyPDF2 import PdfReader
from scholarly import scholarly

global keywords
keywords = []
directory1 = "./texts"
directory2 = "./pdfs"
directory3 = "./ressources"
nlp = spacy.load("en_core_web_sm")


openfile = open("./ressources/listgreetings.txt", "r")
listcomtest = openfile.readlines()
listcom = list(map(lambda s: s.strip(), listcomtest))
openfile.close()

openfile = open("./ressources/listgoodbyes.txt", "r")
listcomendtest = openfile.readlines()
listcomend = list(map(lambda s: s.strip(), listcomendtest))
openfile.close()

openfile = open("./ressources/listquestions.txt", "r")
listqtest = openfile.readlines()
listq = list(map(lambda s: s.strip(), listqtest))
openfile.close()

openfile = open("./ressources/wordsnotimp.txt", "r")
listnottest = openfile.readlines()
listnot = list(map(lambda s: s.strip(), listnottest))
openfile.close()

#main loop
while(True):
    print("Welcome to google scholar filter AI how can i help you?")
    inuser = input("Answer: ")
    print(random.choice(listcom))
    time.sleep(1)
    doc = nlp(inuser)

    for word in doc[:]:
        if word.text != "exit":
            
            if str(word.text) not in listq and str(word.pos_) == "PRON":
                with open("./ressources/listquestions.txt", "a") as file_object:
                    file_object.write("\n" + word.text)
                listq.append(word.text)
            
            if str(word.text) not in listnot and str(word.pos_) != "ADJ" and str(word.pos_) != "NOUN" and str(word.pos_) != "VERB" and str(word.pos_) != "PRON" and str(word.pos_) != "ADP" and str(word.pos_) != "NUM":
                with open("./ressources/wordsnotimp.txt", "a") as file_object:
                    file_object.write("\n" + word.text)
                listnot.append(word.text)

            if str(word.pos_) == "ADJ" or str(word.pos_) == "NOUN" or str(word.pos_) == "VERB" or str(word.pos_) == "ADP" or str(word.pos_) == "NUM"or str(word.pos_) == "PROPN":
                keywords.append(str(word.text))

        elif word.text == "exit":
            Endword = "exit"
            print(random.choice(listcomend))
            time.sleep(5)
            exit()
            
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


    # #open all files in a specific directorie

    # for filename in os.listdir("directory1"):
    #     if filename.endswith(".txt"):
    #         with open(filename, "r") as f:
    #             text = f.read()
    #             if any(word in text for word in keywords):
    #                 print("Found in " + filename)
    #                 print(text)
    #             else:
    #                 print("Not found in " + filename)
    #     else:
    #         None