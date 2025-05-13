import json
import os

class Posting:
    def __init__(self, url: str, token: str, token_freq: int) -> None:
        # int representing the URL the token was found in
        self.url_id = self.get_url_id(url)

        # the token itself
        self.token = token

        # num of times the token occurs in the page
        self.token_freq = token_freq


    def get_url_id(self, url: str) -> int:
        # if the file doesn't exist, or it's empty, initialize it with default data
        if not (os.path.exists("url_ids.json")) or os.stat("url_ids.json").st_size == 0:
            with open("url_ids.json", "w") as file:
                json.dump({"index": 0}, file)

        with open("url_ids.json", "r+") as file:
            data = json.load(file)

            # return existing id
            if url in data:
                return data[url]
            
            index = data["index"]
            index += 1

            # update json index since new URL is being added
            data["index"] = index

            # add new URL with new id
            data[url] = index

            # update file
            file.seek(0)
            json.dump(data, file)
            file.truncate()

            return index

    def __repr__(self) -> str:
        return f"({self.url_id}, {self.token_freq})"
