import logging
class DictionaryWord:
    report = []
    def __init__(self, from_word: str, to_word: str, in_word=''):

        # validation
        assert from_word not in (None, ''), f"The word we translate from must be defined!"
        assert to_word not in (None, ''), f"The word we translate to must be defined!"

        # initialise the objects
        self.from_word = from_word
        self.to_word = to_word
        self.in_word = in_word
        self.counter = 0
        self.right_answer_counter = 0

        # populate the dictionary with the exercises
        DictionaryWord.report.append(self)

    @classmethod
    def instantiate_from_csv(cls, words, from_language, to_language):
        logging.basicConfig(level=logging.INFO)
        if len(words) > 0:
            for word in words:
                logging.debug(f'word: {word}')
                logging.debug(f'from_language: .{from_language}.')
                logging.debug(f'from_language: .{to_language}.')
                logging.debug(f'from word: .{word.get(from_language)}.')
                logging.debug(f'to word: .{word.get(to_language)}.')
                DictionaryWord(
                    from_word=word.get(from_language),
                    to_word=word.get(to_language),
                )
        else:
            logging.error(f'Dictionary file is empty!')
            sys.exit()

    def __repr__(self):
        return self.show_word()

    def show_word(self):
        return f"{self.from_word} is {self.to_word}"

    def add_answer(self, reply_word):
        self.in_word = reply_word

    def increment_counter(self, from_word):
        if self.from_word == from_word:
            self.counter += self.counter
    def was_once(self):
        if self.counter >= 0:
            return True
        else:
            return False

    def right_answer(self):
        if self.to_word == self.in_word:
            return True
        else:
            return False

    # add a window for acceptance of type of errors
    # def AcceptableMistake(self):
