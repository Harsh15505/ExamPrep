# Prolog – Potential Viva Questions & Answers

---

## Section 1: Fundamentals & Theory

---

**Q1. What is Prolog and what paradigm does it belong to?**

Prolog (Programming in Logic) is a **declarative, logic-based programming language**. Unlike imperative languages where you describe *how* to compute something, in Prolog you describe *what is true* using facts and rules, and let the Prolog inference engine figure out *how* to find a solution through **SLD resolution** and **backtracking**.

---

**Q2. What are the three basic building blocks of a Prolog program?**

1. **Facts** — unconditional truths (e.g., `likes(mary, food).`)
2. **Rules** — conditional statements using `:-` (e.g., `mortal(X) :- human(X).`)
3. **Queries** — questions asked to the Prolog system (e.g., `?- mortal(socrates).`)

---

**Q3. What is unification in Prolog?**

Unification is the process of making two terms identical by finding a substitution (binding of variables) that makes them syntactically equal.

- `X = 5` → X is bound to 5
- `f(X, b) = f(a, Y)` → X = a, Y = b
- `[H|T] = [1,2,3]` → H = 1, T = [2,3]

Unification does **not** involve computation — it is purely structural matching.

---

**Q4. What is backtracking in Prolog?**

Backtracking is Prolog's automatic mechanism for exploring alternative solutions. When a goal fails, Prolog **undoes** the last choice and tries the next available alternative. This continues until either a solution is found or all alternatives are exhausted.

Example: If `color(X)` has three clauses (`red`, `blue`, `green`), Prolog tries `red` first. If the rest of the query fails, it backtracks and tries `blue`, and so on.

---

**Q5. What is the difference between `=`, `==`, and `=:=` in Prolog?**

| Operator | Name | Behavior |
|---|---|---|
| `=` | Unification | Tries to unify two terms (no evaluation) |
| `==` | Structural equality | Succeeds if terms are identical **without** binding variables |
| `=:=` | Arithmetic equality | Evaluates both sides as numbers and checks equality |

Examples:
- `X = 3+4` → X = 3+4 (no computation, just unification)
- `3+4 =:= 7` → true
- `3+4 == 7` → false (they are structurally different terms)

---

**Q6. What is the role of the `is` operator?**

`is` is used to **evaluate arithmetic expressions** and bind the result to a variable.

```prolog
X is 3 + 4.   % X = 7
Y is 2 ** 8.  % Y = 256
```

Without `is`, arithmetic expressions are treated as data terms, not computed values. You **cannot** use `=` for arithmetic evaluation.

---

**Q7. What is the Cut (`!`) operator? When should it be used?**

The **cut** (`!`) is a control predicate that, once reached, **permanently commits** to the current clause and prevents Prolog from backtracking past it.

Uses:
1. **Avoiding redundant solutions** — prevent backtracking when the first solution is correct
2. **Implementing negation** — used internally by `\+`
3. **Efficiency** — stop search once a condition is matched

```prolog
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).
```

⚠️ Overuse of cut breaks the logical nature of Prolog.

---

**Q8. What is Negation-as-Failure (`\+`)?**

`\+ Goal` succeeds if `Goal` **fails** — i.e., if Prolog cannot prove `Goal` from the current knowledge base. It does **not** mean `Goal` is logically false; it means it is **unprovable** given the current facts.

```prolog
not_a_bird(X) :- \+ bird(X).
```

This is called the **Closed World Assumption (CWA)**: anything not provable is assumed false.

---

**Q9. How is recursion used in Prolog instead of loops?**

Prolog has no loop constructs (no `for`, `while`). Repetition is achieved through **recursive predicates**:

```prolog
% Count list elements
length_of([], 0).
length_of([_|T], N) :-
    length_of(T, N1),
    N is N1 + 1.
```

Every recursive predicate must have:
1. A **base case** (termination condition)
2. A **recursive case** that moves toward the base case

---

**Q10. What is the difference between `assert` and `retract`?**

