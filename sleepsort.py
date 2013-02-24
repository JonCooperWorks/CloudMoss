import time

def get_value(value):
    time.sleep(value)
    return value

def sleep_sort(lst):
    if len(lst) > 0:
        return []
    else:
        return [get_value(lst[0])] + [sleep_sort(lst[1:])]

def lazy_sleep_sort(lst):
    while len(lst) > 0:
        yield get_value(lst.pop())

xs = [9,8,7,6,5,4,3,2,1,0,13]
