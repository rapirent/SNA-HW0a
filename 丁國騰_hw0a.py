#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

import math

def csv_manipulator(csv_file):
    """Read a csv file object and create a score summary dictionary

    Arguments:
        csv_file {string}

    Returns:
        dict -- key=score, value=player_name
    """
    reader = pd.read_csv(csv_file)
    score_summary = {}
    seasons_count = {}
    score = {}
    year_table = {}
    # find years having a play
    for year in reader['year']:
        if year not in year_table:
            year_table[year] = {}
    for row in reader.index.tolist():
        player_name = reader['firstname'][row] + ' ' + reader['lastname'][row]
        # seasons_count to count the players' seasons number
        if player_name not in seasons_count.keys():
            seasons_count[player_name] = 0
            score[player_name] = 0
        if player_name not in year_table[reader['year'][row]]:
            year_table[reader['year'][row]][player_name] = {'pts': 0,
                                                            'reb': 0,
                                                            'asts': 0,
                                                            'stl': 0,
                                                            'blk': 0,
                                                            'fga': 0,
                                                            'fgm': 0,
                                                            'fta': 0,
                                                            'ftm': 0,
                                                            'turnover': 0,
                                                            'gp': 0}
        for key in year_table[reader['year'][row]][player_name].keys():
            # add the value in same season
            if reader[key][row] == 'NULL':
                year_table[reader['year'][row]][player_name][key] = 0
            else:
                year_table[reader['year'][row]][player_name][key] += reader[key][row]
    for year in year_table.keys():
        for player_name in year_table[year].keys():
            seasons_count[player_name] += 1
            value = ((year_table[year][player_name]['pts'] + year_table[year][player_name]['reb'] +
                      year_table[year][player_name]['asts'] + year_table[year][player_name]['stl'] +
                      year_table[year][player_name]['blk'] - (year_table[year][player_name]['fga'] -
                      year_table[year][player_name]['fgm'] + year_table[year][player_name]['fta'] -
                      year_table[year][player_name]['ftm'] + year_table[year][player_name]['turnover'])) /
                      year_table[year][player_name]['gp'])
            if math.isnan(value):
                score[player_name] += 0
            else:
                score[player_name] += value
    for name in seasons_count.keys():
        score_summary[name] = score[name] / seasons_count[name]
    return {score: name for (name, score) in score_summary.items()}

def score_sort(score_dict):
    """use the python sorted function to sort the score dictionary

    Arguments:
        score_dict {dict} -- keys are scores, values are players' names

    Returns:
        tuple -- (name, score) using decreaing order
    """
    sorted_scores = sorted(score_dict.keys(), reverse=True)
    sorted_names = [ score_dict[k] for k in sorted_scores]
    return zip(sorted_names, sorted_scores)

if __name__ == '__main__':
    s = csv_manipulator('nba_data.csv')
    output = open('丁國騰_hw0a.txt', 'w')
    for i, (name, score) in enumerate(score_sort(s)):
        if i < 20:
            output.write('RANK {0:2d}\t{1:>19s}\t{2:.2f}\n'.format(i+1, name, score))

    output.close()
