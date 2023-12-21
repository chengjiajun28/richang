import time
import dateparser


def get_microsecond():
    return int(round(time.time() * 1000))


def get_second():
    return int(round(time.time()))


def timestamp_to_y_m_d_H_M_S(second):
    try:
        time_local = time.localtime(second)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    except Exception as err:
        return ""


def str_to_y_m_d_H_M_S(date_string):
    parttern = "%Y-%m-%d %H:%M:%S"
    try:
        date = dateparser.parse(date_string)
        return date.strftime(parttern)
    except Exception as err:
        return ""



def date_parse(date_string):
    try:
        return dateparser.parse(date_string)
    except Exception as err:
        return None