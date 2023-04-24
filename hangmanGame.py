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


# Checks if all the letters in secret_word have been guessed by the player
def check_win(secret_word, old_letters_guessed):
    """
    Checks if all the letters in secret_word have been guessed by the player
    :param secret_word: str, the word that the player needs to guess
    :param old_letters_guessed: list, a list of letters that the player has guessed so far
    :return: bool, True if all the letters in secret_word have been guessed, False otherwise
    """
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


# Returns a string that displays the letters in secret_word that have been guessed by the player
def show_hidden_word(secret_word, old_letters_guessed):
    """
    Returns a string that displays the letters in secret_word that have been guessed by the player
    :param secret_word: str, the word that the player needs to guess
    :param old_letters_guessed: list, a list of letters that the player has guessed so far
    :return: str, a string that displays the letters in secret_word that have been guessed by the player
    """
    hidden_word = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            hidden_word += letter + " "
        else:
            hidden_word += "_ "
    return hidden_word.strip()


# Checks if the player's input is valid
def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks if the player's input is valid
    :param letter_guessed: str, the letter that the player guessed
    :param old_letters_guessed: list, a list of letters that the player has guessed so far
    :return: bool, True if the player's input is valid, False otherwise
    """
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        return False
    if letter_guessed.lower() in old_letters_guessed:
        print("You have already guessed that letter:", ' -> '.join(sorted(old_letters_guessed)))
        return False
    return True


# Updates the list of letters that the player has guessed so far with the player's input
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Updates the list of letters that the player has guessed so far with the player's input
    :param letter_guessed: str, the letter that the player guessed
    :param old_letters_guessed: list, a list of letters that the player has guessed so far
    :return: bool, True if the player's input is valid and the list of guessed letters is updated, False otherwise
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        print(":(\n")
        return False


# Asks the player for the file path and the index of the word that they want to guess
def input_details():
    """
    Asks the player for the file path and the index of the word that they want to guess
    :return: tuple, a tuple containing the file path and the index of the word that the player wants to guess
    """
    file_path = input("Enter file path: ")
    index = int(input("Enter index: "))
    return file_path, index


# reads a file from file_path and selects the word at index "index"
# Returns the number of unique words in the file and the selected word
def choose_word(file_path, index):
    try:
        with open(file_path, 'r') as f:
            words = f.read().split()  # Read words from file
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found")
        sys.exit(1)  # Exit program with error code 1

    num_of_words = len(set(words))  # Count the number of unique words
    index -= 1  # Adjust index to start from 0
    word_index = index % len(words)  # Calculate the circular index
    secret_word = words[word_index]  # Choose the word at the selected index
    return num_of_words, secret_word.lower()  # Return number of words and the secret word in lowercase


# prints the hangman image corresponding to the given number of tries
def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries], '\n')


# prints the opening message
def print_opening():
    print("Welcome to the game Hangman.\n", HANGMAN_ASCII_ART + '\n')
    print(f"\nAvailable letters: {'a b c d e f g h i j k l m n o p q r s t u v w x y z'}\n")


# asks the user to input a letter and checks if it is valid
# Returns the letter if valid, otherwise prints "X" and continues to ask for input
def get_user_input(old_letters_guessed):
    while True:
        letter_guessed = input("\nGuess a letter: ").lower()
        if check_valid_input(letter_guessed, old_letters_guessed):  # Check if the input is valid
            return letter_guessed
        else:
            print("X")  # Invalid input, print "X" and continue asking for input


# asks the user if they want to play again and returns True if the answer starts with 'y'
def play_again():
    answer = input("Do you want to play again? (yes/no) ").lower()
    return answer.startswith('y')


# This is the main function that runs the game
def main():
    file_path, index = input_details()  # Get file path and word index from user input
    num_of_words, secret_word = choose_word(file_path, index)  # Choose a secret word from file
    print_opening()  # Print opening message
    old_letters_guessed = []  # List of letters guessed so far
    num_of_tries = 0  # Number of wrong attempts so far

    # Continue game until maximum number of tries is reached or the player wins
    while num_of_tries < MAX_TRIES and not check_win(secret_word, old_letters_guessed):
        print(show_hidden_word(secret_word, old_letters_guessed))  # Print the word with blanks and guessed letters
        letter_guessed = get_user_input(old_letters_guessed)  # Ask the user to input a letter
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
