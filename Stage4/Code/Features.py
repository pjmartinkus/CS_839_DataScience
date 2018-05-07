import pandas as pd
import re


'''
This function returns 1.0 if both laptops are refurbished or neither laptop is 
refurbished. It return 0.5 if the Name feature is missing for either laptop. It
returns 0.0 if one laptop is refurbished and the other isn't.
'''
def refurbished(x, y):
    # Check for null values
    if pd.isnull(x['Name']) or pd.isnull(y['Name']):
        return 0.5

    # Get the laptop names
    x_name = x['Name'].lower()
    y_name = y['Name'].lower()

    if ('refurbished' in x_name) == ('refurbished' in y_name):
        return 1.0
    return 0.0


'''
This function checks that the screen size, RAM, and hard drive capacity are all equal
for the two given tuples. However, whenever there is a missing value for a feature,
the pair of tuples are considered to have equal values for that feature. This prevents
candidates from being killed off from the blocking stage due to missing values. 
Additionally, we allow for a small margin of error (5 percent of the larger value) to
account for minor differences.
'''
def screen_ram_hd_equal(x, y):

    screen = compare_feats(x, y, 'Screen Size')
    ram = compare_feats(x, y, 'RAM')
    drive = compare_feats(x, y, 'Hard Drive Capacity')

    if screen or ram or drive:
        return True
    return False


# This function completes the actual comparison of tuples for screen_ram_hd_equal
def compare_feats(x, y, feat_name):
    # Check for null values
    if pd.isnull(x[feat_name]) or pd.isnull(y[feat_name]):
        return False

    # Set each string to the screen size. Remove non-numeric components
    x_val = float(re.sub('[^0-9.]', '', x[feat_name]))
    y_val = float(re.sub('[^0-9.]', '', y[feat_name]))

    # Get the difference and margin for error for these values
    diff = x_val - y_val
    error = max(x_val, y_val) * 0.05

    # Don't block if the values are close
    if -error < diff < error:
        return False
    # Block otherwise
    return True
