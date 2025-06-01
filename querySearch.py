import sys
import json
from collections import defaultdict
import time


class InvertedIndexSearcher:

    def __init__(self, key_file_path : str, index_file_path: str):

        self.key_file_path = key_file_path
        self.index_file_path = index_file_path
        self.token_to_offset = self._load_keys()
        self.fileHandle = open(index_file_path, 'rb')

    def _load_keys(self) -> dict:
        with open(self.key_file_path, 'r') as f:
            return json.load(f)
    

    def _get_offset(self, token: str):

        if token not in self.token_to_offset:

            return None
        return self.token_to_offset[token]
    
    def _get_postings(self, offset: int):

        #with open(self.index_file_path, 'rb') as f:
            #f.seek(offset)
            #txt = f.readline()
            #obj = json.loads(txt)#(f.readline())

            #return obj
        (self.fileHandle).seek(offset)
        txt = (self.fileHandle).readline()
        obj = json.loads(txt)

        return obj
    def find_docs(self, tokens: list[str]):

        results = []
        for token in tokens:
            token_offset = self._get_offset(token.lower())
            if token_offset is None:
                return []
            #print(token, token_offset)
            postings = self._get_postings(token_offset)[token.lower()][0][0]

            if postings is None:
                return []
            token_map = {post[0]: post[2] for post in postings}
            results.append(token_map)


        # Find common document IDs
        common_doc_ids = set(results[0].keys())
        for postings in results[1:]:
            common_doc_ids &= postings.keys()
        if not common_doc_ids:
            return []
        

        doc_score = {}
        for doc_id in common_doc_ids:
            doc_score[doc_id] = sum(freq_map.get(doc_id, 0) for freq_map in results)

        # Sort by total frequency
        sorted_docs = sorted(doc_score.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs
    
def server_main(query):
    # print(query)
    searcher = InvertedIndexSearcher('offsets.txt', 'inverted_index.txt')
    start_time = time.time()
    docs = searcher.find_docs(query)
    urlMappings = {}
    with open('url_ids.json', 'r') as f:
        urlMappings = json.loads(f.read())
    urls = []
    for elem in docs[:5]:
        url = urlMappings[str(elem[0])]
        urls.append(url)
        print(url, " ,")
        # elem has 2 elements
    #print(docs)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.6f} seconds")
    searcher.fileHandle.close()

    return urls

def main(): # python3 querySearch.py [key_file_path] [index_file_path]

    query = input("Enter Query Below (Ex: cristina lopes): ").split()
    

    # print(query)
    searcher = InvertedIndexSearcher(sys.argv[1], sys.argv[2])
    start_time = time.time()
    docs = searcher.find_docs(query)
    urlMappings = {}
    with open('url_ids.json', 'r') as f:
        urlMappings = json.loads(f.read())
    for elem in docs[:5]:
        print(urlMappings[str(elem[0])], ", ")
        # elem has 2 elements
    #print(docs)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.6f} seconds")
    searcher.fileHandle.close()
if __name__ == "__main__":

    main()
