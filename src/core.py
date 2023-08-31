import os
import re

import pandas as pd
from tqdm.auto import tqdm

from utils import get_relevant_rect_value

from constants import (
    cohort_competitor_sets_cond,
    distractor_competitor_sets_cond,
    full_competitor_sets_cond,
    rhyme_competitor_sets_cond,
    N,
)

def prepare_agg_df(csv_path, relevant_csvs, bins_bounds):
    # create a dataframe to store the bounds of each bin
    bounds_df = pd.DataFrame()
    bounds_df['bin_start'] = bins_bounds[:-1]
    bounds_df['bin_end'] = bins_bounds[1:]

    agg_df = pd.DataFrame()
    for csv in relevant_csvs:
        filename = "sub-" + str(csv) + ".csv"
        df = pd.read_csv(os.path.join(csv_path, filename))
        # replace the bin_start and bin_end with that of bounds_df
        df['bin_start'] = bounds_df['bin_start']
        df['bin_end'] = bounds_df['bin_end']
        # concat the dataframes
        agg_df = pd.concat([agg_df, df], axis=0).reset_index(drop=True)
    return agg_df

def calculate_fixation_probabilities(groupby_time_bins_df):
    # normalize the values in 'seen_referant', 'seen_distractor', 'seen_rhyme', 'seen_cohort' by values in 'val_count'
    # ignore rows where val_count is 0
    groupby_time_bins_df['seen_referant'] = groupby_time_bins_df.apply(lambda x: x['seen_referant'] / x['referant_value_count'] if x['referant_value_count'] != 0 else 0, axis=1)
    groupby_time_bins_df['seen_distractor'] = groupby_time_bins_df.apply(lambda x: x['seen_distractor'] / x['val_count'] if x['val_count'] != 0 else 0, axis=1)
    groupby_time_bins_df['seen_rhyme'] = groupby_time_bins_df.apply(lambda x: x['seen_rhyme'] / x['rhyme_value_count'] if x['rhyme_value_count'] != 0 else 0, axis=1)
    groupby_time_bins_df['seen_cohort'] = groupby_time_bins_df.apply(lambda x: x['seen_cohort'] / x['cohort_value_count'] if x['cohort_value_count'] != 0 else 0, axis=1)

    return groupby_time_bins_df

