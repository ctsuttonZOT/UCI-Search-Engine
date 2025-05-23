from math import log

# weights for normal, title, bold, h1, h2, h3
WEIGHTS = [1.0, 2.5, 1.5, 2.0, 1.7, 1.5]

def calculate_weighted_tf(postings_lists: list[list[tuple[int, int]]], doc_id: int) -> float:
    tf = 0
    for i, posting_list in enumerate(postings_lists):
        for id, freq in posting_list:
            if id == doc_id:
                tf += WEIGHTS[i] * freq
    return tf    


def compute_idf(postings_lists: list[list[tuple[int, int]]], total_docs: int) -> float:
    doc_ids = set()
    for posting_list in postings_lists:
        for id, _ in posting_list:
            doc_ids.add(id)
    df = len(doc_ids)
    return log(total_docs / df) if df != 0 else 0.0


def rank_documents(query: str, total_docs: int) -> list[tuple[int, int]]:
    # TODO: implement once merged index and merged index search is finished
    pass
