#coding=gbk
import codecs
import string
from collections import namedtuple
# urllib模块提供了读取Web页面数据的接口
import json
import os
import time
import sys
reload(sys)

sys.setdefaultencoding('gbk')


import json
with open('all_player_info.txt', 'r') as f:
    all_player_info = json.load(f)
    all_team_name = set()
    for i in xrange(len(all_player_info)):
        all_player_info[i] = all_player_info[i].replace('\n', '')
        all_player_info[i] = eval(all_player_info[i])
        for key, val in all_player_info[i]['match_info_list'].items():
            if 'CBA联赛'.decode('gbk').encode('utf-8') in key:
                all_team_name.add(all_player_info[i]['match_info_list'][key]['match_team_name'])

with open('all_match_info.txt', 'r') as f:
    all_match_info_ls = json.load(f)

with open('foreign_aid_id_ls.txt', 'r') as f:
    foreign_aid_id_ls = json.load(f)
    foreign_aid_id_ls = [int(x) for x in foreign_aid_id_ls]

years = [int(u'20'+ x[5:7]) for x in all_match_info_ls[0] if int(u'20'+ x[5:7]) > 2005]
years = sorted(years, key= lambda x:x)

def get_inner_key_data(player, year, data_key):
    for key, val in player['match_info_list'].items():
        if 'CBA联赛'.decode('gbk').encode('utf-8') in key and (str(year)[-2:] + '-' in key):


            if data_key == 'match_time':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'match_score':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'match_2score_valid':
                data = player['match_info_list'][key]['match_2score']
                ind = data.find('-')
                data = float(data[:ind])
            elif data_key == 'match_2score_total':
                data = player['match_info_list'][key]['match_2score']
                ind = data.find('-')
                ind2 = data.find(' ')
                data = float(data[ind + 1:ind2])
            elif data_key == 'match_3score_valid':
                data = player['match_info_list'][key]['match_3score']
                ind = data.find('-')
                data = float(data[:ind])
            elif data_key == 'match_3score_total':
                data = player['match_info_list'][key]['match_3score']
                ind = data.find('-')
                ind2 = data.find(' ')
                data = float(data[ind + 1:ind2])
            elif data_key == 'match_punish_valid':
                data = player['match_info_list'][key]['match_punish']
                ind = data.find('-')
                data = float(data[:ind])
            elif data_key == 'match_punish_total':
                data = player['match_info_list'][key]['match_punish']
                ind = data.find('-')
                ind2 = data.find(' ')
                data = float(data[ind + 1:ind2])
            elif data_key == 'borad_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'front_borad_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'back_borad_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'assist_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'catch_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'slam_dunk_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'nut_cap_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'break_the_rules':
                data = player['match_info_list'][key][data_key]
                data = float(data)
            elif data_key == 'miss_num':
                data = player['match_info_list'][key][data_key]
                data = float(data)
    return data

def get_scatter_data(key1, key2):
    years = [int(u'20' + x[5:7]) for x in all_match_info_ls[0] if int(u'20' + x[5:7]) > 2005]
    years = sorted(years, key=lambda x: x)
    # 第一个维度表示年份，最后维度8各数字依次表示全部运动员数据求和、计数。前锋运动员的求和、计数。中锋运动员的求和、计数。后卫运动员的求和、计数。
    foreign_player_key_data_ls = [[] for x in xrange(4)]
    country_player_key_data_ls = [[] for x in xrange(4)]
    first_year = years[0]

    for player in all_player_info:

        years = []
        year2team = {}
        for key, val in player['match_info_list'].items():
            if 'CBA联赛'.decode('gbk').encode('utf-8') in key:
                year = u'20' + unicode(player['match_info_list'][key]['match_name'],
                                       'utf-8')[5:7]
                year2team[int(year)] = player['match_info_list'][key]['match_team_name']

                try:
                    if int(year) < 2050 and int(year) >= first_year:
                        year = int(year)
                        years.append(year)
                except:
                    continue

        for year in years:
            data1 = get_inner_key_data(player, year, key1)
            data2 = get_inner_key_data(player, year, key2)

            if player['id'] in foreign_aid_id_ls:
                foreign_player_key_data_ls[0].append([data1, data2])

                if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[1].append([data1, data2])

                if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[2].append([data1, data2])

                if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[3].append([data1, data2])
            else:
                country_player_key_data_ls[0].append([data1, data2])

                if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[1].append([data1, data2])

                if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[2].append([data1, data2])

                if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[3].append([data1, data2])

    return country_player_key_data_ls, foreign_player_key_data_ls

