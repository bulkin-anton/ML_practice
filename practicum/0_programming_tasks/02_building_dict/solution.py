def get_new_dictionary(input_dict_name, output_dict_name):
    input_dictionary = {}
    input_file = open(input_dict_name, 'r')
    lines_number = int(input_file.readline())
    for i in range(0, lines_number):
        line_read = input_file.readline().replace('\n', '')
        words_separation = line_read.split(' - ')
        human_word = words_separation[0]
        dragon_words = words_separation[1].split(', ')
        for word in dragon_words:
            if (word in input_dictionary.keys()):
                input_dictionary[word].append(human_word)
            else:
                input_dictionary[word] = [human_word]
    input_file.close()
    output_file = open(output_dict_name, 'w')
    output_file.write(str(len(input_dictionary)) + '\n')
    for key in sorted(input_dictionary.keys()):
        output_file.write(key + ' - ')
        output_file.write(', '.join(map(str, sorted(input_dictionary[key]))))
        output_file.write('\n')
