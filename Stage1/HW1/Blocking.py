'''
This file contains the code to complete the pruning step. The block_talbes() function
will run the blocking_rules() function on each tuple and each tuple that triggers
any of the rules will be removed from the candidate set. The debug() function returns
all actual names that the prunng rules are eliminating.
'''

import Rules
import pandas as pd

class Blocking:

    def __init__(self):
        pb, pw, fb, fw = Rules.build_lists()
        self.prev_blacklist = pb
        self.prev_whitelist = pw
        self.foll_blacklist = fb
        self.foll_whitelist = fw

    # Removes all tuples from the input dataframe that are blocked by out blocking scheme
    def block_table(self, data):
        rows = []

        # We want to apply the rules for each tuple
        for row in data.itertuples(index=False):

            # Check if the tuple will be blocked
            block = self.blocking_rules(row)

            # If we decide not to block the tuple, keep it in the new table
            if not block:
                rows.append(row)

        # Return the pruned dataframe
        cols = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following','Possessive', 'Punctuation', 'Label']
        return  pd.DataFrame(rows, columns=cols)

    # Returns all true names that were blocked by our blocking scheme
    def debug(self, data):
        rows = []

        # We want to apply the rules for each tuple
        for row in data.itertuples(index=False):

            # Check if the tuple will be blocked
            block = self.blocking_rules(row)

            # If we decide to block but the label is 1, add to list
            if block and row[8] == 1:
                rows.append(row)

        # Return the pruned dataframe
        cols = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following', 'Possessive', 'Punctuation', 'Label']
        return pd.DataFrame(rows, columns=cols)

    # Determines if the tuples will be blocked or not
    def blocking_rules(self, row):

        block = False

        # Check that all words start with caps
        if not Rules.all_caps(row):
            block = True

        # Check if there is non-period punctuation in the name
        if Rules.punct(row):
            block = True

        # Block the tuple if the following word is capitalized, but there is no good reason
        if not row[7] and Rules.follow_caps(row) and not any(row[5].find(day) for day in Rules.days) and \
                not Rules.follow_list(row, self.foll_whitelist):
            block = True

        # Block if the name contains common words such as days and months
        if Rules.common_words(row, 0):
            block = True

        # If the previous and following words are in the blacklists
        if Rules.prev_list(row, self.prev_blacklist) and Rules.follow_list(row, self.foll_blacklist):
            block = True

        # If the previous word is capitalized, but there is no good reason
        if Rules.prev_caps(row) and (not Rules.prev_2_period(row)) and \
                (not Rules.prev_list(row, self.prev_whitelist)) and (not Rules.prev_punct(row)):
            block = True

        # If the name contains a period attached to a words with more than two letters
        if Rules.longer_word_with_period(row):
            block = True

        # Block names where jr or sr is the next word
        if Rules.jr_or_sr(row):
            block = True

        # Block 'White House' as a candidate
        if Rules.white_house(row):
            block = True

        return block