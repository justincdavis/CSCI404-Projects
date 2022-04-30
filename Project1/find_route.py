import sys
import time
from collections import defaultdict
from queue import PriorityQueue
import os


def get_args():
    try:
        return sys.argv[1], sys.argv[2], sys.argv[3]
    except IndexError:
        return sys.argv[1], None, None


def read_file(filename):
    filename = "maps/" + filename
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


def compute_max_distance(graph):
    total_distance = 0
    for city, connections in graph.items():
        for con_city, distance in connections.items():
            total_distance += distance
    return total_distance / 2


def find_path(graph, origin_city, dest_city, max_time=60.0):
    start_time = time.perf_counter()

    queue = PriorityQueue()
    queue.put((0, (origin_city, origin_city)))

    path = {origin_city: (origin_city, 0)}

    max_distance = compute_max_distance(graph)

    while not queue.empty():
        distance, (city1, city2) = queue.get()

        total_time = time.perf_counter() - start_time
        if distance > max_distance or total_time > max_time:
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


def print_output(graph, path, distance, dest_city, print_out=True):
    output_str = []
    if path is None:
        output_str.append("distance: infinity")
        output_str.append("route")
        output_str.append("none")
    else:
        output_str.append(f"distance: {distance}")
        output_str.append("route")
        for idx, city in enumerate(path):
            if idx < len(path) - 1:
                next_city = path[idx + 1]
                output_str.append(f"{city} to {next_city}, {graph[city][next_city]}km")
            else:
                dist = 0 if city == dest_city else graph[city][dest_city]
                output_str.append(f"{city} to {dest_city}, {dist}km")
        output_str = output_str if len(output_str) <= 3 else output_str[0:len(output_str)-1]
    if print_out:
        for line in output_str:
            print(line)
    return output_str


def get_test_files(test_name, test_dir='tests/'):
    test_files = []
    for root, dirs, files in os.walk(test_dir, topdown=False):
        for name in files:
            if test_name in os.path.join(root, name):
                test_files.append(os.path.join(root, name))
    return test_files


def run_tests(maps=('input1', 'custom')):
    for graph in maps:
        world_map = read_file(graph + '.txt')
        test_files = get_test_files(graph)
        for test_file in test_files:
            with open(test_file, 'r') as f:
                lines = f.readlines()
            lines = [line.strip() for line in lines]
            input_data = lines[0].split(' ')
            test_data = lines[1:-1]
            bfs_route, distance = find_path(world_map, input_data[0], input_data[1])
            final_route = get_path(bfs_route, input_data[0], input_data[1])
            output_str = print_output(world_map, final_route, distance, input_data[1], print_out=False)

            for out_line, test_line in zip(output_str, test_data):
                assert out_line == test_line
            print(f"PASSED TEST: {test_file}")


if __name__ == '__main__':
    args = get_args()
    file_name, origin, dest = args

    if file_name.lower() == 'test':
        run_tests()
        exit(0)

    world = read_file(file_name)

    route, final_dist = find_path(world, origin, dest)

    list_route = get_path(route, origin, dest)

    _ = print_output(world, list_route, final_dist, dest)
