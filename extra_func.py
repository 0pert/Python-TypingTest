#!/urs/bin/env python3
"""
Functions not in game loop
"""
import time
import random
from functions import letter_result, accuracy, read_file

def random_challenge(sec):
    """ Random Challenge"""
    characters = "abcdefghijklmnopqrstuvwxyz.1234567890"
    char_list = [[]]
    inp_list = [[]]
    char_dict = {}
    start_time = time.time()
    end_time = time.time()
    while end_time - start_time < sec:
        print(chr(27) + "[2J" + chr(27) + "[;H")
        char = random.choice(characters)
        char_list[0].append(char)
        print(char)
        inp = input()
        inp_list[0].append(inp)
        end_time = time.time()

    sort_list, fail, char_dict = letter_result(char_list, inp_list, char_dict)
    total = len(char_list[0])

    letter_accuracy = accuracy(total, fail)
    print("Misspelled characters:")
    for times, char in sort_list:
        print(f"{char}: {times}")
    print(f"\nLetter Accuracy: {letter_accuracy} %")


def print_score(score_list, difficulty):
    """ prints out score from list"""
    print("Word-Accuracy - " + difficulty)
    for score, name in score_list:
        print(f"{name}: {score} %")
    print()


def sort_score():
    """
    Sort by difficulty and score
    hard --> medium --> easy
    """
    fcont= read_file("score.txt")
    score_list = []
    for row in fcont:
        difficulty, score, name = row.split("_")
        score_list.append((float(score), difficulty, name.strip()))
    hard = []
    medium = []
    easy = []
    score_list.sort(reverse=True)
    for score, difficulty, name in score_list:
        if difficulty == "easy":
            easy.append((score, name))
        if difficulty == "medium":
            medium.append((score, name))
        if difficulty == "hard":
            hard.append((score, name))

    print_score(hard, "Hard:")
    print_score(medium, "Medium:")
    print_score(easy, "Easy:")


if __name__ == "__main__":
    #random_challenge(5)
    sort_score()
