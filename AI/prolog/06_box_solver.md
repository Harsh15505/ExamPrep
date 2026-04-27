# WAP to Solve the Box Sorting Problem in Prolog

---

## Problem Statement

The **Box Sorting Problem** (also called the Block World / Box World problem) involves arranging **labeled boxes** into a target configuration. 

**Scenario:**
- We have boxes labeled A, B, C, D.
- Each box has a **current position** and a **target position**.
- A box can be **moved** from one position to another.
- The goal is to find the sequence of moves that transforms the current arrangement into the desired arrangement.

> This is a classic AI **state-space search** problem used to demonstrate Prolog's ability to represent states, apply operators, and search for solutions.

---

## State Representation

```prolog
state([box(Name, CurrentPos), ...])
```

Each box is represented as `box(Name, Position)` inside a state list.

---

## Program

```prolog
:- initialization(main, main).

% Check if all boxes are in their target position
goal_reached([], []).
goal_reached([box(Name, Pos)|Rest], [target(Name, Pos)|Targets]) :-
    goal_reached(Rest, Targets).

% Find a box in state and return its position
find_box(Name, [box(Name, Pos)|_], Pos) :- !.
find_box(Name, [_|Rest], Pos) :-
    find_box(Name, Rest, Pos).

% Update a box's position in the state
update_box(_, _, [], []).
update_box(Name, NewPos, [box(Name, _)|Rest], [box(Name, NewPos)|Rest]) :- !.
update_box(Name, NewPos, [H|T], [H|T2]) :-
    update_box(Name, NewPos, T, T2).

% Generate a move: pick any box and move it to its target
move_box(State, Targets, box(Name, From, To), NewState) :-
    member(target(Name, To), Targets),
    find_box(Name, State, From),
    From \= To,
    update_box(Name, To, State, NewState).

% Solver with cycle detection via visited list
solve(State, Targets, _, []) :-
    goal_reached(State, Targets), !.

solve(State, Targets, Visited, [Move|Moves]) :-
    move_box(State, Targets, Move, NextState),
    \+ member(NextState, Visited),
    solve(NextState, Targets, [NextState|Visited], Moves).

main :-
    InitialState = [
        box(a, pos1),
        box(b, pos2),
        box(c, pos3),
        box(d, pos4)
    ],
    Targets = [
        target(a, pos3),
        target(b, pos4),
        target(c, pos1),
        target(d, pos2)
    ],
    nl,
    write('=== BOX SORTING PROBLEM ==='), nl, nl,
    write('Initial Positions:'), nl,
    print_state(InitialState),
    nl,
    write('Target Positions:'), nl,
    print_targets(Targets),
    nl,
    ( solve(InitialState, Targets, [InitialState], Moves)
    ->  length(Moves, Total),
        format("Solution found in ~w move(s):~n", [Total]),
        print_moves(Moves, 1)
    ;   write('No solution found.')
    ), nl.

print_state([]).
print_state([box(Name, Pos)|Rest]) :-
    format("  Box ~w  →  ~w~n", [Name, Pos]),
    print_state(Rest).

print_targets([]).
print_targets([target(Name, Pos)|Rest]) :-
    format("  Box ~w  →  ~w~n", [Name, Pos]),
    print_targets(Rest).

print_moves([], _).
print_moves([box(Name, From, To)|Rest], N) :-
    format("  Step ~w: Move Box-~w from ~w to ~w~n", [N, Name, From, To]),
    N1 is N + 1,
    print_moves(Rest, N1).
```

---

## Sample Run

```
=== BOX SORTING PROBLEM ===

Initial Positions:
  Box a  →  pos1
  Box b  →  pos2
  Box c  →  pos3
  Box d  →  pos4

Target Positions:
  Box a  →  pos3
  Box b  →  pos4
  Box c  →  pos1
  Box d  →  pos2

Solution found in 4 move(s):
  Step 1: Move Box-a from pos1 to pos3
  Step 2: Move Box-b from pos2 to pos4
  Step 3: Move Box-c from pos3 to pos1
  Step 4: Move Box-d from pos4 to pos2
```

---

## Line-by-Line Breakdown

### Line 1 — Initialization Directive
```prolog
:- initialization(main, main).
```
Tells SWI-Prolog to auto-execute the `main` predicate on program load. Without it, the user must manually run `?- main.` at the prompt.

---

### Lines 3–6 — Goal Check: Are All Boxes in Target?

#### Base Case
```prolog
goal_reached([], []).
```
A **fact** that states: if both the state list and the target list are empty simultaneously, the goal has been reached. This is the **termination condition** for the recursive goal checker.

