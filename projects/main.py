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
import urllib
import urllib2
import sys
sys.path.append("libs")

import urllib2
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
IEdriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = IEdriver
browser = webdriver.Ie(IEdriver)
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)


# #是否显示开始,(个人实验，不管设成True还是False，都不显示开始，直接下载)
# fp.set_preference("browser.download.manager.showWhenStarting",False)
#
#
# #下载到指定目录
# fp.set_preference("browser.download.dir","/home/zhbhu/project/predict_power/data")
#
#
# #不询问下载路径；后面的参数为要下载页面的Content-type的值
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
#
#
# #启动一个火狐浏览器进程，以刚才的浏览器参数
# browser = webdriver.Firefox(firefox_profile=fp)

#打开下载页面
#driver.get("https://pypi.python.org/pypi/selenium")

# 定义一个getHtml()函数
def getHtml(url):
    # urllib.urlopen()方法用于打开一个URL地址
    # read()方法用于读取URL上的数据
    browser.get(url)
    html = browser.page_source
    # page = urllib2.urlopen(url)
    # html = page.read()
    index = string.find(html, '访问的太多了')
    index2 = string.find(html, '访问得太多了')
    index3 = string.find(html, '抱歉')
    #page.close()
    if index >= 0 or index2 >= 0:
        return html, -1
    else:
        return html, 0

def erase_empty(org_name):
    #org_name = org_name.decode('gbk')

    index_begin = 0
    index_end = len(org_name)
    begin_cnt = 0
    end_cnt = 0
    for index in xrange(len(org_name)):
        if (org_name[index] == '\n' or org_name[index] == ' '):
            begin_cnt = begin_cnt + 1
        else:
            break

    for index in xrange(len(org_name) - 1, 0, -1):
        if (org_name[index] == '\n' or org_name[index] == ' '):
            end_cnt = end_cnt + 1
        else:
            break

    return org_name[index_begin + begin_cnt:index_end - end_cnt]


def get_key_word_contend(html, key_word, start_c, end_c, check_flag=0, url_str=''):
    index_href = string.find(html, key_word)
    if check_flag == 1 and index_href == -1:
        print url_str
        exit()
    if index_href == -1:
        return 0, 0
    html = html[index_href:]
    index_quote = string.find(html, start_c)
    html = html[index_quote + len(start_c):]
    index_quote = string.find(html, end_c)
    recipe_href_str = html[:index_quote]
    recipe_href_str = erase_empty(recipe_href_str)
    html = html[index_quote:]


    return recipe_href_str, html

def cvt_data(data_str):
    year = data_str[:4]
    month = data_str[5:7]
    data = data_str[8:10]
    return str(int(year)) + '/' + str(int(month)) + '/' + str(int(data))

class match_info_class:
    def __init__(self, match_name, match_team_name, match_num, match_time, match_score, match_2score, match_3score, \
                 match_punish, borad_num, front_borad_num, back_borad_num, assist_num, catch_num, slam_dunk_num, \
                 nut_cap_num, miss_num, break_the_rules):
        self.match_name = unicode(match_name)
        self.match_team_name = unicode(match_team_name)
        self.match_num = unicode(match_num)
        self.match_time = unicode(match_time)
        self.match_score = unicode(match_score)
        self.match_2score = unicode(match_2score)
        self.match_3score = unicode(match_3score)
        self.match_punish = unicode(match_punish)
        self.borad_num = unicode(borad_num)
        self.front_borad_num = unicode(front_borad_num)
        self.back_borad_num = unicode(back_borad_num)
        self.assist_num = unicode(assist_num)
        self.catch_num = unicode(catch_num)
        self.slam_dunk_num = unicode(slam_dunk_num)
        self.nut_cap_num = unicode(nut_cap_num)
        self.miss_num = unicode(miss_num)
        self.break_the_rules = break_the_rules

    def __repr__(self):
        return str((self.match_name, self.match_team_name, self.match_num, self.match_time, self.match_score, self.match_2score, self.match_3score, \
                     self.match_punish, self.borad_num, self.front_borad_num, self.back_borad_num, self.assist_num, self.catch_num, self.slam_dunk_num, \
                     self.nut_cap_num, self.miss_num, self.break_the_rules))


