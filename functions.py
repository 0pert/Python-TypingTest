#!/urs/bin/env python3
"""
All functions connected to the game loop
"""
import time

def read_file(fname):
    """ Reads text file, returns list of rows """
    with open(fname, "r", encoding="UTF-8") as fhand:
        rows = fhand.readlines()
    return rows


def counting(fname):
    """ Returns total words and letters """
    fcont = read_file(fname)
    words = 0
    letters = 0
    for row in fcont:
        word_list = row.split()
        for word in word_list:
            words += 1
            for _ in word:
                letters += 1
    return words, letters


def word_result(computer, user):
    """
    Compare original line with user input
    Returns nr of failed words 
    """
    fail = 0
    for index1, row in enumerate(computer):

        for index2, word in enumerate(row):

            if index2 <= len(user[index1]) - 1:
                if word != user[index1][index2]:
                    fail += 1
            else:
                fail += 1

    return fail


def letter_result(computer, user, wrong_char):
    """ 
    Compare original line with user input
    Returns nr of failed words
    Dictionary with misspelled characters loops through
    """
    fail = 0

    for index1, word in enumerate(computer[0]):

        if index1 <= len(user[0]) - 1:
            for index2, char in enumerate(word):

                if index2 < len(user[0][index1]):
                    if char != user[0][index1][index2]:
                        wrong_char[char] = wrong_char.get(char, 0) + 1
                        fail += 1
                else:
                    wrong_char[char] = wrong_char.get(char, 0) + 1
                    fail += 1
        else:
            for char in word:
                wrong_char[char] = wrong_char.get(char, 0) + 1
                fail += 1

    sort_list = []
    for key, val in wrong_char.items():
        sort_list.append((val, key))
    sort_list.sort(reverse=True)

    return sort_list, fail, wrong_char



def print_result(word, letter, sorted_list, game_over=False):
    """ Prints the result """
    print(chr(27) + "[2J" + chr(27) + "[;H")
    if game_over:
        print("Typing test over!")
        print("Here is your result:")
    print(f"Word accuracy: {word} %")
    print(f"Letter accuracy: {letter} %")
    print("Misspelled characters:")
    if sorted_list:
        for val, char in sorted_list:
            print(f"{char}: {str(val)}")
    print("---------------------------")


def print_wpm(gross_wpm, net_wpm, wpm_accuracy):
    """ Print result of WPM """
    print(f"Gross WPM: {gross_wpm}")
    print(f"Net WPM: {net_wpm}")
    print(f"WPM accuracy: {wpm_accuracy} %")
    print("---------------------------")


def accuracy(total, wrong):
    """ Calculates % """
    result = (total - wrong) / total * 100
    return round(result, 2)



def wpm(words, time_passed, wrong):
    """ Calculates words/minute """
    if time_passed < 90:
        minute = 1
    else:
        minute = time_passed // 60
        sec = time_passed % 60
        if sec > 30:
            minute += 1
    net_wpm = (words - wrong) / minute
    gross_wpm = words / minute
    if gross_wpm:
        wpm_accuracy = net_wpm / gross_wpm * 100
        wpm_accuracy = round(wpm_accuracy, 2)
    else:
        wpm_accuracy = 100
    return gross_wpm, net_wpm, wpm_accuracy


def soul_animal(net_wpm):
    """ Returns a animal """
    if net_wpm < 5:
        animal = "Sloth"
    elif net_wpm < 15:
        animal = "Snail"
    elif net_wpm < 30:
        animal = "Manatee"
    elif net_wpm < 40:
        animal = "Human"
    elif net_wpm < 50:
        animal = "Gazelle"
    elif net_wpm < 60:
        animal = "Ostrich"
    elif net_wpm < 70:
        animal = "Cheetah"
    elif net_wpm < 80:
        animal = "Swordfish"
    elif net_wpm < 90:
        animal = "Spur-winged goose"
    elif net_wpm < 100:
        animal = "White-throated needletail"
    elif net_wpm < 120:
        animal = "Golden eagle"
    else:
        animal = "Peregrine falcon"
    return animal


def save_score(name, difficulty, score):
    """ Save score """
    try:
        read_file("score.txt")
        file_exists = True
    except FileNotFoundError:
        file_exists = False
    with open("score.txt", "a", encoding="UTF-8") as fhand:
        if file_exists:
            fhand.write(f"\n{difficulty}_{score}_{name}")
        else:
            fhand.write(f"{difficulty}_{score}_{name}")


def game_loop(fname):
    """ Main Game Function """
    difficulty = fname[:-4]
    total_words, total_letters = counting(fname)
    rows = read_file(fname)
    wrong_words = 0
    wrong_letters = 0
    wrong_char = {}
    sorted_list = []
    total_written_words = 0

    time_passed = 0
    for row in rows:
        start_time = time.time()
        org_rows = []
        user_rows = []
        word_accuracy = accuracy(total_words, wrong_words)
        letter_accuracy = accuracy(total_letters, wrong_letters)

        gross_wpm, net_wpm, wpm_accuracy = wpm(total_written_words, time_passed, wrong_words)

        print_result(word_accuracy, letter_accuracy, sorted_list)
        print_wpm(gross_wpm, net_wpm, wpm_accuracy)

        print("\n",row)
        user_inp = input(">")
        org_rows.append((row.split()))
        user_rows.append((user_inp.split()))
        total_written_words += len(user_rows[0])

        failed_words = word_result(org_rows, user_rows)
        sorted_list, failed_letters, wrong_char = letter_result(org_rows, user_rows, wrong_char)
        wrong_words += failed_words
        wrong_letters += failed_letters
        end_time = time.time()
        time_passed += (end_time - start_time)

    word_accuracy = accuracy(total_words, wrong_words)
    letter_accuracy = accuracy(total_letters, wrong_letters)
    print_result(word_accuracy, letter_accuracy, sorted_list, game_over=True)
    print_wpm(gross_wpm, net_wpm, wpm_accuracy)
    print("You finished the test in", round(time_passed, 4), "Secunds")
    animal = soul_animal(net_wpm)
    print(f"You are fast as a {animal}!")

    name = input("\nWrite your name: ")
    save_score(name, difficulty, word_accuracy)


if __name__ == "__main__":
    # comp = [["hej", "På", "dig", "Igelkott"]]
    # usr = [["he", "jpå", "Dig", "Igelkott"]]
    game_loop("test.txt")
    #save_score("Oliver", "test", 22.5)
    # print(word_result(comp, usr))
    #sort_score()

    # sort_list, fail, wrong_char = letter_result(comp, usr, wrong_char={})
    # print(wrong_char)
