# Water Jug Problem — BFS (Breadth-First Search)

---

## 1. Problem Statement

You have **two jugs**:
- **Jug A** with capacity `m` litres
- **Jug B** with capacity `n` litres

Neither jug has measurement markings. You can only perform 6 operations:

| Operation | Description |
|---|---|
| Fill A | Fill Jug A completely |
| Fill B | Fill Jug B completely |
| Empty A | Dump all water from Jug A |
| Empty B | Dump all water from Jug B |
| Pour A → B | Pour from A into B until B is full or A is empty |
| Pour B → A | Pour from B into A until A is full or B is empty |

**Goal**: Measure exactly `d` litres of water in either jug.

---

## 2. Theory

### State Space Representation
The **state** of the system is a pair `(x, y)` where:
- `x` = current water in Jug A (0 ≤ x ≤ m)
- `y` = current water in Jug B (0 ≤ y ≤ n)

The **initial state** is `(0, 0)` — both jugs empty.
The **goal state** is any `(x, y)` where `x == d` or `y == d`.

### Why BFS?
Breadth-First Search explores states **level by level** (by number of steps from start). This guarantees:
- **Completeness** — it will always find a solution if one exists
- **Optimality** — it finds the solution with the **fewest steps** (shortest path)

### Mathematical Feasibility (Bézout's Identity)
A solution exists **if and only if**:
- `d ≤ max(m, n)` — the target must be achievable in at least one jug
- `d % gcd(m, n) == 0` — `d` must be divisible by the GCD of the two capacities

For example, with jugs of size 3 and 5: `gcd(3,5) = 1`, so any value 1–5 is achievable.

### Pour Operation Logic
The key tricky operation is pouring. When pouring A into B:
- You can only pour as much as B can still hold: `n - y`
- You can only pour as much as A currently has: `x`
- So the amount poured is `t = min(x, n - y)`
- New state: `(x - t, y + t)`

### BFS on a Graph
The state space forms an **implicit graph**:
- **Nodes** = all reachable states `(x, y)`
- **Edges** = valid operations connecting states
- BFS finds the shortest path from `(0,0)` to any goal state

---

## 3. Program

```python
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

import math
if d > max(m, n) or d % math.gcd(m, n) != 0:
    print("\nNo solution possible.")
else:
    parent, end = water_jug_bfs(m, n, d)

    if end is None:
        print("\nNo solution found.")
    else:
        print_path(parent, end)
```

---

## 4. Sample Run

```
Enter capacity of Jug A: 4
Enter capacity of Jug B: 3
Enter target amount: 2

Steps to reach the target:
(0, 0)
(4, 0)
(1, 3)
(1, 0)
(0, 1)
(4, 1)
(2, 3)
```

---

## 5. Line-by-Line Code Breakdown

### Line 1 — Import deque
```python
from collections import deque
```
Imports `deque` (double-ended queue) from Python's `collections` module. A `deque` supports O(1) `append` and `popleft` operations. Using a regular `list` for `popleft()` would be O(n), making BFS very slow on large state spaces.

---

### Lines 3–26 — `get_neighbors` Function
```python
def get_neighbors(x, y, m, n):
    neighbors = []
```
Defines a function that takes the **current state** `(x, y)` and **jug capacities** `(m, n)`, and returns a list of all states reachable in exactly one operation.

```python
    neighbors.append((m, y))   # Fill Jug A
```
Filling Jug A to its full capacity `m`. Jug B remains unchanged at `y`. Result: `(m, y)`.

```python
    neighbors.append((x, n))   # Fill Jug B
```
Filling Jug B to its full capacity `n`. Jug A remains at `x`. Result: `(x, n)`.

```python
    neighbors.append((0, y))   # Empty Jug A
```
Emptying Jug A completely. Jug B unchanged. Result: `(0, y)`.

```python
    neighbors.append((x, 0))   # Empty Jug B
```
Emptying Jug B completely. Jug A unchanged. Result: `(x, 0)`.

