from collections import deque

def get_neighbors(x, y, m, n):
    neighbors = []

    # Fill Jug A
    neighbors.append((m, y))

    # Fill Jug B
    neighbors.append((x, n))

    # Empty Jug A
    neighbors.append((0, y))

    # Empty Jug B
    neighbors.append((x, 0))

    # Pour A -> B
    t = min(x, n - y)
    neighbors.append((x - t, y + t))

    # Pour B -> A
    t = min(y, m - x)
    neighbors.append((x + t, y - t))

    return neighbors


def water_jug_bfs(m, n, d):
    start = (0, 0)
    queue = deque([start])
    visited = set()
    parent = {}

    visited.add(start)
    parent[start] = None

    while queue:
        x, y = queue.popleft()

        # Check goal
        if x == d or y == d:
            return parent, (x, y)

        for nx, ny in get_neighbors(x, y, m, n):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return None, None


def print_path(parent, end):
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    path.reverse()

    print("\nSteps to reach the target:")
    for state in path:
        print(state)


# -------- Main Program --------
m = int(input("Enter capacity of Jug A: "))
n = int(input("Enter capacity of Jug B: "))
d = int(input("Enter target amount: "))

# Mathematical feasibility check
import math
if d > max(m, n) or d % math.gcd(m, n) != 0:
    print("\nNo solution possible.")
else:
    parent, end = water_jug_bfs(m, n, d)

    if end is None:
        print("\nNo solution found.")
    else:
        print_path(parent, end)
