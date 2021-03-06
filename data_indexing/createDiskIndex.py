import json

DATA_SRC = "../data_src/diskmap_indexes/"
LOCALE = "sk"

DATA_TO_PARSE = DATA_SRC + "{locale}_parsed_sorted.jl".format(locale=LOCALE)
INDEX_DST = "../output/diskindex.json"

input_file = open(DATA_TO_PARSE, "r", encoding="utf-8")
output_file = open(INDEX_DST, "w", encoding="utf-8")
disk_offset = input_file.tell()
line = input_file.readline()
disk_index = {}
while line:
    data = json.loads(line)
    disk_index[data["title"]] = disk_offset
    disk_offset = input_file.tell()
    line = input_file.readline()

json.dump(disk_index, output_file, ensure_ascii=False, indent=None, separators=(',', ':'))
