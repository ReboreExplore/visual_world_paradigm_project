import os
import glob

import argparse
import numpy as np

from constants import (
    avg_duration_agg,
    N,
    average_audio_stimuli_offset
)

from core import (
    prepare_agg_df,
)

from plots import (
    plot_analysis_plot,
)

def main():
    ag = argparse.ArgumentParser()
    ag.add_argument("--path", type=str, default="./intermediate_csv", help="Path to the intermediate csv files")
    ag.add_argument("--save", action="store_true", help="Save the plot")

    args = vars(ag.parse_args())

    # path to csv files
    csv_path = args["path"]
    save_fig = args["save"]

    bins_bounds = np.linspace(0, avg_duration_agg, N, endpoint=True)

    # automatically find the relevant csv files
    relevant_csvs = [int(os.path.basename(x).split('.')[0].split('-')[1]) for x in glob.glob(os.path.join(csv_path, '*.csv'))]

    print("Found %d csv files" % len(relevant_csvs))
    print("Subject numbers: ", relevant_csvs)

    agg_df = prepare_agg_df(csv_path, relevant_csvs, bins_bounds)

    # aggregate the data across all subjects
    # group_by bin_start and bin_end and get the mean of the other columns
    agg_df_mean = agg_df.groupby(['bin_start', 'bin_end']).mean().reset_index()

    # plot the analysis plot
    plot_analysis_plot(agg_df_mean, average_audio_stimuli_offset, save_fig)

if __name__ == "__main__":
    main()