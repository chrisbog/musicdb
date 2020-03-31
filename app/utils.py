import time
import logging

def generate_uniqueID():

    '''
    This function will generate a uniqueID for indexes on the data base.   It has nanosecond granularity to ensure
    the the function will always be unique
    :return: unique value
    :rtype: integer
    '''
    logging.debug("Entering generate_uniqueID")
    value = time.strftime("%Y%j%H%M") + str(time.process_time_ns() // 1000)
    logging.debug(f"Unique ID='{value}'")
    return value