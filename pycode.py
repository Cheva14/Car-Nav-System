graph = {
    "Manchester": {"Liverpool": 40, "York": 70, "Carlisle": 120, "Newcastle": 140, "Edinburgh": 220},
    "Holyhead": {"Liverpool": 90},
    "Liverpool": {"Manchester": 40, "Holyhead": 90},
    "York": {"Manchester": 70, "Newcastle": 80},
    "Carlisle": {"Manchester": 120, "Glasgow": 100},
    "Newcastle": {"Manchester": 140, "York": 80, "Edinburgh": 110},
    "Glasgow": {"Carlisle": 100, "Edinburgh": 50, "Oban": 100, "Aberdeen": 140, "Inverness": 170},
    "Edinburgh": {"Manchester": 220, "Newcastle": 110, "Glasgow": 50},
    "Oban": {"Glasgow": 100, "Inverness": 110},
    "Aberdeen": {"Glasgow": 140, "Inverness": 110},
    "Inverness": {"Glasgow": 170, "Oban": 110, "Aberdeen": 110}
}


def valid_city(city):
    if city in graph:
        return True
    return False


from math import radians, sin, cos, sqrt, asin

def haversine(lat1, lon1, lat2, lon2):
    R = 3956  # radius of the earth in miles
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = R * c
    return round(distance)

coordinates = {
    "Manchester": (53.4808, -2.2426),
    "Holyhead": (53.3084, -4.6314),
    "Liverpool": (53.4084, -2.9916),
    "York": (53.9599, -1.0873),
    "Carlisle": (54.8924, -2.9323),
    "Newcastle": (54.9783, -1.6178),
    "Glasgow": (55.8642, -4.2518),
    "Edinburgh": (55.9533, -3.1883),
    "Oban": (56.4124, -5.4700),
    "Aberdeen": (57.1497, -2.0943),
    "Inverness": (57.4778, -4.2247)
}

def get_distances(city):
    distances = {}
    for other_cities in coordinates:
        if other_cities != city:
            lat1, lon1 = coordinates[city]
            lat2, lon2 = coordinates[other_cities]
            distances[other_cities] = haversine(lat1, lon1, lat2, lon2)
        distances[other_cities] = 0
    return distances


def dfs(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return [goal]
    for neighbor in graph[start]:
        if neighbor not in visited:
            path = dfs(graph, neighbor, goal, visited)
            if path:
                return [start] + path
    return None

def print_dfs(graph, start, goal):
    path = dfs(graph, start, goal)
    if path:
        distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        print(f"The path from {start} to {goal} using depth first search is: {' -> '.join(path)} and the distance is: {distance} miles.")
    else:
        print("No path found.")


from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

def print_bfs(graph, start, goal):
    path = bfs(graph, start, goal)
    if path:
        distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        print(f"The path from {start} to {goal} using breadth first search is: {' -> '.join(path)} and the distance is: {distance} miles.")
    else:
        print("No path found.")


from queue import PriorityQueue

def astar(graph, start, goal, heuristic):
    queue = PriorityQueue()
    queue.put((0, start))
    visited = {start: None}
    g_score = {start: 0}
    while not queue.empty():
        (f, current) = queue.get()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return path
        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + graph[current][neighbor]
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f = g_score[neighbor] + heuristic[neighbor]
                queue.put((f, neighbor))
                visited[neighbor] = current
    return None

def print_astar(graph, start, goal, heuristic):
    path = astar(graph, start, goal, heuristic)
    if path:
        distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        print(f"The path from {start} to {goal} using A* search is: {' -> '.join(path)} and the distance is: {distance} miles.")
    else:
        print("No path found.")


def gbfs(graph, start, goal, heuristic):
    queue = PriorityQueue()
    queue.put((heuristic[start], start))
    visited = {start: None}
    while not queue.empty():
        (_, current) = queue.get()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.put((heuristic[neighbor], neighbor))
                visited[neighbor] = current
    return None

def print_gbfs(graph, start, goal, heuristic):
    path = gbfs(graph, start, goal, heuristic)
    if path:
        distance = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        print(f"The path from {start} to {goal} using greedy best-first search is: {' -> '.join(path)} and the distance is: {distance} miles.")
    else:
        print("No path found.")


def run_program():
    while (True):
        run = ""
        start = input("Enter the starting city: ")
        if valid_city(start):
            while (True):
                goal = input("Enter the ending city: ")
                if valid_city(goal):
                    heuristic = get_distances(goal)
                    print_dfs(graph, start, goal)
                    print_bfs(graph, start, goal)
                    print_astar(graph, start, goal, heuristic)
                    print_gbfs(graph, start, goal, heuristic)
                    run = input("If you want to stop, then type 'stop', if you want to continue, then type anything: ")
                    break
                else:
                    print(f"{goal} is not a valid city name, try: Manchester, Holyhead, Liverpool, York, Carlisle, Newcastle, Glasgow, Edinburgh, Oban, Aberdeen or Inverness")
        else:
            print(f"{start} is not a valid city name, try: Manchester, Holyhead, Liverpool, York, Carlisle, Newcastle, Glasgow, Edinburgh, Oban, Aberdeen or Inverness")
        if (run == "stop"):
            print("Goodbye!")
            break
            
run_program()