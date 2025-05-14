import sys
stopwords = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
    "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
    "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves"
}
from bs4 import BeautifulSoup


# Time Complexity: O(1), it does a constant amount of comparisons each function call
def isAlphanumerical(char):
    if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
        return True 
    elif char >= '0' and char <= '9':
        return True
    return False

# Worst Case: O(n ^ 2), n being the number of characters in the file. The while loop
# iterates n times and inside, it could possibly use append() which has a worst case
# of O(n), but amortized has a runtime of O(1)
def tokenize(text):
    
    listTokens = [] # list to return
    bufferChars = "" # buffer for word
    currToken = False
    len_txt = len(text)

    for i in range(0, len_txt):
        char = text[i]
        isChar = isAlphanumerical(char)
        if isChar:
            bufferChars = bufferChars + char
            currToken = True
        else:
            if currToken:
                if len(bufferChars) >= 3 and bufferChars not in stopwords:
                    listTokens.append(bufferChars)
                currToken = False
            bufferChars = ""
    if currToken:
        if len(bufferChars) >= 3 and bufferChars not in stopwords:
            listTokens.append(bufferChars)
    return listTokens

# Time Complexity: O(n ^ 2). The outer loop runs n times, n being the number of tokens (not unique). 
# Inside there is a constant amount of O(n) statements (lower(), dict access/update)
def computeWordFrequencies(listTokens):
    resDict = {}
    for str in listTokens: # O(n)
        tempStr = str.lower() # O(n)
        if tempStr not in resDict: 
            resDict[tempStr] = 1 # O(n) worst, O(1) avg
        else:
            resDict[tempStr] = resDict[tempStr] + 1 # O(n) worst, O(1) avg
    return resDict

# Time Complexity: O(n logn). sorted() is O(n log n). 
def printFreq (freq):
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True) # O(n logn )
    for token in freq: # O(n)
        print(token[0], token[1])

#new method, for M1, getting bolds, anchors, etc. Modify to add more special constraints if needed
def extract_tags(json_file: str) ->list: #maybe change parameter
    html = json_file["content"]
    soup = BeautifulSoup(html, 'html.parser')
    
    #get all the unique/important texts
    anchors = [a.get_text() for a in soup.find_all('a')]
    bolds = [b.get_text() for b in soup.find_all(['b', 'strong'])]
    headers = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    
    special_text = anchors + bolds + headers
    
    return special_text
