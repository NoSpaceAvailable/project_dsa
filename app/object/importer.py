from app.object.dictionary import Dictionary
from app.object.data import DataProcessor


def ImportedDictionary() -> Dictionary:
    """Automatically import English word to dictionary. 
    It reads data from 'english-vietnamese.txt', processes (re-format) the data and returns the formatted data"""

    processor = DataProcessor("./app/object/english-vietnamese.txt")    # Import data to data processor class
    processed_data = processor.process()                                # Processing the data to a prettier format
    dictionary = Dictionary()                                           # Initialize the dictionary

    for key, value in processed_data: 
        dictionary.insert(key.lower(), value)                           # Insert each of keyword - meaning pair to the dictionary

    return dictionary                                                   # Return the dictionary to caller