'''
This file contains many rules used by both the pruning step and feature generation.
'''

import re

# List of top 15 countries by GDP
countries = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'England',
             'India', 'France', 'Brazil', 'Italy', 'Canada', 'Russia', 'Korea',
             'Australia', 'Spain', 'Mexico', 'Indonesia', 'Turkey', 'Netherlands',
             'Switzerland', 'Saudi Arabia', 'Argentina', 'Taiwan', 'Sweden', 'Poland',
             'Belgium']

# List of States
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
          'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
          'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
          'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
          'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
          'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
          'Wisconsin', 'Wyoming']

# List of common political words
political = ['House', 'Senate', 'President', 'Democrat', 'Republican', 'The', 'Military', 'General'
             'North', 'East', 'South', 'Mr.', 'Mrs.', 'Ms.', 'Sen.', 'Rep.', 'First Lady', 'Congress',
             'Governor', 'Representative', 'Leader', 'Sheriff', 'Director', 'Admiral', 'CEO', 'Senator'
             'Minister', 'Doctor', 'Sergeant', 'Prosecutor', 'Commissioner', 'Speaker']

# Days of the week
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Months of the year (Note isnce April, May, and August are common names, they are not in this list
months = ['January' , 'February', 'March', 'June', 'July', 'September', 'October', 'November', 'December']

# Generate the whitelists and blacklists for previous and following words
def build_lists():
    file = open('words.txt')

    # Keep track of all the words
    lists = [[], [], [], []]
    curr_list = -1

    # Go through each line in the file
    for line in file:

        # If we encounter a '#' then go to next list
        if line[0] == '#':
            curr_list += 1
        else:
            # Add the new word to the current list
            lists[curr_list].append(line.strip())
    return lists

# Returns true if each word in the candidate name starts with a capital letter
def all_caps(row):
    # Splits into list of words
    cand = row[0].split(' ')

    # If we find a word that doesn't start with a capital, set to false
    caps = True
    for word in cand:
        if not type(word[0]) == float and not word[0].isupper():
            caps = False
    return caps

# Check if the previous word starts with a capital letter
def prev_caps(row):
    # Return true if previous word starts with a capital
    if type(row[3]) == float:
        return False
    regex = re.compile('[^a-zA-Z]')
    prev = regex.sub('', row[3])
    if len(prev) > 0 and prev[0].isupper():
        return True
    return False

# Check if the word before the previous word starts with a capital letter
def prev_2_caps(row):
    # Return true if previous word starts with a capital
    if type(row[4]) == float:
        return False
    regex = re.compile('[^a-zA-Z]')
    prev = regex.sub('', row[4])
    if len(prev) > 0 and prev[0].isupper():
        return True
    return False

# Check if the following word starts with a capital letter
def follow_caps(row):
    # Return true if previous word starts with a capital
    if type(row[5]) == float:
        return False
    regex = re.compile('[^a-zA-Z]')
    follow = regex.sub('', row[5])
    if len(follow) > 0 and follow[0].isupper():
        return True
    return False

# Check if the previous word is on the previous blacklist/whitelist
def prev_list(row, list):
    # Return true if previous word is in the given list
    if not type(row[3]) == float:
        regex = re.compile('[^a-zA-Z]')
        prev = regex.sub('', row[3])
        prev = prev.lower()

        if prev in list:
            return True
    return False

# Check if the following word is on the following blacklist/whitelist
def follow_list(row, list):
    # Return true if following word is in the given list
    if not type(row[5]) == float:
        regex = re.compile('[^a-zA-Z]')
        follow = regex.sub('', row[5])
        follow = follow.lower()

        if follow in list:
            return True
    return False

# Returns the length of the string
def length(row):
    return len(row[0])

# Returns the average length of each word in the string
def avg_len(row):
    # Splits into list of words
    cand = row[0].split(' ')

    # Find the length of each word
    lengths = []
    for word in cand:
        lengths.append(len(word))

    # Calculate average
    return sum(lengths) / float(len(lengths))

# Returns the length of the previous word
def prev_len(row):
    if not type(row[3]) == float:
        return len(row[3])
    else:
        return 0

# Returns the length of the following word
def follow_len(row):
    if not type(row[5]) == float:
        return len(row[5])
    else:
        return 0

# Counts the number of words in the candidate name
def num_words(row):
    # Splits into list of words
    words = row[0].split(' ')

    return len(words)

# Search for (non period) punctuation in the name
def punct(row):
    # Look for non-letter and non period
    regex = re.compile('[^a-zA-Z.\' ]')

    if regex.search(row[0]) is not None:
        return True
    elif row[0].find("'s") >= 0:
        return True
    return False

# Search for non-letters in the previous word
def prev_punct(row):
    # Look for non-letter and non period
    regex = re.compile('[^a-zA-Z]')

    if regex.search(row[3]) is not None:
        return True
    else:
        return False

# Returns true if the previous word contains a period or doesn't exist
def prev_period(row):
    if not type(row[3]) == float:
        return '.' in row[3] or '?' in row[3] or '!' in row[3]
    else:
        return True

# Returns true if the word before the previous word contains a period or doesn't exist
def prev_2_period(row):
    if not type(row[4]) == float:
        return '.' in row[4] or '?' in row[4] or '!' in row[4]
    else:
        return True

# Returns true if the name contains any word from the following lists: days, months, countries, states, or political
def common_words(row, index):
    if type(row[index]) == float:
        return False
    # Check for days of the week
    if any(row[index].find(day) >= 0 for day in days):
        return True
    # Check for months of the year
    if any(row[index].find(month) >= 0 for month in months):
        return True
    # Check for country names
    if any(row[index].find(country) >= 0 for country in countries):
        return True
    # Check for state names
    if any(row[index].find(state) >= 0 for state in states):
        return True
    # Check for political words
    if any(row[index].find(word) >= 0 for word in political):
        return True
    return False

# Checks if the name contains a period attached to a word with more than two letters
# The idea here is that names often have periods attached to a middle initial or jr or sr
def longer_word_with_period(row):
    words = row[0].split(' ')
    for word in words:
        regex = re.compile('[^a-zA-Z. ]')
        word = regex.sub('', word)
        if len(word) > 3 and '.' in word:
            return True
    return False

# Checks if the following word starts with jr, junior, sr, or senior
def jr_or_sr(row):
    if type(row[5]) == float:
        return False
    foll = row[5].lower()
    regex = re.compile('[^a-zA-Z]')
    foll = regex.sub('', foll)
    list = ['jr', 'junior', 'senior', 'sr']
    if any(foll.find(word) == 0 for word in list):
        return True

# Block any version of white house as a candidate
def white_house(row):
    # previous word is white and name is house
    if type(row[3]) != float:
        if row[3].lower().find('white') >= 0 and row[0].lower().find('house') >= 0:
            return True
    # name is white and next word is house
    if type(row[5]) != float:
        if row[0].lower().find('white') >= 0 and row[5].lower().find('house') >= 0:
            return True
    return False