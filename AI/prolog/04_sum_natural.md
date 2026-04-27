# WAP to Calculate the Sum of First N Natural Numbers in Prolog

---

## Program

```prolog
:- initialization(main, main).

sum_natural(0, 0) :- !.
sum_natural(N, Sum) :-
    N > 0,
    N1 is N - 1,
    sum_natural(N1, Sum1),
    Sum is Sum1 + N.

main :-
    write('Enter the value of N: '),
    read(N),
    ( integer(N), N >= 0
    ->  sum_natural(N, Sum),
        format("Sum of first ~w natural numbers = ~w~n", [N, Sum])
    ;   write('Invalid input. Please enter a non-negative integer.'), nl
    ).
```

---

## Sample Run

```
Enter the value of N: 10.
Sum of first 10 natural numbers = 55
```

```
Enter the value of N: 0.
Sum of first 0 natural numbers = 0
```

---

## Line-by-Line Breakdown

### Line 1 — Initialization Directive
```prolog
:- initialization(main, main).
```
This directive tells SWI-Prolog to run the `main` predicate automatically when the program file is loaded or executed. The second argument `main` specifies the entry-point style. Without this, you'd have to type `?- main.` manually.

---

### Line 3 — Base Case: Sum of 0 is 0
```prolog
sum_natural(0, 0) :- !.
```
This is the **base case** of the recursion. It states: the sum of the first `0` natural numbers is `0`.

- `sum_natural(0, 0)` — when the first argument matches the number `0`, the second argument (the result) is unified with `0`.
- `:-` — separates the head from the body.
- `!` — the **cut** operator. Once this clause fires for `N=0`, the cut ensures Prolog does NOT backtrack and attempt the recursive clause for `N=0`. Without the cut, `sum_natural(0, Sum)` might also try the recursive clause and fail or loop.

---

### Line 4 — Recursive Case Head
```prolog
sum_natural(N, Sum) :-
```
This is the head of the recursive rule. `N` is the input (number of natural numbers), and `Sum` is the output variable that will be bound to the computed sum.

---

### Line 5 — Guard: N Must Be Positive
```prolog
    N > 0,
```
An **arithmetic guard** that ensures this clause only fires when `N` is strictly greater than 0. This prevents unintended application of the recursive rule when `N = 0` (handled by the base case). The comma `,` acts as logical AND.

---

### Line 6 — Compute N−1
```prolog
    N1 is N - 1,
```
- `is` evaluates the arithmetic expression on the right (`N - 1`) and unifies the result with `N1`.
- Prolog variables are **immutable** once bound, so we create a fresh variable `N1` to hold `N - 1`.
- This is the step that moves the recursion toward the base case.

---

### Line 7 — Recursive Call
```prolog
    sum_natural(N1, Sum1),
```
Prolog makes a **recursive call** with `N1` (which is `N-1`). `Sum1` will eventually be bound to the sum of the first `N-1` natural numbers. This call recurses until `N1` reaches `0` (the base case).

---

### Line 8 — Compute Current Sum
```prolog
    Sum is Sum1 + N.
```
After the recursive call returns with `Sum1`, this line computes the total sum by adding `N` (the current number) to `Sum1` (sum of numbers below N). The result is unified with `Sum`. The period `.` terminates the clause.

This is the **accumulation step** — it executes during the **unwinding phase** of the recursion.

---

## Main Predicate

### Line 10 — Entry Point
```prolog
main :-
```
Defines the main entry predicate.

---

### Line 11 — Print Prompt
```prolog
    write('Enter the value of N: '),
```
Prints the user prompt using `write/1`. The atom is quoted because it contains spaces and a colon.

---

### Line 12 — Read User Input
```prolog
    read(N),
```
`read/1` reads a **Prolog term** from standard input and unifies it with `N`. The user must type the number **followed by a period** and press Enter (e.g., `10.`). This is standard Prolog term input syntax.

---

### Lines 13–17 — Input Validation with If-Then-Else
```prolog
    ( integer(N), N >= 0
    ->  sum_natural(N, Sum),
        format("Sum of first ~w natural numbers = ~w~n", [N, Sum])
    ;   write('Invalid input. Please enter a non-negative integer.'), nl
    ).
```
This uses Prolog's **if-then-else** construct: `( Condition -> ThenBranch ; ElseBranch )`.

- `integer(N)` — a **type-checking predicate** that succeeds only if `N` is a Prolog integer (not a float, atom, or variable).
- `N >= 0` — ensures the number is non-negative (natural numbers start from 0 or 1).
- `->` — the **if-then** operator. If both conditions succeed, Prolog executes the `ThenBranch`.
- `;` — the **or/else** operator. If the condition fails, Prolog executes the `ElseBranch`.
- `ThenBranch`: calls `sum_natural(N, Sum)` and prints the result using `format/2`.
  - `~w` — a format placeholder that writes the argument as a term.
  - `~n` — a newline.
  - `[N, Sum]` — the list of arguments that replace the `~w` placeholders.
- `ElseBranch`: prints an error message if the input is invalid.

---

## Execution Trace (for N = 4)

```
sum_natural(4, Sum)
  → N=4 > 0, N1=3, call sum_natural(3, Sum1)
      → N=3 > 0, N1=2, call sum_natural(2, Sum1)
          → N=2 > 0, N1=1, call sum_natural(1, Sum1)
              → N=1 > 0, N1=0, call sum_natural(0, Sum1)
                  → Base case: Sum1=0, cut!
              → Sum = 0 + 1 = 1
          → Sum = 1 + 2 = 3
      → Sum = 3 + 3 = 6
  → Sum = 6 + 4 = 10

Result: sum_natural(4, 10)
```

Verification: 1 + 2 + 3 + 4 = **10** ✓

Using the formula: N*(N+1)/2 = 4*5/2 = **10** ✓
