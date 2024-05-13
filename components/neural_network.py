import numpy as np
import random


class NeuralNetwork:
    """Simple neural network with one hidden layer for the birds."""

    def __init__(self, input_size, hidden_size, output_size):
        """Initialize the neural network with random weights."""
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_ih = np.random.randn(self.hidden_size, self.input_size)
        self.weights_ho = np.random.randn(self.output_size, self.hidden_size)
        self.bias_h = np.random.randn(self.hidden_size, 1)
        self.bias_o = np.random.randn(self.output_size, 1)

    def forward(self, inputs):
        """Perform a forward pass through the network."""
        inputs = np.array(inputs).reshape(-1, 1)
        hidden = np.dot(self.weights_ih, inputs) + self.bias_h
        hidden = self.sigmoid(hidden)
        output = np.dot(self.weights_ho, hidden) + self.bias_o
        output = self.sigmoid(output)
        return output

    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def mutate(self, rate):
        """Mutate the neural network's weights and biases."""
        def mutate_value(value):
            if random.random() < rate:
                return value + np.random.normal()
            else:
                return value

        vectorized_mutate = np.vectorize(mutate_value)
        self.weights_ih = vectorized_mutate(self.weights_ih)
        self.weights_ho = vectorized_mutate(self.weights_ho)
        self.bias_h = vectorized_mutate(self.bias_h)
        self.bias_o = vectorized_mutate(self.bias_o)

    def crossover(self, partner):
        """Perform crossover with another neural network."""
        child = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        child.weights_ih = (self.weights_ih + partner.weights_ih) / 2
        child.weights_ho = (self.weights_ho + partner.weights_ho) / 2
        child.bias_h = (self.bias_h + partner.bias_h) / 2
        child.bias_o = (self.bias_o + partner.bias_o) / 2
        return child
import numpy as np
import random


class NeuralNetwork:
    """Simple neural network with one hidden layer for the birds."""

    def __init__(self, input_size, hidden_size, output_size):
        """Initialize the neural network with random weights."""
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_ih = np.random.randn(self.hidden_size, self.input_size)
        self.weights_ho = np.random.randn(self.output_size, self.hidden_size)
        self.bias_h = np.random.randn(self.hidden_size, 1)
        self.bias_o = np.random.randn(self.output_size, 1)

    def forward(self, inputs):
        """Perform a forward pass through the network."""
        inputs = np.array(inputs).reshape(-1, 1)
        hidden = np.dot(self.weights_ih, inputs) + self.bias_h
        hidden = self.sigmoid(hidden)
        output = np.dot(self.weights_ho, hidden) + self.bias_o
        output = self.sigmoid(output)
        return output

    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def mutate(self, rate):
        """Mutate the neural network's weights and biases."""
        def mutate_value(value):
            if random.random() < rate:
                return value + np.random.normal()
            else:
                return value

        vectorized_mutate = np.vectorize(mutate_value)
        self.weights_ih = vectorized_mutate(self.weights_ih)
        self.weights_ho = vectorized_mutate(self.weights_ho)
        self.bias_h = vectorized_mutate(self.bias_h)
        self.bias_o = vectorized_mutate(self.bias_o)

    def crossover(self, partner):
        """Perform crossover with another neural network."""
        child = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        child.weights_ih = (self.weights_ih + partner.weights_ih) / 2
        child.weights_ho = (self.weights_ho + partner.weights_ho) / 2
        child.bias_h = (self.bias_h + partner.bias_h) / 2
        child.bias_o = (self.bias_o + partner.bias_o) / 2
        return child


