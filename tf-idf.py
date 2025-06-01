import json
import os
import tempfile
import sys
from math import log

# weights for normal, title, bold, h1, h2, h3
WEIGHTS = [1.0, 2.5, 1.5, 2.0, 1.7, 1.5]

lineProcessed = 0

def calculate_weighted_tf(postings_lists: list[list[tuple[int, int]]], doc_id: int) -> float:
    tf = 0
    for i, posting_list in enumerate(postings_lists):
        for posting in posting_list:
            try:
                # if len != 2 then tf-idf has already been added
                if len(posting) == 2:
                    id, freq = posting
                    if id == doc_id:
                        tf += WEIGHTS[i] * freq
            except TypeError:
                continue
    return tf    


def compute_idf(postings_lists: list[list[tuple[int, int]]], total_docs: int) -> float: 
    doc_ids = set()
    for posting_list in postings_lists:
        for posting in posting_list:
            try:
                for id, _ in posting:
                    doc_ids.add(id)
            except TypeError:
                continue
    df = len(doc_ids)
    return log(total_docs / df, 10) if df != 0 else 0.0


def update_index_scores(filename: str, total_docs: int):
    global lineProcessed

    openFile = True
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir='.') as temp_file:
        with open(filename, 'r') as file:
            line = file.readline()
            while openFile:
                if lineProcessed % 10000 == 0:
                    print(lineProcessed)
                lineProcessed += 1
                obj = json.loads(line)
                key = list(obj.keys())[0]
                data = list(obj.values()) # data in form: [  [...], [...], [...], [...], [...], [...]   ] -> each dot can be a [x, y]
                #print("length: ",len(data[0]))
                idf = compute_idf(data, total_docs) # log (number total docs / number docs with token)
                indexes = {}
                for i in range(0, 6): # data[0] is length 6 (and has 6 lists), each data[0][0-6]
                        if i == 1:
                            continue
                        if len(data[0][i]) != 0 and i == 0:
                            for j in range(0, len(data[0][i])):
                                indexes[data[0][i][j][0]] = j
                            #print(indexes)
                        elif len(data[0][i]) != 0:
                            for j in range(0, len(data[0][i])):
                                docNum = data[0][i][j][0]
                                if docNum in indexes:
                                    idx = indexes[docNum]
                                    data[0][0][idx][1] -= data[0][i][j][1]
                                    if data[0][0][idx][1] < 0:
                                        data[0][0][idx][1] = 0
                                    data[0][0][idx][1] += data[0][i][j][1] * (WEIGHTS[i])
                for posting_list in data[0]:
                    # these try except blocks are to avoid bugs caused by index w/ incorrect format
                    try:
                        for posting in posting_list:
                            if len(posting) != 0:
                                tf = calculate_weighted_tf(data[0], posting[0]) # term frequency (in documents)
                                # 'append' tf-idf score to posting
                                posting += [tf*idf]
                    except TypeError:
                        line = file.readline()
                        continue

                temp_file.write(json.dumps({key: data}) + '\n')
                line = file.readline()
                if not(line) or line == "":
                    openFile = False
    # replace original index with new index that has tf-idf scores
    os.replace(temp_file.name, filename)


def createOffsetFile(fileName):
    offsets = {}
    with open(fileName, 'r') as file:
        pos = 0
        cond = True
        line = file.readline()
        while(cond):
            temp = json.loads(line)
            offsets[list(temp.keys())[0]] = pos
            pos = file.tell()
            line = file.readline()
            if line == "" or line == None:
                cond = False
    with open('offsets.txt', 'w') as file:
        file.write(json.dumps(offsets))


# python3 tf-idf.py [index_file_path] [total_docs]
def main():
    update_index_scores(sys.argv[1], int(sys.argv[2]))
    createOffsetFile('inverted_index.txt')

if __name__ == "__main__":
    main()
