

# تعريف الرسم البياني
graph = {
    'A': {'B': (2, 5), 'C': (4, 1)},
    'B': {'D': (5, 3)},
    'C': {'D': (1, 4)},
    'D': {}
}

# ------------------------- Genetic Algorithm (GA) -------------------------
def path_to_chromosome(path):
    return ''.join(path)

def chromosome_to_path(chromo):
    return list(chromo)

def path_fitness(path):
    if not valid_path(path):
        return 0
    security = sum(graph[path[i]][path[i + 1]][1] for i in range(len(path) - 1))
    return security

def valid_path(path):
    for i in range(len(path) - 1):
        if path[i + 1] not in graph[path[i]]:
            return False
    return True

def path_ga(start, end, pop_size=50, generations=100):
    population = [path_to_chromosome([start]) for _ in range(pop_size)]
    for _ in range(generations):
        population = sorted(population, key=lambda x: path_fitness(chromosome_to_path(x)), reverse=True)
        best_path = chromosome_to_path(population[0])
        if best_path[-1] == end:
            return best_path
        new_pop = population[:10]
        while len(new_pop) < pop_size:
            p1, p2 = random.choices(population[:20], k=2)
            child = p1[:len(p1) // 2] + p2[len(p2) // 2:]
            if random.random() < 0.1:
                child = child[:-1] + random.choice(list(graph.keys()))
            new_pop.append(child)
    return None

# ------------------------- A* Search -------------------------
def a_star_secure(start, end):
    heap = [(0, start, [])]
    visited = set()
    
    while heap:
        cost, node, path = heap.pop(0)
        if node == end:
            return path + [node]
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, (dist, security) in graph[node].items():
            new_cost = cost + dist + (10 - security)
            heap.append((new_cost, neighbor, path + [node]))
            heap.sort()
    return None

# ------------------------- Uniform Cost Search (UCS) -------------------------
def ucs_secure(start, end):
    queue = [(0, start, [])]
    visited = set()
    
    while queue:
        cost, node, path = queue.pop(0)
        if node == end:
            return path + [node]
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, (dist, security) in graph[node].items():
            new_cost = cost + dist
            queue.append((new_cost, neighbor, path + [node]))
            queue.sort()
    return None

# ------------------------- BFS -------------------------
def bfs_secure(start, end):
    queue = [[start]]
    visited = set()
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor in graph[node]:
            queue.append(path + [neighbor])
    return None

# ------------------------- DFS -------------------------
def dfs_secure(start, end):
    stack = [[start]]
    visited = set()
    
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == end:
            return path
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor in reversed(list(graph[node].keys())):
            stack.append(path + [neighbor])
    return None

def execute_algorithm(name, func, start, end):
    print(f"\n--- {name} ---")
    start_time = time.time()
    result = func(start, end)
    end_time = time.time()
    if result:
        print(f"Path: {result}")
    else:
        print("No path found.")
    print(f"Execution time: {end_time - start_time:.6f} seconds")

# تنفيذ الخوارزميات
execute_algorithm("Genetic Algorithm (GA)", path_ga, 'A', 'D')
execute_algorithm("A* Search", a_star_secure, 'A', 'D')
execute_algorithm("Uniform Cost Search (UCS)", ucs_secure, 'A', 'D')
execute_algorithm("Breadth-First Search (BFS)", bfs_secure, 'A', 'D')
execute_algorithm("Depth-First Search (DFS)", dfs_secure, 'A', 'D')
