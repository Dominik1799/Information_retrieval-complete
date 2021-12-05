```
.
├── data_indexing // scripts used to create indexes - lucene and custom disk indexes. Includes lucene Dockerfile
│   ├── Dockerfile
│   ├── createDiskIndex.py
│   ├── createLuceneIndex.py
│   └── sortLinks.py // optional: links are sorted by number of links they contain themselves, performance is slightly better
├── data_processing // scripts used for processing original wikipedia dumps. Includes parsing to .jl and also to graph vertices and edges
│   ├── Dockerfile
│   ├── docker-compose.yml // docker compose to create a spark cluster
│   ├── parse.py
│   ├── parseToGraph.py
│   └── wrapers // run every python file using these scripts. They clean after each script, merge output to one file etc.
│       ├── runGraphParsing.sh
│       └── runParsing.sh
└── searching // scripts for searching in final data.
    ├── Dockerfile // lucene dockerfile, same as in data_indexing folder
    ├── diskMapBFS.py // searching using my custom disk map indexes
    ├── diskMapPathFinder // BFS class for diskmap path
    │   └── __init__.py
    ├── docker-compose.yml // run spark cluster, same as in data_processing
    ├── graphBFS.py // searching using Spark and GraphFrames
    ├── luceneBFS.py // searching using lucene index
    ├── lucenePathFinder // BFS class for lucene index path
    │   └── __init__.py
    ├── printGraphPath.py // print path found by spark and GraphFrames
    └── wrappers // wrapper for spark pathfinding, as 2 scripts are used: graphBFS.py. and printGraphPath.py
        └── runGraphPathFinder.sh
```