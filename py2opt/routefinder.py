import random2
import time
from tqdm.auto import tqdm
import numpy as np

from py2opt.solver import Solver


class RouteFinder:
    def __init__(
            self,
            distance_matrix,
            cities_names,
            iterations=5,
            fixed_start=True,
            fixed_end=False,
            writer_flag=False,
            method='py2opt'
    ):
        self.distance_matrix = distance_matrix
        self.iterations = iterations
        self.writer_flag = writer_flag
        self.cities_names = cities_names
        self.fixed_start = fixed_start
        self.fixed_end = fixed_end

    def solve(self, improvement_threshold=0.01):
        print("trips")

        start_time = time.time()
        best_distance = 0
        best_route = []
        best_distances = []

        for iteration in tqdm(range(self.iterations)):
            num_cities = len(self.distance_matrix)
            initial_route = self.initialize_route()
            tsp = Solver(self.distance_matrix, initial_route)
            new_route, new_distance, distances = tsp.three_opt(improvement_threshold=improvement_threshold)

            if iteration == 0:
                best_distance = new_distance
                best_route = new_route
            else:
                pass

            if new_distance < best_distance:
                best_distance = new_distance
                best_route = new_route
                best_distances = distances

        if self.writer_flag:
            self.writer(best_route, best_distance, self.cities_names)

        if self.cities_names:
            best_route = [self.cities_names[i] for i in best_route]
            return best_distance, best_route, best_distances
        else:
            return best_distance, best_route, best_distances

    def initialize_route(self):
        length = len(self.distance_matrix)
        shuffle_start = 0
        shuffle_end = length

        if self.fixed_start:
            shuffle_start += 1
        if self.fixed_end:
            shuffle_end -= 1

        route = np.arange(length)
        shuffled = route[shuffle_start:shuffle_end]
        np.random.shuffle(shuffled)
        route[shuffle_start:shuffle_end] = shuffled
        return route

    @ staticmethod
    def writer(best_route, best_distance, cities_names):
        f = open("../results.txt", "w+")
        for i in best_route:
            f.write(cities_names[i])
            f.write("\n")
            print(cities_names[i])
        f.write(str(best_distance))
        f.close()
