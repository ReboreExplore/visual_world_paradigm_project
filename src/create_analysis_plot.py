import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# common variable
avg_duration = 1.6
N = 80
bins_bounds = np.linspace(0, avg_duration, N, endpoint=True)

# for the average audio stimulus offset bar
# the average audio stimulus offset is 750.2174 ms
average_audio_stimuli_offset = 750.2174 / 1000

# subject numbers to be included in the analysis
relevant_csvs = [0, 2, 69, 5, 6, 7, 11, 12, 13, 14, 15, 16]

# path to csv files
csv_path = "./intermediate_csv/"

# create a dataframe to store the bounds of each bin
bounds_df = pd.DataFrame()
bounds_df['bin_start'] = bins_bounds[:-1]
bounds_df['bin_end'] = bins_bounds[1:]

agg_df = pd.DataFrame()
for csv in relevant_csvs:
    filename = "sub-" + str(csv) + ".csv"
    df = pd.read_csv(csv_path + filename)
    # replace the bin_start and bin_end with that of bounds_df
    df['bin_start'] = bounds_df['bin_start']
    df['bin_end'] = bounds_df['bin_end']
    # concat the dataframes
    agg_df = pd.concat([agg_df, df], axis=0).reset_index(drop=True)

# aggregate the data across all subjects

# group_by bin_start and bin_end and get the mean of the other columns
agg_df_mean = agg_df.groupby(['bin_start', 'bin_end']).mean().reset_index()

# plot as line plots
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(agg_df_mean['bin_start'], agg_df_mean['seen_referant'], 'ro--', label='referant')
ax.plot(agg_df_mean['bin_start'], agg_df_mean['seen_cohort'], 'bs--', label='cohort')
ax.plot(agg_df_mean['bin_start'], agg_df_mean['seen_rhyme'], 'g^--', label='rhyme')
ax.plot(agg_df_mean['bin_start'], agg_df_mean['seen_distractor'], 'c.--', label='distractor')

# get ymax from plot
ymax = ax.get_ylim()[1]
# draw a vertical line at average_audio_stimuli_offset, do not add to legend
ax.vlines(average_audio_stimuli_offset, 0, ymax, colors='k', linestyles='dashed', alpha=0.5)
# add text to the plot
ax.text(average_audio_stimuli_offset + 0.02, ymax - 0.05, 'Average target offset', fontsize=10)

ax.set_xlabel('Time (s)')
ax.set_ylabel('Proportion')
ax.set_title('Proportion of stimuli fixated over time')
ax.legend()
# save the plot
# save_path = os.path.join('final_plots', 'final_plot_ref_target_' + str(subject_number) + '.png')
# plt.savefig(save_path, dpi=300)
plt.show()