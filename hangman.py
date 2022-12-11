import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    loads the word from text file and returns a list with each element as a word of text file
    """
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print(len(wordlist), "words are loaded.")
    return wordlist

def intro(secret_word):
    print('Welcome to the Hangman Game.')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have', 3, 'warnings left')
    print('-------------')
    print('You have', 6, 'guesses left.')
    print('Available letters:', get_available_letters([]))

def choose_word(wordlist):
    """
    takes the list of words
    returns a random word from given list using random module
    """
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    '''
    takes secret word as a string and letters guessed as a list
    returns True if every letter in secret_word is in letters guessed
    '''
    for character in secret_word:
      if character not in letters_guessed:
        return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    takes secret_word and list of letters that has been guessed by player
    returns the right letter in right position that has been guessed by player and underscore(_ ) in remaining place
    '''
    final = ''
    for character in secret_word:
      if character not in letters_guessed:
        final += '_ '
      else:
        final += character

    return final


def get_available_letters(letters_guessed):
    '''
    takes the list of letters that has been guessed by player
    returns the remaining letters for player
    '''
    alphabets = (string.ascii_lowercase)
    remaining = ''
    for character in alphabets:
      if character not in letters_guessed:
        remaining += character

    return remaining

def match_with_gaps(my_word, other_word, letters_guessed):
    '''
    take guessed_word, a random word, and list of guessed letters
    return whether a random word is match for guessed word or not
    '''
    actual_word = actual_len_word(my_word)
    if len(actual_word) != len(other_word):
        return False
    else:
        for index in range(len(other_word)):
            if (actual_word[index] == '_' and other_word[index] in letters_guessed) or (actual_word[index] != '_' and actual_word[index] != other_word[index]):
                return False

        return True


def actual_len_word(my_word):
    '''
    takes in guessed word
    returns guessed word removing space from it
    '''
    actual_word = ''
    for char in my_word:
        if char != ' ':
            actual_word += char

    return actual_word


def show_possible_matches(my_word, letters_guessed):
    '''
    takes in guessed word and list of letters guessed
    returns word that match the guessed word in every order
    '''
    count = 0
    for word in wordlist:
            if match_with_gaps(my_word, word, letters_guessed):
                if count % 10 == 0:
                    print()
                    print(word, end='  ')
                else:
                    print(word, end='  ')
                count += 1
    print()

def player_dict():
    '''
    ask for the number of player and their name from the player
    returns the dict with thier name as key and initializes their score as 0
    '''
    number = int(input("Enter the number of player: "))
    name_score = {}
    for num in range(number):
        name = input(f"Enter {str(num + 1)} player's name: ")
        name_score[name] = 0

    return name_score

def winner(player_dict):
    '''
    takes the dictionary with player name as key and their score as value
    prints the winner
    '''
    scores = list(player_dict.values())
    max_score = max(scores)
    winner_players = []
    for player in player_dict:
        if player_dict[player] == max_score:
            winner_players.append(player)

    if len(winner_players) == 1:
        print(winner_players[0], 'is the winner.')
    else:
        final = ''
        for player in range(len(winner_players)-1):
            final += winner_players[player] + ', '
        final += f'and {winner_players[-1]} are the winners.'
        print(final)


def hangman_with_hints(secret_word):
    '''
    takes a secret word
    run the program hangman
    '''
    num_guess = 6
    num_warning = 3
    intro(secret_word)
    letters_guessed = []
    while num_guess > 0:
        guess = input('Please guess a letter: ')
        if guess == '*':
            print("Possible word matches are:")
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            show_possible_matches(guessed_word,letters_guessed)
            get_available_letters(letters_guessed)

        else:
            guess = guess.lower()
            if not guess.isalpha() or guess in letters_guessed or len(guess) > 1:
                if num_warning == 0:
                    num_guess -= 1
                    if not guess.isalpha():
                        print(
                            "Oops! That is not a valid letter. You have no warnings left so you lose one guess:", end = '')
                    elif guess in letters_guessed:
                        print(
                            "Oops! You've already guessed that letter. You have 0 warnings left so you lose one guess:", end = '')
                    else:
                        print("Oops! You've entered more than a letter. You have 0 warnings left so you lose one guess:", end = '')

                else:
                    num_warning -= 1
                    if not guess.isalpha():
                        print('Oops! That is not a valid letter. You have', num_warning, 'warnings left: ', end = '')
                    elif guess in letters_guessed:
                        print("You've already guessed that letter. You now have",num_warning, 'warnings:', end = '')
                    else:
                        print("Oops! You have entered more than a letter. You have", num_warning, 'warnings left: ', end = '')

            else:
                letters_guessed.append(guess)
                if guess not in secret_word:
                    vowels = {'a', 'e', 'i', 'o', 'u'}
                    if guess in vowels:
                        num_guess -= 2
                    else:
                        num_guess -= 1

                    print('Oops! That letter is not in my word:', end = '')
                else:
                    print('Good guess:')

        print(get_guessed_word(secret_word, letters_guessed))
        print('------------')
        if is_word_guessed(secret_word, letters_guessed):
            break
        elif num_guess > 0:
            print('You have', num_guess, 'guess left.')
            print('Available letters:', get_available_letters(letters_guessed))

    if num_guess <= 0:
        print('Sorry, you ran out of guesses. The word was', secret_word)
        print()
        return 0
    else:
        print('Congratulations, you won!')
        print("Your total score for this game is:",len(set(secret_word)) * num_guess)
        return len(set(secret_word)) * num_guess


if __name__ == "__main__":
    wordlist = load_words()
    players = player_dict()
    for player in players.copy():
        print()
        print(player.upper(),"TURN")
        secret_word = choose_word(wordlist)
        scores = hangman_with_hints(secret_word)
        players[player] = scores

    winner(players)




