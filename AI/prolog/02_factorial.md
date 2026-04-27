# WAP to Calculate the Factorial of a Number in Prolog

---

## Program

```prolog
:- initialization(main, main).

factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

main :-
    write('Enter a number: '),
    read(N),
    factorial(N, F),
    format("Factorial of ~w is ~w~n", [N, F]).
```

---

## Sample Run

```
Enter a number: 5.
Factorial of 5 is 120
```

---

## Line-by-Line Breakdown

### Line 1 — Initialization Directive
```prolog
:- initialization(main, main).
```
This is a **directive** (not a fact or rule). It tells SWI-Prolog to automatically call the predicate `main` when the program is loaded/run. The second `main` refers to the *program* entry point style. This means you don't need to manually type `?- main.` at the prompt.

---

### Line 3 — Base Case Clause
```prolog
factorial(0, 1) :- !.
```
This is the **base case** of the recursive factorial predicate.

- `factorial(0, 1)` — defines that the factorial of `0` is `1`. This matches when the first argument is the atom/number `0` and unifies the second argument with `1`.
- `:-` — separates the head of the rule from the body.
- `!` — this is the **cut** operator. Once Prolog reaches this clause and the head matches (`N = 0`), the cut prevents Prolog from ever backtracking into this clause or trying the next factorial clause. Without the cut, Prolog might try the recursive case for `N=0` as well and loop.

---

### Line 4 — Recursive Case Head
```prolog
factorial(N, F) :-
```
This is the **head** of the recursive rule. `N` and `F` are unbound variables. This clause says: "The factorial of `N` is `F`, provided the following conditions in the body are all true."

---

### Line 5 — Guard: Ensure N is Positive
```prolog
    N > 0,
```
This is an **arithmetic comparison guard**. It succeeds only when `N` is greater than `0`. This prevents the recursive case from firing when `N = 0` (the base case handles that). The comma `,` means logical AND — Prolog must also satisfy the next goal.

---

### Line 6 — Calculate N−1
```prolog
    N1 is N - 1,
```
- `is` is the **arithmetic evaluation operator**. It evaluates the right-hand side expression `N - 1` and **unifies** the result with `N1`.
- `N1` is now bound to the integer `N - 1`.
- This is necessary because Prolog variables are **single-assignment** — once bound, they cannot change. So we create a new variable `N1` to hold the decremented value.

---

### Line 7 — Recursive Call
```prolog
    factorial(N1, F1),
```
This is the **recursive call**. Prolog now calls `factorial` again with `N1` (which is `N-1`) and a fresh unbound variable `F1`. Prolog will search its clauses top-to-bottom again, eventually hitting the base case when `N1` becomes `0`. Once the recursive call succeeds, `F1` is bound to `factorial(N1)`.

---

### Line 8 — Compute Final Result
```prolog
    F is N * F1.
```
After the recursive call returns, `F1` holds the factorial of `N-1`. This line computes `N * F1` and unifies the result with `F`. So `F` now holds the factorial of `N`. The period `.` ends the clause.

---

### Lines 10–14 — Main Predicate
```prolog
main :-
    write('Enter a number: '),
    read(N),
    factorial(N, F),
    format("Factorial of ~w is ~w~n", [N, F]).
```

- `main :-` — defines the `main` predicate (entry point).
- `write('Enter a number: ')` — prints the prompt to the console. The atom is quoted because it contains a space.
- `read(N)` — reads a **Prolog term** from standard input. The user must type a number followed by a period and Enter (e.g., `5.`). The read value is unified with `N`.
- `factorial(N, F)` — calls our predicate with the user-provided `N`, and `F` gets bound to the result.
- `format("Factorial of ~w is ~w~n", [N, F])` — prints the output. `~w` is a placeholder that writes a term, and `~n` is a newline. The values `[N, F]` are substituted in order.

---

## How the Recursion Unwinds (for N = 3)

```
factorial(3, F)
  → N=3 > 0, N1=2, call factorial(2, F1)
      → N=2 > 0, N1=1, call factorial(1, F1)
          → N=1 > 0, N1=0, call factorial(0, F1)
              → Base case: F1 = 1, cut!
          → F = 1 * 1 = 1
      → F = 2 * 1 = 2
  → F = 3 * 2 = 6

Result: factorial(3, 6)
```
