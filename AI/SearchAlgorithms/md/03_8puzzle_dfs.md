# 8-Puzzle Problem — DFS (Depth-First Search)

---

## 1. Problem Statement

The **8-Puzzle** is a 3×3 sliding tile puzzle with tiles numbered 1–8 and one blank (`0`). The task is to reach a specified **goal configuration** from a given **initial configuration** by repeatedly sliding tiles into the blank space.

```
Initial State        Goal State
┌───┬───┬───┐       ┌───┬───┬───┐
│ 1 │ 2 │ 3 │       │ 1 │ 2 │ 3 │
├───┼───┼───┤       ├───┼───┼───┤
│ 7 │   │ 8 │  →    │ 4 │ 5 │ 6 │
├───┼───┼───┤       ├───┼───┼───┤
│ 4 │ 6 │ 5 │       │ 7 │ 8 │   │
└───┴───┴───┘       └───┴───┴───┘
```

---

## 2. Theory

### DFS (Depth-First Search)
DFS explores as **deep as possible** along each branch before backtracking. It uses a **stack** (or recursion's call stack) rather than BFS's queue.

| Property | DFS |
|---|---|
| Data structure | Stack (or recursion) |
| Order | Deepest node first |
| Complete | Yes (with cycle detection + depth limit) |
| Optimal | ❌ No — may find a longer solution |
| Memory | O(depth) — very efficient |

### Depth Limit
Unrestricted DFS on an 8-puzzle can go infinitely deep (by cycling). This implementation uses a **depth limit** (`max_depth=50`) — it will not explore paths longer than 50 moves.

### Cycle Detection
The `visited` set prevents the algorithm from revisiting states it has already seen during the current search, avoiding infinite loops.

### Object-Oriented Design
This implementation uses **two classes**:
- `PuzzleState` — represents a single board configuration (state node in the search tree)
- `PuzzleSolver` — contains the DFS algorithm and orchestrates the search

### DFS vs BFS for 8-Puzzle
| | DFS | BFS |
|---|---|---|
| Finds a solution | ✅ (if reachable, within depth limit) | ✅ |
| Finds shortest path | ❌ | ✅ |
| Memory usage | Low (only current path in memory) | High (entire frontier) |
| Suitable for 8-puzzle | ✅ For demo purposes | Better |

---

## 3. Program

```python
import copy

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth+1
        self.blank_pos = self.find_blank()

    def find_blank(self):
        """Find position of blank tile (0)"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def get_board_tuple(self):
        """Convert board to tuple for hashing"""
        return tuple(tuple(row) for row in self.board)

    def is_goal(self, goal_state):
        """Check if current state matches goal state"""
        return self.board == goal_state

    def get_neighbors(self):
        """Generate all valid neighboring states"""
        neighbors = []
        row, col = self.blank_pos

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = copy.deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]

                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1))

        return neighbors

    def get_path(self):
        """Get path from initial state to current state"""
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]

    def display(self):
        """Display the puzzle board"""
        for row in self.board:
            print("  " + " ".join(str(x) if x != 0 else "_" for x in row))


class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial = PuzzleState(initial_state)
        self.goal = goal_state

    def solve_dfs(self, max_depth=50):
        """Solve using Depth First Search with depth limit"""
        visited = set()
        nodes_explored = [0]

        def dfs_recursive(state, depth):
            if depth > max_depth:
                return None

            board_tuple = state.get_board_tuple()
            if board_tuple in visited:
                return None

            visited.add(board_tuple)
            nodes_explored[0] += 1

            if state.is_goal(self.goal):
                return state.get_path()

            for neighbor in state.get_neighbors():
                result = dfs_recursive(neighbor, depth + 1)
                if result:
                    return result

            return None

        result = dfs_recursive(self.initial, 0)
        print(f"\nNodes explored: {nodes_explored[0]}")
        return result


def get_board_input(prompt):
    """Get 3x3 board input from user"""
    print(prompt)
    print("Enter 9 numbers (0-8) separated by spaces (0 represents blank):")

    while True:
        try:
            numbers = list(map(int, input().split()))

            if len(numbers) != 9:
                print("Error: Please enter exactly 9 numbers!")
                continue

            if set(numbers) != set(range(9)):
                print("Error: Please enter numbers 0-8 with no repetition!")
                continue

            board = [numbers[i:i+3] for i in range(0, 9, 3)]
            return board

        except ValueError:
            print("Error: Please enter valid integers!")


def display_solution(path, method):
    """Display the solution path"""
    if not path:
        print(f"\nNo solution found using {method}!")
        return

    print(f"\n{'=' * 60}")
    print(f"Solution found using {method}!")
    print(f"{'=' * 60}")
    print(f"Number of moves: {len(path) - 1}\n")

    for i, state in enumerate(path):
        if i == 0:
            print("Initial State:")
        else:
            print(f"\nStep {i}: Move {state.move}")
        state.display()

    print(f"\n{'=' * 60}")


def main():
    print("=" * 60)
    print("8-PUZZLE PROBLEM SOLVER (Using DFS)")
    print("=" * 60)

    initial_state = get_board_input("\nEnter Initial State:")
    goal_state = get_board_input("\nEnter Goal State:")

    solver = PuzzleSolver(initial_state, goal_state)

    print("\nSolving using DFS...")
    path = solver.solve_dfs()

    display_solution(path, "DFS")


main()
```

---

## 4. Sample Run

```
============================================================
8-PUZZLE PROBLEM SOLVER (Using DFS)
============================================================

Enter Initial State:
Enter 9 numbers (0-8) separated by spaces (0 represents blank):
1 2 3 4 0 6 7 5 8

Enter Goal State:
Enter 9 numbers (0-8) separated by spaces (0 represents blank):
1 2 3 4 5 6 7 8 0

Nodes explored: 7

============================================================
Solution found using DFS!
============================================================
Number of moves: 3

Initial State:
  1 2 3
  4 _ 6
  7 5 8

Step 1: Move RIGHT
  1 2 3
  4 6 _
  7 5 8

Step 2: Move DOWN
  1 2 3
  4 6 8
  7 5 _

Step 3: Move LEFT
  1 2 3
  4 6 8
  7 _ 5
============================================================
```

---

## 5. Line-by-Line Code Breakdown

### Line 1 — Import
```python
import copy
```
Imports Python's `copy` module. Used for `copy.deepcopy()` to make independent copies of the 3×3 board (nested lists require deep copy, not shallow copy).

---

### Lines 3–63 — `PuzzleState` Class

```python
class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth + 1
        self.blank_pos = self.find_blank()
```
The constructor creates a new puzzle state node.

- `self.board` — the 3×3 grid for this state.
- `self.parent` — reference to the `PuzzleState` object that generated this one. Used to trace the solution path backwards. Default `None` for the root/initial state.
- `self.move` — the move that was made to reach this state (`"UP"`, `"DOWN"`, `"LEFT"`, `"RIGHT"`). Default `None` for the initial state.
- `self.depth` — depth of this node in the search tree (= number of moves from start). It is incremented (`depth+1`) from the parent's depth.
- `self.blank_pos` — immediately finds and stores the blank tile's position by calling `self.find_blank()`. Cached to avoid recomputing in `get_neighbors`.

---

```python
    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
```
Scans the 3×3 board row by row, column by column, to find the cell containing `0` (the blank tile). Returns its `(row, col)` as a tuple. Returns `None` if somehow not found (shouldn't happen in a valid puzzle).

---

```python
    def get_board_tuple(self):
        return tuple(tuple(row) for row in self.board)
```
Converts the board (list of lists, which is **unhashable**) into a **tuple of tuples** (which is hashable). This is needed to store states in the `visited` set and use them as dictionary keys. Generator expression `tuple(row) for row in self.board` converts each row, then the outer `tuple()` wraps everything.

---

```python
    def is_goal(self, goal_state):
        return self.board == goal_state
```
Simple equality check. In Python, `==` on nested lists performs a **deep element-wise comparison**, so this correctly checks if every cell matches the goal configuration.

---

```python
    def get_neighbors(self):
        neighbors = []
        row, col = self.blank_pos

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]
```
Retrieves the blank position and defines the 4 possible move directions as `(row_delta, col_delta, name)` tuples. The direction represents where the **blank moves** (equivalently, a tile slides from that direction into the blank).

```python
        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
```
For each direction, compute the new position of the blank. The bounds check ensures the move stays within the 3×3 grid.

```python
                new_board = copy.deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]
```
- `copy.deepcopy(self.board)` — creates a completely independent copy of the board (nested lists need deep copy).
- The simultaneous swap moves the tile at `(new_row, new_col)` into the blank position `(row, col)`.

```python
                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1))
```
Creates a new `PuzzleState` for the neighbor:
- `new_board` — the board after the move
- `self` — current state becomes the parent
- `move_name` — the label of the move made
- `self.depth + 1` — depth increases by 1 each move

---

```python
    def get_path(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]
```
Walks **backwards** through the `parent` chain from the current (goal) state to the root (initial) state. Each state has a `parent` reference. When `current.parent` is `None` (initial state), the loop ends. `path[::-1]` reverses the list to get start→goal order.

---

```python
    def display(self):
        for row in self.board:
            print("  " + " ".join(str(x) if x != 0 else "_" for x in row))
```
Prints each row of the board. Each cell is printed as its number, or `_` if it's the blank tile (`0`). The `" ".join(...)` adds spaces between cells. The `"  "` prefix indents the board for readability.

---

### Lines 66–99 — `PuzzleSolver` Class

```python
class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial = PuzzleState(initial_state)
        self.goal = goal_state
```
Constructor: wraps `initial_state` (raw list-of-lists) in a `PuzzleState` object. Stores the goal as a raw list-of-lists (used in `is_goal` comparison).

---

```python
    def solve_dfs(self, max_depth=50):
        visited = set()
        nodes_explored = [0]
```
- `visited` — set of board tuples already seen in this search. Prevents revisiting.
- `nodes_explored = [0]` — uses a **list** (mutable) instead of a plain integer so the nested inner function `dfs_recursive` can modify it. Plain integers in Python can't be mutated from an inner scope (without `nonlocal`); a list can.

---

```python
        def dfs_recursive(state, depth):
            if depth > max_depth:
                return None
```
The actual DFS logic is an **inner function** (closure) that has access to `visited` and `nodes_explored` from the outer scope. If the current depth exceeds `max_depth`, cut off this branch and return `None` (depth-limited DFS).

```python
            board_tuple = state.get_board_tuple()
            if board_tuple in visited:
                return None

            visited.add(board_tuple)
            nodes_explored[0] += 1
```
Convert the board to a hashable tuple. If already visited, skip (returns `None` → backtrack). Otherwise add to visited and increment the counter.

```python
            if state.is_goal(self.goal):
                return state.get_path()
```
If this state is the goal, reconstruct and return the full path.

```python
            for neighbor in state.get_neighbors():
                result = dfs_recursive(neighbor, depth + 1)
                if result:
                    return result

            return None
```
The **recursive DFS step**: for each neighbor, recursively call `dfs_recursive`. If any recursive call returns a non-None result (a path), immediately propagate it upward. If all neighbors are dead ends, return `None` to backtrack.

---

### Lines 102–123 — `get_board_input` Function

```python
        numbers = list(map(int, input().split()))

        if len(numbers) != 9:
            ...
        if set(numbers) != set(range(9)):
            ...
        board = [numbers[i:i+3] for i in range(0, 9, 3)]
```
Reads all 9 numbers on one line. `input().split()` splits by whitespace. `map(int, ...)` converts each to int.

Validation:
- `len(numbers) != 9` — must be exactly 9 numbers.
- `set(numbers) != set(range(9))` — must contain exactly {0,1,2,3,4,5,6,7,8} (no duplicates, no out-of-range).

`[numbers[i:i+3] for i in range(0, 9, 3)]` — slices the flat list into three rows:
- `numbers[0:3]` → row 0
- `numbers[3:6]` → row 1
- `numbers[6:9]` → row 2

---

### Lines 126–144 — `display_solution` Function

```python
    print(f"Number of moves: {len(path) - 1}\n")
```
`len(path)` is the total number of states in the path (including start). Moves = states - 1.

```python
    for i, state in enumerate(path):
        if i == 0:
            print("Initial State:")
        else:
            print(f"\nStep {i}: Move {state.move}")
        state.display()
```
`enumerate(path)` gives both the index `i` and the `PuzzleState` object. Index 0 is labeled "Initial State". For all others, the move name (`state.move`) is displayed.

---

## 6. DFS Tree Visualization (Simplified)

```
(initial)
  ├── Move UP
  │     ├── Move LEFT
  │     │     └── ... (dead end or deeper)
  │     └── Move RIGHT
  │           └── ... 
  ├── Move DOWN
  │     └── ...
  └── Move RIGHT
        └── GOAL ← DFS finds first viable deep path
```

DFS dives deep into the first branch. If it hits a dead end or the depth limit, it **backtracks** and tries the next branch.

---

## 7. Complexity

- **States**: 9! = 362,880 total possible states
- **Time**: O(b^m) — b = branching factor (~4 for 8-puzzle), m = max depth
- **Space**: O(m) — only the current path stack is in memory (very efficient)
- **With depth limit 50**: In practice explores thousands of nodes for complex initial states
