import string


### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list


### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    # >>> is_word(word_list, 'bat') returns
    True
    # >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = 'words.txt'


class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        self.mapped_dictionary = {}
        for position in range(len(str(string.ascii_lowercase))):
            self.mapped_dictionary.update({str(string.ascii_lowercase[position]):str((string.ascii_lowercase[shift:]+string.ascii_lowercase[:shift]))[position]})
        for position in range(len(str(string.ascii_uppercase))):
            self.mapped_dictionary.update({str(string.ascii_uppercase[position]):str((string.ascii_uppercase[shift:]+string.ascii_uppercase[:shift]))[position]})

        return self.mapped_dictionary

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''


        self.shifted_word = ""
        for letter in str(self.message_text):
            self.shifted_word += str(self.build_shift_dict(shift).get(str(letter))) if letter.isalpha() else str(letter)

        return self.shifted_word



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less
        code is repeated
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encrypted_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class

        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypted_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift (ie. self.encrypting_dict and
        message_text_encrypted).

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''

        self.encrypted_dict = self.build_shift_dict(self.shift - shift)
        self.message_text_encrypted = self.apply_shift(self.shift - shift)
        self.shift = shift




class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        shift_value = 0
        match_word = 0
        max_match_word = 0
        for shift in range(26):
            for word in list(self.apply_shift(shift).split(" ")):
                if is_word(self.valid_words, word):
                    match_word += 1
            if match_word > max_match_word :
                shift_value = shift
                max_match_word = match_word

        return (shift_value, self.apply_shift(shift_value))

if __name__ == '__main__':
    s = get_story_string()
    ciphertext = CiphertextMessage(s)
    print(ciphertext.decrypt_message())


# test case for build_shift_dict
test1 = Message("hello w")
print(test1.build_shift_dict(2))
print("--------|-------------\n--------v-------------\n")
print(test1.apply_shift(2))
print("---------------------------------------\n")

test2 = Message("Just In Case")
print(test2.build_shift_dict(2))
print("--------|-------------\n--------v-------------\n")
print(test2.apply_shift(2))
print("---------------------------------------\n")

test2 = Message("Hello World!")
print(test2.build_shift_dict(2))
print("--------|-------------\n--------v-------------\n")
print(test2.apply_shift(2))
print("---------------------------------------\n")


# Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())

# Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq, yqtnf!')
print('Expected Output:', (24, 'hello, world!'))
print('Actual Output:', ciphertext.decrypt_message())
