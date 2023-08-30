import os

import argparse
import pandas as pd

from core import (
    prepare_tsv_df,
    organize_into_trials,
    generate_stimuli_loc_dict,  
)

from plots import (
    save_plots,
)

def main():
    ag = argparse.ArgumentParser()
    ag.add_argument("--subject", type=int, default=1, help="Subject number")

    args = vars(ag.parse_args())

    subject_number = args["subject"]

    # form the paths to the csv and tsv files
    tsv_path = os.path.join("./sub-" + str(subject_number), "subject-" + str(subject_number) + ".tsv")

    # read the tsv file
    df = pd.read_csv(tsv_path, sep='\t')

    # get the list of dataframes, the dataframe of interest, the start indices and the end indices
    df_list, df_interest, start_indices, _ = prepare_tsv_df(df)

    # organize the dataframes into trials
    audio_df_list = organize_into_trials(df_list)

    # get all rows whose indices are stored in start_indices
    # get the USER column
    # useful to extract the position of the stimuli, see later
    trial_strings = df_interest.iloc[start_indices]['USER'].reset_index(drop=True)

    # generate a dictionary of stimuli and their locations
    stimuli_loc_dict = generate_stimuli_loc_dict(trial_strings, df_interest)

    # plot and save the gaze data for all trials
    save_plots(audio_df_list, stimuli_loc_dict, subject_number, 'audio_target_plots_' + str(subject_number))

if __name__ == "__main__":
    main()