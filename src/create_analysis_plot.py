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
    bins_bounds = np.linspace(0, avg_duration_agg, N, endpoint=True)

    # subject numbers to be included in the analysis
    relevant_csvs = [0, 2, 5, 6, 7, 11, 12, 13, 14, 15, 16, 69]

    # path to csv files
    csv_path = "./intermediate_csv/"

    agg_df = prepare_agg_df(csv_path, relevant_csvs, bins_bounds)

    # aggregate the data across all subjects
    # group_by bin_start and bin_end and get the mean of the other columns
    agg_df_mean = agg_df.groupby(['bin_start', 'bin_end']).mean().reset_index()

    # plot the analysis plot
    plot_analysis_plot(agg_df_mean, average_audio_stimuli_offset)

if __name__ == "__main__":
    main()