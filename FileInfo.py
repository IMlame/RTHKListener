import sys
import os


def get_file_index(file):
    return get_file_data(file, 0)

def get_file_date(file):
    return get_file_data(file, 1)


def get_file_data(file, data_type):
    # example file name: 0-20220326-radio2-letthemusicspeak.wav
    # datatype - 0: index, 1: date, 2: radio, 3: title
    a = file[0:-4].split("-")
    if data_type == 0:
        return int(a[data_type])
    return a[data_type]

def get_files_in_directory(path: str):
    # find all audio files
    return [f for f in os.listdir(path) if not f.startswith('.')]


def get_oldest_file(path: str):
    file_name = ""
    min_distance = sys.maxsize

    for file in get_files_in_directory(path):
        file_index = get_file_index(file)
        if (file_index < min_distance):
            file_name = file
            min_distance = file_index

    return file_name


def get_newest_file_name(path: str):
    file_name = ""
    largest_num = -1

    for file in get_files_in_directory(path):
        file_index = get_file_index(file)
        if (file_index > largest_num):
            file_name = file
            largest_num = file_index

    return file_name
