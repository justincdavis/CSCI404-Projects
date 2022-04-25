import sys
from collections import defaultdict
from queue import PriorityQueue


def get_args():
    return sys.argv[1], sys.argv[2], sys.argv[3]


def read_file(filename):
    with open(filename, 'r') as f:
        all_lines = f.readlines()
        graph = defaultdict(dict)
        for line in all_lines:
            if line.strip() == 'END OF INPUT':
                return graph
            line_data = line.split()
            graph[line_data[0]][line_data[1]] = int(line_data[2])
            graph[line_data[1]][line_data[0]] = int(line_data[2])
    return graph


def find_path(graph, origin_city, dest_city):
    queue = PriorityQueue()
    queue.put((0, (origin_city, origin_city)))

    path = {origin_city: dest_city}

    while not queue.empty():
        distance, (city1, city2) = queue.get()
        path[city1] = city2

        if city1 == dest_city:
            return path, distance
        else:
            for city, new_distance in graph[city1].items():  # use items since want city and distance
                new_distance += distance
                queue.put((new_distance, (city, city1)))


def get_path(path, origin_city, dest_city):
    final_path = [dest_city]  # create a list too represent the final path
    next_city = path[dest_city]

    while next_city != origin_city:
        final_path.append(next_city)
        next_city = path[next_city]

    return final_path.reverse()


if __name__ == '__main__':
    args = get_args()
    file_name, origin, dest = args

    world = read_file(file_name)

    route, final_dist = find_path(world, origin, dest)

    list_route = get_path(route, origin, dest)
