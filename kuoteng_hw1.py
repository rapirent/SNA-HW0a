#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import csv

def csv_manipulator(csv_file):
    """Read a csv file object and create a score summary dictionary

    Arguments:
        csv_file {file}

    Returns:
        dict -- key=score, value=player_name
    """
    reader = csv.DictReader(csv_file)
    score_summary = dict()
    seasons_count = dict()
    for row in reader:
        for (key, value) in row.items():
            if value == 'NULL':
                row[key] = 0
        player_name = row['firstname'] + ' ' + row['lastname']
        if player_name not in score_summary:
            score_summary[player_name] = seasons_count[player_name] = 0
        seasons_count[player_name] += 1
        score_summary[player_name] += ((int(row['pts']) + int(row['reb']) +
                                int(row['asts']) + int(row['stl']) +
                                int(row['blk']) - int(row['fga']) +
                                int(row['fgm']) + int(row['fta']) -
                                int(row['ftm']) + int(row['turnover'])) / int(row['gp']))
    for keys in seasons_count:
        score_summary[keys] /= seasons_count[keys]
    return {k: v for (v, k) in score_summary.items()}


def score_sort(score_dict):
    """[summary]

    Arguments:
        score_dict {dict} -- keys are scores, values are players' names

    Returns:
        tuple -- (name, score) using decreaing order
    """
    sorted_scores = sorted(score_dict.keys(), reverse=True)
    sorted_names = [ score_dict[k] for k in sorted_scores]
    return zip(sorted_names, sorted_scores)

if __name__ == '__main__':
    f = open('nba_data.csv', newline='')
    s = csv_manipulator(f)
    f.close()
    output = open('丁國騰_hw0a.txt', 'w')
    # print(list(enumerate(score_sort(s))))
    for i, (name, score) in enumerate(score_sort(s)):
        output.write('RANK\t{0}\t{1}\t{2}\n'.format(i+1, name, score))

    output.close()
