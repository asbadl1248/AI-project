import random
import heapq
import collections
import time

# تعريف كلمة المرور الحقيقية
TARGET_PASSWORD = "Sal"
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

# دالة لإنشاء كروموسوم عشوائي
def create_chromosome(length):
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

# دالة لحساب اللياقة
def fitness(chromosome):
    return sum(1 for a, b in zip(chromosome, TARGET_PASSWORD) if a == b)

# دالة لاختيار أفضل الكروموسومات
def selection(population):
    population.sort(key=fitness, reverse=True)
    return population[:len(population) // 2]

# دالة لدمج الكروموسومات
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

# دالة للطفرات
def mutate(chromosome):
    if random.random() < 0.1:
        index = random.randint(0, len(chromosome) - 1)
        new_char = random.choice(CHARACTERS)
        chromosome = chromosome[:index] + new_char + chromosome[index + 1:]
    return chromosome

# تنفيذ الخوارزمية الجينية
def genetic_algorithm():
    population_size = 100
    generations = 1000
    population = [create_chromosome(len(TARGET_PASSWORD)) for _ in range(population_size)]
    
    for generation in range(generations):
        population = selection(population)
        next_generation = []

        # إنتاج الجيل الجديد
        while len(next_generation) < population_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)

        population = next_generation
        
        # تحقق من الحل
        best = max(population, key=fitness)
        if fitness(best) == len(TARGET_PASSWORD):
            print(f"GA Found password: {best} in generation {generation}")
            return True
    return False

# دالة لحساب تكلفة التخمين
def heuristic(guess):
    return sum(1 for a, b in zip(guess, TARGET_PASSWORD) if a != b)

# دالة A* للبحث
def a_star():
    open_set = []
    heapq.heappush(open_set, (0, ""))  # (التكلفة, التخمين)

    while open_set:
        cost, guess = heapq.heappop(open_set)

        # تحقق من الحل
        if guess == TARGET_PASSWORD:
            print(f"A* Found password: {guess}")
            return True

        # توليد التخمينات الجديدة
        for char in CHARACTERS:
            new_guess = guess + char
            if len(new_guess) <= len(TARGET_PASSWORD):
                total_cost = cost + heuristic(new_guess)
                heapq.heappush(open_set, (total_cost, new_guess))
    return False

# دالة UCS
def ucs():
    pq = collections.deque()
    pq.append((0, ""))  # (التكلفة, التخمين)

    while pq:
        cost, guess = pq.popleft()

        # تحقق من الحل
        if guess == TARGET_PASSWORD:
            print(f"UCS Found password: {guess}")
            return True

        # توليد التخمينات الجديدة
        for char in CHARACTERS:
            new_guess = guess + char
            if len(new_guess) <= len(TARGET_PASSWORD):
                new_cost = cost + 1  # كل تخمين له تكلفة ثابتة
                pq.append((new_cost, new_guess))
    return False

# دالة BFS
def bfs():
    queue = collections.deque([""])  # قائمة انتظار للتخمينات

    while queue:
        guess = queue.popleft()

        # تحقق من الحل
        if guess == TARGET_PASSWORD:
            print(f"BFS Found password: {guess}")
            return True

        # توليد التخمينات الجديدة
        for char in CHARACTERS:
            new_guess = guess + char
            if len(new_guess) <= len(TARGET_PASSWORD):
                queue.append(new_guess)
    return False

# دالة DFS
def dfs(guess=""):
    # تحقق من الحل
    if guess == TARGET_PASSWORD:
        print(f"DFS Found password: {guess}")
        return True

    # توليد التخمينات الجديدة
    for char in CHARACTERS:
        new_guess = guess + char
        if len(new_guess) <= len(TARGET_PASSWORD):
            if dfs(new_guess):  # البحث في العمق
                return True
    return False

# دالة لتشغيل جميع الخوارزميات مع قياس الوقت
def run_password_guesses():
    start_time = time.time()
    genetic_algorithm()
    print(f"GA Execution Time: {time.time() - start_time:.4f} seconds")

    start_time = time.time()
    a_star()
    print(f"A* Execution Time: {time.time() - start_time:.4f} seconds")

    start_time = time.time()
    ucs()
    print(f"UCS Execution Time: {time.time() - start_time:.4f} seconds")

    start_time = time.time()
    bfs()
    print(f"BFS Execution Time: {time.time() - start_time:.4f} seconds")

    start_time = time.time()
    dfs()
    print(f"DFS Execution Time: {time.time() - start_time:.4f} seconds")

# تشغيل جميع الخوارزميات
run_password_guesses()
