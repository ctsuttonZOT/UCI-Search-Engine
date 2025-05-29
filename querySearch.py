import sys
import json
from collections import defaultdict


class InvertedIndexSearcher:

    def __init__(self, key_file_path : str, index_file_path: str):

        self.key_file_path = key_file_path
        self.index_file_path = index_file_path
        self.token_to_offset = self._load_keys()


    def _load_keys(self) -> dict:
        with open(self.key_file_path, 'r') as f:
            return json.load(f)
    

    def _get_offset(self, token: str):

        if token not in self.token_to_offset:

            return None
        return self.token_to_offset[token]
    
    def _get_postings(self, offset: int):

        with open(self.index_file_path, 'rb') as f:
            f.seek(offset)

            # print(f.readline())

            obj = json.loads(f.readline())

            return obj

    def find_docs(self, tokens: list[str]):

        results = []
        for token in tokens:

            token_offset = self._get_offset(token.lower())

            if token_offset is None:
                return []
            # print(f'Token: {token.lower()} is at Offset {token_offset[0]}')

            postings = self._get_postings(int(token_offset[0]))[token.lower()][0]
            # token_freq_map = {doc_id: freq for doc_id, freq in postings}
            # print(postings)
            if postings is None:
                return []
            token_map = {doc_id: post[2] for post in postings}
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

def main(): # python3 querySearch.py [key_file_path] [index_file_path]

    query = input("Enter Query (Ex: cristina lopes): ").split()
    # print(query)
    searcher = InvertedIndexSearcher(sys.argv[1], sys.argv[2])
    docs = searcher.find_docs(query)

    print("DOC IDs :", docs[:5])


if __name__ == "__main__":

    main()

        
