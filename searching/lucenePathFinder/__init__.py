from queue import Queue
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, IndexReader, Term
from org.apache.lucene.document import Document, Field, TextField, StoredField, StringField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.queryparser.classic import QueryParser


class PathFinder:
    # start_article -> article name, key in disk_map
    # end_artivle -> article name, key in disk_map
    # index -> path to index directory
    # database -> file pointer
    def __init__(self, index: str):
        self.__index = index
        print("Initializing JVM...")
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        print("JVM ready\n")
        # self.__parsed_articles = parsed_articles # this was file for all articles
        self.__path = {}
        self.__directory = SimpleFSDirectory(Paths.get(self.__index))
        self.__searcher = IndexSearcher(DirectoryReader.open(self.__directory))

    def find_path(self, start_article: str, end_article: str):
        queue = Queue()
        visited = set()
        queue.put(start_article)
        visited.add(start_article)

        while not queue.empty():
            current_article = queue.get()
            query = TermQuery(Term("title", current_article))
            scoreDocs = self.__searcher.search(query, 1).scoreDocs
            if len(scoreDocs) == 0: # not in our collection
                continue
            links = self.__searcher.doc(scoreDocs[0].doc).get("links").split("#")
            # link == neighbour
            for link in links:
                if link in visited:
                    continue
                queue.put(link)
                visited.add(link)
                self.__path[link] = current_article
                if link == end_article:
                    return True

        return False

    def print_path(self, start_article: str, end_article: str):
        articles = []
        current_article = end_article
        articles.append(current_article)
        while True:
            articles.append(self.__path[current_article])
            if self.__path[current_article] == start_article:
                break
            current_article = self.__path[current_article]

        for i in range(len(articles) - 1, -1, -1):
            print(articles[i])
