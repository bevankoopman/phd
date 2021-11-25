#!/usr/bin/env python
#
# Stat sig test
#

import argparse
from scipy import stats
from numpy import array
import eval_reader

def mean(x):
	return sum(x)/len(x)

def stat_sig(first_file, second_file, measure):

	first = eval_reader.read_eval(first_file, measure).values()
	second = eval_reader.read_eval(second_file, measure).values()

	first = [float(x) for x in first]
	second = [float(x) for x in second]
	tstat, p = stats.ttest_rel(array(first), array(second))


	return tstat, p, mean(first), mean(second)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Computes statistical significance between two trec_eval evaluation files.")
	parser.add_argument("-m", "--measure", default="map", help="The evaluation measure (default is 'map')")
	parser.add_argument("first_eval_file", help="The first trec_eval file.")
	parser.add_argument("second_eval_file", help="The second trec_eval file.")
	
	first_file = parser.parse_args().first_eval_file
	second_file = parser.parse_args().second_eval_file
	measure = parser.parse_args().measure

	tstat, p, firstAvg, secondAvg = stat_sig(first_file, second_file, measure)

	print("Measure: %s" % measure)
	print("%s: %.4f" % (first_file, firstAvg))
	print("%s: %.4f" % (second_file, secondAvg))
	print('t-statistic = %6.3f pvalue = %6.4f' % (tstat, p))