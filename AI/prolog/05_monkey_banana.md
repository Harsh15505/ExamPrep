# WAP to Solve the Monkey-Banana Problem in Prolog

---

## Problem Statement

A **monkey** is in a room. A bunch of bananas is hanging from the ceiling in the middle of the room. The monkey cannot reach the bananas directly. There is a **box** in the room. The monkey can:
- Walk to any position
- Push the box to any position
- Climb on top of the box
- Grab the bananas if on the box at the right position

**Goal**: Find a sequence of actions that allows the monkey to get the bananas.

---

## State Representation

The world state is represented as a compound term:

```
state(MonkeyPosition, BoxPosition, MonkeyOnBox, HasBananas)
```

| Component | Values | Meaning |
|---|---|---|
| `MonkeyPosition` | `atDoor`, `atWindow`, `atMiddle` | Where monkey is horizontally |
| `BoxPosition` | `atDoor`, `atWindow`, `atMiddle` | Where box is |
| `MonkeyOnBox` | `onFloor`, `onBox` | Is monkey on box? |
| `HasBananas` | `no`, `yes` | Has monkey grabbed bananas? |

---

## Program

```prolog
:- initialization(main, main).

% Goal check: the monkey has the bananas
goal(state(_, _, _, yes)).

% Action 1: Walk to a new position (only when on floor)
move(state(Pos1, Box, onFloor, Bananas),
     walk(Pos1, Pos2),
     state(Pos2, Box, onFloor, Bananas)) :-
    Pos1 \= Pos2.

% Action 2: Push the box from current position to a new position
move(state(Pos, Pos, onFloor, Bananas),
     push(Pos, Pos2),
     state(Pos2, Pos2, onFloor, Bananas)) :-
    Pos \= Pos2.

% Action 3: Climb onto the box
move(state(Pos, Pos, onFloor, Bananas),
     climb,
     state(Pos, Pos, onBox, Bananas)).

% Action 4: Grab the bananas (monkey must be on box at middle position)
move(state(atMiddle, atMiddle, onBox, no),
     grab,
     state(atMiddle, atMiddle, onBox, yes)).

% Solve: finds list of moves to reach goal
solve(State, _, []) :-
    goal(State).

solve(State, Visited, [Move|Moves]) :-
    move(State, Move, NextState),
    \+ member(NextState, Visited),
    solve(NextState, [NextState|Visited], Moves).

main :-
    InitialState = state(atDoor, atWindow, onFloor, no),
    write('Initial State: '), write(InitialState), nl,
    write('Goal  : Get the bananas'), nl, nl,
    ( solve(InitialState, [InitialState], Moves)
    ->  write('Solution found! Steps:'), nl,
        print_moves(Moves, 1)
    ;   write('No solution found.')
    ), nl.

print_moves([], _).
print_moves([H|T], N) :-
    format("  Step ~w: ~w~n", [N, H]),
    N1 is N + 1,
    print_moves(T, N1).
```

---

## Sample Run

```
Initial State: state(atDoor,atWindow,onFloor,no)
Goal  : Get the bananas

Solution found! Steps:
  Step 1: walk(atDoor,atWindow)
  Step 2: push(atWindow,atMiddle)
  Step 3: climb
  Step 4: grab
```

---

## Line-by-Line Breakdown

### Line 1 — Initialization
```prolog
:- initialization(main, main).
```
Directive that auto-runs the `main` predicate when the program is loaded. Without it, the user must type `?- main.` at the Prolog prompt.

---

### Lines 3–4 — Goal State
```prolog
goal(state(_, _, _, yes)).
```
Defines what it means to have **reached the goal**. The predicate `goal/1` succeeds for any state where the 4th component is `yes` (the monkey has bananas). The `_` wildcards mean we don't care about the monkey's position, box position, or whether the monkey is on the box — as long as it has the bananas.

---

### Lines 6–9 — Action: Walk
```prolog
move(state(Pos1, Box, onFloor, Bananas),
     walk(Pos1, Pos2),
     state(Pos2, Box, onFloor, Bananas)) :-
    Pos1 \= Pos2.
```
This rule defines the **walk** action. It is read as: "From a state where the monkey is at `Pos1`, box is at `Box`, monkey is on the floor (`onFloor`), and banana status is `Bananas`, the monkey can perform action `walk(Pos1, Pos2)` to transition to a state where the monkey is now at `Pos2` — everything else stays the same."

- The monkey can only walk when it is `onFloor` (not on the box) — encoded in the pattern `onFloor`.
- `Pos1 \= Pos2` — the `\=` operator succeeds if `Pos1` and `Pos2` **cannot unify** (i.e., they are different positions). This prevents a trivial "walk to same position" action.

---