| Predicate | Action |
|---|---|
| `assert(Fact)` / `assertz(Fact)` | Adds a fact to the **end** of the database |
| `asserta(Fact)` | Adds a fact to the **beginning** of the database |
| `retract(Fact)` | Removes the **first** matching fact from the database |
| `retractall(Fact)` | Removes **all** matching facts |

These predicates modify the Prolog database **dynamically** at runtime.

---

## Section 2: Lists

---

**Q11. How are lists represented in Prolog?**

Lists are written as `[Element1, Element2, ..., ElementN]` or using the head-tail notation `[Head|Tail]`.

- `[]` — empty list
- `[1, 2, 3]` — list with 3 elements
- `[H|T]` — head `H` is first element, tail `T` is the rest (itself a list)
- `[1, 2 | Rest]` — first two elements and remaining list

---

**Q12. What does `append/3` do?**

`append(L1, L2, L3)` succeeds when `L3` is the concatenation of `L1` and `L2`.

```prolog
?- append([1,2], [3,4], X).  % X = [1,2,3,4]
?- append(X, [3], [1,2,3]).  % X = [1,2]  (can also work in reverse!)
```

`append` is powerful because it can work in **multiple modes** thanks to unification.

---

**Q13. How does `member/2` work?**

`member(X, List)` succeeds if `X` is an element of `List`. It can be used to:
- Check membership: `?- member(2, [1,2,3]).` → `true`
- Enumerate members: `?- member(X, [a,b,c]).` → `X = a; X = b; X = c`

Internal definition:
```prolog
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).
```

---

**Q14. What is the difference between `findall`, `bagof`, and `setof`?**

| Predicate | Behavior on No Solutions | Duplicates | Sorted |
|---|---|---|---|
| `findall(T, Goal, L)` | Returns `[]` (empty list) | Kept | No |
| `bagof(T, Goal, L)` | **Fails** | Kept | No |
| `setof(T, Goal, L)` | **Fails** | Removed | Yes |

---

## Section 3: Program-Specific Questions

---

**Q15. Explain the factorial program. What happens for `factorial(0, F)`?**

For `factorial(0, F)`:
1. Prolog checks the first clause: `factorial(0, 1) :- !.`
2. The head unifies (`N=0`), so `F` is bound to `1`.
3. The cut `!` fires, preventing backtracking to the recursive clause.
4. Result: `F = 1`.

Without the cut, Prolog would try the second clause for `N=0`, which requires `N > 0` — this would fail. So the cut is an optimization here.

---

**Q16. Why do we use `N1 is N - 1` instead of `N-1` directly in recursive calls?**

In Prolog, `N-1` is a **compound term** (functor `-` with arguments `N` and `1`), not a computed value. `factorial(N-1, F1)` would pass the term `N-1` as the first argument, not the integer result.

`N1 is N - 1` **evaluates** the expression and binds `N1` to the integer result, which is then passed correctly to the recursive call `factorial(N1, F1)`.

---

**Q17. How does the Monkey-Banana solver use backtracking?**

The `solve` predicate uses `move/3` to generate moves. `move/3` has multiple clauses (walk, push, climb, grab). Prolog tries each clause in order. If the resulting state leads to a dead end (cycle or no progress), Prolog **backtracks** and tries the next clause of `move/3`, effectively exploring different paths through the state space.

The `\+ member(NextState, Visited)` check prevents infinite loops by avoiding revisiting states.

---

**Q18. What is the Closed World Assumption (CWA)?**

The CWA is the assumption that **anything not provable from the knowledge base is false**. In Prolog, if you query `?- likes(mary, cricket).` and there's no fact or rule that proves it, Prolog returns `false` — not "unknown." This is the basis for negation-as-failure (`\+`).

---

**Q19. What are the differences between Prolog and Imperative languages?**

