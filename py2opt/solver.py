import itertools
import numpy as np


class Solver:
    def __init__(self, distance_matrix, initial_route):
        self.distance_matrix = distance_matrix
        self.num_cities = len(self.distance_matrix)
        self.initial_route = initial_route
        self.best_route = []
        self.best_distance = 0
        self.distances = []

    def update(self, new_route, new_distance):
        self.best_distance = new_distance
        self.best_route = new_route
        return self.best_distance, self.best_route

    def exhaustive_search(self):
        self.best_route = [0] + list(range(1, self.num_cities))
        self.best_distance = self.calculate_path_dist(
            self.distance_matrix, self.best_route)

        for new_route in itertools.permutations(list(range(1, self.num_cities))):
            new_distance = self.calculate_path_dist(
                self.distance_matrix, [0] + list(new_route[:]))

            if new_distance < self.best_distance:
                self.update([0] + list(new_route[:]), new_distance)
                self.distances.append(self.best_distance)

        return self.best_route, self.best_distance, self.distances

    def two_opt(
            self,
            improvement_threshold=0.01,
            fixed_start=True,
            fixed_end=False
    ):
        self.best_route = self.initial_route
        self.best_distance = self.calculate_path_dist(
            self.distance_matrix, self.best_route
        )
        improvement_factor = 1

        shuffle_start = 0
        shuffle_end = self.num_cities
        if fixed_start:
            shuffle_start += 1
        if fixed_end:
            shuffle_end -= 1
        print("Outer")

        while improvement_factor > improvement_threshold:
            print("Looping")
            previous_best = self.best_distance
            for swap_first in range(shuffle_start, shuffle_end - 1):
                for swap_last in range(swap_first + 1, shuffle_end):
                    print("{},{}".format(swap_first, swap_last))

                    new_route = self.swap(
                        self.best_route, swap_first, swap_last)
                    new_distance = self.calculate_path_dist(
                        self.distance_matrix, new_route)
                    self.distances.append(self.best_distance)
                    if self.best_distance > new_distance:
                        self.update(new_route, new_distance)

            improvement_factor = 1 - self.best_distance/previous_best
        return self.best_route, self.best_distance, self.distances

    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        """
        This method calculates the total distance between the first city in the given path to the last city in the path.
        """
        path_distance = 0
        for ind in range(len(path) - 1):
            print("{},{},{}".format(ind,path[ind], path[ind + 1]))

            path_distance += distance_matrix[int(path[ind])][int(path[ind + 1])]
        return float("{0:.2f}".format(path_distance))

    @staticmethod
    def swap(path, swap_first, swap_last):
        print("{}".format(path))
        print("s{},{}".format(swap_first, swap_last))

        path[[swap_first, swap_last]] = path[[swap_last, swap_first]]
        return path
