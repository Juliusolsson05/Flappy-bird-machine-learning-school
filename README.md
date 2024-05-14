# Flappy Bird Machine Learning Project

## Introduction

This repository contains the final project for Julius Olsson in the course "Programmering 1". The project involves creating a Flappy Bird game using Pygame and implementing machine learning to train a neural network to play the game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Getting Started

To get started with this project, follow the steps below:

### Clone the Repository

```bash
git clone https://github.com/Juliusolsson05/Flappy-bird-machine-learning-school.git
cd Flappy-bird-machine-learning-school
```

### Install Required Packages

Install the necessary Python packages using pip:

```bash
pip install pygame neat-python
```

### Project Structure

The project consists of the following main components:

- `main.py`: The main script that runs the game and handles the machine learning simulation.
- `components/`: A directory containing the game components:
  - `bird.py`: Contains the `Bird` class representing the bird character.
  - `pipe.py`: Contains the `Pipe` class representing the pipes.
  - `cloud.py`: Contains the `Cloud` class representing the clouds.

### How to Run

To start the game, run the following command:

```bash
python main.py
```

You will be presented with a menu where you can choose to play the game yourself or run the machine learning simulation.

## How Machine Learning Works in This Project

The machine learning aspect of this project uses the NEAT algorithm to evolve neural networks that control the bird in the Flappy Bird game. Here’s a simplified explanation of how it works:

1. **Neural Network Initialization**: Each bird in the simulation is controlled by a neural network. Initially, these networks are randomly generated.

2. **Fitness Evaluation**: During the game simulation, each bird's performance is evaluated based on how long it survives and how many pipes it successfully passes.

3. **Neuroevolution**: After each generation (a set of game simulations), the NEAT algorithm selects the best-performing neural networks and uses them to produce the next generation through mutation and crossover operations.

4. **Iteration**: This process repeats for multiple generations, gradually improving the performance of the neural networks until they can successfully navigate the game environment.

The NEAT algorithm is particularly effective for this type of task because it evolves both the structure and weights of the neural networks, allowing for the discovery of complex and efficient network topologies.

## Conclusion

This project demonstrates the application of machine learning to a classic game scenario, showcasing how neural networks can be trained to play games through evolutionary algorithms. It serves as an educational example of integrating game development and machine learning techniques.
