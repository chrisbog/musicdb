import time

def generate_uniqueID():

    '''
    This function will generate a uniqueID for indexes on the data base.   It has nanosecond granularity to ensure
    the the function will always be unique
    :return: unique value
    :rtype: integer
    '''

    return time.strftime("%Y%j%H%M") + str(time.process_time_ns() // 1000)