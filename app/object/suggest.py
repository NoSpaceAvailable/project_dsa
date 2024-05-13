import re

def suggestion(lst : list, word : str) -> list:
    """If user enter some characters, suggest word based on the entered chars. 
    For example, if entered word is 'abs', the webapp will suggest all the keywords start with 'abs', like 'absolutely'"""
    res = []
    regex = f'{word}\\w*'
    for string in lst:
        if re.match(regex, string):
            res.append(string.strip())
        else:
            continue
    return res