#### Recursive Case
```prolog
goal_reached([box(Name, Pos)|Rest], [target(Name, Pos)|Targets]) :-
    goal_reached(Rest, Targets).
```
- `[box(Name, Pos)|Rest]` — pattern matches the first box in the state. `Name` is the box label, `Pos` is its current position.
- `[target(Name, Pos)|Targets]` — pattern matches the first target. Crucially, the **same `Name` and `Pos`** variables are used in both patterns. This means **unification checks** that the first box's name and current position match the first target's name and expected position.
- If both patterns unify (box name matches target name, and positions match), Prolog recursively checks the rest of the list.
- The assumption here is that the lists are **aligned** (box a's target is always first in the targets list). For a more robust implementation, `member/2` would be used.

---

### Lines 8–10 — Find Box: Get Position of a Named Box

#### Base Case
```prolog
find_box(Name, [box(Name, Pos)|_], Pos) :- !.
```
- If the first element of the list is `box(Name, Pos)` — i.e., the head's name matches the sought name — we immediately return its `Pos`.
- `_` ignores the tail.
- `!` — cut. Once the box is found, there's no need to search further. Without the cut, Prolog might backtrack and try the recursive case unnecessarily.

#### Recursive Case
```prolog
find_box(Name, [_|Rest], Pos) :-
    find_box(Name, Rest, Pos).
```
If the first box is not the one we want (head doesn't match via the first clause), skip it with `_` and recursively search the `Rest` of the list.

---

### Lines 12–16 — Update Box: Change a Box's Position in State

#### Base Case
```prolog
update_box(_, _, [], []).
```
If the state list is empty, the updated state is also empty. This handles the end of the list.

#### Match Case
```prolog
update_box(Name, NewPos, [box(Name, _)|Rest], [box(Name, NewPos)|Rest]) :- !.
```
- When the first element is the box we want to update (`box(Name, _)` — the current position `_` is irrelevant), we replace it with `box(Name, NewPos)` in the output.
- `Rest` is carried through unchanged.
- `!` — cut ensures we don't process this box again in the recursive case.

#### Recursive Case
```prolog
update_box(Name, NewPos, [H|T], [H|T2]) :-
    update_box(Name, NewPos, T, T2).
```
If the first element is NOT the box we're updating, keep it as `H` in the output and recurse on the tail `T`, producing updated tail `T2`.

---

### Lines 18–22 — Move Generator

```prolog
move_box(State, Targets, box(Name, From, To), NewState) :-
    member(target(Name, To), Targets),
    find_box(Name, State, From),
    From \= To,
    update_box(Name, To, State, NewState).
```
This is the **operator/action generator**. It generates valid moves during search.

- `member(target(Name, To), Targets)` — picks a target from the `Targets` list. `Name` and `To` are bound via this. Thanks to backtracking, Prolog can try each target in turn.
- `find_box(Name, State, From)` — finds the current position `From` of the chosen box in the current state.
- `From \= To` — ensures the box is **not already at its target** (prevents useless moves).
- `update_box(Name, To, State, NewState)` — produces the new state by moving the box to its target position `To`.
- The move is represented as `box(Name, From, To)` — a compound term describing the action.

---

### Lines 24–30 — Solver

#### Goal Base Case
```prolog
solve(State, Targets, _, []) :-
    goal_reached(State, Targets), !.
```
- If the current `State` satisfies `goal_reached/2`, the solution is the empty list `[]` (no more moves needed).
- `_` ignores the visited list.
- `!` — cut prevents Prolog from attempting the recursive case after the goal is reached.

#### Recursive Case
```prolog
solve(State, Targets, Visited, [Move|Moves]) :-
    move_box(State, Targets, Move, NextState),
    \+ member(NextState, Visited),
    solve(NextState, Targets, [NextState|Visited], Moves).
```
- `move_box(State, Targets, Move, NextState)` — generates a move and computes the next state. Backtracking will try different moves if needed.
- `\+ member(NextState, Visited)` — **cycle detection**. Fails if the next state has already been visited, forcing Prolog to backtrack and try another move.
- `solve(NextState, Targets, [NextState|Visited], Moves)` — recursive call with the new state, updated visited list, and `Moves` bound to the remaining steps.
- `[Move|Moves]` — the full solution list is built by prepending the current move to the recursive result.

---

### Lines 32–54 — Main Predicate

```prolog
InitialState = [
    box(a, pos1),
    box(b, pos2),
    box(c, pos3),
    box(d, pos4)
],
```
Defines the **initial configuration** of boxes using unification. Each `box(Name, Position)` term represents one box.

```prolog
Targets = [
    target(a, pos3),
    target(b, pos4),
    target(c, pos1),
    target(d, pos2)
],
```
Defines the **desired final configuration**. `target(Name, DesiredPosition)` states where each box should end up.

```prolog
( solve(InitialState, Targets, [InitialState], Moves)
->  length(Moves, Total),
    format("Solution found in ~w move(s):~n", [Total]),
    print_moves(Moves, 1)
;   write('No solution found.')
)
```
- Calls the solver with the initial state and targets. `[InitialState]` seeds the visited list.
- If successful, `Moves` is bound to the move list.
- `length(Moves, Total)` — built-in predicate that unifies `Total` with the number of elements in `Moves`.
- If the solver fails (no solution), prints a failure message.

---

### Lines 56–68 — Helper Print Predicates

```prolog
print_state([]).
print_state([box(Name, Pos)|Rest]) :-
    format("  Box ~w  →  ~w~n", [Name, Pos]),
    print_state(Rest).
```
Recursively prints each box's current position. Base case: empty list = nothing to print. Recursive case: print first box then recurse.

```prolog
print_moves([], _).
print_moves([box(Name, From, To)|Rest], N) :-
    format("  Step ~w: Move Box-~w from ~w to ~w~n", [N, Name, From, To]),
    N1 is N + 1,
    print_moves(Rest, N1).
```
Recursively prints each move. The move term `box(Name, From, To)` is pattern-matched to extract the three components. Step counter `N` is incremented with `N1 is N + 1`.

---

## Summary: How the Solver Works

```
Initial: [box(a,pos1), box(b,pos2), box(c,pos3), box(d,pos4)]
Target:  [target(a,pos3), target(b,pos4), target(c,pos1), target(d,pos2)]

Solver tries move_box → generates a valid move
  → Updates state
  → Checks if new state was visited (cycle check)
  → Recurses with new state
  → If goal reached: return []
  → If stuck: backtrack and try another move

Solution:
  Move a: pos1 → pos3
  Move b: pos2 → pos4
  Move c: pos3 → pos1
  Move d: pos4 → pos2
```

This is an example of **depth-first search with cycle detection** implemented naturally through Prolog's backtracking mechanism.
