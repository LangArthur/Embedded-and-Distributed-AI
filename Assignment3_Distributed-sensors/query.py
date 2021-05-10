#!/usr/bin/env python3
#
# Created on Mon May 10 2021
#
# Arthur Lang
# query.py
#

from rdflib import Graph

# PRESURRE_FILE = "https://www.wikidata.org/wiki/Special:EntityData/Q2831.ttl"
PRESURRE_FILE = "pressure.ttl"

def main():
    graph = Graph()
    graph.parse(PRESURRE_FILE, format="ttl")
    res = graph.query('''
    SELECT ?resultTime ?hasSimpleResult
    WHERE {
        ?a sosa:resultTime ?resultTime.
        ?a sosa:hasSimpleResult ?hasSimpleResult.
    }
    ORDER BY ?resultTime
    ''')
    for date, pressure in res:
        print("{} | {}".format(date, pressure))
    return 0

if __name__ == '__main__':
    main()