def get_key_data_according_foreign_aid_for_05_16(data_key, team_name = None):
    years = [int(u'20'+ x[5:7]) for x in all_match_info_ls[0] if int(u'20'+ x[5:7]) > 2005]
    years = sorted(years, key= lambda x:x)
    #第一个维度表示年份，最后维度8各数字依次表示全部运动员数据求和、计数。前锋运动员的求和、计数。中锋运动员的求和、计数。后卫运动员的求和、计数。
    foreign_player_key_data_ls = [[0, 0, 0, 0, 0, 0, 0, 0] for x in years]
    country_player_key_data_ls = [[0, 0, 0, 0, 0, 0, 0, 0] for x in years]
    first_year = years[0]

    max_min_str_foreign_player_key_data_ls = [[1000000, '', 0, '', 1000000, '', 0, '', 1000000, '', 0, '', 1000000, '', 0, ''] for x in years]
    max_min_str_country_player_key_data_ls = [[1000000, '', 0, '', 1000000, '', 0, '', 1000000, '', 0, '', 1000000, '', 0, ''] for x in years]

    for player in all_player_info:
        years = []
        year2team = {}
        for key, val in player['match_info_list'].items():
            if 'CBA联赛'.decode('gbk').encode('utf-8') in key:
                year = u'20' + unicode(player['match_info_list'][key]['match_name'],
                    'utf-8')[5:7]

                if year < 2006:
                    continue

                year2team[int(year)] = player['match_info_list'][key]['match_team_name']

                try:
                    if ((team_name == None) or (team_name != None and team_name == player['match_info_list'][key]['match_team_name'])) and int(year) < 2050 and int(year) >= first_year:
                        year = int(year)
                        years.append(year)
                except:
                    continue

        for year in years:
            data = get_inner_key_data(player, year, data_key)

            if player['id'] in foreign_aid_id_ls and data != 0:
                foreign_player_key_data_ls[year - first_year][0] += data
                foreign_player_key_data_ls[year - first_year][1] += 1
                if max_min_str_foreign_player_key_data_ls[year - first_year][0] > data and data != 0:
                    max_min_str_foreign_player_key_data_ls[year - first_year][0] = data
                    max_min_str_foreign_player_key_data_ls[year - first_year][1] = str(year) + '_' + year2team[
                        year] + '_' + player['name'] + '_' + str(player['height']) + '_' + str(player['weight'])

                if max_min_str_foreign_player_key_data_ls[year - first_year][2] < data and data != 0:
                    max_min_str_foreign_player_key_data_ls[year - first_year][2] = data
                    max_min_str_foreign_player_key_data_ls[year - first_year][3] = str(year) + '_' + year2team[
                        year] + '_' + player['name'] + '_' + str(player['height']) + '_' + str(player['weight'])

                if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[year - first_year][2] += data
                    foreign_player_key_data_ls[year - first_year][3] += 1
                    if max_min_str_foreign_player_key_data_ls[year - first_year][4] > data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][4] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][5] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_foreign_player_key_data_ls[year - first_year][6] < data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][6] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][7] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[year - first_year][4] += data
                    foreign_player_key_data_ls[year - first_year][5] += 1
                    if max_min_str_foreign_player_key_data_ls[year - first_year][8] > data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][8] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][9] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_foreign_player_key_data_ls[year - first_year][10] < data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][10] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][11] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                    foreign_player_key_data_ls[year - first_year][6] += data
                    foreign_player_key_data_ls[year - first_year][7] += 1

                    if max_min_str_foreign_player_key_data_ls[year - first_year][12] > data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][12] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][13] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_foreign_player_key_data_ls[year - first_year][14] < data and data != 0:
                        max_min_str_foreign_player_key_data_ls[year - first_year][14] = data
                        max_min_str_foreign_player_key_data_ls[year - first_year][15] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])
            else:
                country_player_key_data_ls[year - first_year][0] += data
                country_player_key_data_ls[year - first_year][1] += 1

                if max_min_str_country_player_key_data_ls[year - first_year][0] > data and data != 0:
                    max_min_str_country_player_key_data_ls[year - first_year][0] = data
                    max_min_str_country_player_key_data_ls[year - first_year][1] = str(year) + '_' + year2team[
                        year] + '_' + \
                                                                                   player['name'] + '_' + str(
                        player['height']) + '_' + str(player['weight'])

                if max_min_str_country_player_key_data_ls[year - first_year][2] < data and data != 0:
                    max_min_str_country_player_key_data_ls[year - first_year][2] = data
                    max_min_str_country_player_key_data_ls[year - first_year][3] = str(year) + '_' + year2team[
                        year] + '_' + \
                                                                                   player['name'] + '_' + str(
                        player['height']) + '_' + str(player['weight'])

                if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[year - first_year][2] += data
                    country_player_key_data_ls[year - first_year][3] += 1

                    if max_min_str_country_player_key_data_ls[year - first_year][4] > data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][4] = data
                        max_min_str_country_player_key_data_ls[year - first_year][5] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_country_player_key_data_ls[year - first_year][6] < data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][6] = data
                        max_min_str_country_player_key_data_ls[year - first_year][7] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[year - first_year][4] += data
                    country_player_key_data_ls[year - first_year][5] += 1

                    if max_min_str_country_player_key_data_ls[year - first_year][8] > data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][8] = data
                        max_min_str_country_player_key_data_ls[year - first_year][9] = str(year) + '_' + \
                                                                                       year2team[
                                                                                           year] + '_' + player[
                                                                                           'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_country_player_key_data_ls[year - first_year][10] < data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][10] = data
                        max_min_str_country_player_key_data_ls[year - first_year][11] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                    country_player_key_data_ls[year - first_year][6] += data
                    country_player_key_data_ls[year - first_year][7] += 1
                    if max_min_str_country_player_key_data_ls[year - first_year][12] > data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][12] = data
                        max_min_str_country_player_key_data_ls[year - first_year][13] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

                    if max_min_str_country_player_key_data_ls[year - first_year][14] < data and data != 0:
                        max_min_str_country_player_key_data_ls[year - first_year][14] = data
                        max_min_str_country_player_key_data_ls[year - first_year][15] = str(year) + '_' + \
                                                                                        year2team[
                                                                                            year] + '_' + \
                                                                                        player[
                                                                                            'name'] + '_' + str(
                            player['height']) + '_' + str(player['weight'])

    return country_player_key_data_ls, foreign_player_key_data_ls, max_min_str_country_player_key_data_ls, max_min_str_foreign_player_key_data_ls



