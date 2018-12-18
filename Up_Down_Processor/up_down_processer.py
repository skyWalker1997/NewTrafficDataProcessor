import re
from os import listdir
from geopy.distance import geodesic
from Up_Down_Processor import time_format_exchange as tfe
import numpy as np

time_slot_arr_stan = ['0601', '0602', '0701', '0702', '0801', '0802', '0901', '0902', '1001', '1002', '1101', '1102', '1201', '1202', '1301', '1302', '1401', '1402', '1501', '1502', '1601', '1602', '1701', '1702', '1801', '1802', '1901', '1902', '2001', '2002', '2101', '2102', '2201', '2202']


__DATA_FOLDER__ = '/Users/PINKFLOYD/Desktop/graduatedesign/NewTrafficDataProcessor/Data/Up_Down_Data_Origin/'
__OUT_FOLDER__ = '/Users/PINKFLOYD/Desktop/graduatedesign/NewTrafficDataProcessor/Data/Up_Down_Data_Midput/'

def file_path():
    """处理每天和每个时段的上下车文件"""
    file = []
    info = listdir(__DATA_FOLDER__)
    filelistlenth = len(info)
    for i in range(filelistlenth):
        filename = info[i]
        file_date = filename.split('_')[1]
        file_geo_slot = filename.split('_')[2]
        file_u_d = filename.split('_')[3].strip('.txt')
        data = read_data_in_line(__DATA_FOLDER__+filename)
        poi,len_poi = data_zip(file_date,data,file_u_d)
        day_dict = data_count(poi)
        day_dict_complete = data_complete(day_dict,file_date)
        out_put(day_dict_complete,file_date,filename)

def read_data_in_line(DATA_PATH):
    data = []
    for line in open(DATA_PATH,'r',encoding='utf-8'): #设置文件对象并读取每一行文件
        line = line[:-1]
        data.append(line)               #将每一行文件加入到list中
    return data


def data_zip(file_date,data,file_u_d):

    poi = []
    for data_in_line in data:
        temp_dict = {}
        data_in_line = re.split('\t',data_in_line)
        if file_u_d == 'up':
            if time_slot_judge(file_date,data_in_line[6]) == None:
                pass
            else:
                temp_dict['time_slot'] = time_slot_judge(file_date,data_in_line[6])
                temp_dict['len'] = float("%.5f" % len_calculate(data_in_line[2], data_in_line[3]))
                poi.append(temp_dict)
        else:
            if time_slot_judge(file_date, data_in_line[7]) == None:
                pass
            else:
                temp_dict['time_slot'] =  time_slot_judge(file_date,data_in_line[7])
                temp_dict['len'] = float("%.5f" % len_calculate(data_in_line[2],data_in_line[3]))
                poi.append(temp_dict)
    return poi,len(poi)

def len_calculate(start_geo,end_geo):
    '''Calculate the length'''
    # print(temp_dict)
    gps_start = re.split(',',start_geo)
    gps_end = re.split(',',end_geo)
    lon1 = gps_start[0]
    lat1 = gps_start[1]
    lon2 = gps_end[0]
    lat2 = gps_end[1]
    len = geodesic((lat1,lon1), (lat2,lon2)).km
    return len

def time_slot_judge(file_date,str_time):
    '''judge the timesolot'''
    day,time  = tfe.date_split(str_time)
    HH,MM = tfe.time_split(time)
    if int(HH) > 22 or int(HH) < 6:
        return None
    else:
        if MM / 30 >= 1:
            return file_date+HH+'02'
        else:
            return file_date + HH + '01'

def data_count(poi):
    day_dict = {}
    for record in poi:
        temp_arr = []
        if record['time_slot'] in day_dict.keys():
            temp_arr = day_dict[record['time_slot']]
            temp_arr.append(record['len'])
            day_dict[record['time_slot']] = temp_arr
        else:
            temp_arr.append(record['len'])
            day_dict[record['time_slot']] = temp_arr
    return day_dict



def data_complete(day_dict,file_date):
    for time_slot in time_slot_arr_stan:
        if file_date+time_slot in day_dict.keys():
            day_dict[file_date+time_slot] = distance_judge(day_dict[file_date+time_slot])
        else:
            day_dict[file_date+time_slot] = []
            day_dict[file_date+time_slot] = distance_judge(day_dict[file_date+time_slot])
    return day_dict


def distance_judge(distance_arr):
    below_5 = 0
    to_10 = 0
    to_15 = 0
    above_15 = 0
    below_5_list = []
    to_10_list = []
    to_15_list = []
    above_15_list = []
    if distance_arr.__len__() == 0:
        return 0,{'5':[0.0,0.0],'10':[0.0,0.0],'15':[0.0,0.0],'15+':[0.0,0.0]}
    length  = distance_arr.__len__()
    for len in distance_arr:
        if float(len) <= 5:
            below_5 = below_5 + 1
            below_5_list.append(float(len))
        elif float(len) > 5 and float(len) <= 10:
            to_10 = to_10 + 1
            to_10_list.append(float(len))
        elif float(len) > 10 and float(len) <= 15:
            to_15 = to_15 + 1
            to_15_list.append(float(len))
        else:
            above_15 = above_15+1
            above_15_list.append(float(len))
    below_5 = below_5/length
    below_5 = float("%.2f" % (below_5))
    if below_5_list.__len__() == 0:
        below_5_mean = 0.00
    else:
        below_5_mean = float("%.2f" % np.mean(below_5_list))
    to_10 = to_10 / length
    to_10 = float("%.2f" % (to_10))
    if to_10_list.__len__() == 0:
        to_10_mean = 0.00
    else:
        to_10_mean = float("%.2f" % np.mean(to_10_list))
    to_15 = to_15 / length
    to_15 = float("%.2f" % (to_15))
    if to_15_list.__len__() == 0:
        to_15_mean = 0.00
    else:
        to_15_mean = float("%.2f" % np.mean(to_15_list))
    above_15 = above_15 / length
    above_15 = float("%.2f" % (above_15))
    if above_15_list.__len__() == 0:
        above_15_mean = 0.00
    else:
        above_15_mean = float("%.2f" % np.mean(above_15_list))
    len_dict = {'5':[below_5,below_5_mean],'10':[to_10,to_10_mean],
                '15':[to_15,to_15_mean],'15+':[above_15,above_15_mean]}
    return length,len_dict

def out_put(day_dict,file_date,filename):
    f = open(__OUT_FOLDER__+filename, 'w')
    for time_solt in time_slot_arr_stan:
        temp = day_dict[file_date+time_solt]
        f.writelines(file_date+time_solt+'\t'+str(temp[0])+'\t'+str(temp[1])+'\n')
    f.close()


if __name__ == '__main__':
    file_path()