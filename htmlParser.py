from bs4 import BeautifulSoup, Tag
from tokenizer import tokenize, computeWordFrequencies
import json
import os
import sys
from pympler import asizeof

root_dir = r"C:\Users\rickg\OneDrive\Desktop\developer\DEV"

mapTemp = {}

fileNum = 0

# want to get count of tokens, bolded or not, header or not, title or not
def htmlParser(htmlContent):

    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    # get list of text for each tag
    bolds = soup.find_all('b')
    titles = soup.find_all('title')
    h1s = soup.find_all('h1')
    h2s = soup.find_all('h2')
    h3s = soup.find_all('h3')

    # gets entire text
    allText = soup.get_text(separator=" ", strip=True)

    # creates single string with all text for each tag
    bold = listToString(bolds)
    title = listToString(titles)
    h1 = listToString(h1s)
    h2 = listToString(h2s)
    h3 = listToString(h3s)

    # return list of pairs with token and count [(token, count), ...]
    bolds = processText(bold)
    titles = processText(title)
    h1s = processText(h1)
    h2s = processText(h2)
    h3s = processText(h3)

    texts = processText(allText)
    #print(bolds)
    
    # update map
    #print(len(h1s))
    #print(len(h1s[0]))
    updateMap(texts, title, bolds, h1s, h2s, h3s)


def updateSingle(stats, k):
    #print(str(k), "---", stats)
    #return
    if len(stats) == 0:
        return
    #if k == 1:

    for i in range(0, len(stats)):
        if stats[i][0] in mapTemp:
            #print(stats)
            if k == 1:
                mapTemp[stats[i][0]][k].append((fileNum))
                return
            (mapTemp[stats[i][0]])[k].append((fileNum, stats[i][1]))
        else:
            if k == 1:
                mapTemp[stats[i][0]] = [ [], [], [], [], [], []]
                mapTemp[stats[i][0]][k].append((fileNum))
                return
            mapTemp[stats[i][0]] = [ [], [], [], [], [], []]
            mapTemp[stats[i][0]][k].append((fileNum, stats[i][1]))
def updateMap(allTxt, title, bolds, h1s, h2s, h3s): # DONE, called after each 
    global fileNum
    updateSingle(allTxt, 0)
    updateSingle(title, 1)
    updateSingle(bolds, 2)
    updateSingle(h1s, 3)
    updateSingle(h2s, 4)
    updateSingle(h3s, 5)
    if fileNum % 5000 == 0:
        print(fileNum)
        total_size = asizeof.asizeof(mapTemp)

        print(total_size)
    fileNum += 1

def listToString(lst):
    str = ""
    for item in lst:
        str += " " + item.get_text(separator=" ", strip=True)
    return str

def processText(text): # text -> [(token, count), ...], returns list of tokens with count for a string of text
    tempMap = computeWordFrequencies(tokenize(text))
    res = []
    for key, val in tempMap.items():
        res.append((key, val))
    return res

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were

<b> bb <a href="http://example.com/elsie" class="sister" id="link1"> Elsie </a> </b>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
 
def fileProcessor(fileName): # CHECK
    #try:
        with open(fileName, 'r') as f:   
            fileJson = json.load(f)
        text = fileJson["content"]
        htmlParser(text)
    #except:
        #print("RUH ROH")


def printToFileEntire(): # CHECK
    with open("results.txt", 'w') as f:   
        f.write(json.dumps(mapTemp) + '\n')
def printToFileEachEntry(): # CHECK
    with open("results.txt", 'a') as f:
        for key, value in mapTemp.items():
            jsonTemp = {key: value}
            f.write(json.dumps(jsonTemp) + "\n")
def mainFunc(): # CHECK
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fn in filenames:
            pathToFile = os.path.join(dirpath, fn)
            fileProcessor(pathToFile)
    printToFileEachEntry()

mainFunc()