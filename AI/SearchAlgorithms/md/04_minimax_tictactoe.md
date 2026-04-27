# Minimax Algorithm — Tic-Tac-Toe AI

---

## 1. Problem Statement

Implement an **AI player** for Tic-Tac-Toe that **never loses**. The AI plays as `O` and the human plays as `X`.

```
Board positions:
1 | 2 | 3
--+---+--
4 | 5 | 6
--+---+--
7 | 8 | 9
```

---

## 2. Theory

### Minimax Algorithm
Minimax is a **decision-making algorithm** used in two-player zero-sum games (where one player's gain = other's loss). It models the game as a **tree of all possible moves** and picks the move that leads to the best worst-case outcome.

**Core idea:**
- The **Maximising player** (AI = `O`) tries to **maximise** the score.
- The **Minimising player** (Human = `X`) tries to **minimise** the score.
- The AI assumes the human always plays optimally.

### Score / Utility Function
| Terminal State | Score |
|---|---|
| AI (`O`) wins | **+1** |
| Human (`X`) wins | **-1** |
| Draw | **0** |

### How Minimax Works
1. Start at the current board state.
2. Recursively generate all possible next moves.
3. For each resulting state, compute the minimax score:
   - If it's AI's turn → take the **maximum** of children's scores.
   - If it's Human's turn → take the **minimum** of children's scores.
4. Propagate scores back up the tree.
5. At the root (current board), pick the move that leads to the highest score.

### Game Tree Example (simplified)
```
         [Current Board] (AI's turn)
              /        |        \
          [O at 1]  [O at 5]  [O at 9]
          score=-1   score=0   score=+1   ← AI picks 9 (highest)
```

### Zero-Sum Property
This is a **zero-sum game**: AI winning is equivalent to human losing. That's why AI maximises and human minimises — they have exactly opposite objectives.

### Minimax Guarantees
- **Perfect play**: With minimax, AI never loses (it always finds the optimal move).
- **Completeness**: Explores the entire game tree to terminal states.
- **Optimal**: Given optimal opponent play, minimax produces the best possible outcome.

### Minimax vs Alpha-Beta Pruning
The standard minimax explores **every** possible game tree path — exponential cost. **Alpha-beta pruning** cuts branches that cannot possibly influence the result, dramatically reducing the search space (not implemented here, but the next step after minimax).

---

## 3. Program

```python
board = [" " for _ in range(9)]

def print_board():
    print()
    for i in range(3):
        print(board[i*3] + " | " + board[i*3+1] + " | " + board[i*3+2])
        if i < 2:
            print("--+---+--")
    print()

def check_winner(player):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False

def is_draw():
    return " " not in board

def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -100
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

while True:
    print_board()

    try:
        position = int(input("Enter position (1-9): ")) - 1
    except ValueError:
        print("Please enter a number!")
        continue

    if position < 0 or position > 8:
        print("Position must be 1-9!")
        continue

    if board[position] == " ":
        board[position] = "X"
    else:
        print("Invalid move!")
        continue

    if check_winner("X"):
        print_board()
        print("You Win!")
        break

    if is_draw():
        print_board()
        print("It's a Draw!")
        break

    ai_move()

    if check_winner("O"):
        print_board()
        print("AI Wins!")
        break

    if is_draw():
        print_board()
        print("It's a Draw!")
        break
```

---

## 4. Sample Run

```
  |   |  
--+---+--
  |   |  
--+---+--
  |   |  

Enter position (1-9): 5

  |   |  
--+---+--
  | X |  
--+---+--
  |   |  

O | O | O
--+---+--
  | X |  
--+---+--
  |   |  

AI Wins!
```

---

## 5. Line-by-Line Code Breakdown

### Line 1 — Board Initialization
```python
board = [" " for _ in range(9)]
```
Creates the game board as a **flat list of 9 strings**, all initialized to `" "` (space = empty cell). The board is stored as a 1D list rather than a 2D grid for simplicity. Position indices 0–8 correspond to:

```
0 | 1 | 2
--+---+--
3 | 4 | 5
--+---+--
6 | 7 | 8
```

