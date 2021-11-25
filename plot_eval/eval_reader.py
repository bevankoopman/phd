#!/usr/bin/env python
#
# Reads a trec eval file and returns dcit queryId -> score

import re, argparse, operator

def read_eval(filename, measure, stop_on_error=True):
    eval = {}
    pattern = re.compile("\\b"+measure.strip()+"\\b")
    for line in open(filename):
        if pattern.search(line) and line.find("all") == -1 and line.find("runid") == -1:
            try:
                query, score = line.split()[1:]
                eval[query] = float(score)
            except:
                "Error reading line: %s", line
                raise
    if len(eval) == 0 and stop_on_error:
        raise(Exception("Error: No results found for measure '%s' in '%s'" % (measure, filename)))
    return eval

def read_eval_map(filename):
    return read_eval(filename, "map")
    
def read_eval_bpref(filename):
    return read_eval(filename, "bpref")

def read_eval_p10(filename):
    return read_eval(filename, "P_10")

def read_total(filename):
    eval = {}
    for line in open(filename):
        if re.findall("all", line):
            measure, all, score = line.strip().split("\t")
            if measure.strip() != 'runid':
                eval[measure.strip()] = float(score)
        if line.startswith("Index:"):
            eval["index"] = line[8:].strip()
        if line.startswith("Queries:"):
            eval["queries"] = line[9:].strip()

    return eval

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads Metamap Extended Indri style query file")
    parser.add_argument("-measure", default="bpref")
    parser.add_argument("-csv", action="store_true")
    parser.add_argument("eval_file")


    for (query, score) in sorted(read_eval(parser.parse_args().eval_file, parser.parse_args().measure).items(), key=operator.itemgetter(0)):
        if parser.parse_args().csv:
            print(score+",",)
        else:
            print(query + "\t" + score)
    