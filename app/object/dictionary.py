# Original code: https://www.naukri.com/code360/library/implement-a-dictionary-using-trie

class Dictionary:
    """A dictionary implementation using trie data structure"""

    def __init__(self):
        """Initialize dictionary's properties"""
        self.is_word_end = False
        self.list_map = dict()
        self.word_meaning = ""

    @staticmethod
    def create_node():
        """Create a new dictionary node
        
        Return:
            * Return a trie node
        """
        node = Dictionary()
        node.is_word_end = False
        return node

    def insert(self, word, meaning):
        """Insert a new word and its meaning to dictionary. 
        If the word is inserted more than once, the last time will be used as the latest version
        
        Parameters:
            * word (str): keyword to be inserted
            * meaning (str): keyword's meaning

        Return:
            * None
        """
        temp = self
        for char in word:
            # If there is no path, make a new node
            if temp.list_map.get(char) is None:
                temp.list_map[char] = Dictionary.create_node()
            temp = temp.list_map.get(char)
        # Store the meaning and mark end of a word 
        temp.is_word_end = True
        temp.word_meaning = meaning

    def translate(self, word):
        """Search for word and get the meaning. 
        
        Parameters:
            * word (str): the keyword to be searched
            
        Return:
            * Return False if the word is not exists, otherwise return the word's meaning
        """
        temp = self
        # Search a word in the dictionary
        for char in word:
            temp = temp.list_map.get(char)
            if temp is None:
                return False
        # If it is the end of a valid word stored before then return its meaning
        if temp.is_word_end:
            return temp.word_meaning
        # If none of above condition match
        return False