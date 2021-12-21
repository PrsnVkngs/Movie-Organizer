import re

pattern = re.compile(r'[^\(]*')


def file_movie_name(file_string):
    """
    This function will return the name of the movie contained in the file name given.
    For example, given:
    Your Highness (2011) [tmdbid=38319].mkv
    This function will return:
    Your Highness
    as a string. If no match is found, (meaning there is a file naming convention that doesn't meet expectations)
    there will be a None return and this can be caught in a try-catch method.

    :param file_string:
    :return:
    """
    global pattern

    match = re.search(pattern, file_string)

    if match:
        return match.group()
    else:
        return None


