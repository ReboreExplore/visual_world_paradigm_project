import pydub
import argparse
 
import os

# this scripts removes the trailing silence from the input audio based on the 
# argument 'silence threshold'

# NOTE: script has issues working with .mp3 file

def detect_leading_silence(sound, silence_threshold, chunk_size=10):
    trim_ms = 0 # ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size
    return trim_ms
 
ag = argparse.ArgumentParser()
ag.add_argument("-i", "--input", required=True, help="path to input audio file")
ag.add_argument("-o", "--output-dir", help="path to output directory", default="output")
ag.add_argument("-s", "--silence-threshold", help="silence threshold in dB", default=-70.0, type=float)
args = vars(ag.parse_args())
 
input_file = args["input"]
# check input extension
if not input_file.endswith(".wav"):
    sound = pydub.AudioSegment.from_file(input_file, format="mp3")
else:
    sound = pydub.AudioSegment.from_wav(input_file)
 
end_trim = detect_leading_silence(sound.reverse(), args["silence_threshold"])
duration = len(sound)
# do not trim in the beginning
start_trim = 0
trimmed = sound[start_trim:duration-end_trim]
 
# create output dir if not exists
output_dir = args["output_dir"]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
 
# export as wav
trimmed.export(output_dir + "/" + os.path.basename(input_file), format="wav")