The list comprehension `[" " for _ in range(9)]` creates 9 space strings. `_` is a throwaway variable (the index value isn't needed).

---

### Lines 3–9 — `print_board` Function
```python
def print_board():
    print()
    for i in range(3):
        print(board[i*3] + " | " + board[i*3+1] + " | " + board[i*3+2])
        if i < 2:
            print("--+---+--")
    print()
```
- `print()` — adds a blank line before the board.
- `for i in range(3)` — loops over 3 rows (0, 1, 2).
- `board[i*3]`, `board[i*3+1]`, `board[i*3+2]` — computes the flat-list indices for the current row. Row 0 → indices 0,1,2. Row 1 → indices 3,4,5. Row 2 → indices 6,7,8.
- String concatenation with `" | "` creates the visual column separators.
- `if i < 2: print("--+---+--")` — prints the horizontal separator after rows 0 and 1 (but not after the last row).

---

### Lines 11–20 — `check_winner` Function
```python
def check_winner(player):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],   # rows
        [0,3,6], [1,4,7], [2,5,8],   # columns
        [0,4,8], [2,4,6]             # diagonals
    ]
```
Hardcodes all **8 winning combinations** as index triplets: 3 rows, 3 columns, 2 diagonals.

```python
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False
```
For each triplet, checks if all three cells contain the specified `player` symbol (`"X"` or `"O"`). Python's **chained comparison** `a == b == c == player` evaluates as `a == b and b == c and c == player`. Returns `True` immediately on first winning triplet found; `False` if no winning line exists.

---

### Line 22–23 — `is_draw` Function
```python
def is_draw():
    return " " not in board
```
Returns `True` if there are **no empty cells** left. `" " not in board` uses Python's `in` operator to check membership in the list. If no spaces remain and neither player has won, it's a draw.

---

### Lines 25–50 — `minimax` Function (Core AI Logic)

```python
def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0
```
**Terminal state checks** — these are the base cases of the recursion. Before doing anything else, check if the game is already over:
- AI (`O`) won → return `+1` (best outcome for AI).
- Human (`X`) won → return `-1` (worst outcome for AI).
- Draw → return `0` (neutral outcome).

These return values propagate back up the recursive tree.

---

```python
    if is_maximizing:
        best_score = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
```
**Maximising branch (AI's turn)**:
- `best_score = -100` — initialise to a very low value (lower than any actual score of -1, 0, +1) so any real score will be higher.
- Loop over all 9 cells. If cell `i` is empty, **try** placing `O` there.
- `board[i] = "O"` — make the move (mutate the board in place).
- `score = minimax(False)` — recursively evaluate the resulting position, now it's the human's turn (`is_maximizing=False`).
- `board[i] = " "` — **undo** the move (backtrack). This is why minimax can explore all possibilities with a single board object — it makes a move, recurses, then undoes.
- `best_score = max(score, best_score)` — keep track of the highest score seen.
- `return best_score` — return the best score AI can achieve from this position.

---

```python
    else:
        best_score = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score
```
**Minimising branch (Human's turn)**:
- Mirror image of the maximising branch.
- `best_score = 100` — initialise to a very high value.
- Tries placing `X` in each empty cell.
- `score = minimax(True)` — recurse, now it's AI's turn.
- `best_score = min(score, best_score)` — human tries to minimise the score.
- Returns the **minimum** score the human can force from this position.

---

### Lines 52–63 — `ai_move` Function

```python
def ai_move():
    best_score = -100
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"
```
This is the **top-level move selection** for the AI. It's similar to the maximising branch of minimax, but instead of just returning the score, it **remembers which cell produced the best score** (`move = i`).

- For each empty cell, try placing `O`, call `minimax(False)` (opponent's turn next), undo the move.
- Track the move with the highest score in `move`.
- After the loop, **actually make** the best move: `board[move] = "O"`.

The key difference from the `minimax` function itself: `ai_move` modifies the board permanently at the end; `minimax` always undoes its moves (it's just simulating).

---

### Lines 65–104 — Main Game Loop

```python
while True:
    print_board()
```
Infinite loop drives the game. `print_board()` shows the current state at the start of each iteration.

```python
    try:
        position = int(input("Enter position (1-9): ")) - 1
    except ValueError:
        print("Please enter a number!")
        continue
```
- `input()` returns a string. `int(...)` converts to integer.
- Subtracting 1 converts from 1-indexed (user-friendly: 1–9) to 0-indexed (array: 0–8).
- `try/except ValueError` catches non-numeric input. `continue` restarts the loop without making a move.

```python
    if position < 0 or position > 8:
        print("Position must be 1-9!")
        continue
```
Range validation. After subtracting 1, valid positions are 0–8.

```python
    if board[position] == " ":
        board[position] = "X"
    else:
        print("Invalid move!")
        continue
```
Check if the cell is empty. If yes, place `X`. If already occupied, print error and `continue` (re-prompt without advancing the game).

```python
    if check_winner("X"):
        print_board()
        print("You Win!")
        break
    if is_draw():
        print_board()
        print("It's a Draw!")
        break
```
After human's move: check if human won or if the board is full (draw). `break` exits the game loop.

```python
    ai_move()

    if check_winner("O"):
        print_board()
        print("AI Wins!")
        break
    if is_draw():
        print_board()
        print("It's a Draw!")
        break
```
AI makes its move via `ai_move()` (which internally runs full minimax). Then check for AI win or draw.

---

## 6. Minimax Tree Depth & Complexity

| Moves Made | Remaining Moves | Tree Nodes (worst case) |
|---|---|---|
| 0 (start) | 9 | 9! = 362,880 |
| 1 | 8 | 8! = 40,320 |
| 2 | 7 | 7! = 5,040 |

In practice, far fewer because many branches end early (wins/draws before all cells filled).

---

## 7. Why the AI Never Loses

Minimax explores **every possible game** to its conclusion and picks the move that guarantees the best outcome **regardless of what the human does**. Against a perfect minimax AI:
- Human can force at most a draw (by playing the center first).
- Any mistake by the human → AI wins.
- AI never makes a mistake.

The AI effectively memorises the entire game tree and plays optimally from it.