def implement_conditions_on_one_hot_df(one_hot_count_df):
    # groupby bin_start and bin_end and sum the values in 'seen_referant', 'seen_distractor', 'seen_rhyme', 'seen_cohort'
    groupby_time_bins_df = one_hot_count_df.groupby(['bin_start', 'bin_end']).sum().reset_index()

    one_hot_count_df_full_competitor_sets = one_hot_count_df[one_hot_count_df['condition'].isin(full_competitor_sets_cond)]
    one_hot_count_df_cohort_competitor_sets = one_hot_count_df[one_hot_count_df['condition'].isin(cohort_competitor_sets_cond)]
    one_hot_count_df_rhyme_competitor_sets = one_hot_count_df[one_hot_count_df['condition'].isin(rhyme_competitor_sets_cond)]

    # combine full_competitor_sets, cohort_competitor_sets and rhyme_competitor_sets for referant_calc_sets
    referant_calc_sets = pd.concat([one_hot_count_df_full_competitor_sets, one_hot_count_df_cohort_competitor_sets, one_hot_count_df_rhyme_competitor_sets], ignore_index=True)
    # combine full_competitor_sets, cohort_competitor_sets for cohort_calc_sets
    cohort_calc_sets = pd.concat([one_hot_count_df_full_competitor_sets, one_hot_count_df_cohort_competitor_sets], ignore_index=True)
    # combine full_competitor_sets, rhyme_competitor_sets for rhyme_calc_sets
    rhyme_calc_sets = pd.concat([one_hot_count_df_full_competitor_sets, one_hot_count_df_rhyme_competitor_sets], ignore_index=True)

    print("Referant calc sets contains the sets: {}".format(referant_calc_sets['condition'].unique()))
    print("Cohort calc sets contains the sets: {}".format(cohort_calc_sets['condition'].unique()))
    print("Rhyme calc sets contains the sets: {}".format(rhyme_calc_sets['condition'].unique()))

    # groupby sum for referant_calc_sets
    groupby_time_bins_df_referant = referant_calc_sets.groupby(['bin_start', 'bin_end']).sum().reset_index()
    # groupby sum for cohort_calc_sets
    groupby_time_bins_df_cohort = cohort_calc_sets.groupby(['bin_start', 'bin_end']).sum().reset_index()
    # groupby sum for rhyme_calc_sets
    groupby_time_bins_df_rhyme = rhyme_calc_sets.groupby(['bin_start', 'bin_end']).sum().reset_index()

    # NOTE: preview point
    # print(groupby_time_bins_df_referant)

    # replace the values in 'seen_referant' in groupby_time_bins_df with the values in 'seen_referant' in groupby_time_bins_df_referant
    groupby_time_bins_df['seen_referant'] = groupby_time_bins_df_referant['seen_referant'].values
    # replace the values in 'seen_cohort' in groupby_time_bins_df with the values in 'seen_cohort' in groupby_time_bins_df_cohort
    groupby_time_bins_df['seen_cohort'] = groupby_time_bins_df_cohort['seen_cohort'].values
    # replace the values in 'seen_rhyme' in groupby_time_bins_df with the values in 'seen_rhyme' in groupby_time_bins_df_rhyme
    groupby_time_bins_df['seen_rhyme'] = groupby_time_bins_df_rhyme['seen_rhyme'].values

    # add the columns 'value_count' from groupby_time_bins_df_referant to groupby_time_bins_df as 'referant_value_count'
    groupby_time_bins_df['referant_value_count'] = groupby_time_bins_df_referant['val_count'].values
    # add the columns 'value_count' from groupby_time_bins_df_cohort to groupby_time_bins_df as 'cohort_value_count'
    groupby_time_bins_df['cohort_value_count'] = groupby_time_bins_df_cohort['val_count'].values
    # add the columns 'value_count' from groupby_time_bins_df_rhyme to groupby_time_bins_df as 'rhyme_value_count'
    groupby_time_bins_df['rhyme_value_count'] = groupby_time_bins_df_rhyme['val_count'].values

    return groupby_time_bins_df

def prepare_one_hot_df(count_df):
    # one hot encode the 'seen' column
    one_hot_count_df = pd.get_dummies(count_df, columns=['seen'])

    # if 'seen_cohort' column does not exist, create it and set all values to 0
    if 'seen_cohort' not in one_hot_count_df.columns:
        one_hot_count_df['seen_cohort'] = 0
    if 'seen_rhyme' not in one_hot_count_df.columns:
        one_hot_count_df['seen_rhyme'] = 0
    if 'seen_referant' not in one_hot_count_df.columns:
        one_hot_count_df['seen_referant'] = 0
    if 'seen_distractor' not in one_hot_count_df.columns:
        one_hot_count_df['seen_distractor'] = 0

    # drop the 'seen_' column
    one_hot_count_df = one_hot_count_df.drop(columns=['seen_'])
    # convert the 'seen_' columns to int
    one_hot_count_df['seen_referant'] = one_hot_count_df['seen_referant'].astype(int)
    one_hot_count_df['seen_distractor'] = one_hot_count_df['seen_distractor'].astype(int)
    one_hot_count_df['seen_rhyme'] = one_hot_count_df['seen_rhyme'].astype(int)
    one_hot_count_df['seen_cohort'] = one_hot_count_df['seen_cohort'].astype(int)

    # NOTE: preview point
    # print(one_hot_count_df)

    # remove the rows that are not relevant for the final analysis
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 2]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 3]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 4]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 6]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 7]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 9]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 10]
    one_hot_count_df = one_hot_count_df[one_hot_count_df['condition'] != 12]

    return one_hot_count_df

