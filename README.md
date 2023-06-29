# **Course project:** Visual Word Paradigm
**Authors**: Kapil Mulchandani, Manpa Barman, Pritom Gogoi. (*The authors are alphabetically ordered.*)

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2023*

## Project Description
A classical visual world study showing how people predict upcoming words with the help of Gazepoint eye tracker. The experiment is based on the visual world paradigm (VWP) which is a method used in cognitive psychology to study language processing. The project is based on the idea that when people look at an object, they will fixate on the object they are currently attending to. The VWP is used to study how people process language in real time. 
In a typical VWP experiment, participants are presented with a line drawings of four stimulus and a spoken instruction about which object the click. The participants' eye movements are recorded while they are listening to the sentence which containes the target object towards the end. The eye movements are used to infer what the participants are attending to at each point in time. For example if the sentence is "Click on the beetle", then the target word to click is  beetle. The drawings available in the screen are beaker, beetle, speaker and carriage. When you are hearing someone say this word, first you just hear [b]. Then you hear [bi]... maybe you think you're hearing the word bee! Then you hear [bik]... maybe you think you're hearing the word beak!. So your predictions about the spoken word change over time, if there are similar sounding or rhyme words. 

Our study project investigates on the effect of presence of competitor words on the gaze pattern of the participants. We hypothesize that the presence of competitor words will increase the number of fixations on the competitor words.

## Instruction for a new student
>If a fellow student wants to reproduce all your results. What scripts, in which order, with which data need to be run?
>
>Be as specific as possible.
>
>Optional: Add a pipeline plot in which the different steps are displayed together with the corresponding scripts.

## Overview of Folder Structure 

```
│projectdir             <- Project's main folder. It is initialized as a Git
│                       repository with a reasonable .gitignore file.
│
├── report              <- Report PDF
|
├── presentation        <- Final presentation slides (PDFs; optionally also .pptx etc.)
|
├── _research           <- WIP scripts, code, notes, comments,
│                       to-dos and anything in a preliminary state.
│
├── plots               <- All exported plots go here, best in date folders.
|                       Note that to ensure reproducibility it is required that all plots can be
|                       recreated using the plotting scripts in the scripts folder.
│
├── scripts             <- Various scripts, e.g. analysis and plotting.
│                       The scripts use the `src` folder for their base code.
│
├── src                 <- Source code for use in this project. Contains functions,
│                       structures and modules that are used throughout
│                       the project and in multiple scripts.
│
├── project_milestones  <- Project progress slides
│
├── sample_data         <- dummy_data used for test run
│
├── experiment          <- OpenSesame file to run the experiment; where applicable also stimuli, randomization
|
├── data                <- **If they have a reasonable file size**
|   ├── raw                 <- Raw eye-tracking data
|   ├── preprocessed        <- Data resulting from preprocessing
|
├── README.md           <- Top-level README. Fellow students need to be able to
|                       reproduce your project. Think about them!
|
├── .gitignore          <- List of files that you don’t want Git to automatically add
|                       (default Python .gitignore was used)
│
└── (requirements.txt)  <- List of modules and packages that are used for your project
                     
```

## Softwares and API's

Link to Gazepoint API: https://www.gazept.com/dl/Gazepoint_API_v2.0.pdf
## Note on sharing your recorded data
If your data is <1GB you can add it to the data folder in your Git repository. Otherwise, only include it in the project package that you submit on Ilias at the end of the term.

## Resources
1. https://people.ku.edu/~sjpa/Classes/CBS592/EyeTracking/visual-world-paradigm.html
2. https://osdoc.cogsci.nl/3.3/tutorials/visual-world/
3. https://www.sciencedirect.com/science/article/abs/pii/S0749596X97925584