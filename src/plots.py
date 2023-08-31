import os

from tqdm.auto import tqdm
import matplotlib.pyplot as plt

from utils import (
    shift_coordinate_system_top_left_to_bottom_left,
)

from constants import (
    outer_points,
    inner_points,
)

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

def save_plots(df_of_interest, stimuli_dict, subject_number, save_path):
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
        new_fpog_x, new_fpog_y = shift_coordinate_system_top_left_to_bottom_left(df_of_interest[i]['FPOGX'], df_of_interest[i]['FPOGY'])
        # plot fpogx and fpogy
        # extract indices of rows where FPOGV is 1
        fpog_indices = df_of_interest[i][df_of_interest[i]['FPOGV'] == 1].index
        new_fpog_x = new_fpog_x[fpog_indices]
        new_fpog_y = new_fpog_y[fpog_indices]
        ax.scatter(new_fpog_x, new_fpog_y, color='red', s=5)
        
        # ax.plot(new_bpog_x, new_bpog_y, color='blue')
        draw_grid(inner_points, outer_points, ax)

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
        # close the figure
        plt.close(fig)
        # break

def plot_analysis_plot(agg_df_mean, average_audio_stimuli_offset, save_fig = False):
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
    if save_fig:
        os.makedirs('final_plots', exist_ok=True)
        # save the plot
        save_path = os.path.join('final_plots', 'final_plot_ref_target.png')
        plt.savefig(save_path, dpi=300)
    plt.show()

def hist_num_of_entries_per_trial(audio_df_valid_fixation):
    # plot a histogram of the number of entries for each trial
    plt.figure()
    plt.hist(audio_df_valid_fixation['trial_number'], bins=36, linewidth=.5, edgecolor='black')
    plt.xlabel('Trial Number')
    plt.ylabel('Number of Entries')
    plt.title('Number of Entries for Each Trial')
    plt.show()

def plt_trial_num_vs_duration(logger_df):
    # logger_df sorted by condition
    sorted_logger_df = logger_df.sort_values(by=['condition']).reset_index(drop=True)

    # plot trial number vs duration
    plt.figure(figsize=(8, 6))
    rects = plt.bar(sorted_logger_df.index, sorted_logger_df['duration'])
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        # write the condition number above each bar
        plt.text(rect.get_x() + rect.get_width()/2., 1.01*height, sorted_logger_df['condition'][idx], ha='center', va='bottom')
    plt.xlabel('Trial Number')
    plt.ylabel('Duration (ms)')

    plt.title('Trial Number vs Duration')
    plt.show()