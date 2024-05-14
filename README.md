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
- `config-feedforward.txt`: The NEAT configuration file that specifies the parameters for the neural network and evolutionary algorithm.

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

## NEAT Configuration File

The `config-feedforward.txt` file specifies the parameters for the NEAT algorithm. Here is the content of the file with explanations for each line:

```ini
[NEAT]
fitness_criterion     = max
fitness_threshold     = 100000.0
pop_size              = 30
reset_on_extinction   = True

[DefaultGenome]
# node activation options
activation_default      = relu
activation_mutate_rate  = 0.1
activation_options      = relu

# node aggregation options
aggregation_default     = sum
aggregation_mutate_rate = 0.0
aggregation_options     = sum

# default node bias configuration
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 1.0
bias_mutate_rate        = 0.8
bias_replace_rate       = 0.1

# default genome configuration
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5
conn_delete_prob      = 0.2
conn_add_prob         = 0.2
# connection gene configuration
enabled_default         = True
enabled_mutate_rate     = 0.1

feed_forward            = True
initial_connection      = full_direct

# node add/remove rates
node_add_prob           = 0.1
node_delete_prob        = 0.1

# network parameters
num_hidden              = 0
num_inputs              = 4
num_outputs             = 1

# node response options
response_init_mean      = 0.0
response_init_stdev     = 1.0
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 1.0
response_mutate_rate    = 0.8
response_replace_rate   = 0.1

# connection weight parameters
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 30.0
weight_min_value        = -30.0
weight_mutate_power     = 1.0
weight_mutate_rate      = 0.75
weight_replace_rate     = 0.1

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func    = max
max_stagnation          = 20
species_elitism         = 2

[DefaultReproduction]
elitism                 = 2
survival_threshold      = 0.2
```

### Explanation of the Configuration File

#### [NEAT]
- **fitness_criterion = max**: The criterion used to determine the best genome. Here, it maximizes the fitness value.
- **fitness_threshold = 100000.0**: The fitness value that, if achieved, will terminate the evolution.
- **pop_size = 30**: The number of genomes in each generation.
- **reset_on_extinction = True**: If all species go extinct, reset the population.

#### [DefaultGenome]
- **activation_default = relu**: The default activation function for the nodes.
- **activation_mutate_rate = 0.1**: The rate at which the activation function can mutate.
- **activation_options = relu**: The available activation functions.
- **aggregation_default = sum**: The default aggregation function for nodes.
- **aggregation_mutate_rate = 0.0**: The rate at which the aggregation function can mutate.
- **aggregation_options = sum**: The available aggregation functions.
- **bias_init_mean = 0.0**: The mean of the initial bias values.
- **bias_init_stdev = 1.0**: The standard deviation of the initial bias values.
- **bias_max_value = 30.0**: The maximum bias value.
- **bias_min_value = -30.0**: The minimum bias value.
- **bias_mutate_power = 1.0**: The power of the mutation for bias values.
- **bias_mutate_rate = 0.8**: The rate at which bias values can mutate.
- **bias_replace_rate = 0.1**: The rate at which bias values can be replaced.
- **compatibility_disjoint_coefficient = 1.0**: The coefficient for disjoint genes in the compatibility function.
- **compatibility_weight_coefficient = 0.5**: The coefficient for weight differences in the compatibility function.
- **conn_delete_prob = 0.2**: The probability of deleting a connection gene.
- **conn_add_prob = 0.2**: The probability of adding a new connection gene.
- **enabled_default = True**: Whether new connection genes are enabled by default.
- **enabled_mutate_rate = 0.1**: The rate at which connection genes can change their enabled status.
- **feed_forward = True**: Whether the network is feedforward.
- **initial_connection = full_direct**: The type of initial connections (full direct).
- **node_add_prob = 0.1**: The probability of adding a new node.
- **node_delete_prob = 0.1**: The probability of deleting a node.
- **num_hidden = 0**: The number of hidden nodes.
- **num_inputs = 4**: The number of input nodes.
- **num_outputs = 1**: The number of output nodes.
- **response_init_mean = 0.0**: The mean of the initial response values.
- **response_init_stdev = 1.0**: The standard deviation of the initial response values.
- **response_max_value = 30.0**: The maximum response value.
- **response_min_value = -30.0**: The minimum response value.
- **response_mutate_power = 1.0**: The power of the mutation for response values.
- **response_mutate_rate = 0.8**: The rate at which response values can mutate.
- **response_replace_rate = 0.1**: The rate at which response values can be replaced.
- **weight_init_mean = 0.0**: The mean of the initial weight values.
- **weight_init_stdev = 1.0**: The standard deviation of the initial weight values.
- **weight_max_value = 30.0**: The maximum weight value.
- **weight_min_value = -30.0**: The minimum weight value.
- **weight_mutate_power = 1.0**: The power of the mutation for weight values.
- **weight_mutate_rate = 0.75**: The rate at which weight values can mutate.
- **weight_replace_rate = 0.1**: The rate at which weight values can be replaced.

#### [DefaultSpeciesSet]
- **compatibility_threshold = 3.0**: The threshold for compatibility between genomes.



#### [DefaultStagnation]
- **species_fitness_func = max**: The function to determine the fitness of a species.
- **max_stagnation = 20**: The maximum number of generations a species can stagnate.
- **species_elitism = 2**: The number of species that are protected from extinction each generation.

#### [DefaultReproduction]
- **elitism = 2**: The number of top genomes that are carried over to the next generation unchanged.
- **survival_threshold = 0.2**: The fraction of the population allowed to reproduce.

## Conclusion

This project demonstrates the application of machine learning to a classic game scenario, showcasing how neural networks can be trained to play games through evolutionary algorithms. It serves as an educational example of integrating game development and machine learning techniques.

