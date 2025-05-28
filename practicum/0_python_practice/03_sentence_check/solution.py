def check_first_sentence_is_second(first_str, second_str):
    first_str_words = first_str.split()
    second_str_words = second_str.split()
    for word in second_str_words:
        if (second_str_words.count(word) > first_str_words.count(word)):
            return False
    return True