def modify_seen_column_for_conditions(count_df):
    # for trials with condition numbers in cohort_competitor_sets_cond, replace 'rhyme' with 'distractor'
    count_df.loc[count_df['condition'].isin(cohort_competitor_sets_cond), 'seen'] = count_df['seen'].apply(lambda x: 'distractor' if x == 'rhyme' else x)
    # for trials with condition numbers in rhyme_competitor_sets_cond, replace 'cohort' with 'distractor'
    count_df.loc[count_df['condition'].isin(rhyme_competitor_sets_cond), 'seen'] = count_df['seen'].apply(lambda x: 'distractor' if x == 'cohort' else x)
    # for trials with condition numbers in distractor_competitor_sets_cond, replace 'cohort' and 'rhyme' with 'distractor'
    count_df.loc[count_df['condition'].isin(distractor_competitor_sets_cond), 'seen'] = count_df['seen'].apply(lambda x: 'distractor' if x == 'cohort' or x == 'rhyme' else x)

def create_count_df(logger_df, duration_thresholds, audio_df_valid_fixation):
    count_df = pd.DataFrame(columns=['trial_number', 'condition', 'start_time', 'end_time', 'bin_start', 'bin_end', 'real_val_count', 'val_count', 'seen'])

    for idx, row in tqdm(logger_df.iterrows(), total=logger_df.shape[0]):
        start_offset = row['first_fixation_time']
        for i in range(N - 1):
            start_val = duration_thresholds[i] + start_offset
            end_val = duration_thresholds[i+1] + start_offset
            # get rows in audio_df_valid_fixation where trial_number is idx
            trial_df = audio_df_valid_fixation[audio_df_valid_fixation['trial_number'] == idx]
            # get rows in trial_df where TIME is between start_val and end_val
            trial_df = trial_df[(trial_df['TIME'] >= start_val) & (trial_df['TIME'] < end_val)]
            # print the count of rows in trial_df
            real_val_count = len(trial_df)
            # get the values of rect column
            seen = trial_df['rect'].values
            
            seen = get_relevant_rect_value(seen)
            val_count = min(real_val_count, 1)
            # append the values to count_df using pd.concat
            concat_df = pd.DataFrame([[idx, row['condition'], start_val, end_val, duration_thresholds[i], duration_thresholds[i+1], real_val_count, val_count, seen]], columns=['trial_number', 'condition', 'start_time', 'end_time', 'bin_start', 'bin_end', 'real_val_count', 'val_count', 'seen'])
            count_df = pd.concat([count_df, concat_df], ignore_index=True)
    return count_df