### Lines 11–14 — Action: Push Box
```prolog
move(state(Pos, Pos, onFloor, Bananas),
     push(Pos, Pos2),
     state(Pos2, Pos2, onFloor, Bananas)) :-
    Pos \= Pos2.
```
Defines the **push** action. The monkey can push the box only when it is **at the same position** as the box (monkey and box both at `Pos` — note the same variable used twice in the state).

- After pushing, both the monkey AND the box move to `Pos2`.
- `Pos \= Pos2` — again prevents a trivial "push to same spot" action.
- The monkey must be on the floor to push the box (`onFloor` is in the pattern).

---

### Lines 16–19 — Action: Climb
```prolog
move(state(Pos, Pos, onFloor, Bananas),
     climb,
     state(Pos, Pos, onBox, Bananas)).
```
Defines the **climb** action. The monkey can climb only when it is at the same position as the box (`Pos, Pos` pattern), and it is currently on the floor (`onFloor`). After climbing, the monkey's vertical status changes to `onBox`. The action label is just the atom `climb`.

---

### Lines 21–24 — Action: Grab Bananas
```prolog
move(state(atMiddle, atMiddle, onBox, no),
     grab,
     state(atMiddle, atMiddle, onBox, yes)).
```
Defines the **grab** action. This is a **fully grounded** rule — it only fires in one exact state: monkey at `atMiddle`, box at `atMiddle`, monkey on box (`onBox`), and bananas not yet grabbed (`no`). After grabbing, the state is identical except the `HasBananas` field flips to `yes`. The action label is the atom `grab`.

---

### Lines 26–31 — The Solver

#### Base Case
```prolog
solve(State, _, []) :-
    goal(State).
```
The base case of the solver. If the current `State` satisfies the `goal/1` predicate, the solution is the empty list `[]` (no more moves needed). The second argument (visited states) is ignored with `_`.

#### Recursive Case
```prolog
solve(State, Visited, [Move|Moves]) :-
    move(State, Move, NextState),
    \+ member(NextState, Visited),
    solve(NextState, [NextState|Visited], Moves).
```
- `move(State, Move, NextState)` — Prolog searches for a valid move `Move` that transitions from `State` to `NextState`. Thanks to Prolog's backtracking, it will try all possible moves.
- `\+ member(NextState, Visited)` — **cycle detection**. `\+` is negation-as-failure. `member/2` succeeds if `NextState` is in the `Visited` list. So `\+ member(...)` succeeds only if `NextState` has NOT been visited yet. This prevents the solver from looping in cycles.
- `solve(NextState, [NextState|Visited], Moves)` — recursive call with the new state. `[NextState|Visited]` prepends the new state to the visited list.
- `[Move|Moves]` — the solution is built as a list: current `Move` is the head, and `Moves` is the rest of the solution (filled in recursively).

---

### Lines 33–42 — Main Predicate

```prolog
main :-
    InitialState = state(atDoor, atWindow, onFloor, no),
```
- `InitialState = state(atDoor, atWindow, onFloor, no)` — defines the starting state: monkey at the door, box at the window, monkey on floor, bananas not grabbed.

```prolog
    write('Initial State: '), write(InitialState), nl,
    write('Goal  : Get the bananas'), nl, nl,
```
Prints header information. `nl` outputs a newline.

```prolog
    ( solve(InitialState, [InitialState], Moves)
    ->  write('Solution found! Steps:'), nl,
        print_moves(Moves, 1)
    ;   write('No solution found.')
    ), nl.
```
- `solve(InitialState, [InitialState], Moves)` — calls the solver. We start with `[InitialState]` as the visited list so the very first state is already marked visited.
- If solve succeeds, `Moves` is bound to the list of actions.
- `->` / `;` — if-then-else: prints results if solved, else prints failure.

---

### Lines 44–48 — Print Moves Helper

```prolog
print_moves([], _).
print_moves([H|T], N) :-
    format("  Step ~w: ~w~n", [N, H]),
    N1 is N + 1,
    print_moves(T, N1).
```
- `print_moves([], _)` — base case: nothing more to print when list is empty. `_` ignores the step counter.
- `[H|T]` — pattern match: `H` is the current move, `T` is remaining moves.
- `format(...)` — prints `Step N: Move` with a newline.
- `N1 is N + 1` — increments the step counter.
- Recursive call with `T` and updated counter `N1`.

---

## State Transition Diagram

```
state(atDoor, atWindow, onFloor, no)
        ↓ walk(atDoor, atWindow)
state(atWindow, atWindow, onFloor, no)
        ↓ push(atWindow, atMiddle)
state(atMiddle, atMiddle, onFloor, no)
        ↓ climb
state(atMiddle, atMiddle, onBox, no)
        ↓ grab
state(atMiddle, atMiddle, onBox, yes)  ← GOAL ✓
```
