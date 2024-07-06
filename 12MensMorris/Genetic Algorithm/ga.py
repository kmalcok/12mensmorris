# genetic_algorithm.py

import random
import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.01, generations=100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []

    def initialize_population(self, game):
        self.population = [game.copy() for _ in range(self.population_size)]

    def fitness(self, game):
        player_mills = game.count_mills('X')
        opponent_mills = game.count_mills('O')
        return player_mills - opponent_mills

    def selection(self):
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)
        return sorted_population[:self.population_size // 2]

    def crossover(self, parent1, parent2):
        child = parent1.copy()
        crossover_point = random.randint(0, len(child.board) - 1)
        child.board[crossover_point:] = parent2.board[crossover_point:]
        return child

    def mutate(self, game):
        for i in range(len(game.board)):
            if random.uniform(0, 1) < self.mutation_rate:
                game.board[i] = random.choice(['X', 'O', None])
        return game

    def evolve(self, game):
        self.initialize_population(game)
        for generation in range(self.generations):
            selected_population = self.selection()
            next_generation = []
            for i in range(0, len(selected_population), 2):
                parent1 = selected_population[i]
                parent2 = selected_population[i + 1] if i + 1 < len(selected_population) else selected_population[0]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                next_generation.append(self.mutate(child1))
                next_generation.append(self.mutate(child2))
            self.population = next_generation

        best_game = max(self.population, key=self.fitness)
        return best_game

