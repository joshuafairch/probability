import os
import numpy as np
import matplotlib.pyplot as plt

import random

def format_plot(ax,title=None,xlabel=None,ylabel=None,xmin=None,xmax=None,ymin=None,ymax=None):

    ax.set_title(title)

    ax.set_xlabel(xlabel)
    ax.set_xlim([xmin,xmax])

    ax.set_ylabel(ylabel)
    ax.set_ylim([ymin,ymax])

def main():

    # ---
    # preprocess
    # ---

    # convert frequency to something more convenient
    period = int(1/freq)

    # assign number for true case
    target = round(period/2)
    # simulation will roll a number in range [1,period]
    # target is within this range
    # if simulation lands on this value, then hit is true
    # else, hit is false

    # ---
    # simulate
    # ---

    # stop after success = geometric (below)
    # continue to set number = binomial

    # trial_record:
    #   index = case number - 1
    #   value = number of attempts to first hit
    trial_record = np.zeros(cases)

    for case in range (0,cases):

        # reset counters for new case
        hit = False
        trial = 0

        while trial < trial_max and hit == False:

            # increase trial counter
            trial = trial + 1

            # generate random number
            instance = random.randint(1,period)

            # if hit or maxed out number of trials
            if instance == target or trial == trial_max:

                # log required number of trials
                trial_record[case] = trial
                hit = True

    # convert from float to integer for later np.zeros(max(trial_record))
    trial_record = np.asarray(trial_record,int)

    # setup trial index for later x-axis plotting
    trial_index = np.linspace(0,max(trial_record),max(trial_record)+1)

    # ---
    # postprocess
    # ---

    # num_first_success:
    #   index = number of attempts to first hit (note no offset -> index = #)
    #   value = number of occurrences of index
    num_first_success = np.zeros(max(trial_record)+1)

    for trial in range(0,max(trial_record)+1):
        num_first_success[trial] = trial_record.tolist().count(trial)

    # print(num_first_success)
    # above should always:
    #   num_first_success[0] == 0
    #   num_first_success[-1] > 0

    # total (cumulative) chance of first hit
    cumulative_cases = np.zeros(max(trial_record)+1)
    for trial in range(1,max(trial_record)+1):
        # start from 1 for sum
        # holds since num_first_success[0] == 0 always true
        cumulative_cases[trial] = cumulative_cases[trial-1] + num_first_success[trial]
    cumulative_chance = cumulative_cases/cases*100

    # print(cumulative_chance)
    # above should always:
    #   cumulative_chance[0] == 0
    #   cumulative_chance[-1] == 100 (which is not logically true)

    # ---
    # shifted geometric distribution functions
    # ---

    pmf = np.zeros(max(trial_record)+1)
    cdf = np.zeros(max(trial_record)+1)

    for trial in range(1,max(trial_record)+1):

        # probability mass function
        pmf[trial] = (1-freq)**(trial-1)*freq
        
        # cumulative distribution function
        cdf[trial] = 1-(1-freq)**trial

    # adjust bounds
    pmf[0] = np.nan     # pmf only valid for trial >=1
    cdf[0] = 0          # cdf = 0 for trial < 1

    # print((pmf))
    # print((cdf))

    # ---
    # plot
    # ---

    fig,[ax11,ax21] = plt.subplots(2,1)

    # probability distribution
    ax11.bar(trial_index,num_first_success)
    ax12 = ax11.twinx()
    ax12.plot(trial_index[1:],pmf[1:],'red')

    ax11.grid(True)
    format_plot(ax11,'Trials to First Success','Trials','Cases',0,max(trial_record),0,max(num_first_success))
    format_plot(ax12,None,None,'Probability Mass Function',None,None,0,max(pmf[1:]))

    # percent chance
    ax21.bar(trial_index,cumulative_chance)
    ax22 = ax21.twinx()
    ax22.plot(trial_index,cdf,'red')

    ax21.grid(True)
    format_plot(ax21,'Chance of One or More Successes','Trials','Percent Chance',0,max(trial_record),0,100)
    format_plot(ax22,None,None,'Cumulative Distribution Function',None,None,0,1)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':

    # rate of success
    freq = 1/10

    # number of independent cases
    cases = 10000
    
    # max number of trials per case
    # recommend trial_max >> 1/freq
    trial_max = 1/freq*20

    # therefore, total trials <= cases * trial_max

    main()
