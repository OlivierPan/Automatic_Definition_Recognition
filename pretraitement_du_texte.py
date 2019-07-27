
#coding:utf-8
# Script qui fait le prétraitement du text, c'est-à-dire, pour chaque text
# éliminer la partie avant résumé et celle après conclusion
# segmenter en phrase
# eliminer des phrases dont lenth es inférieur à 150 ( min(len(phrase-avec-definition))=103, moyen=311.
# prendre que des phrases qui contiennet des marqueurs, et la mettre dans un nouveau fichier, une phrase par linge
# Ce nouveau fichier, on le soummettra au chuncker

from nltk.tokenize import sent_tokenize
import os
import numpy
import re

file_list=[]
mypath="/Users/pansa/Desktop/enrichissement_corpus_projet/15_article_test_sans_balise"


def get_document_route():
	for root, dirs, files in os.walk(mypath):
		for name in files:
			if name.endswith(".txt"):
				file_name=os.path.join(root,name)
				file_list.append(file_name)
	return file_list

file_list=get_document_route()

#print(file_list)

"""
def nettyoyer_balise_du_document():
    for file in file_list:
        fileobject=open(file,'r',encoding='utf-8')
        content=fileobject.read()
        fileobject.close()
        newcontent=re.sub(r"<.{1,15}>","",content)
        newfile=open(file+"new.txt","w",encoding="utf-8")
        newfile.write(newcontent)
        newfile.close()
        
nettyoyer_balise_du_document()
"""

with open('marqueurs.txt','r',encoding='utf-8') as file:
    marqueurlist=re.split("\n",file.read())
#print(marqueurlist)

bingo_phrase=[]

pattern=re.compile(r"\(.{10,150}\)")
year=re.compile(r",[0-9]{4}")

parenthese_phrase=[]

def pretraitement_chaque_text():
    for file in file_list:
        fileobject=open(file,'r',encoding='utf-8')
        content=fileobject.read()
        core_content=re.split("Introduction\n",content)[1]
        fileobject.close()
        core_content=re.sub(r"\n{2,4}","\n",core_content)#nettoyer des \n
        #print(core_content)
        phrase_list=sent_tokenize(core_content)
        for phrase in phrase_list:
            phrase=phrase.strip()
            if len(phrase) > 150:
                if any(marqueur in phrase for marqueur in marqueurlist):
                    bingo_phrase.append(phrase)
                elif re.findall(pattern,phrase):
                    if all(re.findall(year,parenthese) for parenthese in re.findall(pattern,phrase)):
                        pass
                    else:
                        bingo_phrase.append(phrase)        


pretraitement_chaque_text()
#print(bingo_phrase)
if len(bingo_phrase)==len(set(bingo_phrase)):
    print("OUI,pas de doublon")

def nettoyer_bingo_phrase():
    for phrase in bingo_phrase:
        if "\n" in phrase:
            bingo_phrase.remove(phrase)
            phraselist=[phrase for phrase in re.split("\n",phrase) if len(phrase)>150 if any(marqueur in phrase for marqueur in marqueurlist)]
            bingo_phrase.extend(phraselist)
nettoyer_bingo_phrase()#nettoyer encore des \n
nettoyer_bingo_phrase()#double nettoyage

fileend=open("phrasecandidate.txt","w+")
bingo_phrase=list(set(bingo_phrase))
for phrase in bingo_phrase:
    if phrase not in fileend.read():
    #print(phrase)
        fileend.write(phrase+"\n")
fileend.close()
        
  





                                                       
    
                                                       
  
  
