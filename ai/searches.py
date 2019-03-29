#!/usr/bin/env python3

import heapq
import math

MAX_DEPTH = 10

class HeuristicAStar():

    def __init__(self):

        self.cities = {}
        self.heuristics = {}

    def add_city_coords(self, name, latitude, longitude):

        self.cities[name] = (float(latitude), float(longitude))

    def calculate_for(self, destination):

        for city in self.cities:
            self.heuristics[city] = self.__calculate(city, destination)

    def __calculate(self, origin, destination):

        lat_o, lon_o = self.cities[origin]
        lat_d, lon_d = self.cities[destination]
        radius = 6371

        diff_lat = math.radians(lat_o-lat_d)
        diff_lon = math.radians(lon_o-lon_d)

        a = math.sin(diff_lat/2)**2 + math.cos(math.radians(lat_o)) * math.cos(math.radians(lat_d)) * math.sin(diff_lon/2)**2
        distance = radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return distance

    def erase_heuristics(self):
        del self.heuristics
        self.heuristics = {}

    def print_heuristic(self):
        for city in self.heuristics:
            print(f"{city} -> {self.heuristics[city]}")

    def get_heursitic(self, city):
        return self.heuristics[city]


class CountryMap():

    def __init__(self, name):
        self.name = name
        self.cities = 0
        self.__city_relation = {}
        self.__graph = []
        self.__heuristic = HeuristicAStar()

        #Debug
        self.__reverse_relation = []

    def print_dict(self):
        print(self.__graph)

    def add_city(self, city):

        name, lat, long = city
        if self.__city_relation.get(name) is None:

            self.__city_relation[name] = self.cities
            self.__reverse_relation.append(name)
            self.__graph.append([])

            self.__heuristic.add_city_coords(name, lat, long)

            self.cities += 1
        # print(self.__city_relation)

    def add_connection(self, city_1, city_2, cost):
        self.__graph[self.__city_relation[city_1]].append( (self.__city_relation[city_2], cost) )
        self.__graph[self.__city_relation[city_2]].append( (self.__city_relation[city_1], cost) )

    def reverse(self, cities):
        return [self.__reverse_relation[city] for city in cities]

    def depth_search(self, origin, target):

        visited = [False]*self.cities

        result = self.__dfs(self.__city_relation[origin], self.__city_relation[target], visited)
        result[0].reverse()
        return (result[0], result[1])

    def __dfs(self, origin, target, visited):

        if origin == target:
            return  [[target], 0]

        visited[origin] = True
        for node, cost in self.__graph[origin]:

            if visited[node] is False:
                result = self.__dfs(node, target, visited)
                if result is not None:
                    result[0].append(origin)
                    result[1] += cost
                    return result

        return None

    def iterative_search(self, origin, target, max_depth=MAX_DEPTH):

        for depth in range(max_depth+1):
            result = self.__iddfs(self.__city_relation[origin], self.__city_relation[target], depth)
            if result is not None:
                return result
        return None

    def __iddfs(self, origin, target, limit):

        if origin == target:
            return [[target], 0]
        if limit <= 0:
            return None

        for node, cost in self.__graph[origin]:
            result = self.__iddfs(node, target, limit-1)
            if result is not None:
                result[0].append(origin)
                result[1] += cost
                return result

        return None

    def breadth_search(self, origin, target):

        origin = self.__city_relation[origin]
        target = self.__city_relation[target]

        queue = []
        visited = [False]*self.cities
        queue.append(([origin],0))
        result = None

        while True:

            path, total_cost = queue[0]
            # print("path = {}; cost = {}".format([self.__reverse_relation[city] for city in path], total_cost))
            current = path[-1]
            queue.remove(queue[0])

            if visited[current]:
                continue
            if current == target:
                result = (path, total_cost)
                break
            visited[current] = True

            for node, cost in self.__graph[current]:

                new_path = list(path)
                new_path.append(node)
                queue.append( ( new_path, total_cost + cost ) )

        return result

    def uniform_search(self, origin, target):

        priority_q = [(0, [self.__city_relation[ origin ]] )]
        result = None
        target = self.__city_relation[target]

        while True:
            total_cost, path = heapq.heappop(priority_q)
            current = path[-1]

            if current == target:
                result = (path, total_cost)
                break

            for node, cost in self.__graph[current]:

                new_path = list(path)
                new_path.append(node)
                heapq.heappush( priority_q, (cost+total_cost, new_path) )

        return result

    def a_star_search(self, origin, target):

        # print("Hello\n")

        self.__heuristic.calculate_for(target)
        # self.__heuristic.print_heuristic()

        # Priority queue: Heuristic, Real cost, Path
        priority_q = [(self.__heuristic.get_heursitic(origin), 0, [self.__city_relation[origin]])]
        result = None
        target = self.__city_relation[target]

        while True:
            heur_cost, total_cost, path = heapq.heappop(priority_q)
            current = path[-1]

            if current == target:
                result = path, total_cost
                break

            for node, cost in self.__graph[current]:

                new_path = list(path)
                new_path.append(node)
                heapq.heappush(priority_q, (self.__heuristic.get_heursitic(
                    self.__reverse_relation[node]), cost+total_cost, new_path))

        # print("Goodbye!\n")

        self.__heuristic.erase_heuristics()
        return result


def main():
    country = read_file()

    while True:

        choice = input("""Escolha o metodo:\n
                          [0].Largura\n
                          [1].Profundidade\n
                          [2].Custo Uniforme\n
                          [3].Busca Iterativa\n
                          [4].A-estrela\n
                          [5].Sair\n\n""")
        choice = int(choice)
        if choice not in [0, 1, 2, 3, 4]:
            break

        city_1 = input("Cidade de origem: ")
        city_2 = input("Cidade de destino: ")

        if choice == 3:
            depth = int(input("Profundidade maxima: "))

        if choice == 0:
            result = country.breadth_search(city_1, city_2)
        elif choice == 1:
            result = country.depth_search(city_1, city_2)
        elif choice == 2:
            result = country.uniform_search(city_1, city_2)
        elif choice == 3:
            result = country.iterative_search(city_1, city_2, depth)
        else:
            result = country.a_star_search(city_1, city_2)

        if result is None:
            print("\nSem caminho!\n\n")
        else:
            print(f"\nCaminho: {country.reverse(result[0])}")
            print(f"Custo total: {result[1]}\n\n")

def read_file():

    filename = input("Nome do arquivo: ")
    print("Lendo arquivo...\n")

    with open(filename) as file:

        name = file.readline()
        country = CountryMap(name)
        file.readline()

        while True:
            line = file.readline().strip()
            if line == '':
                break
            line = line.split(";")
            print(line)
            country.add_city(line)

        while True:
            line = file.readline().strip()
            if line == '':
                break
            line = line.split(';')
            country.add_connection(line[0], line[1], int(line[2]))


    print("Feito...\n")
    # country.print_dict()
    return country

if __name__ == "__main__":
    main()
