#!/usr/bin/env python
#
# Reads results file, return dict of query_id -> (score, results_line, doc, pos, runid)
# 


import sys, argparse, operator

def read(fh):
    results = {}
    for line in fh:
        items = line.split()
        query = items[0]
        score = float(items[4])
        doc = items[2]
        pos = items[3]
        runid = items[5]
    
        results[query] = results[query] + [(score, line.strip(), doc, pos, runid)] if query in results else [(score, line.strip(), doc, pos, runid)]

    return results

if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Reads a set of TREC results.")
	args.add_argument("qrel_file", nargs='?')
	args.add_argument("results_file")
	
	qrels = {}
	if args.parse_args().qrel_file != None:
		import qrel_reader
		qrels = qrel_reader.QrelReader(args.parse_args().qrel_file, True).get_judgements()

	results = read(open(args.parse_args().results_file))
	for (qId, docs) in sorted(results.items()):
		for (score, line, doc, pos, runid) in docs:
			relevance = qrels[qId][doc] if qId in qrels and doc in qrels[qId] else ''
			print("{}\t{}".format(line, relevance))
