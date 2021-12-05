from lucenePathFinder import PathFinder
import time


LANGUAGE = "en"
INDEX_DIR = "../data_src/lucene_indexes/{lan}".format(lan=LANGUAGE)


bfs = PathFinder(INDEX_DIR)

while True:
    START = input("Starting article: ")
    END = input("Ending article: ")
    if START == "" or END == "":
        break
    print("Searching...")
    start = time.time()
    if bfs.find_path(start_article=START, end_article=END):
        end = time.time()
        print("\n### PATH FOUND ###\n")
        bfs.print_path(start_article=START, end_article=END)
        print("\n### Time elapsed:  {time} seconds ###\n".format(time=int((end - start))))
    else:
        print("!!! PATH NOT FOUND !!!")
        print("Path does not exist")
