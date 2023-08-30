## Stimuli Preprocessing Steps

### 1. Download the stimuli

- **Visual Stimuli** : Download line drawings using Creative Commons BY-SA.
      
    > [!NOTE]  
    > For the images you donot find line drawings, you can use the [GIMP](https://www.gimp.org/) software to convert the images to line drawings, using its edge detection feature. The files were in ```png``` format.
- **Audio Stimuli** : Digital audio was generated using [this](app.acoust.io.) online utility with voice profile of _'David'_ and  a playback speed of _'0.8x'_.

### 2. Preprocess the stimuli

The stimuli collected needed to be preprocessed before they could be used in the experiment. The preprocessing steps are as follows:

1. Resizing the line drawings into 256x256 pixels. The OpenCV library was was used to read and resize the images. 

      [![Code](https://img.shields.io/badge/code-008000)](../scripts/resize_imgs.py)
      
      ```python
          img = cv2.resize(img, size)
      ```

2. Converting the audio files to ```.wav``` format. The audio files were generated in ```.mp3``` format. 

      [![Code](https://img.shields.io/badge/code-008000)](../scripts/conv_to_wav.sh)
              
      ```bash
              for file in $DIRPATH/*.mp3; do
                  filename=$(basename "$file")
                  filename="${filename%.*}"
                  ffmpeg -i $file $OUTDIR/$filename.wav
              done
      ```

3. A trailing silence after each audio was observed which would affect the response time of the participants. The silence was removed using the ```pydub``` library.

      [![Code](https://img.shields.io/badge/code-008000)](../scripts/remove_trailing_silence.py)
      
      ```python
          def detect_leading_silence(sound, silence_threshold, chunk_size=10):
                  trim_ms = 0 # ms
                  while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
                      trim_ms += chunk_size
                  return trim_ms
      ```
      The function analyzes an audio snippet to find the duration of the silence at the beginning of the signal. It iterates over chunks of the audio and measuring the volume (dBFS) in each chunk until the volume exceeds the provided silence threshold. The accumulated time of trimmed silence is then returned as the result and then removed using the ```sound[trim_ms:]``` function, spectifying the start and the end trim duration.

4. The sampling rate of all the audio samples was also made equal to work with the ```PsychoPy``` backend. The sampling rate was changed to 48Hz.

5. Run all. 

This will generate the preprocessed stimuli in the ```stimuli``` folder.

