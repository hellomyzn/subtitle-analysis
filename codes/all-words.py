import sys
import os
import csv

from helper import calculate
from helper import manipulate
from helper import system


def main():
    words = []
    word_and_times = []

    # get folder path
    words_folder_path = "./data/words/"

    # get files in the folder
    words_files = system.get_files_name(words_folder_path)

    # get words from files
    for file in words_files:
        file_path = words_folder_path + file
        words.extend(manipulate.import_txt(file_path))

    word_and_times = calculate.count_words(words)
    # system.make_dir("./data/", "all-words")
    manipulate.export_csv(word_and_times, "word_and_times", "all-words")
    words_by_frequency = calculate.count_words_by_frequency(10, word_and_times)

    for (k,v) in words_by_frequency.items():
        print(k + ": " + str(len(v)))
    
    print("all: " + str(len(words)))
    
    

    
# print("ONE TIME:                " + str(len(one_time)) + " (" + str(cal_percentage(len(all_word_times), len(one_time))) + ")")
    # print("TWO TIMES:               " + str(len(two_times)) + " (" + str(cal_percentage(len(all_word_times), len(two_times))) + ")")
    # print("MORE THAN THREE TIMES:   " + str(len(more_than_three_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_three_times))) + ")")
    # print("MORE THAN FIVE TIMES:    " + str(len(more_than_five_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_five_times))) + ")")
    # print("MORE THAN TEN TIMES:     " + str(len(more_than_ten_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_ten_times))) + ")")



def aggregate_words(all_word_times, 
                    total_words,
                    one_time, 
                    two_times, 
                    more_than_three_times, 
                    more_than_five_times, 
                    more_than_ten_times):
    for k, v in all_word_times:
        if int(v) == 1:
            one_time.append(k)
            total_words += int(v)
        elif int(v) == 2:
            two_times.append(k)
            total_words += int(v)
        elif int(v) >= 10:
            more_than_ten_times.append(k)
            more_than_five_times.append(k)
            more_than_three_times.append(k)
            total_words += int(v)
        elif int(v) >= 5:
            more_than_five_times.append(k)
            more_than_three_times.append(k)
            total_words += int(v)
        elif int(v) >= 3:
            more_than_three_times.append(k)
            total_words += int(v)

    return  total_words

def cal_percentage(all_word_times: int, words: int):
    percentage = round(words / all_word_times, 3) * 100
    return percentage

    

if __name__ == "__main__":
    main()