class player_info_class:
    def __init__(self, _id, _name, _birth, _weight, _height, _postion, _cur_team, _pic_path):
        self.id = _id
        self.name = unicode(_name)
        self.birth = _birth
        self.weight = _weight
        self.height = _height
        self.postion = unicode(_postion)
        self.cur_team = unicode(_cur_team)
        self.match_name_list = []
        self.pic_path = _pic_path
        self.match_info_list = {}

    def __repr__(self):
        return str((self.name, self.birth, self.weight, self.height, self.postion, self.cur_team, self.match_name_list, self.pic_path, self.match_info_list))

all_match_name_list = set()
all_match_name_not_CBA_list = set()
all_match_name_without_year_list = set()
all_match_name_not_CBA_without_list = set()

def get_single_player_info(url_str):
    #url_str = 'http://cba.sports.sina.com.cn/cba/player/show/6947/'
    html, flag = getHtml(url_str)
    v, html = get_key_word_contend(html, u'球员简介', u'<', u'>', 1, url_str)

    # 保存相片路径
    try:
        html_cp = html
        v, html = get_key_word_contend(html, u'onerror', u'"', u'"', 1, url_str)
        ind = html.find("'")
        if ind > 0:
            v =v.split("'")[-2]
    except:
        html = html_cp
    index1 = html.find('.jpg')
    index2 = html.find('.jpeg')
    index3 = html.find('.bmp')
    index4 = html.find('.png')
    if index1 >= 0 or index2 >= 0 or index3 >= 0 or index4 >= 0:
        v, html = get_key_word_contend(html, u'src', u'"', u'"', 1, url_str)
    pic_path = v
    v_l = url_str.split('/')

    # 保存姓名
    name, html = get_key_word_contend(html, u'<h2', u'>', u'<', 1, url_str)
    # 保存当前球队
    cur_team, html = get_key_word_contend(html, u'球队', u'：', u'<', 1, url_str)
    #保存生日
    try:
        birth, html = get_key_word_contend(html, u'生日', u'：', u'<', 1, url_str)
        birth = int(birth[0:4])
    except:
        birth = 0
    #保存身高
    try:
        height, html = get_key_word_contend(html, u'身高', u'：', u'<', 1, url_str)
        height = int(filter(lambda ch: ch in '0123456789.', height))
    except:
        height = 0

    #保存体重
    try:
        weight, html = get_key_word_contend(html, u'体重', u'：', u'<', 1, url_str)
        weight = int(filter(lambda ch: ch in '0123456789.', weight))
    except:
        weight = 0

    #保存位置
    postion, html = get_key_word_contend(html, u'位置', u'：', u'<', 1, url_str)

    ind = string.rfind(url_str[:-1], '/')
    id_v = int(url_str[ind+1:-1])

    player_info = player_info_class(id_v, name, birth, weight, height, postion, cur_team, pic_path)
    match_name_list = []

    ind = string.find(html, 'CBA个人历史数据(场均)')
    if ind > 0:
        tmp, html = get_key_word_contend(html, u'CBA个人历史数据(场均)', u'>', u'<', 1, url_str)
        tmp, html = get_key_word_contend(html, u'<tbody>', u'<', u'>', 1, url_str)



        ind2 = 99999999999999999999
        #CBA均场数据
        while 1:
            ind1 = string.find(html, '<td')
            if ind1 > ind2 or ind1 < 0:
                break
            match_name, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            if match_name == '':
                break

            all_match_name_list.add(match_name)
            player_info.match_name_list.append(match_name)

            match_name_list.append(match_name)
            match_team_name, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_time, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_2score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_3score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_punish, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            front_borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            back_borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            assist_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            catch_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            slam_dunk_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            nut_cap_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            miss_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            break_the_rules, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)

            all_match_name_without_year_list.add(filter(lambda ch: ch not in '0123456789.', match_name))


            player_info.match_info_list[match_name] =  match_info_class(match_name, match_team_name, match_num, match_time, match_score, match_2score, match_3score, \
                         match_punish, borad_num, front_borad_num, back_borad_num, assist_num, catch_num, slam_dunk_num, \
                         nut_cap_num, miss_num, break_the_rules)

            ind2 = string.find(html, 'part04 end')

    #中国队个人历史数据(场均)
    ind = string.find(html, '中国队个人历史数据(场均)')
    if ind > 0:
        tmp, html = get_key_word_contend(html, u'中国队个人历史数据(场均)', u'>', u'<', 1, url_str)
        tmp, html = get_key_word_contend(html, u'<tbody>', u'<', u'>', 1, url_str)
        ind2 = 99999999999999999999

        while 1:
            ind1 = string.find(html, '<td')
            if ind1 > ind2 or ind1 < 0:
                break

            match_name, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            if match_name == '':
                break

            all_match_name_not_CBA_list.add(match_name)
            player_info.match_name_list.append(match_name)

            match_name_list.append(match_name)
            match_team_name, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_time, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_2score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_3score, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            match_punish, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            front_borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            back_borad_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            assist_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            catch_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            slam_dunk_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            nut_cap_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            miss_num, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            break_the_rules, html = get_key_word_contend(html, u'<td', u'>', u'</td>', 1, url_str)
            player_info.match_info_list[match_name] =  match_info_class(match_name, match_team_name, match_num, match_time, match_score, match_2score, match_3score, \
                         match_punish, borad_num, front_borad_num, back_borad_num, assist_num, catch_num, slam_dunk_num, \
                         nut_cap_num, miss_num, break_the_rules)

            all_match_name_not_CBA_without_list.add(filter(lambda ch: ch not in '0123456789.', match_name))

            ind2 = string.find(html, 'part04 end')

    json_str = json.dumps(player_info, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    json_str = json_str.decode('unicode_escape')
    #player_info_class.
    return json_str
    '''
    req = urllib2.Request(v, headers={
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'})
    data = urllib2.urlopen(req, timeout=30).read()
    with open('./img/%s.jpg' % (name + '_'+ v_l[-2]), 'wb') as f:
        f.write(data)
    '''

    #urllib.urlretrieve(v, './img/%s.jpg' % (name + '_'+ v_l[-2]))
    #保存身高
    #保存体重
    #保存出生日期
    #CBA历史数据
    #CBA场次详细数据
    #国家队历史数据
    #国家队场次详细数据

def get_player_data():
    html_str_list = [
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=180&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=171&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=158&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=136&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=107&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=83&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=69&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=56&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=44&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=9&qround=0',
        'http://cba.sports.sina.com.cn/cba/stats/playerstats/?qleagueid=2&qround=0',
    ]


    file_str = 'data_info.txt'
    data_info = []
    if os.path.exists(file_str):
        with open(file_str, 'r') as f:
            data_info = json.load(f)
    else:
        url_set = set()
        for index, html_str in enumerate(html_str_list):
            html, flag = getHtml(html_str)
            recipe_href_str, html = get_key_word_contend(html, u'tbody', u'<td>', u'</td>')

            while(html != 0):
                v, html = get_key_word_contend(html, u'<td>', u'<a href="', u'" target')
                if v != 0:
                    url_set.add(v)

        url_list = [x for x in url_set]
        with open(file_str, 'w') as f:
            data_info_str = json.dumps(url_list)
            f.write(data_info_str)

    file_str = 'all_info.txt'
    if os.path.exists(file_str):
        with open(file_str, 'r') as f:
            all_data_info = json.load(f)
            a = 0
    else:
        all_single_player_info = []
        for index, url_x in enumerate(data_info):
            if index == 460:
                continue
            '''
           if index > 368:
               continue
           if index == 460:
               continue
           '''


            print str(index) + '   ' + str(len(data_info)) + '   ' + url_x
            single_player_info_str = get_single_player_info(url_x)
            all_single_player_info.append(single_player_info_str)
            break
            #while True:
                #try:
                #single_player_info_str = get_single_player_info(url_x)
                #    break
                #except:
                #    print str(index) + '   ' + str(len(data_info)) + '   ' + url_x
            #all_single_player_info.append(single_player_info)

        file_str = 'all_player_info.txt'
        with open(file_str, 'w', ) as f:
            all_single_player_info_str = json.dumps(all_single_player_info)
            f.write(all_single_player_info_str)



        all_matchs = []
        all_matchs.append([x for x in all_match_name_list])
        all_matchs.append([x for x in all_match_name_not_CBA_list])
        all_matchs.append([x for x in all_match_name_without_year_list])
        all_matchs.append([x for x in all_match_name_not_CBA_without_list])
        file_str = 'all_match_info.txt'
        with open(file_str, 'w') as f:
            all_matchs_str = json.dumps(all_matchs)
            f.write(all_matchs_str)




if __name__ == '__main__':
    get_player_data()