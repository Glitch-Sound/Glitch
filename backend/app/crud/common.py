from datetime import datetime, timedelta
from enum import Enum
import pytz


class ItemType(Enum):
    PROJECT = 1
    EVENT   = 2
    FEATURE = 3
    STORY   = 4
    TASK    = 5
    BUG     = 6

class ItemState(Enum):
    IDLE     = 1
    RUN      = 2
    ALERT    = 3
    REVIEW   = 4
    COMPLETE = 5

class ExtractType(Enum):
    INCOMPLETE   =  1
    ALL          =  2
    HIGH_RISK    =  3
    ALERT        =  4
    ASSIGNMENT   =  5
    RELATION     =  6
    SEARCH       =  7
    ANCESTOR     = 11
    SUMMARY_USER = 21

class TaskType(Enum):
    WORKLOAD = 1
    NUMBER   = 2

class WorkloadType(Enum):
    WITHIN_AN_HOUR    =  1
    WITHIN_HALF_A_DAY =  3
    WITHIN_A_DAY      =  7
    WITHIN_2_DAYS     = 14
    WITHIN_3_DAYS     = 21
    WITHIN_A_WEEK     = 35

class RiskType(Enum):
    NONE  = 0
    LIMIT = 1
    OVER  = 9


def generate_bigrams(text):
    if not text:
        return ''
    text = text.replace(' ', '')
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    return ' '.join(bigrams)


def get_date_previous():
    current_utc_time = datetime.now(pytz.timezone('Asia/Tokyo'))
    previous_date_time = current_utc_time - timedelta(days=1)
    previous_date = previous_date_time.strftime('%Y-%m-%d')
    return previous_date


def get_date_current():
    current_utc_time = datetime.now(pytz.timezone('Asia/Tokyo'))
    current_date = current_utc_time.strftime('%Y-%m-%d')
    return current_date


def get_datetime_current():
    current_utc_time = datetime.now(pytz.timezone('Asia/Tokyo'))
    current_datetime = current_utc_time.strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime
