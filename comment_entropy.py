#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: comment_entropy.py
#Author: yuxuan
#Created Time: 2016-07-31 09:59:49
############################

from draw_data import draw_data
import numpy as np
from matplotlib import pyplot as plt
import logging
import multiprocessing
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def func(begin_time, end_time):
    each_count = []
    mydraw = draw_data()
    title_item = mydraw.get_title_data(str(begin_time), str(end_time), 0)
    for ti in title_item:
        each_count.append(mydraw.title_comment_count(ti['_id']))
    entropy_i = 0.0
    for count_i in each_count:
        pro_count = 1.0*count_i/np.sum(each_count)
        if pro_count != 0:
            entropy_i += ( -pro_count*np.log2(pro_count) )
    mydraw.close_db()
    logging.info(begin_time)
    return entropy_i

def entropy():
    import datetime
    entropy_day = []
    result_func = []
    mydraw = draw_data()
    begin_time = datetime.datetime.strptime('2015-09-25', '%Y-%m-%d')
    end_time = datetime.datetime.strptime('2015-09-26', '%Y-%m-%d')
    pool = multiprocessing.Pool(processes=8)
    for i in range(60): 
        result_func.append( pool.apply_async(func, (begin_time, end_time, )) )
        begin_time = end_time
        end_time = end_time + datetime.timedelta(days = 1)
    pool.close()
    pool.join()
    for res in result_func:
        if res.get()<1:
            entropy_day.append(4.0)
        else:
            entropy_day.append(res.get())
    print entropy_day
    plt.plot(entropy_day)
    plt.show()

if __name__ == "__main__":
    entropy()
