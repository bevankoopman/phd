#!/usr/bin/env python
#
# Compare two sets of TREC retrieval results.
#
# Input: 
#	1.results, 2,results, qrel
# Output:
#	Both results file annotated with i) '*' to indicate relevance ii) the position of the 
# 	document as [x,y] where x = pos in 1.results and y = pos in 2.results.

import argparse
import results_reader, qrel_reader

max_results = 10000

def find_pos(d, sdocs):
	for (score, line, doc, pos) in sdocs:
		if d == doc:
			return pos
	return "-" 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two sets of TREC retrieval results.")
    parser.add_argument("first_results")
    parser.add_argument("second_results")
    parser.add_argument("qrel")
    
    first = results_reader.read(open(parser.parse_args().first_results))
    second = results_reader.read(open(parser.parse_args().second_results))
    qrels = qrel_reader.QrelReader(parser.parse_args().qrel).get_qrels()
    
    for query in sorted(qrels.keys()):
    	fdocs = first[query] if query in first else []
    	sdocs = second[query] if query in second else []
    
    	max_docs = max(len(fdocs), len(sdocs))
    	for i in range(0, max_docs):
    		print query+"\t",
    		if i < len(fdocs):
    			fdoc = fdocs[i][1].split()[2]
    			if fdoc in qrels[query]:
    				print "*",
    			print fdoc,
    			print "[%i,%s]" % (i+1, find_pos(fdoc, sdocs)),
    			print fdocs[i][0],
    		else:
    			print '-',
    			
    		print "\t\t",
    			
    		if i < len(sdocs):
    			sdoc = sdocs[i][1].split()[2]
    			if sdoc in qrels[query]:
    				print "*",
    			print sdoc,
    			pos = find_pos(sdoc, fdocs)
    			print "[%s,%i]" % (pos, i+1),
    			print sdocs[i][0],
    			if pos == '-':
    				pos = max_results
    			print "\t"+`int(pos) - int(i+1)`,
				
    		else:
    			print '-',
    			
    		print ""
    		
    		if i > max_results:
    			break