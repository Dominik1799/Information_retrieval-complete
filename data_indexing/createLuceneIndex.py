import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StoredField, StringField
from org.apache.lucene.store import SimpleFSDirectory
import json


LANGUAGE = "sk"
WIKI_DATA = "/data/data_src/diskmap_indexes/{lan}_parsed_sorted.jl".format(lan=LANGUAGE)
INDEX_DESTINATION = "/data/data_src/lucene_indexes/{lan}_dummy".format(lan=LANGUAGE)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# config for index
store = SimpleFSDirectory(Paths.get(INDEX_DESTINATION))
analyzer = KeywordAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
config.setRAMBufferSizeMB(float(1000))
writer = IndexWriter(store, config)

wiki_file = open(WIKI_DATA, "r", encoding="utf-8")
line_counter = 0
for line in wiki_file:
    line_counter += 1
    article_dict = json.loads(line)
    title = article_dict["title"]
    links = "#".join(article_dict["links"])
    doc = Document()
    doc.add(Field("title", title, StringField.TYPE_STORED))
    doc.add(StoredField("links", links))
    writer.addDocument(doc)
    if line_counter % 100000 == 0:
        print("processed ", line_counter, " lines")

writer.commit()
writer.close()
print("\nDONE")