import json
import os
import tempfile
from math import log

# weights for normal, title, bold, h1, h2, h3
WEIGHTS = [1.0, 2.5, 1.5, 2.0, 1.7, 1.5]

def calculate_weighted_tf(postings_lists: list[list[tuple[int, int]]], doc_id: int) -> float:
    tf = 0
    for i, posting_list in enumerate(postings_lists):
        # print(posting_list)
        for posting in posting_list:
            try:
                # if len != 2 then tf-idf has already been added
                if len(posting) == 2:
                    id, freq = posting
                    if id == doc_id:
                        tf += WEIGHTS[i] * freq
            except TypeError:
                continue
    # print(tf)
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
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir='.') as temp_file:
        with open(filename, 'r') as file:
            for line in file:
                obj = json.loads(line)
                key = list(obj.keys())[0]
                data = list(obj.values())
                idf = compute_idf(data, total_docs)
                for posting_lists in data:
                    for posting_list in posting_lists:
                        for posting in posting_list:
                            if len(posting) != 0:
                                tf = calculate_weighted_tf(data[0], posting[0])
                                # 'append' tf-idf score to posting
                                posting += [tf*idf]
                                # print(tf*idf)
                # write updated line to temp file
                temp_file.write(json.dumps({key: data}) + '\n')
    # replace original index with new index that has tf-idf scores
    os.replace(temp_file.name, filename)


def rank_documents(query: str, total_docs: int) -> list[tuple[int, int]]:
    # TODO: implement once merged index and merged index search is finished
    pass
