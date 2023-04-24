import os
import sys

MAX_TRIES = 6
HANGMAN_PHOTOS = {
    0: """    x-------x""",

    1: """
    x-------x
    |
    |
    |
    |
    |
    """,
    2: """
    x-------x
    |       |
    |       0
    |
    |
    |
    """,
    3: """
    x-------x
    |       |
    |       0
    |       |
    |
    |
    """,
    4: """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
    """,
    5: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
    """,
    6: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
    """
}
HANGMAN_ASCII_ART = """ 
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/"""
HANGMAN_ASCII_ART = "\033[95m" + HANGMAN_ASCII_ART + "\033[0m"


def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def show_hidden_word(secret_word, old_letters_guessed):
    hidden_word = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            hidden_word += letter + " "
        else:
            hidden_word += "_ "
    return hidden_word.strip()


def check_valid_input(letter_guessed, old_letters_guessed):
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        return False
    if letter_guessed.lower() in old_letters_guessed:
        print("You have already guessed that letter:", ' -> '.join(sorted(old_letters_guessed)))
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        print(":(\n")
        return False


def input_details():
    file_path = input("Enter file path: ")
    index = int(input("Enter index: "))
    return file_path, index


def choose_word(file_path, index):
    try:
        with open(file_path, 'r') as f:
            words = f.read().split()
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found")
        sys.exit(1)

    num_of_words = len(set(words))
    index -= 1  # Adjust index to start from 0
    word_index = index % len(words)  # Circular index
    secret_word = words[word_index]
    return num_of_words, secret_word.lower()


def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries], '\n')


def print_opening():
    print("Welcome to the game Hangman.\n", HANGMAN_ASCII_ART + '\n')
    print(f"\nAvailable letters: {'a b c d e f g h i j k l m n o p q r s t u v w x y z'}\n")


def get_user_input(old_letters_guessed):
    while True:
        letter_guessed = input("\nGuess a letter: ").lower()
        if check_valid_input(letter_guessed, old_letters_guessed):
            return letter_guessed
        else:
            print("X")


def play_again():
    answer = input("Do you want to play again? (yes/no) ").lower()
    return answer.startswith('y')


def main():
    file_path, index = input_details()
    num_of_words, secret_word = choose_word(file_path, index)
    print_opening()
    old_letters_guessed = []
    num_of_tries = 0

    while num_of_tries < MAX_TRIES and not check_win(secret_word, old_letters_guessed):
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter_guessed = get_user_input(old_letters_guessed)
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                num_of_tries += 1
                print(":(\n")
                print_hangman(num_of_tries)

    if check_win(secret_word, old_letters_guessed):
        print(show_hidden_word(secret_word, old_letters_guessed))
        print("Congratulations! You won!")
    else:
        print_hangman(MAX_TRIES)
        print(f"Sorry, you lost. The word was '{secret_word}'.")

    if play_again():
        main()


if __name__ == '__main__':
    main()
