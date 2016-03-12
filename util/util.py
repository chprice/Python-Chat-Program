def format_number(number, size=4):
    """Ensures that number is at least length 4 by
    adding extra 0s to the front.

    """
    temp = str(number)
    while len(temp) < size:
        temp = '0' + temp
    return temp