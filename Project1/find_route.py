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


def find_path(graph, origin_city, dest_city, max_searches=None):
    if max_searches is None:
        max_searches = len(graph) ** 3
    total_searches = 0

    queue = PriorityQueue()
    queue.put((0, (origin_city, origin_city)))

    path = {origin_city: (origin_city, 0)}

    while not queue.empty():
        distance, (city1, city2) = queue.get()

        if total_searches > max_searches:
            break

        if city1 in path and distance < path[city1][1]:
            path[city1] = (city2, distance)
        elif city1 not in path:
            path[city1] = (city2, distance)

        if city1 == dest_city:
            return path, distance
        else:
            for city, new_distance in graph[city1].items():  # use items since want city and distance
                new_distance += distance
                queue.put((new_distance, (city, city1)))

        total_searches += 1

    return None, "inf"


def get_path(path, origin_city, dest_city):
    if path is None:
        return None

    final_path = [dest_city]  # create a list too represent the final path
    next_city = path[dest_city][0]

    while next_city != origin_city:
        final_path.append(next_city)
        next_city = path[next_city][0]

    if len(final_path) > 1:
        final_path.append(origin_city)
    final_path.reverse()
    return final_path


def print_output(graph, path, distance, origin_city, dest_city):
    if path is None:
        print("distance: infinity")
        print("route")
        print("none")
    else:
        print(f"distance: {distance}")
        print("route")
        for idx, city in enumerate(path):
            if idx < len(path) - 2:
                next_city = path[idx + 1]
                print(f"{city} to {next_city}, {graph[city][next_city]}km")
            else:
                dist = 0 if city == dest_city else graph[city][dest_city]
                print(f"{city} to {dest_city}, {dist}km")


if __name__ == '__main__':
    args = get_args()
    file_name, origin, dest = args

    world = read_file(file_name)

    route, final_dist = find_path(world, origin, dest)

    list_route = get_path(route, origin, dest)

    print_output(world, list_route, final_dist, origin, dest)
