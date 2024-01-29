import configparser
import logging
import pandas as pd
import random
import os
import sys


def choose_file(exercises_folder):

    # noinspection PyBroadException
    try:
        list_of_files = os.listdir(exercises_folder)
    except Exception:
        logging.error(f'Cannot open Exercises directory')
        sys.exit()

    logging.debug(f'List of files in Exercises folder: {list_of_files}')
    file_names = []
    for input_file in list_of_files:
        file_parts = input_file.split('.')
        if file_parts[1] == 'csv':
            file_names.append(file_parts[0])
    return file_names


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Variables from the config file
    config = configparser.ConfigParser()

    # noinspection PyBroadException
    try:
        config.read('WordPractice.conf')
    except Exception:
        logging.error(f'Unable to process the config file')
        sys.exit()

    directory = config.get('word_practice', 'directory')
    subjects = choose_file(directory)

    if len(subjects) == 0:
        logging.error(f'There is no exercise file in the Exercises folder')
        sys.exit()
    elif len(subjects) == 1:
        subject = subjects[0]
    else:
        subject = input(f'Choose a subject: {subjects} ')

    exercise = directory + subject + '.csv'

    # noinspection PyBroadException
    try:
        df = pd.read_csv(exercise)
        logging.debug(df.head())
    except Exception:
        logging.error(f'Unable to process the exercise file: {exercise} ')
        sys.exit()

    # the number of words but the dataframe indexing from 0
    word_count = len(df.index)
    logging.debug(f'Number of words in file: {word_count}')

    header = df.columns.to_list()

    number_of_tries = int(input(f'Number of tries? '))

    repeat = True
    while repeat:
        from_language = header[1]
        to_language = input(
            f'Which language do you want to practice: {header[0]} or {header[1]}? Default[{header[0]}] ')
        if to_language.strip().lower() == header[1].strip().lower():
            from_language = header[0]
        else:
            to_language = header[0]
            from_language = header[1]

        right_answers = {}
        wrong_answers = {}
        was_once = []

        for i in range(number_of_tries):
            # Random word from row 0 to row len(df.index)

            index = random.randint(0, word_count - 1)
            while index in was_once:
                index = random.randint(0, word_count - 1)
            was_once.append(index)

            # from language to language variable
            original_word = df.loc[index, from_language]
            original_word = original_word.strip()
            original_word = original_word.lower()

            reply_word = input(f'Translate {original_word}: ')
            reply_word = reply_word.strip()
            reply_word = reply_word.lower()

            to_word = df.loc[index, to_language]
            to_word = to_word.strip()
            to_word = to_word.lower()

            if to_word == reply_word:
                print(f'Correct')
                right_answers[original_word] = to_word
            else:
                print(f'Incorrect')
                print(f'{original_word} is {to_word}')
                wrong_answers[original_word] = to_word

        percentage = len(right_answers) * 100 / number_of_tries

        print()
        print(f'*** Summary ***')
        print(f'You got {percentage}% right')
        print(f'Wrong answers: {wrong_answers}')
        print(f'Right answers: {right_answers}')
        again = input('Do you want to give it another try? [Y/N] (Default: y): ')
        if 'n' in again.lower():
            repeat = False
