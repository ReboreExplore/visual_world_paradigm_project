import os
import re

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

ag = argparse.ArgumentParser()
ag.add_argument("-s", "--subject", required=True, help="Subject number")

args = vars(ag.parse_args())

subject_number = args["subject"]
tsv_path = os.path.join("./sub-" + str(subject_number), "subject-" + str(subject_number) + ".tsv")
csv_path = os.path.join("./sub-" + str(subject_number), "subject-" + str(subject_number) + ".csv")

# read the tsv file
df = pd.read_csv(tsv_path, sep='\t')

# get columns of interest: TIME, BPOGX, BPOGY
df_interest = df[['TIME', 'BPOGX', 'BPOGY', 'FPOGD', 'FPOGX', 'FPOGY', 'FPOGV', 'USER']]

# replace all NaN values with empty string
df_interest = df_interest.fillna('')

# get the indices of the rows where the user column contains the phrase 'START_TRIAL'
start_indices = df_interest[df_interest['USER'].str.contains('START_TRIAL')].index

# get the indices of the rows where the user column contains the phrase 'FINAL_FIXATION_END'
end_indices = df_interest[df_interest['USER'].str.contains('FINAL_FIXATION_END')].index

# split the dataframe based on the start and end indices
df_list = [df_interest.iloc[start_indices[i]:end_indices[i]] for i in range(len(start_indices))]

audio_df_list = []

for key, selected_df in enumerate(df_list):
    selected_df = selected_df.reset_index(drop=True)
    # extract the row index where the user column contains the phrase 'LOG_AUDIO_TARGET_START'
    audio_start_index = selected_df[selected_df['USER'].str.contains('LOG_AUDIO_TARGET_START')].index[0]
    # extract the row index where the user column contains the phrase 'LOG_AUDIO_TARGET_END'
    audio_end_index = selected_df[selected_df['USER'].str.contains('CLICK_RESPONSE_END')].index[0]
    # split the dataframe based on the audio start and end indices
    # store the split dataframe in a list
    audio_df_list.append(selected_df.iloc[audio_start_index:audio_end_index + 1])
    # audio_df_list = [selected_df.iloc[audio_start_index:audio_end_index + 1]]

outer_points = {'A': (-416, -416), 'B': (-416, 416), 'C': (416, 416), 'D': (416, -416)}
inner_points = {'E': (-128, -416), 'F': (-128, 416), 'G': (128, 416), 'H': (128, -416), 'I': (-416, -128), 'J': (-416, 128), 'K': (416, 128), 'L': (416, -128), 'M': (0, 0)}
test_points = {'P': (-960, -540), 'Q': (-960, 540), 'R': (960, 540), 'S': (960, -540)}

# shift the origin from (0, 0) to (-960, 540)
# perform the same on outer_points and inner_points
def shift_coordinate_system(coord_dict):
    for key, value in coord_dict.items():
        coord_dict[key] = (value[0] + 960, -1 * value[1] + 540)
    
        # scale to [0, 1]
        coord_dict[key] = (coord_dict[key][0] / 1920, coord_dict[key][1] / 1080)
    return coord_dict

inner_points_new = shift_coordinate_system(inner_points)
outer_points_new = shift_coordinate_system(outer_points)

def shift_coordinate_system_bottom_left_to_top_left(x, y):
    return (x, -1 * y + 1)

# get all rows whose indexes are stored in start_indices
# get the USER column
trial_strings = df_interest.iloc[start_indices]['USER'].reset_index(drop=True)

# get the indices of rows that contain the phrase 'FIXATE_CENTER_AUDIO_ONSET'
target_row_indices = df_interest[df_interest['USER'].str.contains('FIXATE_CENTER_AUDIO_ONSET')].index
target_rows = df_interest.iloc[target_row_indices].reset_index(drop=True)['USER']
target_rows = target_rows.tolist()

# get the indices of rows that contain the phrase 'FINAL_FIXATION_START'
fixation_row_indices = df_interest[df_interest['USER'].str.contains('FINAL_FIXATION_START')].index
fixation_rows = df_interest.iloc[fixation_row_indices].reset_index(drop=True)['USER']
fixation_rows = fixation_rows.tolist()

# use regex to extract the number afer 'COND:'
cond_numbers = [re.findall(r'COND: (\d+)', row)[0] for row in target_rows]
# use regex to extract the word after 'TARGET:'
target_words = [re.findall(r'TARGET: (\w+)', row)[0] for row in target_rows]
# use regex to extract the word after 'SELECTED: '
selected_words = [re.findall(r'SELECTED: (\w+)', row)[0] for row in fixation_rows]

