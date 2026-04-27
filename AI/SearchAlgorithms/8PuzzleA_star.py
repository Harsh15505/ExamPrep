# Heuristic: Manhattan Distance
def heuristic(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(goal.index(state[i][j]), 3)
                distance += abs(x - i) + abs(y - j)
    return distance

# Find blank tile position
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate neighbors
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# A* Algorithm without heap
def a_star(start, goal):
    goal_flat = sum(goal, [])

    open_list = [start]
    closed_list = set()
    parent = {}
    g_cost = {tuple(map(tuple, start)): 0}

    while open_list:
        # Select node with minimum f(n)
        current = min(
            open_list,
            key=lambda s: g_cost[tuple(map(tuple, s))] + heuristic(s, goal_flat)
        )

        if current == goal:
            path = []
            while tuple(map(tuple, current)) in parent:
                path.append(current)
                current = parent[tuple(map(tuple, current))]
            path.append(start)
            return path[::-1]

        open_list.remove(current)
        closed_list.add(tuple(map(tuple, current)))

        for neighbor in get_neighbors(current):
            neighbor_t = tuple(map(tuple, neighbor))
            tentative_g = g_cost[tuple(map(tuple, current))] + 1

            if neighbor_t in closed_list:
                continue

            if neighbor not in open_list or tentative_g < g_cost.get(neighbor_t, float('inf')):
                parent[neighbor_t] = current
                g_cost[neighbor_t] = tentative_g
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None

# -------- Main Program --------
print("Enter Initial State (use 0 for blank):")
start = [list(map(int, input().split())) for _ in range(3)]

print("Enter Goal State:")
goal = [list(map(int, input().split())) for _ in range(3)]

solution = a_star(start, goal)

if solution:
    print("\nSolution Path:")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No solution found.")
