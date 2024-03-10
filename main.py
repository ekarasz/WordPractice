import configparser
import csv
import logging
import random
import os
import sys
from dictionaryword import DictionaryWord
def choose_file(exercises_folder):
    try:
        list_of_files = os.listdir(exercises_folder)
    except FileNotFoundError:
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

    logging.basicConfig(level=logging.INFO)
    # Variables from the config file
    config = configparser.ConfigParser()

    try:
        config.read('WordPractice.conf')
    except FileNotFoundError:
        logging.error(f'Unable to process the config file!')
        sys.exit()

    number_of_tries = int(config.get('word_practice', 'number_of_tries'))
    directory = config.get('word_practice', 'directory')
    subjects = choose_file(directory)

    if len(subjects) == 0:
        logging.error(f'There is no exercise file in the {directory} folder!')
        sys.exit()
    elif len(subjects) == 1:
        subject = subjects[0]
    else:
        subject = input(f'Choose a subject: {subjects} ')

    exercise = directory + subject + '.csv'

    try:
        with open(exercise, 'r') as filehandler:
            reader = csv.DictReader(filehandler, skipinitialspace=True)
            header = reader.fieldnames
            dictionary = list(reader)
            filehandler.close()
    except FileNotFoundError:
        logging.error(f'Unable to process the exercise file: {exercise} ')
        sys.exit()

    logging.debug(header)
    logging.debug(dictionary)

    translate_from = header[0]
    translate_to = input(f'Which language do you want to practice: {header[0]} or {header[1]}? Default[{header[0]}] ')
    if translate_to.strip().lower() == header[1].strip().lower():
        translate_from = header[0]
    else:
        translate_to = header[0]
        translate_from = header[1]

    DictionaryWord.instantiate_from_csv(words=dictionary, from_language=translate_from, to_language=translate_to)
    word_count = len(DictionaryWord.report)
    logging.debug(f'Number of words: {word_count}')

    while number_of_tries <= 0:
        number_of_tries = int(input(f'Number of tries: '))

    repeat = True
    while repeat:

        for i in range(number_of_tries):
            # Random word from row 0 to row len(df.index)

            index = random.randint(0, word_count - 1)

            # from language to language variable
            original_word = DictionaryWord.report[index].from_word

            user_answer = input(f'Translate {original_word}: ')
            user_answer = user_answer.strip().lower()

            right_answer = DictionaryWord.report[index].to_word
            right_answer = right_answer.strip().lower()

            DictionaryWord.report[index].add_answer(user_answer)

            if DictionaryWord.report[index].right_answer():
                print(f'Correct')
            else:
                print(f'Incorrect')
                print(f'{original_word} is {right_answer}')

        right_answers = 0
        for answer in DictionaryWord.report:
            if answer.right_answer():
                right_answers += 1

        logging.debug(f'number of right answers {right_answers}')
        percentage = 0
        if right_answers > 0:
            percentage = right_answers * 100 / number_of_tries

        print()
        print(f'*** Summary ***')
        print(f'You got {percentage}% right')
        again = input('Do you want to give it another try? [Y/N] (Default: y): ')
        if 'n' in again.lower():
            repeat = False
