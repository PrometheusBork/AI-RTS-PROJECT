# AI-RTS-PROJECT

## Installation
Use a package manager such as pip to install packages required for the game

```bash
pip install pygame
pip install pygame-ce
pip install pygame_gui
pip install psutil
pip install numpy
```

## Usage
After installing all required packages you can run the program by either right clicking main.py and running the file in the python terminal
or you can write the following in the python terminal:
```bash
python3 src/main.py
```
When running the game you are met with a menu screen with three options:
- New game
- Options
- Exit

To start the game press "New game".

The game starts picking the default map (map1).

To train units you select a base with the left mouse button and then press "i" or "w" on your keyboard, depending on if you want infantry or workers.

The units are controlled by selecting them and using the arrow keys on the keyboard to move them.

Workers can collect resources by simply moving into trees but they cannot attack units or bases.

Infantry can damage units, bases and also trees.

The game ends when a base is destroyed.

The game is primarily an environment for AI's to be trained in, so the game is not suitable for human players, as the human player can interact with all bases and units on the map.

## Contributing
Pull requests are welcome. If there is major changes please contact us or create an issue for discussion.
In this project we name our branches as "feature/(insert feature name)" or "enhancement/(enhancement name)".
Remember to test the code before pushing or creating a pull request.
Pull requests should follow this format:
### Description
Short description of what the pull request features
### Changes
Bulletpoints of changes made in pull request
### Related Issues
If there is any issues from the github that is related to the PR
### Screenshots (if applicable)
Screenshots showing the features/enhancements made
### Notes for Reviewers
Notes or advice for reviewers of the PR
