import sys
import os
import csv

import count_words


def main():
    words = []
    # get folder path
    folder_path = count_words.get_args(1)

    # get files in the folder
    files = count_words.get_files_name(folder_path)

    # get words from files
    for file in files:
        file_path = folder_path + file
        get_csv_data(file_path, words)
    print(words)



    # all_word_times = []
    # total_words = 0
    # one_time = []
    # two_times = []
    # more_than_three_times = []
    # more_than_five_times = []
    # more_than_ten_times = []
    

    
    # total_words = aggregate_words(
    #         all_word_times, 
    #         total_words,
    #         one_time, two_times, 
    #         more_than_three_times, 
    #         more_than_five_times, 
    #         more_than_ten_times)
    # print(total_words)
    # print("ALL-WORDS:               " + str(len(all_word_times)))
    # print("ONE TIME:                " + str(len(one_time)) + " (" + str(cal_percentage(len(all_word_times), len(one_time))) + ")")
    # print("TWO TIMES:               " + str(len(two_times)) + " (" + str(cal_percentage(len(all_word_times), len(two_times))) + ")")
    # print("MORE THAN THREE TIMES:   " + str(len(more_than_three_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_three_times))) + ")")
    # print("MORE THAN FIVE TIMES:    " + str(len(more_than_five_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_five_times))) + ")")
    # print("MORE THAN TEN TIMES:     " + str(len(more_than_ten_times)) + " (" + str(cal_percentage(len(all_word_times), len(more_than_ten_times))) + ")")




def get_csv_data(file_path, words):
    with open (file_path, 'r') as f:
        reader = csv.reader(f)
        # skip header of csv
        header = next(reader) 

        for line in reader:
            words.append(line)


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