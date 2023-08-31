# Quarto template for html and pdf reports

Basic structure to create a report using Quarto, based on Pandoc's markdown and LaTeX. 

Check the doc at <https://quarto.org/> and simply install Quarto.


## Installation

1. Download and install [Quarto](https://quarto.org/docs/download/).
2. Get the quarto extension ```quarto_titlepages``` to create custom cover pages.
 ```
 quarto install extension nmfs-opensci/quarto_titlepages
 ```
> [!NOTE]  
> Install the extention in the same folder where you have the main quarto project files i.e the src folder.

## Requirements

- Working latex installation (e.g. [MikTex](https://miktex.org/download), [TinyTex](https://yihui.org/tinytex/), [TexLive](https://www.tug.org/texlive/), etc.)

## Usage

Using quarto is a one-liner (`quarto render src --to html` or `quarto render src --to pdf`), but the provided Makefile makes it even easier:

> [!NOTE]  
> Run the following make commands from the `/report` folder.

```
make html
make pdf
make # both pdf and html
```


The resulting webpage is in `docs/index.html`, which can be used directly with Github Pages. The resulting pdf is at `docs/report.pdf`.
