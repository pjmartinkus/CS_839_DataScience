'''
This file contains the post-processing rules. The post_rules() function looks for tuples
that are predicted to be positive names and if the tuple triggers any of the rules, it will
be changed to a negative prediction.
'''

import pandas as pd

# Post Processing Words
post_words = ['st.', 'while', 'when', 'olympic', 'syria', 'civil', 'university', 'national', 'miami', 'new york',
              'chicago', 'cleveland', 'florid', 'office', 'boeing', 'uber', 'google', 'policy', 'north',
              'south', 'east', 'west', 'times', 'ireland', 'netflix', 'amendment', 'seaworld', 'business',
              'islam', 'moscow', 'league', 'britain', 'cabinet', 'senator', 'news', 'tonight', 'burger'
              'hotel', 'court', 'cnn', 'tribune', 'times', 'defense', 'sandy hook', 'americans', 'persian',
              'nation', 'capital', 'communist', 'capital', 'ministry', 'wales', 'but ', 'africa', 'college',
              'lt. ', 'minister', 'police', 'vanity', 'brother', 'sister',  'las vegas', 'pyeong', 'assembly',
              'vietnam', 'after', 'department', 'school', 'hospital', 'charleston', 'general', 'haram',
              'second', 'games', 'medal', 'embassy', 'county', 'first', 'second', 'third', 'fourth', 'public',
              'san ', 'province', 'stadium', 'attendance', 'world', 'passenger', 'Burger', 'taliban', 'puerto'
              'dr. ', 'award', 'control', 'capitol', "i've", "we've", "i'm", "we're", 'hollywood', 'district',
              'childhood', 'politics', 'seasons', 'chinese', 'japonese', 'british', 'german', 'twitter', 'laden',
              'extrem', 'us. ', 'detroit', 'cambridge', 'petersburg', 'english', 'purple', 'yellow', 'orange',
              'lord ', 'management', 'explosives', 'prevenion', 'america', 'first', 'enforcement', 'solidarity',
              'deputies', 'using', 'hundrend', 'multiple', 'welsh', 'signaling', 'axios', 'center', 'venice',
              'union', 'candidate', 'delta', 'airline', 'asked', 'mobile', 'petroleum', 'bashar', 'dreamer',
              'town hall', 'speaking', 'port ', 'administration', ' day', 'generation' 'congrats', 'dr. ']
post_words_complete = ['and', 'but', 'i', 'at', 'when', 'while', 'during', 'this', 'the', 'that', 'board', 'xers', 'state', 'read']

# If any word from the above lists is found in a name labeled positive, change the label to negative
def post_rules(data):

    cols = list(data.columns.values)
    rows = []

    # Check each name
    for tuple in data.itertuples(index=False):
        row = list(tuple)
        set_to_false = False

        # Check if the name is all caps
        if row[0] == row[0].upper():
            set_to_false = True

        # Check if any of the post processing words are in the name
        if any(row[0].lower().find(word) >= 0 for word in post_words):
            set_to_false = True

        # Check if the name is exactly equal to any word in post_words_complete
        if any(row[0].lower() == word for word in post_words_complete):
            set_to_false = True

        # Check if we have donald as a name and the following word is trump
        if row[0].lower().find('donald') >= 0:
            if type(row[5]) != float and row[5].lower().find('trump') >= 0:
                set_to_false = True

        # Change the label if necessary
        if row[len(row) - 1] == 1 and set_to_false:
            row[len(row) - 1] = 0

        rows.append(row)

    # Return the dataframe
    return pd.DataFrame(rows, columns=cols)