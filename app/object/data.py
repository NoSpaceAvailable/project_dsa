class DataProcessor:
    """A class to process and prepare data for dictionary"""

    def __init__(self, data_path : str) -> None:
        """Initialize a processor for reading data from a file. Only support .txt file!
        
        Parameters:
            * data_path(str): the OS path to the destination which the dataset located
        """
        self.data = open(data_path, "r", encoding="utf-8").readlines()


    def process(self) -> list:
        """Transform data from txt file to word - meaning pairs
        
        Return:
            * Return a list that contain well-formatted data
        """
        self.prepared_data = []     # Initialize a list that contain only formatted data
        key = pronunciation = value = ''

        for line in self.data:

            if line.startswith('@'):    # The line that start with @ is a keyword
                line = line.strip()
                
                if key and value:
                    self.prepared_data.append([key.strip(), value.strip()])     # Insert data to prepared list
                    key = pronunciation = value = ''

                if '/' in line:     # Some words have pronunciations, some are not
                    key, pronunciation = line.replace('@', '').split('/', maxsplit=1)
                    value = '[Phiên âm] /' + pronunciation

                else:
                    key = line.replace('@', '')     # Remove the @ character before use the data

            else:
                value += line       # If the line not contain @, it must be the meaning of the keyword

        return self.prepared_data   # Return data to caller