def prepare_logger_df(logger_df_raw, audio_df_valid_fixation, stimuli_loc_dict):
    # extract the rows 'referant', 'cohort', 'distractor', 'target', 'count_trial_sequence', 'condition'
    logger_df = logger_df_raw[['referant', 'cohort', 'rhyme', 'distractor', 'target', 'count_trial_sequence', 'condition']]

    # NOTE: preview point
    # print(logger_df)

    # add the data from the stimuli_loc_dict to the logger_df
    logger_df['top'] = [stimuli_loc_dict[idx][0].lower() for idx in logger_df['count_trial_sequence']]
    logger_df['right'] = [stimuli_loc_dict[idx][1].lower() for idx in logger_df['count_trial_sequence']]
    logger_df['bottom'] = [stimuli_loc_dict[idx][2].lower() for idx in logger_df['count_trial_sequence']]
    logger_df['left'] = [stimuli_loc_dict[idx][3].lower() for idx in logger_df['count_trial_sequence']]

    # NOTE: preview point
    # print(logger_df)

    # create columns 'top_type', 'right_type', 'bottom_type', 'left_type' and populate them with the type of stimuli
    # by checking if the stimuli is a referant, distractor, rhyme or cohort
    logger_df['top_type'] = logger_df.apply(lambda row: 'referant' if row['top'] == row['referant'] else 'distractor' if row['top'] == row['distractor'] else 'rhyme' if row['top'] == row['rhyme'] else 'cohort' if row['top'] == row['cohort'] else 'NA', axis=1)
    logger_df['right_type'] = logger_df.apply(lambda row: 'referant' if row['right'] == row['referant'] else 'distractor' if row['right'] == row['distractor'] else 'rhyme' if row['right'] == row['rhyme'] else 'cohort' if row['right'] == row['cohort'] else 'NA', axis=1)
    logger_df['bottom_type'] = logger_df.apply(lambda row: 'referant' if row['bottom'] == row['referant'] else 'distractor' if row['bottom'] == row['distractor'] else 'rhyme' if row['bottom'] == row['rhyme'] else 'cohort' if row['bottom'] == row['cohort'] else 'NA', axis=1)
    logger_df['left_type'] = logger_df.apply(lambda row: 'referant' if row['left'] == row['referant'] else 'distractor' if row['left'] == row['distractor'] else 'rhyme' if row['left'] == row['rhyme'] else 'cohort' if row['left'] == row['cohort'] else 'NA', axis=1)

    # NOTE: preview point
    # print(logger_df)

    # calculate the time of earliest fixation and latest fixation for each trial from the audio_df_valid_fixation dataframe
    # add it to the column 'first_fixation_time' and 'last_fixation_time' in logger_df
    first_fixation_time = []
    last_fixation_time = []
    for idx, row in logger_df.iterrows():
        trial_df = audio_df_valid_fixation[audio_df_valid_fixation['trial_number'] == idx]
        first_fixation_time.append(trial_df['TIME'].min())
        last_fixation_time.append(trial_df['TIME'].max())

    logger_df['first_fixation_time'] = first_fixation_time
    logger_df['last_fixation_time'] = last_fixation_time

    logger_df['duration'] = logger_df['last_fixation_time'] - logger_df['first_fixation_time']
    return logger_df

def prepare_tsv_df(df):
    # get columns of interest: TIME, BPOGX, BPOGY
    df_interest = df[['TIME', 'BPOGX', 'BPOGY', 'FPOGD', 'FPOGX', 'FPOGY', 'FPOGV', 'USER']]

    # replace all NaN values with empty string
    df_interest = df_interest.fillna('')

    found_trial_count = df_interest['USER'].str.contains('START_TRIAL').sum()
    print("Found {} trials".format(found_trial_count))

    # get the indices of the rows where the user column contains the phrase 'START_TRIAL'
    start_indices = df_interest[df_interest['USER'].str.contains('START_TRIAL')].index
    # get the indices of the rows where the user column contains the phrase 'FINAL_FIXATION_END'
    end_indices = df_interest[df_interest['USER'].str.contains('FINAL_FIXATION_END')].index

    # split the dataframe based on the start and end indices
    df_list = [df_interest.iloc[start_indices[i]:end_indices[i]] for i in range(len(start_indices))]

    return df_list, df_interest, start_indices, end_indices

def organize_into_trials(df_list):
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

    print("Extracted {} trials in trial list".format(len(audio_df_list)))

    return audio_df_list

def generate_stimuli_loc_dict(trial_strings, df_interest):
    # convert dataframe to list
    trial_strings = trial_strings.tolist()

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

    # use regex to extract the word after 'T:', delimited by a space
    top_stimuli = [re.findall(r'T: (\w+)', trial_string)[0] for trial_string in trial_strings]
    bottom_stimuli = [re.findall(r'B: (\w+)', trial_string)[0] for trial_string in trial_strings]
    right_stimuli = [re.findall(r'R: (\w+)', trial_string)[0] for trial_string in trial_strings]
    left_stimuli = [re.findall(r'\sL: (\w+)', trial_string)[0] for trial_string in trial_strings]

    stimuli_loc_dict = {}
    # zip the stimuli and their locations together
    for idx, stimuli in enumerate(zip(top_stimuli, right_stimuli, bottom_stimuli, left_stimuli, cond_numbers, target_words, selected_words)):
        stimuli_loc_dict[idx] = stimuli
    return stimuli_loc_dict


