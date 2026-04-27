# WAP to Find the Length of a List and Reverse Its Elements in Prolog

---

## Program

```prolog
:- initialization(main, main).

% --- Length of a List ---
list_length([], 0).
list_length([_|T], N) :-
    list_length(T, N1),
    N is N1 + 1.

% --- Reverse a List ---
list_reverse([], []).
list_reverse([H|T], Rev) :-
    list_reverse(T, RevT),
    append(RevT, [H], Rev).

main :-
    List = [10, 20, 30, 40, 50],
    write('Original List : '), write(List), nl,
    list_length(List, Len),
    format("Length        : ~w~n", [Len]),
    list_reverse(List, Rev),
    format("Reversed List : ~w~n", [Rev]).
```

---

## Sample Run

```
Original List : [10,20,30,40,50]
Length        : 5
Reversed List : [50,40,30,20,10]
```

---

## Line-by-Line Breakdown

### Line 1 — Initialization
```prolog
:- initialization(main, main).
```
A directive that instructs SWI-Prolog to execute the `main` predicate automatically when the file is loaded. Without this, you would need to manually query `?- main.` at the REPL prompt.

---

## Length Predicate

### Line 3 — Length Base Case
```prolog
list_length([], 0).
```
This is a **fact** (a rule with no body). It states: the length of the **empty list** `[]` is `0`. This is the termination condition for the recursion. When the recursive unwinding finally reaches an empty list, it returns `0`.

---

### Line 4 — Length Recursive Case Head
```prolog
list_length([_|T], N) :-
```
This is the **head** of the recursive rule for `list_length`.

- `[_|T]` is a **list pattern**: `_` (anonymous variable) matches the **head** (first element) of the list — we don't care about its value, hence the underscore. `T` is bound to the **tail** (remainder of the list).
- `N` is the output variable that will be bound to the computed length.

---

### Line 5 — Recursive Call for Tail
```prolog
    list_length(T, N1),
```
Prolog recursively calls `list_length` on the **tail** `T`. `N1` will be bound to the length of the tail. This call keeps unwinding the list one element at a time until it hits the empty list `[]`.

---

### Line 6 — Add 1 for Current Element
```prolog
    N is N1 + 1.
```
Once the recursive call returns with `N1` (the length of the tail), we add `1` to account for the current head element. The result is unified with `N`. This builds up the length count as the recursion **unwinds**.

---

## Reverse Predicate

### Line 9 — Reverse Base Case
```prolog
list_reverse([], []).
```
Another **fact**. It states: the reverse of an empty list `[]` is also an empty list `[]`. This is the base case — when there are no elements left to reverse, the accumulation is complete.

---

### Line 10 — Reverse Recursive Case Head
```prolog
list_reverse([H|T], Rev) :-
```
- `[H|T]` — pattern match: `H` is the **head** (first element), `T` is the **tail**.
- `Rev` — the output variable that will hold the fully reversed list.

The strategy is: reverse the tail, then **append** the head to the *end* of the reversed tail.

---

### Line 11 — Reverse the Tail
```prolog
    list_reverse(T, RevT),
```
Recursive call: reverse the tail `T` and store the result in `RevT`. This call recurses until `T` is empty (base case), then unwinds building the reversed sections.

---

### Line 12 — Append Head to End of Reversed Tail
```prolog
    append(RevT, [H], Rev).
```
- `append(RevT, [H], Rev)` — the built-in `append/3` predicate concatenates the list `RevT` with the single-element list `[H]` and unifies the result with `Rev`.
- We wrap `H` in `[H]` because `append` expects **lists**, not individual elements.
- This places the current head `H` at the **end** of the reversed tail, effectively building the reversed list.

---

## Main Predicate

### Line 14 — Define Input List
```prolog
    List = [10, 20, 30, 40, 50],
```
- `=` is the **unification operator** (NOT assignment). It unifies `List` with the given list.
- This is equivalent to declaring a variable in imperative languages, but in Prolog, once `List` is unified, it cannot change.

### Line 15 — Print Original List
```prolog
    write('Original List : '), write(List), nl,
```
- `write('Original List : ')` — prints the label string.
- `write(List)` — prints the list.
- `nl` — prints a newline character. Each goal is separated by `,` (AND).

### Line 16–17 — Compute and Print Length
```prolog
    list_length(List, Len),
    format("Length        : ~w~n", [Len]),
```
- Calls our `list_length` predicate, binding `Len` to the result.
- `format/2` prints the formatted output where `~w` is replaced by `Len` and `~n` is a newline.

### Line 18–19 — Compute and Print Reversed List
```prolog
    list_reverse(List, Rev),
    format("Reversed List : ~w~n", [Rev]).
```
- Calls `list_reverse` with the original list, binding `Rev` to the reversed list.
- Prints the result. The final `.` ends the `main` clause.

---

## How the Recursion Works (for List = [1, 2, 3])

### Length Trace
```
list_length([1,2,3], N)
  → list_length([2,3], N1), N is N1+1
      → list_length([3], N1), N is N1+1
          → list_length([], N1), N is N1+1
              → Base: N1=0
          → N = 0+1 = 1
      → N = 1+1 = 2
  → N = 2+1 = 3

Result: N = 3
```

### Reverse Trace
```
list_reverse([1,2,3], Rev)
  → list_reverse([2,3], RevT), append(RevT, [1], Rev)
      → list_reverse([3], RevT), append(RevT, [2], Rev)
          → list_reverse([], RevT), append(RevT, [3], Rev)
              → Base: RevT = []
          → append([], [3], Rev) → Rev = [3]
      → append([3], [2], Rev) → Rev = [3,2]
  → append([3,2], [1], Rev) → Rev = [3,2,1]

Result: Rev = [3,2,1]
```
