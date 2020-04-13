import time
import logging


def generate_uniqueID():

    """
    This function will generate a uniqueID for indexes on the data base.   It has nanosecond granularity to ensure
    the the function will always be unique
    :return: unique value
    :rtype: integer
    """
    logging.debug("Entering generate_uniqueID")
    value = time.strftime("%Y%j%H%M") + str(time.process_time_ns() // 1000)
    logging.debug(f"Unique ID='{value}'")
    return value


def cleanup_songs(songs):

    """
    This function will take a list of songs and then attempt to clean up the list.
    For example, removing leading spaces, removing trailing spaces, removing any blank albums.
    :param songs: list of songs to clean up
    :type songs: list
    :return: updated songs
    :rtype: list
    """

    logging.debug(f"Entering cleanup_songs")
    logging.debug(f"Song list to be cleaned up: {songs}")

    # First lets remove any entries that are blanked
    blanks = []
    count = 0
    for i in songs:
        if i.isspace() or i is "":
            blanks.append(i)
        count += 1

    # Now let's remove the blank characters
    for i in blanks:
        songs.remove(i)

    final_songs = []
    for i in songs:
        final_songs.append(i.strip().title())

    logging.debug(f"Song list after cleaned up:{final_songs}")

    return final_songs
