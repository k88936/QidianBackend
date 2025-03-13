from whoosh.index import open_dir
from whoosh.qparser import QueryParser

ix = open_dir("index")
with ix.searcher() as searcher:
    for doc in searcher.documents():
        print(doc)
