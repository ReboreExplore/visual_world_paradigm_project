import os

import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import (
    get_rect,
    get_seen_stimuli_type,
)

from core import (
    prepare_tsv_df,
    organize_into_trials,
    generate_stimuli_loc_dict,
    create_count_df,
    prepare_one_hot_df,
    implement_conditions_on_one_hot_df,
    calculate_fixation_probabilities,   
)

from plots import (
    hist_num_of_entries_per_trial,
    plt_trial_num_vs_duration,
)

from constants import (
    avg_duration_process,
    N,
)

def main():
    ag = argparse.ArgumentParser()
    ag.add_argument("--subject", type=int, default=1, help="Subject number")
    ag.add_argument("--path", type=str, default="./", help="Path to the data")

    args = vars(ag.parse_args())

    subject_number = args["subject"]

    # form the paths to the csv and tsv files
    tsv_path = os.path.join(args["path"], "sub-" + str(subject_number), "subject-" + str(subject_number) + ".tsv")
    csv_path = os.path.join(args["path"], "sub-" + str(subject_number), "subject-" + str(subject_number) + ".csv")

    # read the tsv file
    df = pd.read_csv(tsv_path, sep='\t')

    # get the list of dataframes, the dataframe of interest, the start indices and the end indices
    df_list, df_interest, start_indices, end_indices = prepare_tsv_df(df)

    # organize the dataframes into trials
    audio_df_list = organize_into_trials(df_list)

    # get all rows whose indices are stored in start_indices
    # get the USER column
    # useful to extract the position of the stimuli, see later
    trial_strings = df_interest.iloc[start_indices]['USER'].reset_index(drop=True)

    # generate a dictionary of stimuli and their locations
    stimuli_loc_dict = generate_stimuli_loc_dict(trial_strings, df_interest)

    # NOTE: preview point
    # print(stimuli_loc_dict)

    # combine all audio_df_list dataframes into one dataframe, create a new column called 'trial_number' that 
    for idx, df in enumerate(audio_df_list):
        df['trial_number'] = idx

    audio_df = pd.concat(audio_df_list).reset_index(drop=True)

    # NOTE: preview point
    # print(audio_df)

    use_only_valid = True
    if use_only_valid:
        # remove rows where FPOGV is 0
        audio_df_valid_fixation = audio_df[audio_df['FPOGV'] != 0].reset_index(drop=True)
    else:
        audio_df_valid_fixation = audio_df

    # use df.apply to apply the get_rect function to each row
    audio_df_valid_fixation['rect'] = audio_df_valid_fixation.apply(lambda row: get_rect(row['FPOGX'], row['FPOGY']), axis=1)

    # get the rows belonging to trial 0
    trial_0_valid_count = audio_df_valid_fixation[audio_df_valid_fixation['trial_number'] == 35].value_counts('rect')

    # sanity check
    print("Trial 0 contains: ")
    print(trial_0_valid_count)

    hist_num_of_entries_per_trial(audio_df_valid_fixation)

    # read the csv file into a dataframe
    logger_df_raw = pd.read_csv(csv_path)

    logger_df = prepare_tsv_df(logger_df_raw, audio_df_valid_fixation, stimuli_loc_dict)

    # NOTE: preview point
    # print(logger_df)

    plt_trial_num_vs_duration(logger_df)

    print("Average duration is set to {} s".format(avg_duration_process))

    # divide the avg duration into N equal parts
    duration_thresholds = np.linspace(0, avg_duration_process, N, endpoint=True)

    # NOTE: preview point
    # print(duration_thresholds)

    print("Duration threshold count: {}".format(len(duration_thresholds)))

    count_df = create_count_df(logger_df, duration_thresholds, audio_df_valid_fixation)
    # NOTE: preview point
    # print(count_df)

    print("val count: {}, real val count: {}".format(count_df['val_count'].sum(), count_df['real_val_count'].sum()))

    count_df = get_seen_stimuli_type(count_df, logger_df)

    # NOTE: preview point
    # print(count_df)

    one_hot_count_df = prepare_one_hot_df(count_df)

    # NOTE: preview point
    # print(groupby_time_bins_df)

    groupby_time_bins_df = implement_conditions_on_one_hot_df(one_hot_count_df)

    # NOTE: preview point
    # print(groupby_time_bins_df)

    groupby_time_bins_df = calculate_fixation_probabilities(groupby_time_bins_df)

    # NOTE: preview point
    # print(groupby_time_bins_df)

    # make the directory 'intermediate_csv' if it doesn't exist
    if not os.path.exists('intermediate_csv'):
        os.makedirs('intermediate_csv')

    # save groupby_time_bins_df as 'intermediate_csv/sub-x.csv'
    groupby_time_bins_df.to_csv('intermediate_csv/sub-' + str(subject_number) + '.csv', index=False)

if __name__ == "__main__":
    main()