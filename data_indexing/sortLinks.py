import json
import operator
from dataclasses import dataclass

LANGUAGE = "sk"
PARSED_WIKIPEDIA = "../data_src/diskmap_indexes/{lan}_parsed.jl".format(lan=LANGUAGE)
DISK_MAP = "../data_src/diskmap_indexes/{lan}_parsed_index.json".format(lan=LANGUAGE)
SORTED_WIKIPEDIA_DESTINATION = "../data_src/diskmap_indexes/{lan}_parsed_sorted_dummy.jl".format(lan=LANGUAGE)

output_file = open(SORTED_WIKIPEDIA_DESTINATION, "w", encoding="utf-8")
input_file = open(PARSED_WIKIPEDIA, "r", encoding="utf-8")  # for line by line reading
input_file_degrees_seek = open(PARSED_WIKIPEDIA, "r", encoding="utf-8")  # for seeking the degree of each graph node

with open(DISK_MAP, "r", encoding="utf-8") as f:
    disk_map = json.load(f)


@dataclass
class Link:
    link: str
    degree: int


def get_degree(link):
    if link not in disk_map:
        return 0
    input_file_degrees_seek.seek(disk_map[link])
    art = json.loads(input_file_degrees_seek.readline())
    return len(art["links"])


def main():
    line = input_file.readline()
    while line:
        # create empty array of dataclasses for links
        link_nodes = []
        article = json.loads(line)
        article["links"] = list(dict.fromkeys(article["links"]))
        for link in article["links"]:
            dtcls = Link(link, get_degree(link))
            link_nodes.append(dtcls)
        link_nodes = sorted(link_nodes, key=operator.attrgetter("degree"), reverse=True)
        final_array = [node.link for node in link_nodes]
        article["links"] = final_array
        output_file.write(json.dumps(article, ensure_ascii=False, indent=None, separators=(',', ':')))
        output_file.write("\n")
        output_file.flush()
        line = input_file.readline()


if __name__ == "__main__":
    main()


