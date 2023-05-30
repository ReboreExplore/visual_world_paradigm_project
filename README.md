# **Course project:** Visual Word Paradigm
**Authors**: Kapil Mulchandani, Manpa Barman, Pritom Gogoi. (*The authors are alphabetically ordered.*)

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2023*

## Project Description
A classical visual world study showing how people predict upcoming words.

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
## Note on sharing your recorded data
If your data is <1GB you can add it to the data folder in your Git repository. Otherwise, only include it in the project package that you submit on Ilias at the end of the term.

## Resources
1. https://people.ku.edu/~sjpa/Classes/CBS592/EyeTracking/visual-world-paradigm.html
2. https://osdoc.cogsci.nl/3.3/tutorials/visual-world/
3. https://www.sciencedirect.com/science/article/abs/pii/S0749596X97925584