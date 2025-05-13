def find_word_in_circle(circle, word):
    if (len(circle) == 0):
        return -1
    new_circle = circle * (len(word) // len(circle) + 2)
    pointer = new_circle.find(word)
    if ((pointer != -1) and (pointer < len(circle))):
        return pointer, 1
    else:
        pointer = new_circle[::-1].find(word)
        if ((pointer != -1) and (pointer < len(circle))):
            return len(circle) - pointer - 1, -1
    return -1