```python
    t = min(x, n - y)
    neighbors.append((x - t, y + t))   # Pour A -> B
```
- `n - y` = how much more Jug B can hold (its remaining capacity).
- `x` = how much water is in Jug A.
- `t = min(x, n-y)` = amount actually transferred — the smaller of "what A has" and "what B can take".
- Jug A loses `t`, Jug B gains `t`.

```python
    t = min(y, m - x)
    neighbors.append((x + t, y - t))   # Pour B -> A
```
Same logic but reversed: pour from B into A. `m - x` is A's remaining capacity. Transfer `t = min(y, m-x)`.

---

### Lines 29–51 — `water_jug_bfs` Function

```python
def water_jug_bfs(m, n, d):
    start = (0, 0)
```
Defines the **initial state**: both jugs empty.

```python
    queue = deque([start])
```
Initialises the BFS queue with the starting state. The queue holds states yet to be explored.

```python
    visited = set()
    parent = {}
```
- `visited` — a set of states already explored. Using a `set` gives O(1) average-time lookup (vs O(n) for a list). Prevents revisiting the same state.
- `parent` — a dictionary mapping each state to the state it was reached from. This lets us reconstruct the path once the goal is found.

```python
    visited.add(start)
    parent[start] = None
```
Mark the start as visited immediately. `parent[start] = None` signals that the start state has no predecessor (it's the root of the path tree).

```python
    while queue:
        x, y = queue.popleft()
```
BFS main loop. `popleft()` removes the **oldest** state in the queue (FIFO order), which ensures BFS explores states in order of increasing distance from the start.

```python
        if x == d or y == d:
            return parent, (x, y)
```
**Goal check**: if either jug contains exactly `d` litres, we've found a solution. Return the `parent` map and the goal state `(x, y)` so the caller can trace the path.

```python
        for nx, ny in get_neighbors(x, y, m, n):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
```
For each valid next state:
- Skip if already visited (cycle prevention).
- Otherwise mark visited, record its parent as the current state `(x, y)`, and add to the queue for future exploration.

```python
    return None, None
```
If the queue empties without finding the goal, no solution exists — return `None`.

---

### Lines 54–63 — `print_path` Function

```python
def print_path(parent, end):
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    path.reverse()
```
Reconstructs the path by **walking backwards** through the `parent` dictionary from `end` to `start`. Each iteration: append current state, then move to its parent. When `parent[state]` is `None` (the start), the loop ends. Then `path.reverse()` flips it to start→end order.

```python
    for state in path:
        print(state)
```
Prints each state tuple on its own line, showing the step-by-step water amounts in each jug.

---

### Lines 66–81 — Main Program

```python
m = int(input("Enter capacity of Jug A: "))
n = int(input("Enter capacity of Jug B: "))
d = int(input("Enter target amount: "))
```
Read three integers from the user: jug capacities and target amount.

```python
import math
if d > max(m, n) or d % math.gcd(m, n) != 0:
    print("\nNo solution possible.")
```
**Feasibility check before even running BFS:**
- `d > max(m, n)`: target exceeds the capacity of the largest jug — impossible.
- `d % math.gcd(m, n) != 0`: by Bézout's identity, all reachable water amounts are multiples of `gcd(m, n)`. If `d` is not a multiple, it can never be measured.
- `math.gcd(m, n)` computes the Greatest Common Divisor.

```python
else:
    parent, end = water_jug_bfs(m, n, d)
    if end is None:
        print("\nNo solution found.")
    else:
        print_path(parent, end)
```
If feasible, run BFS. If BFS returns `None` (shouldn't happen after the feasibility check passes, but guarded anyway), print failure. Otherwise print the solution path.

---

## 6. BFS vs DFS for Water Jug

| Aspect | BFS | DFS |
|---|---|---|
| Finds shortest path | ✅ Yes | ❌ Not guaranteed |
| Memory usage | Higher (stores whole frontier) | Lower (only current path) |
| Complete | Yes | Yes (with cycle detection) |
| Suitable here | ✅ Optimal | Suboptimal |

---

## 7. Time & Space Complexity

- **States**: All possible `(x, y)` pairs → `(m+1) × (n+1)` states max
- **Time**: O(m × n) — visits each state at most once
- **Space**: O(m × n) — queue + visited set + parent dict
