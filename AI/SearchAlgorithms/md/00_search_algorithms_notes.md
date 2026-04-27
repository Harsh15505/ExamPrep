# Search Algorithms — Viva Study Notes

> Based on Lecture Notes · AI Subject

---

## 📌 Quick Definitions (Know These Cold)

| Term | Definition |
|---|---|
| **Search Space** | Set of all possible solutions/states a system may have |
| **Start State** | The initial state from where the agent begins searching |
| **Goal Test** | A function that checks whether the current state is the goal |
| **Search Tree** | A tree representation of the search problem; root = initial state |
| **Path Cost** | A numeric cost assigned to a path (sequence of actions) |
| **Solution** | An action sequence from start node to goal node |
| **Optimal Solution** | The solution with the lowest cost among all solutions |
| **Heuristic h(n)** | An estimated cost from node n to the goal (a hint/guess) |
| **Branching Factor (b)** | Number of child nodes each node can expand into |

---

## 📌 Four Properties of Every Search Algorithm

| Property | What it Means |
|---|---|
| **Completeness** | Will the algorithm always find a solution if one exists? |
| **Optimality** | Does it always find the best (lowest-cost) solution? |
| **Time Complexity** | How many nodes/operations does it need? |
| **Space Complexity** | How much memory does it need at any point? |

> **Viva tip**: Every algorithm question will ask about these 4. Have them ready.

---

## 📌 Two Categories of Search

```
Search Algorithms
├── Uninformed (Blind) Search       ← No domain knowledge
│     ├── BFS
│     ├── DFS
│     ├── Depth-Limited Search (DLS)
│     ├── Iterative Deepening DFS (IDDFS)
│     ├── Uniform-Cost Search (UCS)
│     └── Bidirectional Search
│
└── Informed (Heuristic) Search     ← Uses h(n) to guide search
      ├── Greedy Best-First Search
      ├── A* Search
      └── Hill Climbing
```

### Uninformed vs Informed — Key Difference
| | Uninformed | Informed |
|---|---|---|
| Uses domain knowledge? | ❌ No | ✅ Yes |
| Uses heuristic h(n)? | ❌ No | ✅ Yes |
| Also called | Blind Search | Heuristic Search |
| Efficiency | Lower | Higher |
| Example | BFS, DFS | A*, Greedy |

---

## 1. Breadth-First Search (BFS)

### How it works
- Starts at root node, explores **all nodes at depth d** before going to depth d+1.
- Searches **layer by layer** (breadth-wise).
- Uses a **FIFO Queue** as its data structure.

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes — finds solution if it exists at finite depth |
| Optimal | ✅ Yes — finds shallowest (fewest steps) solution first |
| Time Complexity | O(b^d) — exponential in depth |
| Space Complexity | O(b^d) — entire frontier stored in memory |

Where **b** = branching factor, **d** = depth of shallowest solution.

### Advantages
- Guaranteed to find a solution if one exists.
- Finds the minimum-step solution.

### Disadvantages
- **High memory** — every level must be stored to expand the next.
- **Slow** if the solution is far from the root.

### BFS Traversal Order (Example)
```
S → A → B → C → D → G → H → E → F → I → K
(level by level, left to right)
```

---

## 2. Depth-First Search (DFS)

