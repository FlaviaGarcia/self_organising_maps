# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 23:00:11 2020

@author: flaviagv
"""

import numpy as np

def get_neighbours_index(index, offset, n_nodes, circular_offset):
    if circular_offset:
        neighbours_indexes = []
        lower_neighbour = (index - offset)%n_nodes
        n_steps = offset*2 + 1
        for index in range(n_steps):
            neighbours_indexes.append((index+lower_neighbour)%n_nodes)
        return neighbours_indexes
            
    else:
        lower_neighbour = (index - offset) if (index - offset) > 0 else 0
        upper_neighbour = (index + offset) if (index + offset) < n_nodes else n_nodes-1
        neighbours_indexes = np.arange(lower_neighbour, upper_neighbour + 1, 1)
        return neighbours_indexes


def get_winner_node(weights, sample):
    distances = np.sum(np.square(weights - sample), axis = 1)
    winner_node = np.argmin(distances) 
    return winner_node


def SOM_train(dataset, n_nodes=100, n_epochs = 20, initial_neighbourhood_size=50, circular_offset=False, learning_rate=0.2, exp_descrease=False, alpha=0.5):
    dimension_dataset = dataset.shape[1]
    
    # Initialize weights
    weights = np.random.uniform(size=(n_nodes, dimension_dataset))
    current_lr = learning_rate
    for epoch in range(n_epochs):
        for sample in dataset:
            winner_node = get_winner_node(weights, sample)
            offset = initial_neighbourhood_size - int(np.round((epoch+1)/n_epochs*(initial_neighbourhood_size)))
            neighbours_indexes = get_neighbours_index(winner_node, offset, n_nodes, circular_offset=circular_offset)
            weights[neighbours_indexes, :] += current_lr*(sample - weights[neighbours_indexes,:])
        if exp_descrease:
            current_lr = alpha * current_lr**(epoch/n_epochs)
    
    return weights
