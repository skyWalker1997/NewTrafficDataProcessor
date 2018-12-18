import re
from os import listdir

__DATA_FOLDER__ = '/Users/PINKFLOYD/Desktop/graduatedesign/NewTrafficDataProcessor/Data/Up_Down_Data_Origin/'
__OUT_FOLDER__ = '/Users/PINKFLOYD/Desktop/graduatedesign/NewTrafficDataProcessor/Data/Up_Down_Data_Midput/'

def file_path():
    """处理每天和每个时段的上下车文件"""
    file = []
    info = listdir(__DATA_FOLDER__)
    filelistlenth = len(info)
    for i in range(filelistlenth):
        day_timeslot_dict = {}
        day_dict_arr = []
        filename = info[i]
        file_date = filename.split('_')[1]
        file_geo_slot = filename.split('_')[2]
        file_u_d = filename.split('_')[3].strip('.txt')
        # data = read_data_in_line(__DATA_FOLDER__+filename)
        # poi = data_zip(data)
        # day_timeslot_dict = data_count(poi,day_timeslot_dict,file_date)
        # day_arr = dict_zip(day_timeslot_dict, day_dict_arr)

def read_data_in_line(DATA_PATH):
    data = []
    for line in open(DATA_PATH,'r',encoding='utf-8'): #设置文件对象并读取每一行文件
        line = line[:-1]
        data.append(line)               #将每一行文件加入到list中
    return data


def data_zip(data):
    poi = []
    for data_in_line in data:
        data_in_line = re.split('\t',data_in_line)
        i = 1
        temp_dict = {}
        for temp_data in data_in_line:
            if i != 5 and i!= 6:
                temp_dict[i] = temp_data
                i = i+1
            else:
                i = i+1

        len = ("%.5f" % len_calculate(temp_dict))
        temp_dict['len'] = str(len)
        poi.append(temp_dict)
    # print(poi)
    return poi

if __name__ == '__main__':
    print(123)
    # file_path()