#!/usr/bin/env python3
'''
created on Sun March 29 2020
author: Christian Olaf Haeusler
'''
from glob import glob
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
matplotlib.use('Agg')


TAG_DESIGN_PATTERN = 'sub-01/run-?_speech-validation.feat/design.mat'
TAG_USED = list(range(1, 27)) # [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 17, 18]
TAG_NAMES = {
    1: 'adjective, attributive',
    2: 'adjective, adverbial or predicative',
    3: 'adverbial determination',
    4: 'preposition; circumposition left',
    5: 'preposition with article',
    6: 'definite or indefinite article',
    7: 'coordinate conjunction',
    8: 'proper noun',
    9: 'noun (singular or mass)',
    10: 'substituting demonstrative pronoun',
    11: 'substituting indefinite pronoun',
    12: 'non-reflexive personal pronoun',
    13: 'attributive possessive pronoun',
    14: 'reflexive personal pronoun',
    15: 'separable verbal particle',
    16: 'finite verb,auxiliary',
    17: 'finite verb, modal',
    18: 'finite verb, full',
    19: 'infinitive, full',
    20: 'perfect participle, full',
    21: 'other tags',
    22: 'end of sentence',
    23: 'phonemes',
    24: 'no speech',
    25: 'left-right diff',
    26: 'root mean square'
}


def parse_arguments():
    '''
    '''
    parser = argparse.ArgumentParser(
        description="creates the correlation of convoluted regressors from \
        a subject's 1st lvl results directories (= all single run dirs ")


    parser.add_argument('-exmpl',
                        default='sub-01/run-01_speech-validation.feat/design.mat',
                    help='pattern of path/file for 1st lvl design files')

    parser.add_argument('-o',
                        default='figures',
                        help='the output directory for the PDF and SVG file')

    args = parser.parse_args()

    outDir = args.o
    example = args.exmpl

    return outDir, example


def plot_heatmap(matrix, outFpath):
    '''
    '''
    # generate a mask for the upper triangle
    mask = np.zeros_like(matrix, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # custom diverging colormap
    cmap = sns.diverging_palette(220, 10, sep=1, as_cmap=True)

    # draw the heatmap with the mask and correct aspect ratio
    sns_plot = sns.heatmap(matrix, mask=mask,
                           cmap=cmap,
                           square=True,
                           center = 0,
                           vmin=-1.0, vmax=1,
                           annot=True, annot_kws={"size": 8}, fmt='.1f',
                           #linewidths=.5,
                           cbar_kws={"shrink": .6}
                           )

    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(rotation=0, fontsize=12)

    for x in range(0, 21):
        plt.gca().get_xticklabels()[x].set_color('black') #  black = default

    for x in range(21, 26):
        plt.gca().get_xticklabels()[x].set_color('gray')

    for y in range(21, 26):
        plt.gca().get_yticklabels()[y].set_color('gray')

    for y in range(0, 21):
        plt.gca().get_yticklabels()[y].set_color('black')

    os.makedirs(outFpath, exist_ok=True)

    file_name = os.path.join(outFpath, 'regressor-corr.%s')
    f.savefig(file_name % 'svg', bbox_inches='tight', transparent=True)
    f.savefig(file_name % 'pdf', bbox_inches='tight', transparent=True)
    plt.close()


if __name__ == "__main__":
    outDir, designExample = parse_arguments()

    # from example, create the pattern to find design files for all runs
    run = re.search('run-\d', designExample)
    run = run.group()
    designPattern = designExample.replace(run, 'run-*')

    # just in case, create substitute random subject for sub-01
    subj = re.search('sub-\d{2}', designExample)
    subj = subj.group()
    designPattern = designPattern.replace(subj, 'sub-01')

    # get design.mat files for the 8 runs
    designFpathes = sorted(glob(designPattern))
    # specify which columns of the design file to use
    # correct for python index starting at 0
    # & use every 2nd column because odd numbered columns
    # in the design file are temporal derivatives
    tag_columns = [(x-1) * 2 for x in TAG_USED]
    tag_names = [TAG_NAMES[x] for x in TAG_USED]

    # read the all 8 design files and concatenate
    all_df = pd.concat([pd.read_csv(
        run,
        usecols=tag_columns,
        names=tag_names,
        skiprows=5, sep='\t')
        for run in designFpathes], ignore_index=True)

    # create the correlation matrix for all columns
    regCorrMat = all_df.corr()

    # plot it
    plot_heatmap(regCorrMat, outDir)
