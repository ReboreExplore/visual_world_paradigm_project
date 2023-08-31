<h1 align="center">Visual World Paradigm</h1>
<p align="center"><i>A classical visual world study showing how people predict upcoming words with the help of Gazepoint eye tracker.</i></p>



**Authors**: Kapil Mulchandani, Manpa Barman, Pritom Gogoi. (*The authors are alphabetically ordered.*)

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2023*

## :bulb: Project Abstract
 The study presented in this paper explores the dynamics of predictive language processing through the visual world paradigm (VWP), a widely employed method in cognitive psychology. The primary objective of the research is to unwind how individuals anticipate or predict forthcoming words during the unfolding of the spoken instructions, leveraging the Gazepoint eye tracker for precise gaze pattern analysis. The investigation delves into the impact of competitor words on gaze patterns, to study the cognitive mechanisms underlying real-time language comprehension. Our experiment uses a collection of competitor words sharing phonetic or semantic similarities with the target, and validates the hypothesis that the existence of such competitors leads to an increased number of fixations on them, reflecting the participants' evolving predictions of the upcoming word.

 _Reference Paper: Allopenna, P., Magnuson, J., & Tanenhaus, M. (1998). [Tracking the time course of spoken word recognition using eye movements: evidence for continuous mapping models](https://www.sciencedirect.com/science/article/abs/pii/S0749596X97925584). Journal of Memory and Language, 38, 419-439._

## :computer: Installations

Software requirements: 
- [Python 3.9](https://www.python.org/downloads/)
- [OpenSesame 3.3.10](https://osdoc.cogsci.nl/4.0/download/)

Hardware requirements:
- Gazepoint GP3+ Eye Tracker
- [PyGaze API](https://www.gazept.com/dl/Gazepoint_API_v2.0.pdf)

Our report is created using [Quarto](report/README.md). You can install Quarto from [here](https://quarto.org/docs/get-started/).


## :page_facing_up: Overview of Folder Structure 

```bash
.
├── docs # Contains the documentation for the project.
│   ├── analysis
│   └── experiment
├── experiment # Contains the Opensesame experiment file for the project.
├── plots  # Contains all the plots generated during the analysis
│   ├── agg_plot_square.png
│   ├── final
│   └── fixation
├── presentation # Contains the final presentation for the project.
├── project_milestones # Contains the project milestones for the project.
├── README.md
├── report # Contains the report files for the project.
│   ├── custom.scss
│   ├── docs
│   ├── frontiers.csl
│   ├── Makefile
│   ├── README.md
│   └── src
├── scripts # Contains all the scripts used for preprocessing the stimuli
│   ├── conv_to_wav.sh
│   ├── remove_trailing_silence.py
│   ├── resize_imgs.py
│   └── run_py_for_all.sh
├── src # Contains all the source code for the analysis
│   ├── generate_fixation_plots.py
│   └── run_analysis.py
├──  stimuli # Contains all the stimuli files used in the experiment
│    ├── audio-stimuli
│    ├── grid.png
│    ├── image-stimuli
│    ├── README-md
│   └── stimuli-final.csv
├── LICENSE

```
## :bar_chart: How to run the experiment

1. Clone the repository 
        
    ```bash
    git clone https://github.com/ReboreExplore/visual_word_paradigm_project
    ```
2. Download the experiment file from the ```experiment``` folder and open it in OpenSesame.

    > [!NOTE]  
    > For the next two steps (3 and 4), the stimuli files are already available in the experiment file downloaded. However if you wish to design the experiment from scratch, you can follow the next two steps to load the stimuli,  otherwise directly jump to step 5 .

3. Load the ```audio-stimuli``` files and the ```image-stimuli``` files in the Opensesame file pool. The files are available in the ```stimuli``` folder.
4. Load the randomization file named ```stimuli-final.csv``` file in the loop item. The file is available in the ```stimuli``` folder.
5. Select the backend as ```PsychoPy```.
6. Select ```Gazepoint``` as the eye tracker. 
    > [!NOTE]  
    > If you are not using the eye tracker you can also choose the ```Advanced mouse click``` option to run the experiment.
7. Run the experiment.

_The experiments will run for 24 trials and will take around 5 minutes to complete.You are required to calibrate the eye tracker before starting the experiment independently for each participant, according to the eye tracker manual._

> [!IMPORTANT]  
> If you use some other stimuli files or generate your own stimuli, make sure you follow the stimuli preprocessing steps mentioned in the [stimuli](stimuli/README.md) folder, prior to running the experiment.

## :closed_book: Experiment Guidelines

It is necessary to follow the guidelines mentioned below to ensure that the experiment runs smoothly. Follow the documents below to know more about the experiment guidelines.

1. [Before the Experiment](docs/experiment/before_the_experiment.md)
2. [Consent Form](docs/experiment/consent_form.pdf)
3. [After the Experiment](docs/experiment/after_the_experiment.md)
4. [Study Information Sheet](docs/experiment/study_subject_information_and_questionaire.md)

## 🗃 Dataset

The data recorded during our experiments can be obtained [here](https://drive.google.com/drive/folders/1MOGFGCpygDrBIc9OiFi1-KMkIljtp1X1?usp=sharing). The data has been anonymized and there exists no possible way to associate it with the participants.

The folders `processed` and `raw` need to be placed in the `/data` folder.

## :chart_with_upwards_trend: How to run the analysis

1. 

## :pencil: License

[![MIT License](https://img.shields.io/github/license/roypriyanshu02/Impressive-Profile-Readmes?style=for-the-badge)](https://github.com/roypriyanshu02/impressive-profile-readmes/blob/main/LICENSE)

## :man_astronaut: Show your support

Give a ⭐️ if this project helped you!

## Resources
1. https://www.sciencedirect.com/science/article/abs/pii/S0749596X97925584
2. https://people.ku.edu/~sjpa/Classes/CBS592/EyeTracking/visual-world-paradigm.html
3. https://osdoc.cogsci.nl/3.3/tutorials/visual-world/
