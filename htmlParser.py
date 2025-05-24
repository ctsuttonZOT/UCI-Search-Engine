from bs4 import BeautifulSoup, Tag
from tokenizer import tokenize, computeWordFrequencies
from posting import Posting
import json
import os
from pympler import asizeof

root_dir = "DEV"

milestone = 400000000
countPrints = 0
mapTemp = {}

fileNum = 0

# want to get count of tokens, bolded or not, header or not, title or not
def htmlParser(htmlContent, url):

    if fileNum % 500 == 0 and fileNum != 0:
        sz1 = asizeof.asizeof(mapTemp)
        if sz1 >= milestone:
            printToFileEachEntry()


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
    bolds = processText(bold, url)
    titles = processText(title, url)
    h1s = processText(h1, url)
    h2s = processText(h2, url)
    h3s = processText(h3, url)

    texts = processText(allText, url)
    #print(bolds)
    
    # update map
    #print(len(h1s))
    #print(len(h1s[0]))
    updateMap(texts, titles, bolds, h1s, h2s, h3s)


def updateSingle(stats: list[Posting], k):
    # print(str(k), "---", stats)
    #return
    if len(stats) == 0:
        return
    #if k == 1:

    for i in range(0, len(stats)):
        curr_posting = stats[i]
        if curr_posting.token in mapTemp:
            #print(stats)
            if k == 1:
                mapTemp[curr_posting.token][k].append((curr_posting.url_id))
                return
            (mapTemp[curr_posting.token])[k].append((curr_posting.url_id, curr_posting.token_freq))
        else:
            if k == 1:
                mapTemp[curr_posting.token] = [ [], [], [], [], [], []]
                mapTemp[curr_posting.token][k].append((curr_posting.url_id))
                return
            mapTemp[curr_posting.token] = [ [], [], [], [], [], []]
            mapTemp[curr_posting.token][k].append((curr_posting.url_id, curr_posting.token_freq))


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


def processText(text, url): # text -> [(token, count), ...], returns list of tokens with count of occurences 
    tempMap = computeWordFrequencies(tokenize(text))
    res = []
    for key, val in tempMap.items():
        res.append(Posting(url, key, val))
    return res


def fileProcessor(fileName): # opens file, loads json, sends text content to json
    #try:
        with open(fileName, 'r') as f:   
            fileJson = json.load(f)
        text = fileJson["content"]
        htmlParser(text, fileJson["url"])
    #except:
        #print("error")


def printToFileEachEntry(): # CHECK
    # Sort map
    global mapTemp
    global countPrints
    sortedKeys = sorted(mapTemp.keys())
    mapTemp = {key: mapTemp[key] for key in sortedKeys}
    # Dump jsons
    with open("results" + str(countPrints) + ".txt", 'a') as f:
        for key, value in mapTemp.items():
            jsonTemp = {key: value}
            f.write(json.dumps(jsonTemp) + "\n")
    # Clear map
    countPrints += 1
    mapTemp = {}

    # update doc id file
    with open("url_ids.json", "w") as file:
        json.dump(Posting.id_cache, file)


def mainFunc(): # For all files in directory root_dir, call fileProcessor
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fn in filenames:
            pathToFile = os.path.join(dirpath, fn)
            fileProcessor(pathToFile)
    printToFileEachEntry() # printFileAtEnd

def mergeTester(numPartitions): # num partitions is the number of results(x).txt files that are produced
    keyFilePos = {} # (key, value) -> key = token, value = position integer
    arrayFiles = []
    arrayLines = []
    for i in range(0, numPartitions):
        fn = f"results{i}.txt"
        f = open(fn, 'r')
        arrayFiles.append(f)
        arrayLines.append(f.readline())
    currPos = 0
    countOpenFiles = numPartitions
    

    with open("inverted_indexii.txt", 'a') as ii:
        while(countOpenFiles):
            listObjs = []
            listKeys = []
            for ln in arrayLines:
                if ln != "":
                    obj = json.loads(ln)
                    listObjs.append(obj)
                    listKeys.append(list(obj.keys())[0])
                else:
                    listObjs.append(None)
                    listKeys.append(None)
            smallestKey = None
            firstEncountered = True
            for key in listKeys:
                if (firstEncountered and key) or (key and key < smallestKey):
                    firstEncountered = False
                    smallestKey = key
            # should have smallest key at this point
            k = smallestKey
            res = {}
            
            for i in range(0, len(listObjs)):
                obj = listObjs[i]
                if not(obj):
                    continue
                if k in obj:
                    if k in res:
                        res[k][0].extend(obj[k][0])
                        res[k][1].extend(obj[k][1])
                        res[k][2].extend(obj[k][2])
                        res[k][3].extend(obj[k][3])
                        res[k][4].extend(obj[k][4])
                        res[k][5].extend(obj[k][5])
                    else:
                        res[k] = (obj[k])
                    
                    fn = arrayFiles[i]
                    aL = fn.readline()
                    if aL == "":
                        fn.close()
                        arrayFiles[i] = None
                        arrayLines[i] = ""
                        countOpenFiles -= 1
                    else:
                        arrayLines[i] = aL
            ii.write(json.dumps(res) + "\n")


if __name__ == "__main__":
    mainFunc()
