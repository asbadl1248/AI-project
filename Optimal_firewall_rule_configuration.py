
# قاعدة البيانات الأساسية للقواعد
all_possible_rules = [
    ("ALLOW", "192.168.1.*", "80"),
    ("DENY", "10.0.0.5", "22"),
    ("ALLOW", "*", "443"),
    ("DENY", "10.0.0.0/24", "23"),
    ("ALLOW", "172.16.*.*", "8080")
]

# ------------------------- Genetic Algorithm (GA) -------------------------

def firewall_fitness(rules):
    conflicts = sum(1 for r1 in rules for r2 in rules if r1[1] == r2[1] and r1[2] == r2[2] and r1[0] != r2[0])
    return 1 / (1 + conflicts + len(rules))

def firewall_crossover(parent1, parent2):
    return list(set(parent1[:len(parent1)//2] + parent2[len(parent2)//2:]))

def firewall_mutate(rules):
    if random.random() < 0.1:
        if rules and random.random() < 0.5:
            rules.pop(random.randint(0, len(rules)-1))
        else:
            rules.append(random.choice(all_possible_rules))
    return rules

def firewall_ga(pop_size=50, generations=100):
    population = [random.sample(all_possible_rules, k=random.randint(1, 3)) for _ in range(pop_size)]
    for _ in range(generations):
        population = sorted(population, key=firewall_fitness, reverse=True)
        if firewall_fitness(population[0]) == 1:
            return population[0]
        new_pop = population[:5]
        while len(new_pop) < pop_size:
            p1, p2 = random.choices(population[:20], k=2)
            child = firewall_mutate(firewall_crossover(p1, p2))
            new_pop.append(child)
    return population[0]

# ------------------------- A* Search -------------------------

class FirewallNode:
    def __init__(self, rules, cost):
        self.rules = rules
        self.cost = cost + sum(1 for r in rules if r not in all_possible_rules)

    def __lt__(self, other):
        return self.cost < other.cost

def has_conflicts(rules):
    conflicts = sum(1 for r1 in rules for r2 in rules if r1[1] == r2[1] and r1[2] == r2[2] and r1[0] != r2[0])
    return conflicts > 0

def firewall_a_star():
    heap = [FirewallNode([], 0)]
    while heap:
        heap.sort(key=lambda x: x.cost)
        node = heap.pop(0)
        if all(r in all_possible_rules for r in node.rules) and not has_conflicts(node.rules):
            return node.rules
        for rule in all_possible_rules:
            new_rules = node.rules + [rule]
            heap.append(FirewallNode(new_rules, node.cost + 1))
    return None

# ------------------------- Uniform Cost Search (UCS) -------------------------

def firewall_ucs():
    queue = [(0, [])]
    while queue:
        cost, rules = queue.pop(0)
        if not has_conflicts(rules):
            return rules
        for rule in all_possible_rules:
            new_rules = rules + [rule]
            queue.append((cost + 1, new_rules))
    return None

# ------------------------- BFS -------------------------

def firewall_bfs():
    queue = [[]]
    while queue:
        rules = queue.pop(0)
        if not has_conflicts(rules):
            return rules
        for rule in all_possible_rules:
            queue.append(rules + [rule])
    return None

# ------------------------- DFS -------------------------

def firewall_dfs():
    stack = [[]]
    while stack:
        rules = stack.pop()
        if not has_conflicts(rules):
            return rules
        for rule in reversed(all_possible_rules):
            stack.append(rules + [rule])
    return None

# اختبار
ga_rules = firewall_ga()
print("GA Rules:", ga_rules if ga_rules else "No valid rules found.")

a_star_rules = firewall_a_star()
print("A* Rules:", a_star_rules if a_star_rules else "No valid rules found.")

ucs_rules = firewall_ucs()
print("UCS Rules:", ucs_rules if ucs_rules else "No valid rules found.")

bfs_rules = firewall_bfs()
print("BFS Rules:", bfs_rules if bfs_rules else "No valid rules found.")

dfs_rules = firewall_dfs()
print("DFS Rules:", dfs_rules if dfs_rules else "No valid rules found.")
