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

def cleanup_songs(songs):

    logging.debug(f"Entering cleanup_songs")
    logging.debug(f"Song list to be cleaned up: {songs}")

    # First lets remove any entries that are blanked
    blanks = []
    count = 0
    for i in songs:
        if i.isspace() or i is "":
            blanks.append(i)
        count += 1

    # Noe let's remove the blank charaters
    for i in blanks:
        songs.remove(i)


    final_songs = []
    for i in songs:
        final_songs.append(i.strip())

    logging.debug(f"Song list after cleaned up:{final_songs}")

    return (final_songs)