| Aspect | Prolog | Python/Java |
|---|---|---|
| Style | Declarative | Imperative |
| Variables | Single-assignment | Mutable |
| Iteration | Recursion | Loops (for, while) |
| Control Flow | Backtracking | Sequential execution |
| "Functions" | Predicates (succeed/fail) | Functions (return values) |
| Data | Terms & Lists | Objects, arrays |

---

**Q20. What happens if you remove the cut from the factorial base case?**

```prolog
factorial(0, 1).   % Without cut
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.
```

For `factorial(0, F)`:
1. First clause matches → `F = 1`. ✓
2. If asked for another solution (`;`), Prolog tries the second clause.
3. Second clause requires `N > 0`, which is `0 > 0` → **fails**.
4. So the result is the same, but with slightly more work.

In practice, the cut is a performance optimization here — it signals that once `N=0` is matched, there's definitively only one answer.

---

**Q21. What is `initialization/2` and why is it used?**

`initialization(Goal, When)` is a **directive** in SWI-Prolog that schedules `Goal` to be called at a specified time. With `When = main`, it runs `Goal` when the program is executed as a script (via `swipl -g halt` or just running the file).

Without it, loading the file only adds clauses to the database — you'd have to manually type `?- main.` to run the program.

---

**Q22. How does the Box Solver handle cycle detection?**

The `solve/4` predicate maintains a `Visited` list of all states encountered so far. Before expanding a state, it checks:

```prolog
\+ member(NextState, Visited)
```

If `NextState` is already in `Visited`, this goal **fails**, forcing Prolog to backtrack and try a different move. The state is added to `Visited` only when it passes this check:

```prolog
solve(NextState, Targets, [NextState|Visited], Moves).
```

---

**Q23. What is `format/2` and how does it differ from `write/1`?**

- `write(Term)` — prints a single Prolog term, no formatting control.
- `format(Format, Args)` — prints formatted output with placeholders:
  - `~w` — write a term
  - `~n` — newline
  - `~a` — write an atom
  - `~d` — write an integer
  - `~f` — write a float

`format` is more powerful when you need to mix text with multiple values in a single output statement.

---

**Q24. Explain the `goal_reached/2` predicate in the Box Solver.**

```prolog
goal_reached([], []).
goal_reached([box(Name, Pos)|Rest], [target(Name, Pos)|Targets]) :-
    goal_reached(Rest, Targets).
```

It works by **simultaneous pattern matching** on both lists. When the head of the state list is `box(Name, Pos)` and the head of the target list is `target(Name, Pos)` — using the **same** `Name` and `Pos` variables — unification ensures that both the name matches AND the position matches the target. If any pair fails to unify, the predicate fails, meaning the goal is not yet reached.

---

**Q25. What is SLD Resolution?**

**SLD Resolution** (Selective Linear Definite clause resolution) is the inference algorithm used by Prolog. It works by:

1. Taking the **leftmost goal** in the query.
2. Finding a clause in the database whose **head** unifies with the goal.
3. **Replacing** the goal with the body of the matching clause.
4. Repeating until no goals remain (success) or no matching clause is found (failure/backtrack).

This is essentially **goal-directed backward chaining** — Prolog works backwards from the query toward the known facts.

---

## Section 4: Quick-Fire Questions

| Question | Answer |
|---|---|
| What symbol ends every Prolog clause? | `.` (period) |
| What does `_` mean in Prolog? | Anonymous variable — matches anything, never bound |
| Can a Prolog variable be reassigned? | No — single assignment only |
| What is the `:-` operator called? | The neck / "if" operator |
| What is `,` between goals? | Logical AND (conjunction) |
| What is `;` between goals? | Logical OR (disjunction) |
| What does `\+` mean? | Negation as failure |
| What does `functor/3` do? | Decomposes a term into functor name, arity, and arguments |
| What is arity? | The number of arguments a predicate takes |
| What is a singleton variable warning? | Variable appears only once (likely a typo — use `_` instead) |
| What is `trace/0`? | Enables step-by-step debugging in the Prolog REPL |
| What is `consult/1`? | Loads a Prolog file into the interpreter |