# convert dataframe to list
trial_strings = trial_strings.tolist()

# use regex to extract the word after 'T:', delimited by a space
top_stimuli = [re.findall(r'T: (\w+)', trial_string)[0] for trial_string in trial_strings]
bottom_stimuli = [re.findall(r'B: (\w+)', trial_string)[0] for trial_string in trial_strings]
right_stimuli = [re.findall(r'R: (\w+)', trial_string)[0] for trial_string in trial_strings]
left_stimuli = [re.findall(r'\sL: (\w+)', trial_string)[0] for trial_string in trial_strings]

stimuli_loc_dict = {}
# zip the stimuli and their locations together
for idx, stimuli in enumerate(zip(top_stimuli, right_stimuli, bottom_stimuli, left_stimuli, cond_numbers, target_words, selected_words)):
    stimuli_loc_dict[idx] = stimuli

# NOTE: preview point
# print(stimuli_loc_dict[0])

def draw_grid(inn, out, ax):
    # draw line from A to B
    ax.plot([out['A'][0], out['B'][0]], [out['A'][1], out['B'][1]], color='black', alpha=0.3)
    # draw line from B to C
    ax.plot([out['B'][0], out['C'][0]], [out['B'][1], out['C'][1]], color='black', alpha=0.3)
    # draw line from C to D
    ax.plot([out['C'][0], out['D'][0]], [out['C'][1], out['D'][1]], color='black', alpha=0.3)
    # draw line from D to A
    ax.plot([out['D'][0], out['A'][0]], [out['D'][1], out['A'][1]], color='black', alpha=0.3)
    # draw line from E to F
    ax.plot([inn['E'][0], inn['F'][0]], [inn['E'][1], inn['F'][1]], color='black', alpha=0.3)
    # draw line from H to G
    ax.plot([inn['H'][0], inn['G'][0]], [inn['H'][1], inn['G'][1]], color='black', alpha=0.3)
    # draw line I to L
    ax.plot([inn['I'][0], inn['L'][0]], [inn['I'][1], inn['L'][1]], color='black', alpha=0.3)
    # draw line from J to K
    ax.plot([inn['J'][0], inn['K'][0]], [inn['J'][1], inn['K'][1]], color='black', alpha=0.3)
    # create a tiny circle at the center
    ax.scatter(inn['M'][0], inn['M'][1], color='black', s=5)

# plot the gaze data for all trials

def save_plots(df_of_interest, stimuli_dict, save_path):
    # make directory to store the plots
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for i in tqdm(range(len(df_of_interest))):
        fig = plt.figure(figsize=(16, 9))
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('Subject ' + str(subject_number) + ' - Trial ' + str(i + 1))
        ax.set_xlabel('FPOGx')
        ax.set_ylabel('FPOGy')
        # switch the coordinate system to move the origin to the top left corner
        new_fpog_x, new_fpog_y = shift_coordinate_system_bottom_left_to_top_left(df_of_interest[i]['FPOGX'], df_of_interest[i]['FPOGY'])
        # plot fpogx and fpogy
        # extract indices of rows where FPOGV is 1
        fpog_indices = df_of_interest[i][df_of_interest[i]['FPOGV'] == 1].index
        new_fpog_x = new_fpog_x[fpog_indices]
        new_fpog_y = new_fpog_y[fpog_indices]
        ax.scatter(new_fpog_x, new_fpog_y, color='red', s=5)
        
        # ax.plot(new_bpog_x, new_bpog_y, color='blue')
        draw_grid(inner_points_new, outer_points_new, ax)

        # infobox text
        text_str = 'Condition: {}\nTarget: {}\nSelected: {}'.format(stimuli_dict[i][4], stimuli_dict[i][5].lower(), stimuli_dict[i][6].lower())
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
        
        # top stimuli
        ax.text(0.5, 0.8685, stimuli_dict[i][0].lower(), transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, ha='center')
        # left stimuli
        ax.text(0.3583, 0.4185, stimuli_dict[i][3].lower(), transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, ha='center')
        # right stimuli
        ax.text(0.6416, 0.4185, stimuli_dict[i][1].lower(), transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, ha='center')
        # bottom stimuli
        ax.text(0.5, 0.1522, stimuli_dict[i][2].lower(), transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props, ha='center')

        fig.savefig(os.path.join(save_path, 'trial_' + str(i + 1) + '.png'))
        # break

save_plots(audio_df_list, stimuli_loc_dict, 'audio_target_plots_' + str(subject_number))