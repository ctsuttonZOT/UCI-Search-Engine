import json
import os

class Posting:
    # stores urls and ids in memory to speed up indexer
    #id_cache = {}

    def __init__(self, url: str, token: str, token_freq: int) -> None:
        # int representing the URL the token was found in
        #self.url_id = self.get_url_id(url)

        # the token itself
        self.token = token

        # num of times the token occurs in the page
        self.token_freq = token_freq


    def get_url_id(self, url: str) -> int:
        # if the file doesn't exist, or it's empty, initialize it with default data
        if not (os.path.exists("url_ids.json")) or os.stat("url_ids.json").st_size == 0:
            with open("url_ids.json", "w") as file:
                json.dump({"index": 0}, file)

        if len(Posting.id_cache) == 0:
            with open("url_ids.json", "r") as file:
                Posting.id_cache = json.load(file)

        # return existing id
        if url in Posting.id_cache:
            return Posting.id_cache[url]
        
        index = Posting.id_cache["index"]
        index += 1

        # update json index since new URL is being added
        Posting.id_cache["index"] = index

        # add new URL with new id
        Posting.id_cache[url] = index

        return index



    def __repr__(self) -> str:
        return f"({self.token}, {self.token_freq})"
