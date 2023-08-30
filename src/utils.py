import numpy as np

from constants import (
    top_rect,
    right_rect,
    bottom_rect,
    left_rect,
    centre_rect
)

# shift the origin from (0, 0) to (-960, 540)
# perform the same on outer_points and inner_points
def shift_coordinate_system(coord_dict):
    for key, value in coord_dict.items():
        coord_dict[key] = (value[0] + 960, -1 * value[1] + 540)
    
        # scale to [0, 1]
        coord_dict[key] = (coord_dict[key][0] / 1920, coord_dict[key][1] / 1080)
    return coord_dict

def shift_coordinate_system_single(coord):
    coord = (coord[0] + 960, -1 * coord[1] + 540)
    coord = (coord[0] / 1920, coord[1] / 1080)
    return coord

def shift_coordinate_system_bottom_left_to_top_left(x, y):
    return (x, -1 * y + 1)

def check_if_within_rect(x, y, rect):
    # convert rect to new coordinate system
    conv_rect = [shift_coordinate_system_single(coord) for coord in rect]

    # convert x, y to new coordinate system
    x, y = shift_coordinate_system_bottom_left_to_top_left(x, y)
    
    if x >= conv_rect[0][0] and x <= conv_rect[1][0] and y <= conv_rect[0][1] and y >= conv_rect[1][1]:
        return True
    else:
        return False

def get_rect(x, y):
    if check_if_within_rect(x, y, top_rect):
        return 'top'
    elif check_if_within_rect(x, y, right_rect):
        return 'right'
    elif check_if_within_rect(x, y, bottom_rect):
        return 'bottom'
    elif check_if_within_rect(x, y, left_rect):
        return 'left'
    elif check_if_within_rect(x, y, centre_rect):
        return 'centre'
    else:
        return 'outside'

def get_relevant_rect_value(list_of_val):
    # remove 'centre' and 'outside' from the list
    list_of_val = [val for val in list_of_val if val != 'centre' and val != 'outside']
    # if the list is empty, return ''
    if len(list_of_val) == 0:
        return ''
    # if unique() returns a list of length 1, return the value
    elif len(np.unique(list_of_val)) == 1:
        return list_of_val[0]
    # if unique() returns a list of length > 1, return the value with the higher count
    else:
        return max(set(list_of_val), key=list_of_val.count)
    
def map_position_to_stimuli_type(position, map_dict):
    if position not in map_dict.keys():
        return ''
    else:
        return map_dict[position]
    
def get_seen_stimuli_type(count_df, logger_df):
    # loop through each row in logger_df and get the values of 'top_type', 'right_type', 'bottom_type', 'left_type'
    for idx, row in logger_df.iterrows():
        # get rows in count_df where trial_number is idx
        trial_df = count_df[count_df['trial_number'] == idx]
        # get the values of 'top_type', 'right_type', 'bottom_type', 'left_type'
        top_type = logger_df['top_type'][idx]
        right_type = logger_df['right_type'][idx]
        bottom_type = logger_df['bottom_type'][idx]
        left_type = logger_df['left_type'][idx]
        # create a mapping dictionary
        mapping_dict = {'top': top_type, 'right': right_type, 'bottom': bottom_type, 'left': left_type}
        # apply to map_position_to_stimuli_type to each row in trial_df
        trial_df['seen'] = trial_df['seen'].apply(lambda x: map_position_to_stimuli_type(x, mapping_dict))
        # update the values in count_df
        count_df.loc[count_df['trial_number'] == idx, 'seen'] = trial_df['seen'].values
    return count_df