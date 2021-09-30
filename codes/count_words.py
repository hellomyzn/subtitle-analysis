import sys

def main():
    args = sys.argv

    file_path = get_file_path(args)

    read_file(file_path)

    # extract sentence

    # separate words
    print("done")


def get_file_path(args):
    try:
        return args[1]
    except:
        print(str.upper("***   choose file which you want to try   ***"))
        exit()


def read_file(file_path):
    try:
        with open(file_path) as f:
            for line in f:
                print(line)
    except:
        print(str.upper("***   wrong file path   ***"))
        exit()



# def extract_subtitle()


# def create_words_list()


    

if __name__ == "__main__":
    main()