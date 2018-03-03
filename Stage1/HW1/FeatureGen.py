'''
This file contains the code to generate features. It uses the data from the
generated examples and the rules in the Rules.py file to create many
different features that can by used by the ML models to predict whether
a candidate is an actual name.
'''

import Rules
import pandas as pd

class FeatureGen:

    def __init__(self):
        pb, pw, fb, fw = Rules.build_lists()
        self.prev_whitelist = pw
        self.prev_blacklist = pb
        self.foll_blacklist = fb
        self.foll_whitelist = fw

    def gen_features(self, data):

        rows = []

        # We want to generate features for each tuple
        for row in data.itertuples(index=False):

            # Start building the new tuple
            tuple = {}
            tuple['String'] = row[0]
            tuple['Position'] = row[1]
            tuple['Article'] = row[2]
            tuple['Previous'] = row[3]
            tuple['Previous_2'] = row[4]
            tuple['Following'] = row[5]
            tuple['Possessive'] = row[6]
            tuple['Punctuation'] = row[7]
            tuple['Label'] = row[8]

            # Add the features
            tuple['Prev_Caps'] = Rules.prev_caps(row)
            tuple['Prev_2_Caps'] = Rules.prev_2_caps(row)
            tuple['Follow_Caps'] = Rules.follow_caps(row)
            tuple['Prev_Whitelist'] = Rules.prev_list(row, self.prev_whitelist)
            tuple['Prev_Blacklist'] = Rules.prev_list(row, self.prev_blacklist)
            tuple['Follow_Whitelist'] = Rules.follow_list(row, self.foll_whitelist)
            tuple['Follow_Blacklist'] = Rules.follow_list(row, self.foll_blacklist)
            tuple['Prev_Period'] = Rules.prev_period(row)
            tuple['Prev_2_Period'] = Rules.prev_2_period(row)
            tuple['Prev_Common'] = Rules.common_words(row, 3)
            tuple['Prev_2_Common'] = Rules.common_words(row, 4)
            tuple['Follow_Common'] = Rules.common_words(row, 5)
            tuple['Length'] = Rules.length(row)
            tuple['Avg_Length'] = Rules.avg_len(row)
            tuple['Num_Words'] = Rules.num_words(row)

            # Add the new tuple
            rows.append(tuple)

        # Return the pruned dataframe
        cols = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following']
        features = ['Possessive', 'Punctuation', 'Prev_Caps', 'Prev_2_Caps', 'Follow_Caps',
                    'Prev_Whitelist', 'Prev_Blacklist', 'Follow_Whitelist', 'Follow_Blacklist',
                    'Prev_Period', 'Prev_2_Period', 'Prev_Common', 'Prev_2_Common', 'Follow_Common',
                    'Length', 'Avg_Length', 'Num_Words']
        cols.extend(features)
        cols.append('Label')
        return pd.DataFrame(rows, columns=cols), features
