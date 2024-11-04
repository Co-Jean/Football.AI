import numpy as np
import random


class Network:
    """
    Simple neural network
    """
    def __init__(self, layer_sizes):
        self.sizes = layer_sizes
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(layer_sizes[:-1], layer_sizes[1:])]

    def feedforward(self, a):
        """
        Get the output of the networ
        :param a: network input
        :return: values of the output nodes
        """
        for w in self.weights:
            a = sigmoid(np.dot(w, a))
        return a

    def mutate(self):
        """
        Gives all weights in the network a random chance to change by -3 to 3
        """
        for i in range(len(self.weights[0])):
            for k in range(len(self.weights[0][i])):
                if random.randint(0, 1) == 0:
                    self.weights[0][i][k] += random.uniform(-3, 3)


def sigmoid(z):
    """Sigmoid activation function"""
    return 1.0 / (1.0 + np.exp(-z))


def relu(z):
    """relu activation function"""
    return np.maximum(0.0, z)
