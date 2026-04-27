# 8-Puzzle Problem — A* (A-Star) Search

---

## 1. Problem Statement

The **8-Puzzle** is a sliding tile puzzle on a **3×3 grid** containing tiles numbered 1–8 and one blank space (`0`). Tiles adjacent to the blank can slide into it.

**Goal**: Transform a given initial configuration into a target goal configuration by sliding tiles.

```
Initial State        Goal State
┌───┬───┬───┐       ┌───┬───┬───┐
│ 1 │ 2 │ 3 │       │ 1 │ 2 │ 3 │
├───┼───┼───┤       ├───┼───┼───┤
│ 4 │   │ 6 │  →    │ 4 │ 5 │ 6 │
├───┼───┼───┤       ├───┼───┼───┤
│ 7 │ 5 │ 8 │       │ 7 │ 8 │   │
└───┴───┴───┘       └───┴───┴───┘
```

---

## 2. Theory

### State Representation
A state is the full 3×3 grid as a list of lists. The blank tile is represented by `0`.

### A* Algorithm
A* is an **informed (heuristic) best-first search** algorithm. It is the most widely used pathfinding algorithm in AI because it is both **complete** and **optimal** when using an admissible heuristic.

**Core formula:**
```
f(n) = g(n) + h(n)
```
| Symbol | Meaning |
|---|---|
| `g(n)` | Cost to reach node `n` from start (number of moves made so far) |
| `h(n)` | Estimated cost from `n` to goal (heuristic — educated guess) |
| `f(n)` | Total estimated cost of the cheapest solution through `n` |

A* always expands the node with the **lowest `f(n)`** first — it is greedy toward the goal but also accounts for the path cost so far.

### Heuristic: Manhattan Distance
The **Manhattan Distance** for a tile is the sum of its horizontal and vertical displacement from its goal position.

```
For tile at position (r, c) that should be at (gr, gc):
  manhattan = |r - gr| + |c - gc|
```

Total h(n) = sum of Manhattan distances of all tiles (excluding blank).