### How it works
- Starts at root, follows each path to its **greatest depth** before backtracking.
- Explores: Root → Left → Right.
- Uses a **Stack** (or recursion's call stack).

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes (within finite state space) |
| Optimal | ❌ No — may find a longer path first |
| Time Complexity | O(b^m) where m = maximum depth |
| Space Complexity | O(b·m) — stores only the current path |

### Advantages
- Very **memory efficient** — only stores current path on the stack.
- Faster than BFS if goal is deep and on the left branch.

### Disadvantages
- States may **re-occur** — no guarantee of finding solution without cycle detection.
- Can go into an **infinite loop** without a depth limit.

### DFS Traversal Order (Example)
```
S → A → B → D → E (backtrack) → C → G (found goal)
(deep first, backtrack when stuck)
```

---

## 3. Depth-Limited Search (DLS)

### How it works
- DFS with a **predetermined depth limit `l`**.
- Nodes at depth `l` are treated as having **no successors**.
- Solves DFS's infinite loop problem.

### Two Failure Conditions
| Failure Type | Meaning |
|---|---|
| **Standard failure** | No solution exists at all |
| **Cutoff failure** | No solution exists within the depth limit |

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes — if solution is above the depth limit |
| Optimal | ❌ No |
| Time Complexity | O(b^l) |
| Space Complexity | O(b·l) |

### Advantages / Disadvantages
- ✅ Memory efficient
- ❌ Incomplete if depth limit is set too low
- ❌ Not optimal

---

## 4. Uniform-Cost Search (UCS)

### How it works
- Expands nodes in order of their **cumulative path cost g(n)** from the root.
- Uses a **Priority Queue** (lowest cost = highest priority).
- Equivalent to BFS when all edge costs are equal.

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes |
| Optimal | ✅ Yes — always picks lowest-cost path |
| Time Complexity | O(b^(1 + C*/ε)) |
| Space Complexity | O(b^(1 + C*/ε)) |

> C* = cost of optimal solution; ε = minimum step cost.

### Key Insight
UCS only cares about **total cost**, not number of steps — can get stuck in infinite loop if zero-cost actions exist.

---

## 5. Iterative Deepening DFS (IDDFS)

### How it works
- Combines **DFS's space efficiency** + **BFS's completeness**.
- Runs DFS with depth limit = 0, then 1, then 2, ... until goal is found.
- Repeats nodes in earlier iterations — acceptable because it's still efficient.

### Key Characteristics
- **Depth-limited** each iteration
- **Gradually increases** the depth limit
- **Complete** and **optimal** (like BFS)

### IDDFS Iteration Example
```
Iteration 1 → A
Iteration 2 → A, B, C
Iteration 3 → A, B, D, E, C, F, G
Iteration 4 → A, B, D, H, I, E, C, F, K, G  ← Goal found
```

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes |
| Optimal | ✅ Yes (uniform costs) |
| Time Complexity | O(b^d) |
| Space Complexity | O(b·d) — like DFS! |

### Why IDDFS beats BFS in Space
BFS needs O(b^d) space. IDDFS needs only O(b·d) — it never stores more than the current path depth.

---

## 6. Bidirectional Search

### How it works
- Runs **two simultaneous searches**:
  1. **Forward**: from start → goal
  2. **Backward**: from goal → start
- Terminates when the two frontiers **meet/intersect**.

### Why it's faster
A single BFS grows exponentially: O(b^d)
Two BFS each growing to d/2: O(b^(d/2)) — **exponentially smaller**!

```
Start --------→ [MEET POINT] ←-------- Goal
    Forward search      Backward search
```

---

## 7. Heuristic Function h(n)

### Definition
A function that **estimates how close** a state n is to the goal state.
- h(n) ≥ 0 always
- h(goal) = 0

### Admissible Heuristic
`h(n) ≤ h*(n)` where h*(n) is the true optimal cost.
- A heuristic that **never overestimates** the actual cost.
- Required for A* to be optimal.
- An admissible heuristic is **optimistic** in nature.

### Consistent (Monotonic) Heuristic
For every node n and successor n' with action cost c:
`h(n) ≤ c(n, n') + h(n')`
Required for A* **graph search** to be optimal.

### Example Heuristics
| Problem | Heuristic |
|---|---|
| 8-Puzzle | Number of misplaced tiles (admissible) |
| 8-Puzzle | Manhattan Distance (admissible, better) |
| Map navigation | Straight-line distance to goal |

---

## 8. Greedy Best-First Search

### How it works
- Selects node with **lowest h(n)** (estimated distance to goal).
- Only uses heuristic — **ignores path cost g(n)**.
- `f(n) = h(n)`
- Uses a **Priority Queue** sorted by h(n).

### Algorithm
```
1. Put start in OPEN list
2. If OPEN is empty → failure
3. Remove node with lowest h(n) from OPEN → move to CLOSED
4. Expand node, generate successors
5. If any successor = goal → success
6. For each successor: if not in OPEN or CLOSED → add to OPEN
7. Go to step 2
```

### Properties
| Property | Answer |
|---|---|
| Complete | ❌ Can get stuck in loops |
| Optimal | ❌ No |
| Time Complexity | O(b^m) worst case |
| Space Complexity | O(b^m) |

### Advantages / Disadvantages
- ✅ More efficient than BFS/DFS in practice
- ✅ Can switch between BFS-like and DFS-like behavior
- ❌ Can behave like unguided DFS in worst case
- ❌ Not optimal — greedy, not globally aware

---

## 9. A* Search Algorithm ⭐

### How it works
- Combines **UCS** (tracks actual cost) + **Greedy Best-First** (uses heuristic).
- Selects node with **lowest f(n) = g(n) + h(n)**.

```
f(n) = g(n) + h(n)
      ↑          ↑
cost to reach n  estimated cost to goal
```

- Uses OPEN and CLOSED lists.
- **Only expands a node if it has the lowest f(n)**.

### Algorithm
```
1. Put start node in OPEN list
2. If OPEN is empty → return failure
3. Select node with lowest f(n)=g(n)+h(n)
   → If it's the goal → SUCCESS, stop
4. Expand it; put it in CLOSED list
5. For each successor n':
   → If not in OPEN or CLOSED → compute f(n'), add to OPEN
   → If already in OPEN/CLOSED → update if new path is cheaper
6. Go to step 2
```

### Properties
| Property | Answer |
|---|---|
| Complete | ✅ Yes (finite branching factor, positive step costs) |
| Optimal | ✅ Yes (with admissible heuristic) |
| Time Complexity | O(b^d) |
| Space Complexity | O(b^d) — keeps all nodes in memory |

### A* Example Walkthrough
```
Graph: A → F (cost 3, h=6), A → B (cost 6, h=8)

f(F) = 3 + 6 = 9
f(B) = 6 + 8 = 14
→ Expand F first (lower f)

From F: G (h=5, g=4), H (h=5, g=10)
f(G) = 4+5=9, f(H) = 10+5=15
→ Expand G

From G: I (h=1, g=7)
f(I) = 7+1 = 8
→ Expand I

From I: J (goal, h=0, g=10)
f(J) = 10+0 = 10 → GOAL!
Path: A → F → G → I → J, Cost = 10
```

### Key Points to Remember
- A* returns the **first path found** — does not continue searching others.
- **Efficiency depends on quality of heuristic** — better h(n) = fewer nodes expanded.
- **Main drawback**: Memory — keeps all generated nodes in memory.
- h(n) = 0 for all n → A* behaves like UCS (pure cost-based).
- h(n) = h*(n) (perfect heuristic) → A* expands only nodes on optimal path.

### A* vs Greedy Best-First
| | A* | Greedy Best-First |
|---|---|---|
| Formula | f = g + h | f = h |
| Considers path cost? | ✅ Yes | ❌ No |
| Optimal? | ✅ Yes | ❌ No |
| Slower/Faster | Slower but correct | Faster but suboptimal |

---

## 10. Hill Climbing Algorithm

### What it is
- A **local search** algorithm — only looks at the **current state and its immediate neighbors**.
- Continuously moves in the direction of **increasing value/objective**.
- Terminates when no neighbor has a higher value (peak reached).
- Also called **greedy local search**.
- **Does NOT maintain a search tree or graph** — only keeps the current state.

### Features
| Feature | Description |
|---|---|
| Generate-and-Test | Generates neighbors, tests if they're better |
| Greedy | Moves in direction that optimizes cost function |
| No backtracking | Cannot go back to previous states |

### Types of Hill Climbing

#### 1. Simple Hill Climbing
- Evaluates **one neighbor at a time**.
- Moves to first neighbor that is better than current state.
- Less optimal, less time consuming.

**Algorithm:**
```
1. Evaluate initial state → if goal, stop
2. Repeat until solution or no operators left:
   a. Apply an operator → get new state
   b. If new state = goal → stop (success)
   c. If new state > current → make it current
   d. Else → go back to step 2
```

#### 2. Steepest-Ascent Hill Climbing
- Examines **all neighbors** first.
- Selects the **best** neighbor (highest value).
- More thorough but slower.

**Algorithm:**
```
1. Evaluate initial state → if goal, stop; else set as current
2. Repeat until solution or current state unchanged:
   SUCC = any state better than current
   For each operator:
     → Apply, get new state
     → If goal → stop
     → If better than SUCC → set SUCC = new state
   If SUCC > current → current = SUCC
```

#### 3. Stochastic Hill Climbing
- Selects **one neighbor at random**.
- Decides whether to move to it or try another.
- Balances exploration and exploitation.

---

### State-Space Landscape Regions
```
                      🏔 Global Maximum (best possible)
             🗻 Local Maximum
    ════════ Shoulder (plateau with uphill edge)
  ══════════ Flat Local Maximum (plateau)
```

| Region | Description |
|---|---|
| **Global Maximum** | Best possible state — goal of search |
| **Local Maximum** | Better than all neighbors, but not globally best |
| **Current State** | Where agent currently is |
| **Flat Local Maximum** | All neighbors have same value — can't tell direction |
| **Shoulder** | Plateau with an uphill edge |

### Problems in Hill Climbing

| Problem | Description | Solution |
|---|---|---|
| **Local Maximum** | Better than neighbors but not the best | Backtracking / random restart |
| **Plateau** | All neighbors have the same value — stuck | Take big/small random step; jump to distant state |
| **Ridge** | Area higher than surroundings but slope can't be reached in one move | Bidirectional search; move in multiple directions |

---

## 📊 Master Comparison Table

| Algorithm | Complete | Optimal | Time | Space | Data Structure |
|---|---|---|---|---|---|
| BFS | ✅ | ✅ | O(b^d) | O(b^d) | FIFO Queue |
| DFS | ✅ | ❌ | O(b^m) | O(b·m) | Stack |
| DLS | ✅ (if l≥d) | ❌ | O(b^l) | O(b·l) | Stack |
| IDDFS | ✅ | ✅ | O(b^d) | O(b·d) | Stack |
| UCS | ✅ | ✅ | O(b^(C*/ε)) | O(b^(C*/ε)) | Priority Queue |
| Greedy Best-First | ❌ | ❌ | O(b^m) | O(b^m) | Priority Queue |
| A* | ✅ | ✅ | O(b^d) | O(b^d) | Priority Queue |
| Hill Climbing | ❌ | ❌ | — | O(1) | None (single state) |

> **b** = branching factor · **d** = depth of solution · **m** = max depth · **l** = depth limit

---

## ❓ Likely Viva Questions

**Q: What is the difference between informed and uninformed search?**
Uninformed search (BFS, DFS) has no domain knowledge — it blindly explores the state space. Informed search uses a heuristic function h(n) that estimates cost to the goal, allowing it to prioritize promising paths and find solutions faster.

**Q: What makes A* optimal?**
A* is optimal when the heuristic h(n) is **admissible** (never overestimates the true cost). Because it always underestimates, A* will never skip the optimal path. For graph search, it also needs to be **consistent** (monotonic).

**Q: What is the difference between A* and Greedy Best-First Search?**
Greedy uses only `f(n) = h(n)` (heuristic estimate) — it ignores how much it cost to get here. A* uses `f(n) = g(n) + h(n)` — it considers both the cost to reach the node AND the estimated cost to the goal. A* is optimal; Greedy is not.

**Q: Why is IDDFS preferred over BFS in memory-constrained environments?**
BFS stores the entire frontier of size O(b^d), which is exponential. IDDFS uses DFS-style exploration so it only needs O(b·d) space (linear in depth). It achieves the same completeness and optimality as BFS at much lower memory cost.

**Q: What are the problems with Hill Climbing? How are they solved?**
Three problems: (1) **Local Maximum** — solved by backtracking or random restarts. (2) **Plateau** — solved by taking random large/small steps to escape. (3) **Ridge** — solved by bidirectional search or moving in multiple directions simultaneously.

**Q: What is the formula used in A*? Explain each part.**
`f(n) = g(n) + h(n)`. Here g(n) is the actual cost to reach node n from the start state, and h(n) is the heuristic estimate of the cost from n to the goal. A* always expands the node with the lowest f(n) first.

**Q: What is an admissible heuristic?**
An admissible heuristic never overestimates the true cost to reach the goal. Formally: `h(n) ≤ h*(n)` where h*(n) is the actual optimal cost. Example: Manhattan distance for 8-puzzle is admissible because it counts the minimum possible moves for each tile.

**Q: What data structure does BFS use? What about DFS?**
BFS uses a **FIFO Queue** (first-in, first-out) — this ensures nodes are explored level by level. DFS uses a **Stack** (last-in, first-out) — this ensures the most recently discovered node is explored first, driving deep into the tree.

**Q: What is Bidirectional Search and what is its advantage?**
It runs two simultaneous searches — one from the start toward the goal, and one from the goal toward the start. The search terminates when they meet. A single BFS grows as O(b^d); bidirectional search grows as O(b^(d/2)) — exponentially more efficient.

**Q: What is the difference between Depth-Limited Search and IDDFS?**
DLS applies a fixed depth limit l and stops — it can miss solutions deeper than l. IDDFS progressively increases the depth limit (0, 1, 2, ...) and reruns DFS each time. This makes IDDFS complete (like BFS) while using the low memory of DFS.

**Q: Why can Hill Climbing not backtrack?**
Hill Climbing is a local search algorithm that only maintains the current state — it has no memory of where it came from. It greedily moves to the best immediate neighbor, so backtracking is architecturally impossible. This is also why it gets stuck at local maxima.

**Q: What is the space complexity of A* and why is it a disadvantage?**
A* has O(b^d) space complexity because it keeps **all generated nodes** in memory (both open and closed lists). This makes it impractical for large-scale problems where millions of nodes may be expanded.

---

## ❓ Extended Viva Questions — Category-Wise

---

### 🔵 BFS — Deep Dive

**Q: Is BFS always optimal? When does it fail to be optimal?**
BFS is optimal only when the path cost is a **non-decreasing function of depth** — i.e., all edge costs are equal (e.g., each step costs 1). If edges have different costs, BFS might find a shorter path that is costlier than a longer path. In that case, **UCS** should be used instead.

**Q: What happens to BFS if the goal node is at a very deep level?**
BFS will explore every node at every level above the goal before it reaches it. Since it stores the entire frontier in memory (O(b^d)), memory becomes the bottleneck before time does — the algorithm may exhaust RAM before finding the solution.

**Q: Why is BFS called a complete algorithm?**
BFS is complete because it systematically explores all nodes at every depth level before going deeper. As long as the branching factor b is finite and the goal exists at some finite depth d, BFS will always find it. It never skips any reachable state.

**Q: Can BFS detect cycles? How?**
Yes, BFS uses a `visited` set (or explored set) to track nodes already added to the queue. Before enqueuing a neighbor, BFS checks if it has been visited. If yes, it skips it — this prevents cycles and redundant exploration.

---

### 🟢 DFS — Deep Dive

**Q: Why is DFS not optimal?**
DFS dives deep into the first available branch without comparing costs. It may find a solution on a very long branch when a much shorter solution exists in an unexplored branch. It has no mechanism to compare path costs across branches.

**Q: What is the worst-case for DFS?**
The worst case is when the goal is on the rightmost branch at the maximum depth m, and DFS exhausts all other branches first. Time complexity is O(b^m), which can be much worse than BFS's O(b^d) if m >> d.

**Q: How does DFS handle infinite state spaces?**
Plain DFS will loop infinitely in infinite state spaces without cycle detection. With cycle detection (visited set), DFS terminates but may still take a very long time if the search tree is large. A depth limit (DLS) or IDDFS is the standard fix.

**Q: What does it mean that DFS uses O(bm) space?**
At any point, DFS only keeps track of the nodes on the current path from root to the frontier (depth m) and the untried siblings of each node on that path. For a branching factor b and max depth m, this is O(b×m) — linear in depth, not exponential.

---

### 🟡 UCS — Deep Dive

**Q: How is UCS different from BFS?**
BFS expands nodes level-by-level (by number of steps). UCS expands nodes by **cumulative path cost** using a priority queue. When all edges have equal cost, UCS behaves identically to BFS. UCS is strictly more general — it handles graphs with variable edge costs.

**Q: Why can UCS get stuck in an infinite loop?**
UCS only terminates when it finds the goal or exhausts all nodes. If there are zero-cost edges, UCS might endlessly expand nodes with cost 0 without making progress toward the goal, since their priority never increases.

**Q: UCS is said to be "optimal." What exactly does it optimize?**
UCS minimizes **total path cost g(n)** from the start to the goal. It guarantees that the first time it reaches the goal, it has done so via the cheapest possible path — because it always expands the cheapest unexplored node first.

---

### 🟠 IDDFS — Deep Dive

**Q: Doesn't IDDFS waste time by re-expanding nodes from previous iterations?**
Yes, nodes near the top of the tree are re-expanded in every iteration. However, most nodes in a tree are at the deepest level — for branching factor b and depth d, roughly b^d nodes are at depth d, while only b^(d-1) are at depth d-1. The overhead of re-expansion is bounded by a constant factor (~b/(b-1)), making it negligible in practice.

**Q: What is the time complexity of IDDFS and why is it the same as BFS?**
Both are O(b^d). IDDFS re-expands nodes at shallower levels, but since the number of nodes grows exponentially by depth, the deepest level dominates the total work. The re-expansion overhead is a small constant multiplier.

**Q: When would you choose IDDFS over BFS?**
When memory is limited. BFS needs O(b^d) memory — it stores the entire frontier. IDDFS needs only O(b×d) — it only stores the current path. For large problems where RAM is the bottleneck, IDDFS is preferred.

---

### 🔴 Heuristic & A* — Deep Dive

**Q: What happens to A* if h(n) = 0 for all nodes?**
If h(n) = 0, the heuristic provides no information. A* degenerates into **Uniform-Cost Search** — it expands nodes purely based on path cost g(n), ignoring any estimate of the remaining cost.

**Q: What happens to A* if h(n) is not admissible (overestimates)?**
A* may skip the optimal path. If h(n) overestimates the true cost, the f(n) of the optimal path may appear larger than a suboptimal path's f(n), causing A* to prefer and return the suboptimal solution. Optimality is no longer guaranteed.

**Q: What is the difference between admissible and consistent heuristics?**
- **Admissible**: h(n) ≤ h*(n) — never overestimates. Required for A* tree search to be optimal.
- **Consistent (monotonic)**: h(n) ≤ cost(n→n') + h(n') — the triangle inequality holds. Required for A* graph search (with closed list) to be optimal.
Every consistent heuristic is also admissible, but not vice versa.

**Q: What are the OPEN and CLOSED lists in A*?**
- **OPEN list**: Nodes that have been discovered but not yet fully expanded. Sorted by f(n). A* always picks the node with the lowest f from here.
- **CLOSED list**: Nodes that have already been expanded. A* never re-expands a node in the closed list (with a consistent heuristic).

**Q: Between "misplaced tiles" and "Manhattan Distance" for 8-puzzle, which is the better heuristic?**
Manhattan Distance is the better (more informed) heuristic. It counts the total steps each tile needs to travel to its goal position, while misplaced tiles only counts whether a tile is out of place (0 or 1 per tile, not how far off). Manhattan Distance dominates misplaced tiles — it is always ≥ misplaced tiles count — so it prunes more nodes while remaining admissible.

**Q: What does it mean for one heuristic to "dominate" another?**
Heuristic h2 dominates h1 if h2(n) ≥ h1(n) for all n, and both are admissible. A dominating heuristic is closer to the true cost h*(n) and therefore expands fewer nodes — it is a strictly better heuristic for A*.

**Q: Why is A* called "complete"?**
A* is complete when the branching factor is finite and every action has a positive cost ε > 0. Under these conditions, f(n) along any path grows without bound, so A* will eventually reach the goal or exhaust the search space.

---

### 🟣 Hill Climbing — Deep Dive

**Q: What is the difference between Simple Hill Climbing and Steepest-Ascent Hill Climbing?**
Simple Hill Climbing evaluates one neighbor at a time and immediately moves to the first neighbor that is better than the current state. Steepest-Ascent evaluates **all** neighbors and moves to the **best** one. Steepest-Ascent makes more informed decisions but is slower because it examines every neighbor before deciding.

**Q: Why is Hill Climbing called "greedy local search"?**
It is greedy because it always moves to the best immediate neighbor without looking ahead. It is local because it only considers the current state's neighbors — it has no global view of the search space. It cannot detect that a local maximum is not the global maximum.

**Q: What is a "plateau" in Hill Climbing and why is it a problem?**
A plateau is a flat area in the state-space landscape where all neighbors of the current state have the same value. The hill-climbing algorithm cannot determine which direction to move because no neighbor is better — it gets stuck. Solution: take a random large step to escape, or restart from a different random state.

**Q: What is the difference between a local maximum and a plateau?**
A **local maximum** has one peak value that is strictly better than all its neighbors, but not the global best. A **plateau** (flat local maximum) is where the current state and all its neighbors have the same value — there's no uphill direction visible. At a local maximum, the algorithm knows to stop (wrongly). On a plateau, it can wander indefinitely.

**Q: Can Hill Climbing solve the Traveling Salesman Problem?**
Yes, Hill Climbing is commonly applied to TSP as a local search optimization. The state space is all possible routes, and the objective function is total distance. The algorithm starts with a random tour and repeatedly swaps pairs of cities (neighbors) to reduce total distance. It converges to a local minimum, which may not be the global optimum.

---

### 🔵 General / Conceptual Questions

**Q: What is the role of a "frontier" (open list) in search algorithms?**
The frontier is the boundary between explored and unexplored territory — the set of nodes that have been discovered (their parent was expanded) but not yet themselves expanded. Different data structures for the frontier give different search behaviors: queue → BFS, stack → DFS, priority queue → UCS/A*.

**Q: What is a "state space"? How is it different from a search tree?**
The state space is the abstract set of all possible states of the problem. The search tree is one way to represent the search process — it may re-visit the same state through different paths (different tree nodes can map to the same state). The search graph explicitly shares nodes for the same state, avoiding redundancy.

**Q: What is the "branching factor" and why does it matter?**
The branching factor b is the average number of successors each node generates. It matters because time and space complexity grow as b^d (or b^m). A higher branching factor means exponentially more nodes to explore at each depth — making the algorithm much slower and more memory-hungry.

**Q: Name one real-world application of each: BFS, DFS, A*, Hill Climbing.**
| Algorithm | Real-World Application |
|---|---|
| BFS | Social network shortest-path (LinkedIn degrees of separation), web crawler |
| DFS | Maze solving, topological sort, detecting cycles in a graph |
| A* | GPS navigation (Google Maps), game pathfinding (e.g., Pac-Man ghosts) |
| Hill Climbing | Hyperparameter tuning in ML, circuit design optimization, TSP |

**Q: What is the Traveling Salesman Problem (TSP) and why is it used as an example?**
TSP asks: "Given N cities, find the shortest tour that visits every city exactly once and returns to the start." It is a classic NP-hard combinatorial optimization problem with no known polynomial-time exact solution. It is used to illustrate informed search, local search, and heuristic methods because its enormous search space (N! routes) makes brute force impractical.

**Q: What is "backtracking" in the context of search?**
Backtracking means undoing the last move when the current path leads to a dead end and trying an alternative. DFS inherently backtracks when it hits a dead-end leaf or a depth limit. Hill Climbing does NOT backtrack — it only moves forward to a better state.

**Q: What is the difference between a "complete" and an "optimal" algorithm?**
A complete algorithm guarantees it will find a solution if one exists. An optimal algorithm guarantees the solution it finds is the best (lowest cost) one. An algorithm can be complete but not optimal (DFS finds a solution, but maybe not the shortest). An algorithm can also fail both (Hill Climbing can get stuck at a local maximum).

**Q: Why does A* expand fewer nodes than BFS for the same problem?**
A* uses the heuristic h(n) to prioritize nodes that are estimated to be closer to the goal. It avoids expanding nodes that have high f(n) values (i.e., those far from the goal or reached expensively). BFS expands every node at each level without any notion of which direction the goal is in. The better the heuristic, the fewer nodes A* expands compared to BFS.

**Q: Can two different heuristics both be admissible for the same problem?**
Yes. For example, for the 8-puzzle: "misplaced tiles" and "Manhattan distance" are both admissible. A heuristic just needs to satisfy h(n) ≤ h*(n). Many heuristics can satisfy this — the one closest to h*(n) (without exceeding it) is the most efficient.

**Q: What is the Generate-and-Test method?**
Generate-and-Test is the simplest AI search strategy: systematically generate candidate solutions and test each one against the goal. If it passes, done; if not, generate the next candidate. It is essentially brute-force search. Hill Climbing is a smarter variant — it generates neighbors and tests them, but uses feedback (the objective value) to decide which direction to generate next.

