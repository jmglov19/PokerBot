# PokerBot

## Intro
Welcome to the GloverLab PokerBot! This Repo is the build of my 2023 AI Seminar Project but with many imporvements since then including a TkinterUI and some better explanations of what is actually happening. The game of poker this game is built on is the classic Texas Hold'em version of poker. The Repo contains the structure to play the game as well as a Effective Card Strengh algortithm and my own Evaluation Algorithm that I made.

## Setup
Currently the version of python supported is 3.12 but other version as long as they are below 4.0 should work. To get the program working create a virtual python enviroment, and then run `pip install poetry`. Poetry is what is being used for dependency management. After installing poetry run `poetry install` to install the dependencies listed in the `pyproject.toml`. Tk is requuired beut becuase it is in most python installations by default it is not listed in here. After installing dependencies run the main script and a tkinter page should pop up. To start the game click Deal Cards. Currently you can just play forever and bet what ever for testing purposes and you can see how much money you have earned or lost.

## EHS Algorithm

Effective Hand Strength (EHS) is a poker algorithm conceived by computer scientists Darse Billings, Denis Papp, Jonathan Schaeffer and Duane Szafron that was published for the first time in the research paper (1998). "Opponent Modeling in Poker".

### Algorithm
This is from the Wiki page on EHS

[Link Text](https://en.wikipedia.org/wiki/Effective_hand_strength_algorithm#:~:text=Effective%20Hand%20Strength%20(EHS)%20is,in%20Poker%22%20(PDF) "EHS Algorithm")

The algorithm is a numerical approach to quantify the strength of a poker hand where its result expresses the strength of a particular hand in percentile (i.e. ranging from 0 to 1), compared to all other possible hands. The underlying assumption is that an Effective Hand Strength (EHS) is composed of the current Hand Strength (HS) and its potential to improve or deteriorate (PPOT and NPOT):

EHS = HS x (1 - NPOT) + (1-HS) x PPOT

EHS is the Effective Hand Strength

HS is the current Hand Strength (i.e. not taking into account potential to improve or deteriorate, depending on upcoming table cards)

NPOT is the Negative POTential (i.e. the probability that our current hand, if the strongest, deteriorates and becomes a losing hand)

PPOT is the Positive POTential (i.e. the probability that our current hand, if losing, improves and becomes the winning hand)

### Pseudocode

Hand Strength (HS) will enumerate all possible opponent hand cards and count the occurrences where our hand is strongest (+50% of the cases where we are tied):

```
HandStrength(ourcards, boardcards) {
    ahead = tied = behind = 0
    ourrank = Rank(ourcards, boardcards)

    for each case(oppcards) {
        opprank = Rank(oppcards, boardcards)
        if (ourrank > opprank) ahead += 1
        else if (ourrank == opprank) tied += 1
        else behind += 1
    }

    handstrength = (ahead + tied / 2) / (ahead + tied + behind)

    return handstrength
}
```
In addition, EHS will consider the hand potential (i.e. its probabilities to improve or deteriorate):

```
HandPotential(ourcards, boardcards) {
    // Hand potential array, each index represents ahead, tied, and behind
    integer array HP[3][3] // initialize to 0
    integer array HPTotal[3] // initialize to 0
    ourrank = Rank(ourcards, boardcards)

    // Consider all two card combinations of the remaining cards for the opponent
    for each case(oppcards) {
        opprank = Rank(oppcards, boardcards)
        if (ourrank > opprank) index = ahead
        else if (ourrank == opprank) index = tied
        else index = behind
        HPTotal[index] += 1

        // All possible board cards to come
        for each case(turn, river) {
            // Final 5-card board
            board = [boardcards, turn, river]
            ourbest = Rank(ourcards, board)
            oppbest = Rank(oppcards, board)
            if (ourbest > oppbest) HP[index][ahead] += 1
            else if (ourbest == oppbest) HP[index][tied] += 1
            else HP[index][behind] += 1
        }
    }

    // Ppot: were behind but moved ahead
    Ppot = (HP[behind][ahead] + HP[behind][tied] / 2 + HP[tied][ahead] / 2) / (HPTotal[behind] + HPTotal[tied])
    // Npot: were ahead but fell behind
    Npot = (HP[ahead][behind] + HP[tied][behind] / 2 + HP[ahead][tied] / 2) / (HPTotal[ahead] + HPTotal[tied])

    return [ Ppot, Npot ]
}
```


## Eval Algorithm

## Technologies Used

### Tkinter

### Threading

