#!/usr/bin/env python
#
# Read a qrel file, based in this format:
#   101 0 corpus/3abFaPdbkmHh-832.xml 2
#
# get_qrels() return dictionary:
#   qId -> [docs]
# get_judgements() returns dictionary:
#   qId -> docId -> relevance

import argparse

class QrelReader:
  
  def __init__(self, qrel_file, all_judged=False):
    self.qrels = {}
    self.judgements = {}
    for line in open(qrel_file):
      query, zero, doc, rel = line.strip().split()

      docs = self.judgements[query] if query in self.judgements else {}
      docs[doc] = int(rel)
      self.judgements[query] = docs

      if all_judged or rel != "0":
        docs = self.qrels[query] if query in self.qrels else []
        docs.append(doc)
        self.qrels[query] = docs
      
  def get_qrels(self):
    return self.qrels

  def get_judgements(self):
    return self.judgements
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read a qrel file, based in this format")
  parser.add_argument("qrel_file")
  
  qrel = QrelReader(parser.parse_args().qrel_file)
  
  for (query, docs) in qrel.get_judgements().items():
    for (doc, rel) in docs.items():
      print query, doc, rel