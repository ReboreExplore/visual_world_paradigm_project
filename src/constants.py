# TODO: candidate for new script
outer_points = {'A': (-416, -416), 'B': (-416, 416), 'C': (416, 416), 'D': (416, -416)}
inner_points = {'E': (-128, -416), 'F': (-128, 416), 'G': (128, 416), 'H': (128, -416), 'I': (-416, -128), 'J': (-416, 128), 'K': (416, 128), 'L': (416, -128), 'M': (0, 0)}
test_points = {'P': (-960, -540), 'Q': (-960, 540), 'R': (960, 540), 'S': (960, -540)}

# define the bounds of the rectangles
top_rect = [(-128, -416), (128, -128)]
right_rect = [(128, -128), (416, 128)]
bottom_rect = [(-128, 128), (128, 416)]
left_rect = [(-416, -128), (-128, 128)]
centre_rect = [(-128, -128), (128, 128)]

avg_duration_agg = 1.5
avg_duration_process = 1.6

N = 80

full_competitor_sets_cond = [1, 2, 3, 4]
cohort_competitor_sets_cond = [5, 6, 7]
rhyme_competitor_sets_cond = [8, 9, 10]
distractor_competitor_sets_cond = [11, 12]

# for the average audio stimulus offset bar
# the average audio stimulus offset is 750.2174 ms
average_audio_stimuli_offset = 750.2174 / 1000