**Why Manhattan Distance?**
- It is **admissible**: it never overestimates the actual number of moves (each move can only reduce a tile's distance by 1).
- It is **consistent** (monotonic): satisfies the triangle inequality.
- It is much more informative than simply counting misplaced tiles.

### Open List & Closed List
| List | Purpose |
|---|---|
| **Open List** | States discovered but not yet fully explored (candidates) |
| **Closed List** | States already expanded — never revisit these |

At each step:
1. Pick the state with lowest `f(n)` from open list.
2. If it's the goal → reconstruct path.
3. Otherwise move it to closed list, expand its neighbors, update open list.

### Solvability
Not all 8-puzzle states are solvable. A state is solvable if and only if the number of **inversions** has the same parity as the goal state. (The program does not check this — it will return `None` if unsolvable.)

---

## 3. Program

```python
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
```

---

## 4. Sample Run

```
Enter Initial State (use 0 for blank):
1 2 3
4 0 6
7 5 8

Enter Goal State:
1 2 3
4 5 6
7 8 0

Solution Path:
[1, 2, 3]
[4, 0, 6]
[7, 5, 8]

[1, 2, 3]
[4, 5, 6]
[7, 0, 8]

[1, 2, 3]
[4, 5, 6]
[7, 8, 0]
```

---

## 5. Line-by-Line Code Breakdown

### Lines 1–9 — `heuristic` Function (Manhattan Distance)

```python
def heuristic(state, goal):
    distance = 0
```
Initialises the total Manhattan distance to 0. This will accumulate the displacement of every tile from its goal position.

```python
    for i in range(3):
        for j in range(3):
```
Nested loops iterate over every cell `(i, j)` in the 3×3 grid.

```python
            if state[i][j] != 0:
```
Skip the blank tile (`0`). The blank has no fixed goal position in the heuristic calculation.

```python
                x, y = divmod(goal.index(state[i][j]), 3)
```
- `goal` is passed as a **flat list** (e.g., `[1,2,3,4,5,6,7,8,0]`).
- `goal.index(state[i][j])` finds the **1D index** of the current tile in the goal list.
- `divmod(idx, 3)` converts the 1D index to `(row, col)` in the 3×3 grid: `row = idx // 3`, `col = idx % 3`.
- So `x, y` is where this tile **should be** in the goal state.

```python
                distance += abs(x - i) + abs(y - j)
```
Adds the **Manhattan distance** for this tile: the sum of the absolute row difference and absolute column difference between current position `(i, j)` and goal position `(x, y)`.

---

### Lines 11–16 — `find_blank` Function

```python
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
```
Scans the 3×3 grid to find and return the `(row, col)` position of the blank tile (`0`). The blank's position is needed to know which tiles can slide.

---

### Lines 18–30 — `get_neighbors` Function

```python
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
```
- Finds the blank's position `(x, y)`.
- Defines the 4 possible slide directions: UP `(-1,0)`, DOWN `(1,0)`, LEFT `(0,-1)`, RIGHT `(0,1)`. These represent the direction the **blank moves**, which is equivalent to a tile sliding the opposite way.

```python
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
```
For each direction, compute the new blank position `(nx, ny)`. The bounds check `0 <= nx < 3 and 0 <= ny < 3` ensures we don't move the blank off the grid.

```python
            new_state = [row[:] for row in state]
```
Creates a **deep copy** of the current state (list of lists). `row[:]` makes a shallow copy of each row, and the list comprehension copies all rows. This is essential — without copying, modifying `new_state` would modify `state`.

```python
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
```
Python **simultaneous assignment** to swap the blank `(x, y)` with the tile at `(nx, ny)`. This simulates the tile sliding into the blank's position.

```python
            neighbors.append(new_state)
    return neighbors
```
Adds the new state to the neighbors list and returns all generated neighbors.

---

### Lines 32–72 — `a_star` Function

```python
def a_star(start, goal):
    goal_flat = sum(goal, [])
```
`sum(goal, [])` flattens the 3×3 list of lists `goal` into a 1D list. This is a Python idiom: `sum([[1,2],[3,4]], [])` = `[1,2,3,4]`. The flat list is needed by the `heuristic` function's `goal.index()` call.

```python
    open_list = [start]
    closed_list = set()
    parent = {}
    g_cost = {tuple(map(tuple, start)): 0}
```
- `open_list` — list of states to be explored. Starts with just the initial state.
- `closed_list` — set of already-explored state tuples (hashable). Sets give O(1) lookup.
- `parent` — maps each state's tuple representation to its predecessor state. Used for path reconstruction.
- `g_cost` — maps each state tuple to its `g(n)` cost (number of moves from start). The start state has g=0.
- `tuple(map(tuple, start))` converts the list-of-lists to a tuple-of-tuples so it can be used as a dictionary key (lists are not hashable).

```python
        current = min(
            open_list,
            key=lambda s: g_cost[tuple(map(tuple, s))] + heuristic(s, goal_flat)
        )
```
Selects the state with the **minimum `f(n) = g(n) + h(n)`** from the open list. This is the core A* selection step. `lambda s:` defines an anonymous function that computes `f` for any state `s`. `min(..., key=...)` returns the state with the smallest `f` value.

> Note: Using `min()` on a list is O(n) per step. A proper A* uses a **priority queue (heap)** for O(log n) extraction, but this simpler version is correct for small puzzles.

```python
        if current == goal:
            path = []
            while tuple(map(tuple, current)) in parent:
                path.append(current)
                current = parent[tuple(map(tuple, current))]
            path.append(start)
            return path[::-1]
```
**Goal check**: when `current == goal`, reconstruct the path. Walk backwards through `parent` from the goal to the start, collecting each state. `path[::-1]` reverses the list so it runs start→goal.

```python
        open_list.remove(current)
        closed_list.add(tuple(map(tuple, current)))
```
Move `current` from open to closed. It has been fully processed.

```python
        for neighbor in get_neighbors(current):
            neighbor_t = tuple(map(tuple, neighbor))
            tentative_g = g_cost[tuple(map(tuple, current))] + 1
```
For each neighbor:
- `neighbor_t` — hashable tuple form of the neighbor.
- `tentative_g` — the `g` cost if we reach this neighbor via `current`. Since each move costs 1, it's `g(current) + 1`.

```python
            if neighbor_t in closed_list:
                continue
```
Skip states already in the closed list — they have already been optimally processed.

```python
            if neighbor not in open_list or tentative_g < g_cost.get(neighbor_t, float('inf')):
                parent[neighbor_t] = current
                g_cost[neighbor_t] = tentative_g
                if neighbor not in open_list:
                    open_list.append(neighbor)
```
Update the neighbor if:
- It hasn't been seen yet (not in open list), OR
- We found a cheaper path to it (`tentative_g` is less than the currently recorded cost).

`g_cost.get(neighbor_t, float('inf'))` returns infinity if the state hasn't been seen, ensuring the condition is true for new states.

---

### Lines 74–91 — Main Program

```python
start = [list(map(int, input().split())) for _ in range(3)]
```
A list comprehension that reads 3 lines of input. Each line is split on spaces, converted to integers with `map(int, ...)`, and wrapped in a list. Result: a 3×3 list-of-lists.

```python
solution = a_star(start, goal)
```
Run A* and store the result (a list of states from start to goal, or `None`).

```python
if solution:
    for step in solution:
        for row in step:
            print(row)
        print()
```
Print each intermediate state. The outer loop iterates states; the inner loop prints each row. `print()` adds a blank line between states.

---

## 6. A* vs DFS vs BFS Comparison

| Property | BFS | DFS | A* |
|---|---|---|---|
| Complete | ✅ | ✅ (with limit) | ✅ |
| Optimal | ✅ | ❌ | ✅ (admissible h) |
| Uses heuristic | ❌ | ❌ | ✅ |
| Speed | Slow | Fast but wrong path | Fast & correct |
| Memory | High | Low | Medium |

---

## 7. Time & Space Complexity

- **States**: 9! = 362,880 possible states for 8-puzzle
- **Time**: O(b^d) worst case, but heuristic drastically reduces nodes expanded
- **Space**: O(b^d) for open + closed lists
- With Manhattan Distance: typically explores only a few hundred nodes for solvable puzzles
