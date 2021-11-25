#!/usr/bin/env python
#
# Plot a TREC eval results
#

import sys, operator, argparse, re, os, matplotlib
#matplotlib.use('MacOSX')
import pylab
import matplotlib.pyplot as plt
from pylab import arange,pi,sin,cos,sqrt
import eval_reader, stat_sig

# '-' solid line style
# '--'    dashed line style
# '-.'    dash-dot line style
# ':' dotted line style
# '.' point marker
# ',' pixel marker
# 'o' circle marker
# 'v' triangle_down marker
# '^' triangle_up marker
# '<' triangle_left marker
# '>' triangle_right marker
# '1' tri_down marker
# '2' tri_up marker
# '3' tri_left marker
# '4' tri_right marker
# 's' square marker
# 'p' pentagon marker
# '*' star marker
# 'h' hexagon1 marker
# 'H' hexagon2 marker
# '+' plus marker
# 'x' x marker
# 'D' diamond marker
# 'd' thin_diamond marker
# '|' vline marker
# '_' hline marker
plot_style = [':o', '--', '-', 'o', '1', 's', 'x']
# b : blue
# g : green
# r : red
# c : cyan
# m : magenta
# y : yellow
# k : black
# w : white
colours = ['r', 'y', 'c', 'k', 'k', 'k', 'k']
# colours = ['k', 'k', 'k', 'k', 'k', 'k', 'k']

SORT_BASELINE = True
SORT_EVAL = False
OUTPUT_FILE = ""
width = 0

#
# Plot line and averge
#  data - list of values to plot
#  avg - average line to plot
#  measure - map, P10 etc
#  label - name on graph
#  linestyle - color and solid, dashed etc
def plot(data, avg, measure, label, linestyle):
    global width


    #plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
    


    plt.plot(data, linestyle, label="%s" % label.replace(".eval", ""))
    scale = plt.axis()
    plt.axis([scale[0], scale[1], 0, 1])
    #plt.bar([x + width for x in range(len(data))], data, color=linestyle[0])
    width += 10
    print(label, avg)
    #plt.axhline(y=avg, color=linestyle[0], linestyle=linestyle[1])    

def main(base_eval, run_evals, measures):

    fig_width_pt = 700  # Get this from LaTeX using \showthe\columnwidth 221 columnwidth
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
    golden_mean = 3.0/4
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*golden_mean      # height in inches
    fig_size =  [fig_width,fig_height]

    # print(plt.rcParams.keys())
    params = {'backend': 'pdf',
          'axes.labelsize': 14,
          'font.size': 12,
          'legend.fontsize': 10,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'text.usetex': False,
          'figure.figsize': fig_size}
    #pylab.rcParams.update(params)
    
    #plt.rcParams['figure.figsize'] = fig_size
    #plt.rc('text', usetex=False)
    #plt.rc('font', family='sans-serif')
    #plt.rc('legend', fontsize='10')

    #params = {'backend': 'pdf', 'axes.labelsize': 10, 'text.fontsize': 10, 'legend.fontsize': 10,'xtick.labelsize': 8, 'ytick.labelsize': 8, 'text.usetex': True,'figure.figsize': fig_size}
    pylab.rcParams.update(params)
    

    baseline_total = eval_reader.read_total(base_eval)

    for measure in measures:

        # read the baseline eval
        baseline = eval_reader.read_eval(base_eval, measure).items()
        if SORT_BASELINE:
            baseline = sorted(baseline, key=operator.itemgetter(1), reverse=True)
        
        # a comparison file is supplied - plot first
        for run_eval in run_evals:
            if run_eval != None:
                #print(run_eval)
                run_total = eval_reader.read_total(run_eval)
                run = eval_reader.read_eval(run_eval, measure)
                if SORT_EVAL:
                    sorted_run = [float(v) for (k,v) in sorted(run.items(), key=operator.itemgetter(1), reverse=True)]
                else:
                    sorted_run = [float(run[k]) for (k,v) in baseline if k in run]
                    
                legend = f"{run_eval} ({measure} = {run_total[measure]})"
                styleCount = run_evals.index(run_eval)+1
                this_plot_style = plot_style[styleCount] if run_evals.index(run_eval) < (len(run_evals)-1) else "-"
                print(run_total)
                plot(sorted_run, run_total[measure], measure, legend, colours[styleCount]+this_plot_style+'o')

        # plot the baseline
        legend = f"{base_eval} ({measure} = {baseline_total[measure]})"
        plot([float(v) for (k,v) in baseline], baseline_total[measure], measure, legend, \
                 colours[0]+plot_style[0])

    measure_label = re.sub("^P_", "P@", measure)

    
    plt.ylabel(", ".join([m.upper() for m in measures]))
    plt.ylabel(measure_label)
    plt.xlabel("Topic")
    # ax = plt.subplot(111)
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.legend(loc='lower left')
    if len(OUTPUT_FILE) > 0:
        plt.savefig(os.environ['HOME']+'/tmp/plot-'+run_evals[len(run_evals)-1]+'.'+OUTPUT_FILE, format=OUTPUT_FILE)
    else:
        plt.show()

def printUsage():
    print("Usage: plot_eval.py TREC_EVAL_FILE [OTHER_TREC_EVAL]")

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Creates graph plot of trec eval run.')
    #parser.add_argument("eval_file", action='store', type=argparse.FileType('rt'))
    #parser.add_argument("

    if len(sys.argv) < 2:
        printUsage()
    else:
        measures = []
        for arg in sys.argv[:]:
            if arg.startswith("-s"):
                SORT_EVAL = True
                sys.argv.remove(arg)
            elif arg.startswith("-pdf") or arg.startswith("-png"):
                OUTPUT_FILE = arg[1:]
                sys.argv.remove(arg)
            elif arg.startswith("-"):
                measures += [arg[1:]]
                sys.argv.remove(arg)

        measures = measures if len(measures) > 0 else ["recip_rank"]

        if len(sys.argv) > 2:
        	tstat, p, firstAvg, secondAvg = stat_sig.stat_sig(sys.argv[1], sys.argv[2], measures[0])
        	print('t-statistic = %6.3f pvalue = %6.4f' % (tstat, p))
        main(sys.argv[1], sys.argv[2:] if len(sys.argv) > 2 else None, measures)

        
                
        
