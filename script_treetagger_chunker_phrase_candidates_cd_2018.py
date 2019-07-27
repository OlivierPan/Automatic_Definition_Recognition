#coding:utf-8
import os
import subprocess
import datetime
import re
import time
starttime=datetime.datetime.now()
from tempfile import TemporaryFile
with open('/users/pansa/desktop/enrichissement_corpus_projet/phrasecandidate.txt','r',encoding='utf-8') as file:
    content=file.readlines()
marqueurslist=[]
with open('/users/pansa/desktop/enrichissement_corpus_projet/marqueurs.txt','r',encoding='utf-8') as file:
    marqueurs=file.readlines()
    for marqeur in marqueurs:
        marqueurslist.append(marqeur.strip())

sortie=open('/users/pansa/desktop/enrichissement_corpus_projet/phrase_resultat.txt','w',encoding='utf-8')

#newfile=open("/users/pansa/desktop/enrichissement_corpus_projet/phrasecandidate_sortie_treetagger_chunker.xml",'w',encoding="utf=8")
#newfile.write("<?xml version='1.0' encoding='UTF-8'?>")
#newfile.write("\n")
#newfile.write('<racine>')
#newfile.write("\n")
patternNP=re.compile(r"<NP>.{1,60}</NP>")
patternParenthese=re.compile(r"(.{1,250})")




for phrase in content:
    #newfile.write('<article>')
    #newfile.write("\n")
    with open('/users/pansa/desktop/enrichissement_corpus_projet/tobedelete_chunker.txt','w') as file:
        file.write(phrase)
    output=subprocess.check_output("/Users/pansa/Desktop/treetagger/tagger-chunker-french /users/pansa/desktop/enrichissement_corpus_projet/tobedelete_chunker.txt",shell=True)
    temp=str(output,'utf-8')
    temp=temp.strip()#这是最干净的chuncker结果
    stripbackslachn="".join(temp.split("\n"))
    temp="".join(stripbackslachn.split("\t"))
    # The lines under here are for phrase with marqueur
    for marqueur in marqueurslist:
        if marqueur in phrase:
            #print("marqueur dans la phrase.--------------->",marqueur)
            if " " in marqueur:#这是复合词的情况
                marqueursplit=marqueur.split()#将这个单词撕开
                debut=marqueursplit[0]
                fin=marqueursplit[-1]
                my_regex=re.escape(debut)+r".+"+re.escape(fin)
                split_marqueur=re.findall(my_regex,temp)
                split_marqueur="".join(split_marqueur)
                splitList=temp.split(split_marqueur)
                #print(splitList)
                if re.findall(patternNP,splitList[0][-120:]):
                #if "<NP>" in splitList[0]:
                    if re.findall(patternNP,splitList[1][:120]):
                    #if "<NP>" in splitList[1]:
                        #print("Oui, cette phrase a une defintion avec marqueur mot composé")
                        #print("Terme est",re.findall(patternNP,splitList[0]))
                        #print("Definition est",re.findall(patternNP,splitList[1]))
                        #print(phrase)
                        sortie.write(phrase+"\n")
                        #sortie.write("Marqueur est -----------> "+marqueur+"\n")
                        #sortie.write("Terme est------------->"+"".join(re.findall(patternNP,splitList[0][-120:]))+"\n")#第一次是70
                        #sortie.write("Definition est-----------> "+"".join(re.findall(patternNP,splitList[1][:120]))+"\n")
                        sortie.write("\n\n")
                del splitList[:]

            elif marqueur in temp:
                splitList=temp.split(marqueur)
                if re.findall(patternNP,splitList[0][-120:]):
                #if "<NP>" in splitList[0]:
                    if re.findall(patternNP,splitList[1][:120]):
                #if "<NP>" in splitList[0]:
                    #if "<NP>" in splitList[1]:
                        #print("Oui, cette phrase a une defintion")
                        #print("Terme est", str(re.findall(patternNP,splitList[0])))
                        #print("Definition est",str(re.findall(patternNP,splitList[1])))
                        #print(phrase)
                        sortie.write(phrase+"\n")
                        #sortie.write("Marqueur est -----------> "+marqueur+"\n")
                        #sortie.write("Terme est------------->"+"".join(re.findall(patternNP,splitList[0][-120:]))+"\n")
                        #sortie.write("Definition est-----------> "+"".join(re.findall(patternNP,splitList[1][:120]))+"\n")
                        sortie.write("\n\n")
                #else:
                 #   print("Cette phrase n'a pas de definition!")
                del splitList[:]

        if all(marqueur not in phrase for marqueur in marqueurslist):
            if re.findall(patternParenthese,temp):
                parenthese_list=re.findall(patternParenthese,temp)
                if len(parenthese_list)==1:
                    parenthese_content="".join(parenthese_list)
                    if ",PUN," in parenthese_content:
                        parenthese_content_splitup=parenthese_content.split(",PUN,")
                        if re.findall(patternNP,parenthese_content_splitup[0][-80:]):
                            if re.findall(patternNP,parenthese_content_splitup[1][:80]):
                                sortie.write(phrase+"\n")
                                #sortie.write("Cette phrase a une definition entre parenthese")
                                #sortie.write("la definition est ------->   "+parenthese_content)
                    elif "VER:presêtre" in parenthese_content:
                        parenthese_content_splitup=parenthese_content.split("VER:presêtre")
                        if re.findall(patternNP,parenthese_content_splitup[0][-85:]):
                            if re.findall(patternNP,parenthese_content_splitup[1][:85]):
                                sortie.write(phrase+"\n")
                                #sortie.write("Cette phrase a une definition entre parenthese")
                                #sortie.write("la definition est ------->   "+parenthese_content)
                    elif "<VN>" not in parenthese_content:
                        sortie.write(phrase+"\n")
                        #sortie.write("Cette phrase a une definition entre parenthese")
                        #sortie.write("la definition est ------->   "+parenthese_content)

                if len(parenthese_list) > 1:
                    for eachparenthse in parenthese_list:
                        parenthese_content="".join(eachparenthse)
                        if ",PUN," in parenthese_content:
                            parenthese_content_splitup=parenthese_content.split(",PUN,")
                            if re.findall(patternNP,parenthese_content_splitup[0][-80:]):
                                if re.findall(patternNP,parenthese_content_splitup[1][:80]):
                                    sortie.write(phrase+"\n")
                                    #sortie.write("Cette phrase a une definition entre parenthese")
                                    #sortie.write("la definition est ------->   "+parenthese_content)
                        elif "VER:presêtre" in parenthese_content:
                            parenthese_content_splitup=parenthese_content.split("VER:presêtre")
                            if re.findall(patternNP,parenthese_content_splitup[0][-85:]):
                                if re.findall(patternNP,parenthese_content_splitup[1][:85]):
                                    sortie.write(phrase+"\n")
                                    #sortie.write("Cette phrase a une definition entre parenthese")
                                    #sortie.write("la definition est ------->   "+parenthese_content)
                        elif "<VN>" not in parenthese_content:
                            sortie.write(phrase+"\n")
                            #sortie.write("Cette phrase a une definition entre parenthese")
                            #sortie.write("la definition est ------->   "+parenthese_content)




    os.remove('/users/pansa/desktop/enrichissement_corpus_projet/tobedelete_chunker.txt')
    #newfile.write('</article>')
    #newfile.write("\n")
#newfile.write('</racine>')
#newfile.close()
endtime=datetime.datetime.now()
print(endtime-starttime)
sortie.close()
