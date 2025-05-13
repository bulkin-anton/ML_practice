def find_max_substring_occurrence(str_given):
    for i in range(1, len(str_given) // 2 + 1):
        substr_repetitions = str_given.count(str_given[:i])
        if (substr_repetitions == len(str_given) / i):
            return substr_repetitions
    return 1