def write_hist_global(file_name, data_key, max_min_str_country_player_key_data_ls, max_min_str_foreign_player_key_data_ls, team_name = None):
    with open(file_name, 'w') as f:
        years = [int(u'20' + x[5:7]) for x in all_match_info_ls[0] if int(u'20' + x[5:7]) > 2005]
        years = sorted(years, key=lambda x: x)
        first_year = years[0]

        hist_border_country_player = [10000000, 0, 10000000, 0, 10000000, 0, 10000000, 0]
        hist_border_foreign_player = [10000000, 0, 10000000, 0, 10000000, 0, 10000000, 0]

        country_player_hist_res_ls = [[], [], [], []]
        foreign_player_hist_res_ls = [[], [], [], []]

        for ind in xrange(4):
            country_player_hist_res_ls[ind] = [0 for x in range(10)]
            foreign_player_hist_res_ls[ind] = [0 for x in range(10)]

        for max_min_str_country_player_key_data in max_min_str_country_player_key_data_ls:
            for ind in xrange(0, 16, 4):
                hist_border_country_player[int(ind/2 + 0.5)] = min(hist_border_country_player[int(ind/2 + 0.5)], max_min_str_country_player_key_data[ind])

            for ind in xrange(2, 16, 4):
                hist_border_country_player[int(ind/2 + 0.5)] = max(hist_border_country_player[int(ind/2 + 0.5)], max_min_str_country_player_key_data[ind])

        for max_min_str_foreign_player_key_data in max_min_str_foreign_player_key_data_ls:
            for ind in xrange(0, 16, 4):
                hist_border_foreign_player[int(ind/2 + 0.5)] = min(hist_border_foreign_player[int(ind/2 + 0.5)], max_min_str_foreign_player_key_data[ind])

            for ind in xrange(2, 16, 4):
                hist_border_foreign_player[int(ind/2 + 0.5)] = max(hist_border_foreign_player[int(ind/2 + 0.5)], max_min_str_foreign_player_key_data[ind])
        cnt_cnt = 0
        for player in all_player_info:
            if player['id'] == 6931:
                a = 0
            years = []
            year2team = {}
            for key, val in player['match_info_list'].items():
                if 'CBA联赛'.decode('gbk').encode('utf-8') in key:
                    year = u'20' + unicode(player['match_info_list'][key]['match_name'],
                                           'utf-8')[5:7]
                    year2team[int(year)] = player['match_info_list'][key]['match_team_name']

                    try:
                        if ((team_name == None) or (team_name != None and team_name == player['match_info_list'][key][
                            'match_team_name'])) and int(year) < 2050 and int(year) >= first_year:
                            year = int(year)
                            years.append(year)
                    except:
                        continue

            for year in years:
                data = get_inner_key_data(player, year, data_key)

                cnt_cnt += 1
                if player['id'] in foreign_aid_id_ls and data != 0:
                    ind_hist = int(1.0 * (data - hist_border_country_player[0]) / (hist_border_country_player[1] - hist_border_country_player[0]) * 10 + 0.5)
                    ind_hist = 9 if ind_hist > 9 else ind_hist
                    ind_hist = 0 if ind_hist < 0 else ind_hist
                    foreign_player_hist_res_ls[0][ind_hist] += 1

                    if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[2]) / (
                            hist_border_country_player[3] - hist_border_country_player[2]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        foreign_player_hist_res_ls[1][ind_hist] += 1

                    if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[4]) / (
                            hist_border_country_player[5] - hist_border_country_player[4]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        foreign_player_hist_res_ls[2][ind_hist] += 1

                    if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[6]) / (
                            hist_border_country_player[7] - hist_border_country_player[6]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        foreign_player_hist_res_ls[3][ind_hist] += 1
                else:
                    ind_hist = int(1.0 * (data - hist_border_country_player[0]) / (hist_border_country_player[1] - hist_border_country_player[0]) * 10 + 0.5)
                    ind_hist = 9 if ind_hist > 9 else ind_hist
                    ind_hist = 0 if ind_hist < 0 else ind_hist
                    country_player_hist_res_ls[0][ind_hist] += 1

                    if player['postion'] == '前锋'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[2]) / (
                        hist_border_country_player[3] - hist_border_country_player[2]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        country_player_hist_res_ls[1][ind_hist] += 1

                    if player['postion'] == '中锋'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[4]) / (
                        hist_border_country_player[5] - hist_border_country_player[4]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        country_player_hist_res_ls[2][ind_hist] += 1

                    if player['postion'] == '后卫'.decode('gbk').encode('utf-8'):
                        ind_hist = int(1.0 * (data - hist_border_country_player[6]) / (
                        hist_border_country_player[7] - hist_border_country_player[6]) * 10 + 0.5)
                        ind_hist = 9 if ind_hist > 9 else ind_hist
                        ind_hist = 0 if ind_hist < 0 else ind_hist
                        country_player_hist_res_ls[3][ind_hist] += 1

        country_player_range_ls = [[], [], [], []]
        foreign_player_range_ls = [[], [], [], []]
        for ind in xrange(4):
            country_player_range_ls[ind] = [(hist_border_country_player[ind*2] + ind_r * (hist_border_country_player[ind*2+1] - hist_border_country_player[ind*2])/10.) for ind_r in range(10)]

            foreign_player_range_ls[ind] = [hist_border_foreign_player[ind * 2] + ind_r * (
                hist_border_foreign_player[ind * 2 + 1] - hist_border_foreign_player[ind * 2]) / 10. for ind_r in range(10)]

        str_line = ''
        for ind2 in xrange(10):
            for ind1 in xrange(4):
                str_line += (str(country_player_range_ls[ind1][ind2]) + '\t')
                str_line += (str(country_player_hist_res_ls[ind1][ind2]) + '\t')
                str_line += (str(foreign_player_range_ls[ind1][ind2]) + '\t')
                str_line += (str(foreign_player_hist_res_ls[ind1][ind2]) + '\t')
            str_line += '\n'
        f.write(str_line)




def write_data_global(file_name, country_player_age_data_ls, foreign_player_age_data_ls, max_min_str_country_player_age_data_ls, max_min_str_foreign_player_age_data_ls):
    with open(file_name, 'w') as f:
        for ind in xrange(len(years)):
            line_str = ''
            line_str += str(years[ind]) + '\t'
            #f.write(str(years[ind]) + '\t')
            for ind2 in xrange(0, 8, 2):
                #f.write(str(country_player_age_data_ls[ind][ind2] / country_player_age_data_ls[ind][ind2 + 1]) + '\t')
                #f.write(str(foreign_player_age_data_ls[ind][ind2] / foreign_player_age_data_ls[ind][ind2 + 1]) + '\t')
                try:
                    line_str += str(country_player_age_data_ls[ind][ind2] / country_player_age_data_ls[ind][ind2 + 1]) + '\t' if country_player_age_data_ls[ind][ind2 + 1] > 0 else 0
                    line_str += str(foreign_player_age_data_ls[ind][ind2] / foreign_player_age_data_ls[ind][ind2 + 1]) + '\t' if foreign_player_age_data_ls[ind][ind2 + 1] > 0 else 0
                except:
                    a = 0

            for ind2 in xrange(0, 16, 4):
                #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(1, 16, 4):
                #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(2, 16, 4):
                #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(3, 16, 4):
                #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'
            line_str += '\n'
            f.write(unicode(line_str, 'utf-8'))


def write_team_data_global(file_name, country_player_age_data_withteam_dic, foreign_player_age_data_withteam_dic, max_min_str_country_player_age_data_withteam_dic, max_min_str_foreign_player_age_data_withteam_dic):
    with open(file_name, 'w') as f:
        for ind in xrange(len(years)):
            line_str = ''
            line_str += str(years[ind]) + '\t'
            #f.write(str(years[ind]) + '\t')
            for ind2 in xrange(0, 8, 2):
                for key in country_player_age_data_withteam_dic.keys():
                    country_player_age_data_ls = country_player_age_data_withteam_dic[key]
                    foreign_player_age_data_ls = foreign_player_age_data_withteam_dic[key]
                    #f.write(str(country_player_age_data_ls[ind][ind2] / country_player_age_data_ls[ind][ind2 + 1]) + '\t')
                    #f.write(str(foreign_player_age_data_ls[ind][ind2] / foreign_player_age_data_ls[ind][ind2 + 1]) + '\t')
                    line_str += str(country_player_age_data_ls[ind][ind2] / max(1, country_player_age_data_ls[ind][ind2 + 1])) + '\t'
                    line_str += str(foreign_player_age_data_ls[ind][ind2] / max(1, foreign_player_age_data_ls[ind][ind2 + 1])) + '\t'

            for ind2 in xrange(0, 16, 4):
                for key in country_player_age_data_withteam_dic.keys():
                    country_player_age_data_ls = country_player_age_data_withteam_dic[key]
                    foreign_player_age_data_ls = foreign_player_age_data_withteam_dic[key]
                    #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                    #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                    line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                    line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(1, 16, 4):
                for key in country_player_age_data_withteam_dic.keys():
                    country_player_age_data_ls = country_player_age_data_withteam_dic[key]
                    foreign_player_age_data_ls = foreign_player_age_data_withteam_dic[key]
                    #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                    #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                    line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                    line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(2, 16, 4):
                for key in country_player_age_data_withteam_dic.keys():
                    country_player_age_data_ls = country_player_age_data_withteam_dic[key]
                    foreign_player_age_data_ls = foreign_player_age_data_withteam_dic[key]
                    #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                    #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                    line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                    line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'

            for ind2 in xrange(3, 16, 4):
                for key in country_player_age_data_withteam_dic.keys():
                    country_player_age_data_ls = country_player_age_data_withteam_dic[key]
                    foreign_player_age_data_ls = foreign_player_age_data_withteam_dic[key]
                    #f.write(str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t')
                    #f.write(str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t')
                    line_str += str(max_min_str_country_player_age_data_ls[ind][ind2]) + '\t'
                    line_str += str(max_min_str_foreign_player_age_data_ls[ind][ind2]) + '\t'
            line_str += '\n'
            f.write(unicode(line_str, 'utf-8'))

def write_scatter_data(file_name, country_scatter_data_wh, foreign_scatter_data_wh):
    with open(file_name, 'w') as f:
        str_v = ''
        for ind in xrange(len(country_scatter_data_wh)):
            for ind3 in xrange(2):
                for ind2 in xrange(len(country_scatter_data_wh[ind])):
                    str_v += (str(country_scatter_data_wh[ind][ind2][ind3]) + '\t')
                str_v += '\n'

        for ind in xrange(len(foreign_scatter_data_wh)):
            for ind3 in xrange(2):
                for ind2 in xrange(len(foreign_scatter_data_wh[ind])):
                    str_v += (str(foreign_scatter_data_wh[ind][ind2][ind3]) + '\t')
                str_v += '\n'

        f.write(str_v)

#match_time  match_score match_2score_valid match_2score_total match_3score_valid match_3score_total match_punish_valid
#match_punish_total borad_num front_borad_num back_borad_num assist_num catch_num slam_dunk_num nut_cap_num
#break_the_rules miss_num

if __name__ == '__main__':
    all_ls = [['match_time', 'match_score', 'scatter_match_time_score.xls', 'match_time_hist.xls', 'match_time.xls', 'match_score_hist.xls', 'match_score.xls'],
    ['match_2score_total', 'match_2score_valid', 'scatter_match_2score.xls', 'match_2score_total_hist.xls', 'match_2score_total.xls', 'match_2score_valid_hist.xls', 'match_2score_valid.xls'],
    ['match_3score_total', 'match_3score_valid', 'scatter_match_3score.xls', 'match_3score_total_hist.xls', 'match_3score_total.xls', 'match_3score_valid_hist.xls', 'match_3score_valid.xls'],
    ['match_punish_total', 'match_punish_valid', 'scatter_match_punish_score.xls', 'match_punish_total_hist.xls', 'match_punish_total.xls', 'match_punish_valid_hist.xls', 'match_punish_valid.xls'],
    ['match_time', 'borad_num', 'scatter_match_time_borad_num.xls', 'match_time_borad_num_hist.xls',
     'match_time_num.xls', 'borad_num_hist.xls', 'borad_num.xls'],
    ['front_borad_num', 'back_borad_num', 'scatter_front_back_borad_num.xls', 'front_borad_num_hist.xls',
     'front_borad_num.xls', 'back_borad_num_hist.xls', 'back_borad_num.xls'],
    ['match_time', 'assist_num', 'scatter_match_time_assist_num.xls', 'match_time_assist_num_hist.xls',
    'match_time_assist_num.xls', 'assist_num_hist.xls', 'assist_num.xls'],
    ['match_time', 'catch_num', 'scatter_match_time_catch_num.xls', 'match_time_catch_num_hist.xls',
    'match_time_catch_num.xls', 'catch_num_hist.xls', 'catch_num.xls'],
    ['match_time', 'slam_dunk_num', 'scatter_match_time_slam_dunk_num.xls', 'match_time_slam_dunk_num_hist.xls',
    'match_time_slam_dunk_num.xls', 'slam_dunk_num_hist.xls', 'slam_dunk_num.xls'],
    ['match_time', 'nut_cap_num', 'scatter_match_time_nut_cap_num.xls', 'match_time_nut_cap_num_hist.xls',
    'match_time_nut_cap_num.xls', 'nut_cap_num_hist.xls', 'nut_cap_num.xls'],
    ['match_time', 'break_the_rules', 'scatter_match_time_break_the_rules.xls', 'match_time_break_the_rules_hist.xls',
    'match_time_break_the_rules.xls', 'break_the_rules_hist.xls', 'break_the_rules.xls'],
    ['match_time', 'miss_num', 'scatter_match_time_miss_num.xls', 'match_time_miss_num_hist.xls',
    'match_time_miss_num.xls', 'miss_num_hist.xls', 'miss_num.xls']
    ]
    for v_info in all_ls:
        key1 = v_info[0]
        key2 = v_info[1]
        scatter_file_path = v_info[2]
        hist_file_path1 = v_info[3]
        all_file_path1 = v_info[4]
        hist_file_path2 = v_info[5]
        all_file_path2 = v_info[6]

        country_scatter_data_time_score, foreign_scatter_data_time_score = get_scatter_data(key1, key2)
        write_scatter_data(scatter_file_path, country_scatter_data_time_score, foreign_scatter_data_time_score)

        country_player_match_score_ls, foreign_player_match_score_ls, max_min_str_country_player_match_score_ls, max_min_str_foreign_player_match_score_ls = get_key_data_according_foreign_aid_for_05_16(
            key1)
        write_hist_global(hist_file_path1, key1, max_min_str_country_player_match_score_ls,
                          max_min_str_foreign_player_match_score_ls)
        write_data_global(all_file_path1, country_player_match_score_ls, foreign_player_match_score_ls, max_min_str_country_player_match_score_ls, max_min_str_foreign_player_match_score_ls)

        country_player_match_score_ls, foreign_player_match_score_ls, max_min_str_country_player_match_score_ls, max_min_str_foreign_player_match_score_ls = get_key_data_according_foreign_aid_for_05_16(
            key2)
        write_hist_global(hist_file_path2, key2, max_min_str_country_player_match_score_ls,
                          max_min_str_foreign_player_match_score_ls)
        write_data_global(all_file_path2, country_player_match_score_ls, foreign_player_match_score_ls,
                          max_min_str_country_player_match_score_ls, max_min_str_foreign_player_match_score_ls)




    '''
    country_player_age_data_ls, foreign_player_age_data_ls, max_min_str_country_player_age_data_ls, max_min_str_foreign_player_age_data_ls = get_key_data_according_foreign_aid_for_05_16('birth')
    country_player_height_data_ls, foreign_player_height_data_ls, max_min_str_country_player_height_data_ls, max_min_str_foreign_player_height_data_ls = get_key_data_according_foreign_aid_for_05_16('height')
    country_player_weight_data_ls, foreign_player_weight_data_ls, max_min_str_country_player_weight_data_ls, max_min_str_foreign_player_weight_data_ls = get_key_data_according_foreign_aid_for_05_16('weight')
    country_player_ktl_data_ls, foreign_player_ktl_data_ls, max_min_str_country_player_ktl_data_ls, max_min_str_foreign_player_ktl_data_ls = get_key_data_according_foreign_aid_for_05_16(
        'ktl')

    country_player_age_data_withteam_dic, foreign_player_age_data_withteam_dic, max_min_str_country_player_age_data_withteam_dic, max_min_str_foreign_player_age_data_withteam_dic = {}, {}, {}, {}
    country_player_height_data_withteam_dic, foreign_player_height_data_withteam_dic, max_min_str_country_player_height_data_withteam_dic, max_min_str_foreign_player_height_data_withteam_dic = {}, {}, {}, {}
    country_player_weight_data_withteam_dic, foreign_player_weight_data_withteam_dic, max_min_str_country_player_weight_data_withteam_dic, max_min_str_foreign_player_weight_data_withteam_dic = {}, {}, {}, {}
    country_player_ktl_data_withteam_dic, foreign_player_ktl_data_withteam_dic, max_min_str_country_player_ktl_data_withteam_dic, max_min_str_foreign_player_ktl_data_withteam_dic = {}, {}, {}, {}

    for team_name in all_team_name:
        country_player_age_data_withteam_dic[team_name], foreign_player_age_data_withteam_dic[team_name], \
        max_min_str_country_player_age_data_withteam_dic[team_name], max_min_str_foreign_player_age_data_withteam_dic[team_name]\
            = get_key_data_according_foreign_aid_for_05_16('birth', team_name)

        country_player_height_data_withteam_dic[team_name], foreign_player_height_data_withteam_dic[team_name], \
        max_min_str_country_player_height_data_withteam_dic[team_name], max_min_str_foreign_player_height_data_withteam_dic[team_name]\
            = get_key_data_according_foreign_aid_for_05_16(
            'height', team_name)

        country_player_weight_data_withteam_dic[team_name], foreign_player_weight_data_withteam_dic[team_name], \
        max_min_str_country_player_weight_data_withteam_dic[team_name], \
        max_min_str_foreign_player_weight_data_withteam_dic[team_name] = get_key_data_according_foreign_aid_for_05_16(
            'weight', team_name)

        country_player_ktl_data_withteam_dic[team_name], foreign_player_ktl_data_withteam_dic[team_name], \
        max_min_str_country_player_ktl_data_withteam_dic[team_name], \
        max_min_str_foreign_player_ktl_data_withteam_dic[team_name] = get_key_data_according_foreign_aid_for_05_16(
            'ktl', team_name)

    

    write_hist_global('ktl_hist.xls', 'ktl', max_min_str_country_player_ktl_data_ls, max_min_str_foreign_player_ktl_data_ls)
    write_hist_global('age_hist.xls', 'birth', max_min_str_country_player_age_data_ls, max_min_str_foreign_player_age_data_ls)
    write_hist_global('height_hist.xls', 'height', max_min_str_country_player_height_data_ls, max_min_str_foreign_player_height_data_ls)
    write_hist_global('weight_hist.xls', 'weight', max_min_str_country_player_weight_data_ls, max_min_str_foreign_player_weight_data_ls)

    write_data_global('ktl.xls', country_player_ktl_data_ls, foreign_player_ktl_data_ls, max_min_str_country_player_ktl_data_ls, max_min_str_foreign_player_ktl_data_ls)
    write_data_global('age.xls', country_player_age_data_ls, foreign_player_age_data_ls, max_min_str_country_player_age_data_ls, max_min_str_foreign_player_age_data_ls)
    write_data_global('height.xls', country_player_height_data_ls, foreign_player_height_data_ls, max_min_str_country_player_height_data_ls, max_min_str_foreign_player_height_data_ls)
    write_data_global('weight.xls', country_player_weight_data_ls, foreign_player_weight_data_ls, max_min_str_country_player_weight_data_ls, max_min_str_foreign_player_weight_data_ls)

    write_team_data_global('age_team.xls', country_player_age_data_withteam_dic, foreign_player_age_data_withteam_dic, max_min_str_country_player_age_data_withteam_dic, max_min_str_foreign_player_age_data_withteam_dic)
    write_team_data_global('height_team.xls', country_player_height_data_withteam_dic, foreign_player_height_data_withteam_dic, max_min_str_country_player_height_data_withteam_dic, max_min_str_foreign_player_height_data_withteam_dic)
    write_team_data_global('weight_team.xls', country_player_weight_data_withteam_dic, foreign_player_height_data_withteam_dic, max_min_str_country_player_weight_data_withteam_dic, max_min_str_foreign_player_height_data_withteam_dic)
    '''
    a = 0