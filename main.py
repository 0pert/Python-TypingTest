#!/urs/bin/env python3
"""
Typing-Test
Main file, menu
"""
from functions import game_loop
from extra_func import sort_score, random_challenge

EASY = "easy.txt"
MEDIUM = "medium.txt"
HARD = "hard.txt"

TYPING = r"""
  _______  ______  _____   ________
 /_  __| \/ / __ \/  _/ | / / ____/
  / /   \  / /_/ // //  |/ / / __  
 / /    / / ____// // /|  / /_/ /  
/_/    /_/_/___/___/_/_|_/\____/   
      /_  __/ ____/ ___/_  __/     
       / / / __/  \__ \ / /        
      / / / /___ ___/ // /         
     /_/ /_____//____//_/                                       
"""

def main():
    """ Main """
    stop = False
    while not stop:
        print(chr(27) + "[2J" + chr(27) + "[;H")
        print(TYPING)
        print("1) Easy")
        print("2) Medium")
        print("3) Hard")
        print("4) Score")
        print("5) Random Challenge")
        print()
        print("# q) - Quit program.")
        print()
        inp = input(">>> ")
        print()
        if inp == "q":
            stop = True


        elif inp == "1":
            game_loop(EASY)

        elif inp == "2":
            game_loop(MEDIUM)

        elif inp == "3":
            game_loop(HARD)

        elif inp == "4":
            try:
                sort_score()
            except FileNotFoundError:
                print("No scores avaviable.")

        elif inp == "5":
            sec = input("Time: ")
            try:
                sec = int(sec)
                random_challenge(sec)
            except ValueError:
                print("Please enter a number.")


        else:
            print("Invalid choice....")

        if not stop:
            print()
            input("[ENTER]")



if __name__ == "__main__":
    main()
