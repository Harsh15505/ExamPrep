# Prolog – Complete Theory, Syntax & Cheatsheet

---

## 1. What is Prolog?

**Prolog** (Programming in Logic) is a **declarative, logic-based programming language** developed in the early 1970s by Alain Colmerauer and Robert Kowalski. Unlike imperative languages (C, Java, Python) where you tell the computer *how* to compute, in Prolog you describe *what is true* and let the inference engine figure out *how*.

Prolog is based on **first-order predicate logic** and uses a technique called **SLD resolution** (Selective Linear Definite clause resolution) for automated theorem proving.

### Key Characteristics
| Feature | Description |
|---|---|
| Paradigm | Logic / Declarative |
| Execution Model | Backtracking search |
| Data Structures | Terms, Lists, Atoms |
| Primary Use | AI, NLP, Expert Systems, Parsing |
| Popular Implementations | SWI-Prolog, GNU Prolog, SICStus |

---

## 2. Core Concepts

### 2.1 Terms
Everything in Prolog is a **term**. There are four types:

| Type | Example | Description |
|---|---|---|
| Atom | `hello`, `mary`, `'John Doe'` | Lowercase or quoted string constants |
| Number | `42`, `3.14` | Integer or float |
| Variable | `X`, `Name`, `_Result` | Start with uppercase or underscore |
| Compound Term | `likes(mary, food)`, `f(X, g(Y))` | Functor + arguments |

### 2.2 Facts
A **fact** is an unconditionally true statement.

```prolog
cat(tom).
likes(mary, food).
parent(tom, bob).
```

### 2.3 Rules
A **rule** is a conditional statement: the **head** is true if the **body** is true.

```prolog
Head :- Body.

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
mortal(X)         :- human(X).
```

### 2.4 Queries
You ask Prolog questions at the interactive prompt `?-`

```prolog
?- cat(tom).        % true
?- cat(jerry).      % false (not in database)
?- likes(mary, X).  % X = food
```

### 2.5 The Prolog Database (Knowledge Base)
A Prolog program is a collection of **clauses** (facts + rules) stored in the database. Prolog searches them **top-to-bottom, left-to-right**.

---

## 3. Unification

Unification is the process of making two terms identical by finding variable bindings.

```prolog
?- X = 5.           % X = 5
?- f(X, b) = f(a, Y). % X = a, Y = b
?- [H|T] = [1,2,3]. % H = 1, T = [2,3]
```

**Rules of Unification:**
- Two atoms unify if they are identical: `cat = cat` ✓
- A variable unifies with anything and gets bound
- Two compound terms unify if their functors and all arguments unify recursively

---

## 4. Backtracking

Prolog automatically **backtracks** when a goal fails — it goes back to the last choice point and tries the next alternative.

```prolog
color(red).
color(blue).
color(green).

?- color(X).
% X = red   ; (press ; to get next)
% X = blue  ;
% X = green.
```

The **cut** operator `!` stops backtracking at a specific point.

```prolog
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).
```

---

## 5. Built-in Predicates

### 5.1 Arithmetic
```prolog
X is 3 + 4.           % X = 7   (evaluate expression)
Y is 10 mod 3.        % Y = 1
Z is sqrt(16).        % Z = 4.0
W is max(5, 9).       % W = 9
```

> ⚠️ Always use `is` for arithmetic evaluation. `=` only unifies, it does NOT evaluate.

### 5.2 Comparison Operators
```prolog
X =:= Y   % arithmetic equal
X =\= Y   % arithmetic not equal
X < Y     % less than
X > Y     % greater than
X =< Y    % less than or equal (note: not <=)
X >= Y    % greater than or equal

X == Y    % structural equality (no evaluation)
X \== Y   % structural inequality
```

### 5.3 I/O Predicates
```prolog
write(hello).          % prints hello
writeln(hello).        % prints hello + newline
nl.                    % prints newline
read(X).               % reads a term from stdin (must end with .)
format("Value: ~w~n", [X]).  % formatted output
```

### 5.4 Control Predicates
```prolog
true.         % always succeeds
fail.         % always fails (used to force backtracking)
!             % cut – stops backtracking
\+ Goal       % negation as failure (succeeds if Goal fails)
not(Goal)     % same as \+
```

### 5.5 Type Checking
```prolog
integer(X)    % succeeds if X is an integer
float(X)      % succeeds if X is a float
number(X)     % integer or float
atom(X)       % succeeds if X is an atom
is_list(X)    % succeeds if X is a list
var(X)        % succeeds if X is unbound variable
nonvar(X)     % succeeds if X is bound
```

### 5.6 List Predicates
```prolog
length(List, N)           % N = length of List
append(L1, L2, L3)        % L3 = L1 concatenated with L2
member(X, List)           % X is a member of List
reverse(List, Rev)        % Rev = reversed List
last(List, X)             % X = last element
nth0(N, List, X)          % X = Nth element (0-indexed)
nth1(N, List, X)          % X = Nth element (1-indexed)
msort(List, Sorted)       % sorted without removing duplicates
sort(List, Sorted)        % sorted, duplicates removed
flatten(List, Flat)       % flatten nested list
```

### 5.7 Assert / Retract (Dynamic Database)
```prolog
assert(fact(a)).          % add fact to database
asserta(fact(a)).         % add at beginning
assertz(fact(a)).         % add at end
retract(fact(a)).         % remove first matching fact
retractall(fact(_)).      % remove all matching facts
```

---

## 6. Lists in Prolog

Lists are fundamental data structures in Prolog.

### Syntax
```prolog
[]              % empty list
[1, 2, 3]       % list with three elements
[H|T]           % H = head, T = tail (rest of list)
[1, 2 | Rest]   % first two elements + rest
```

### Pattern Matching
```prolog
first([H|_], H).          % get first element
rest([_|T], T).           % get tail

% Example usage:
?- first([a, b, c], X).   % X = a
?- rest([a, b, c], T).    % T = [b, c]
```

### Recursive List Processing Template
```prolog
predicate([], ...).                          % base case: empty list
predicate([H|T], ...) :- predicate(T, ...). % recursive case
```

---

## 7. Recursion in Prolog

Prolog has no loops — iteration is done through **recursion**.

```prolog
% Factorial
factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

% Count elements in list
count([], 0).
count([_|T], N) :-
    count(T, N1),
    N is N1 + 1.
```

---

## 8. Operators — Complete Reference

> **Key concept**: In Prolog, operators are just **syntactic sugar** for compound terms.
> `3 + 4` is really `+(3, 4)`. `X = Y` is really `=(X, Y)`. They look like operators, but they are predicates/functors underneath.

---

### 8.1 Arithmetic Operators (used inside `is`)

| Operator | Meaning | Example |
|---|---|---|
| `+` | Addition | `X is 3 + 4` → 7 |
| `-` | Subtraction | `X is 10 - 3` → 7 |
| `*` | Multiplication | `X is 4 * 5` → 20 |
| `/` | Division (float) | `X is 7 / 2` → 3.5 |
| `//` | Integer division | `X is 7 // 2` → 3 |
| `mod` | Modulo (remainder) | `X is 10 mod 3` → 1 |
| `rem` | Remainder (sign of dividend) | `X is -7 rem 3` → -1 |
| `**` | Power (float result) | `X is 2 ** 10` → 1024.0 |
| `^` | Power (integer) | `X is 2 ^ 10` → 1024 |
| `-` (unary) | Negation | `X is -5` |
| `abs` | Absolute value | `X is abs(-7)` → 7 |
| `max` | Maximum of two | `X is max(3, 9)` → 9 |
| `min` | Minimum of two | `X is min(3, 9)` → 3 |
| `sign` | Sign (-1, 0, 1) | `X is sign(-5)` → -1 |

---

### 8.2 Bitwise Operators (integers only, inside `is`)

| Operator | Meaning | Example |
|---|---|---|
| `\/` | Bitwise OR | `X is 5 \/ 3` → 7 |
| `/\` | Bitwise AND | `X is 5 /\ 3` → 1 |
| `xor` | Bitwise XOR | `X is 5 xor 3` → 6 |
| `\` | Bitwise complement | `X is \ 0` → -1 |
| `<<` | Left shift | `X is 1 << 3` → 8 |
| `>>` | Right shift | `X is 8 >> 2` → 2 |

---

### 8.3 Math Functions (used inside `is`)

| Function | Meaning | Example |
|---|---|---|
| `sqrt(X)` | Square root | `X is sqrt(16)` → 4.0 |
| `sin(X)` | Sine (radians) | `X is sin(0)` → 0.0 |
| `cos(X)` | Cosine | `X is cos(0)` → 1.0 |
| `tan(X)` | Tangent | `X is tan(0)` → 0.0 |
| `exp(X)` | e^X | `X is exp(1)` → 2.718... |
| `log(X)` | Natural logarithm | `X is log(1)` → 0.0 |
| `ceiling(X)` | Round up | `X is ceiling(3.2)` → 4 |
| `floor(X)` | Round down | `X is floor(3.9)` → 3 |
| `round(X)` | Round to nearest | `X is round(3.5)` → 4 |
| `truncate(X)` | Drop decimal part | `X is truncate(3.9)` → 3 |
| `float(X)` | Convert to float | `X is float(5)` → 5.0 |
| `integer(X)` | Convert to integer | `X is integer(3.7)` → 3 |
| `float_integer_part(X)` | Integer part as float | → 3.0 |
| `pi` | π constant | `X is pi` → 3.14159... |
| `e` | Euler's number | `X is e` → 2.71828... |

```prolog
% Examples
?- X is sqrt(25).          % X = 5.0
?- X is ceiling(4.1).      % X = 5
?- X is 2 ** 8.            % X = 256.0
?- X is 17 mod 5.          % X = 2
?- X is max(10, abs(-15)). % X = 15
```

---

### 8.4 Comparison / Relational Operators

#### Arithmetic Comparison (evaluates expressions first)
| Operator | Meaning |
|---|---|
| `X =:= Y` | Arithmetic equal |
| `X =\= Y` | Arithmetic not equal |
| `X < Y` | Less than |
| `X > Y` | Greater than |
| `X =< Y` | Less than or equal (note: NOT `<=`) |
| `X >= Y` | Greater than or equal |

```prolog
?- 3 + 4 =:= 7.     % true  (evaluates both sides)
?- 3 + 4 == 7.      % false (structural: term '3+4' ≠ term '7')
```

#### Structural / Term Comparison (does NOT evaluate)
| Operator | Meaning |
|---|---|
| `X == Y` | Structurally identical (no evaluation, no binding) |
| `X \== Y` | Structurally different |
| `X = Y` | Unification (binds variables) |
| `X \= Y` | Fails if X and Y can unify |

#### Term Ordering (alphabetical/canonical order)
| Operator | Meaning |
|---|---|
| `X @< Y` | X comes before Y in standard order |
| `X @> Y` | X comes after Y |
| `X @=< Y` | X comes before or same |
| `X @>= Y` | X comes after or same |

**Standard term ordering:** `var < number < atom < compound`
```prolog
?- a @< b.      % true
?- 1 @< a.      % true (numbers before atoms)
?- compare(Order, foo, bar).  % Order = > (bar @< foo alphabetically)
```

---

### 8.5 Unification Operators

| Operator | Meaning |
|---|---|
| `X = Y` | Unify X and Y (binds variables) |
| `X \= Y` | Succeeds if X and Y **cannot** unify |
| `X =.. List` | Univ — decompose/construct terms (see below) |

---

### 8.6 Logical / Control Operators

| Operator | Meaning | Example |
|---|---|---|
| `,` | AND (conjunction) | `Goal1, Goal2` |
| `;` | OR (disjunction) | `Goal1 ; Goal2` |
| `->` | If-Then | `Cond -> Then` |
| `\+` | Negation-as-failure | `\+ member(x, [a,b])` |
| `!` | Cut | Stops backtracking |

---

### 8.7 Operator Precedence Table (lower number = tighter binding)

| Operator | Priority | Type | Notes |
|---|---|---|---|
| `:-` `-->` | 1200 | xfx | Clause neck / DCG |
| `:-` `?-` | 1200 | fx | Directive / query |
| `;` `\|` | 1100 | xfy | Or / DCG alternative |
| `->` | 1050 | xfy | If-then |
| `,` | 1000 | xfy | Conjunction |
| `\+` `not` | 900 | fy | Negation |
| `=` `\=` `==` `\==` `is` `=:=` `=\=` `<` `>` `=<` `>=` `@<` `@>` `=..` | 700 | xfx | Comparison/unification |
| `:` | 600 | xfy | Module qualification |
| `+` `-` `/\` `\/` `xor` | 500 | yfx | Additive |
| `*` `/` `//` `mod` `rem` `div` `rdiv` `<<` `>>` | 400 | yfx | Multiplicative |
| `**` | 200 | xfx | Power (float) |
| `^` | 200 | xfy | Power (int) / setof variable |
| `-` `+` `\` | 200 | fy | Unary |

---

### 8.8 Defining Custom Operators
```prolog
:- op(Priority, Type, Name).

% Type specifiers:
%   xfx  – infix, non-associative      (neither side can repeat)
%   xfy  – infix, right-associative    (right side can repeat: a:b:c = a:(b:c))
%   yfx  – infix, left-associative     (left side can repeat:  a+b+c = (a+b)+c)
%   fx   – prefix, non-associative
%   fy   – prefix, right-associative
%   xf   – postfix, non-associative

% Example: define 'isa' as an infix operator
:- op(700, xfx, isa).

dog isa animal.
?- dog isa X.     % X = animal
```

---

## 8b. Functions vs Predicates — A Critical Distinction

### Prolog Has NO Functions!

In languages like Python, a function **returns a value**:
```python
def square(x): return x * x
y = square(5)   # y = 25
```

In Prolog, **everything is a predicate** — predicates **succeed or fail**, they do NOT return values. To "return" a result, you add an extra argument:

```prolog
% square/2 — "returns" result via second argument
square(X, Y) :- Y is X * X.

?- square(5, Y).   % Y = 25
```

### The `is` Evaluator
The only place arithmetic is "computed" is inside `is`. The right-hand side of `is` is called an **arithmetic expression** — it looks functional, but it's a special syntactic context:

```prolog
X is sqrt(16) + abs(-3).   % X = 7.0
```

Math symbols like `sqrt`, `abs`, `sin` are **evaluable functors**, not Prolog predicates. They only work inside `is`/`=:=`/`<`/`>` etc.

```prolog
?- X = sqrt(16).      % X = sqrt(16)  ← just a term, not evaluated!
?- X is sqrt(16).     % X = 4.0       ← evaluated by 'is'
```

### Higher-Order via `call/N`
Prolog can simulate function passing with `call`:
```prolog
apply(Pred, X, Y) :- call(Pred, X, Y).

double(X, Y) :- Y is X * 2.
?- apply(double, 5, Y).   % Y = 10
```

---

## 8c. String and Atom Predicates

Prolog has no "string" type in classic Prolog — text is handled as **atoms**, **character lists**, or (in SWI-Prolog) **string objects**.

### Atom Manipulation
```prolog
atom_length(hello, N).              % N = 5
atom_concat(foo, bar, X).           % X = foobar
atom_concat(X, bar, foobar).        % X = foo  (works in reverse!)
sub_atom(abcdef, 2, 3, _, Sub).     % Sub = cde (from pos 2, length 3)
upcase_atom(hello, X).              % X = 'HELLO'
downcase_atom('HELLO', X).          % X = hello
atom_chars(hello, Cs).              % Cs = [h,e,l,l,o]
atom_codes(hello, Codes).           % Codes = [104,101,108,108,111]
char_code('A', C).                  % C = 65
```

### Number ↔ Atom Conversion
```prolog
atom_number('42', N).               % N = 42 (atom to number)
atom_number(A, 3.14).               % A = '3.14' (number to atom)
number_chars(42, Cs).               % Cs = ['4','2']
number_codes(42, Codes).            % Codes = [52, 50]
```

### Term ↔ Atom (read/write to atoms)
```prolog
term_to_atom(foo(1,2), A).          % A = 'foo(1,2)'
term_to_atom(T, 'foo(1,2)').        % T = foo(1,2)
with_output_to(atom(A), write(hi)). % A = hi  (capture output as atom)
```

### String Predicates (SWI-Prolog specific)
```prolog
string_concat("foo", "bar", S).     % S = "foobar"
string_length("hello", N).          % N = 5
string_lower("HELLO", S).           % S = "hello"
string_upper("hello", S).           % S = "HELLO"
split_string("a,b,c", ",", "", L).  % L = ["a","b","c"]
```

---

## 8d. Meta-Predicates (Term Inspection)

These allow Prolog programs to **inspect and construct terms at runtime** — this is what gives Prolog its reflective, meta-programming power.

### `functor/3` — Decompose a Term
```prolog
functor(Term, Name, Arity)

?- functor(foo(a, b, c), Name, Arity).  % Name = foo, Arity = 3
?- functor(42, Name, Arity).            % Name = 42,  Arity = 0
?- functor(T, foo, 2).                  % T = foo(_,_)  (construct!)
```

### `arg/3` — Get Nth Argument
```prolog
arg(N, Term, Arg)

?- arg(1, foo(a, b, c), X).  % X = a
?- arg(2, foo(a, b, c), X).  % X = b
```

### `=../2` — Univ Operator (Term ↔ List)
```prolog
Term =.. [Functor | Args]

?- foo(a, b) =.. L.          % L = [foo, a, b]
?- T =.. [bar, 1, 2, 3].     % T = bar(1, 2, 3)
?- atom(hello) =.. L.        % L = [hello]
```

### `copy_term/2` — Deep Copy with Fresh Variables
```prolog
?- copy_term(f(X, X), Copy).  % Copy = f(_A, _A) — same var, new instance
```

### `call/N` — Call a Goal Dynamically
```prolog
?- call(write, hello).             % prints hello — same as write(hello)
?- call(format, "~w~n", [42]).     % prints 42

% Useful for higher-order programming:
apply_to_list(_, []).
apply_to_list(Pred, [H|T]) :-
    call(Pred, H),
    apply_to_list(Pred, T).

?- apply_to_list(writeln, [a, b, c]).
% a
% b
% c
```

### `assert/retract` — Runtime Database Modification
```prolog
assert(likes(tom, ice_cream)).     % add fact
assertz(likes(tom, pizza)).        % add at end
asserta(likes(tom, sushi)).        % add at beginning
retract(likes(tom, ice_cream)).    % remove first match
retractall(likes(tom, _)).         % remove all matching
```

---

### Quick Reference: Operators at a Glance

```
┌──────────────────────────────────────────────────────────────┐
│  ARITHMETIC       │  COMPARISON        │  UNIFICATION        │
│  X is Expr        │  =:=  =\=          │  X = Y  (unify)     │
│  + - * /          │  <  >  =<  >=      │  X \= Y (cant unify)│
│  //  mod  rem     │  ==  \==  (struct) │  X == Y (identical) │
│  **  ^  abs       │  @<  @>  (order)   │  X =.. L (univ)     │
│  sqrt  sin  cos   │                    │                     │
│  floor  ceiling   │  LOGICAL           │  CONTROL            │
│  round  truncate  │  ,  (AND)          │  !  (cut)           │
│  max  min  sign   │  ;  (OR)           │  fail / true        │
│  pi  e            │  ->  (if-then)     │  \+  (negation)     │
└──────────────────────────────────────────────────────────────┘
```

---

## 9. Prolog Program Structure

```prolog
% ============================================
% Module declaration (optional in SWI-Prolog)
% ============================================
:- module(my_module, [predicate/arity]).

% ============================================
% Directives
% ============================================
:- dynamic fact/1.          % declare fact as modifiable
:- use_module(library(lists)).  % import library

% ============================================
% Facts
% ============================================
animal(dog).
animal(cat).
animal(bird).

can_fly(bird).

% ============================================
% Rules
% ============================================
has_legs(X) :- animal(X), \+ can_fly(X).

% ============================================
% Main entry point
% ============================================
:- initialization(main, main).

main :-
    write('Animals with legs:'), nl,
    forall(has_legs(X), (write(X), nl)).
```

---

## 10. Running Prolog (SWI-Prolog)

```bash
# Start interactive interpreter
swipl

# Load a file
?- consult('myfile.pl').
% OR
?- [myfile].

# Run a query
?- factorial(5, F).

# Exit
?- halt.

# Run from command line
swipl -g "consult('myfile.pl'), main, halt."
```

---

## 11. Cheatsheet – Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROLOG QUICK CHEATSHEET                      │
├─────────────────────────────────────────────────────────────────┤
│ SYNTAX                                                          │
│  fact(args).           → Fact (note the period!)               │
│  head :- body.         → Rule                                   │
│  ?- query.             → Query at prompt                        │
│  % comment             → Single-line comment                    │
│  /* comment */         → Multi-line comment                     │
│                                                                 │
│ VARIABLES                                                       │
│  X, Name, _Anon       → Variables (Uppercase/underscore start) │
│  _                     → Anonymous variable (never bound)       │
│                                                                 │
│ UNIFICATION                                                     │
│  X = Y                 → Unify X and Y                         │
│  X \= Y                → Fail if X and Y unify                 │
│                                                                 │
│ ARITHMETIC                                                       │
│  X is Expr             → Evaluate and bind                      │
│  =:=  =\=  <  >  =< >= → Arithmetic comparison                 │
│                                                                 │
│ LISTS                                                           │
│  [H|T]                 → Head and Tail pattern                 │
│  []                    → Empty list                             │
│  append/3, member/2, length/2, reverse/2, last/2, nth1/3       │
│                                                                 │
│ CONTROL                                                         │
│  !                     → Cut (no backtrack past here)          │
│  fail                  → Always fails                           │
│  true                  → Always succeeds                        │
│  \+ Goal               → Negation as failure                   │
│  ; (semicolon)         → OR                                     │
│  , (comma)             → AND                                    │
│                                                                 │
│ DATABASE                                                        │
│  assert/1, asserta/1, assertz/1                                 │
│  retract/1, retractall/1                                        │
│                                                                 │
│ I/O                                                             │
│  write/1, writeln/1, nl/0, read/1, format/2                    │
│                                                                 │
│ META                                                            │
│  functor/3, arg/3, =../2 (univ), call/N, findall/3, bagof/3   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. findall / bagof / setof

```prolog
% findall(Template, Goal, List)
% Collects ALL solutions for Template where Goal succeeds

age(peter, 7).
age(ann, 11).
age(pat, 8).

?- findall(X, age(X, _), L).     % L = [peter, ann, pat]
?- findall(X-A, age(X, A), L).   % L = [peter-7, ann-11, pat-8]

% bagof is like findall but fails when no solutions exist
% setof is like bagof but returns sorted, unique list
```

---

## 13. Difference Between Prolog and Imperative Languages

| Aspect | Prolog | Python/Java |
|---|---|---|
| Style | Declarative – *what* | Imperative – *how* |
| Control | Backtracking + Unification | Explicit loops, conditionals |
| Data | Terms & Lists | Objects, arrays |
| Functions | Predicates (succeed/fail) | Functions (return values) |
| Variables | Single-assignment | Mutable |
| Loops | Recursion | for/while |

---

## 14. Control Structures in Prolog

Prolog is **not purely recursive** — it has explicit control structures too.

### 14.1 If-Then-Else
```prolog
( Condition -> ThenBranch ; ElseBranch )

% Example
classify(N) :-
    ( N > 0  -> write(positive)
    ; N =:= 0 -> write(zero)
    ;            write(negative)
    ).
```
- `->` is the **if-then** operator
- `;` acts as **else** when paired with `->`
- Can be nested for multi-way branching

### 14.2 Conjunction and Disjunction
```prolog
Goal1, Goal2        % AND — both must succeed (left to right)
Goal1 ; Goal2       % OR  — try Goal1; if it fails, try Goal2
```

### 14.3 Cut, Fail, True
```prolog
!       % cut   — commits to current clause, stops backtracking past here
fail    % fail  — always fails, forces backtracking
true    % true  — always succeeds, a no-op
\+ Goal % negation-as-failure — succeeds if Goal cannot be proved
```

---

## 15. Loop Equivalents in Prolog

Prolog has **no built-in for/while loops**, but several patterns achieve the same effect:

### 15.1 `between/3` — Numeric Range Loop
```prolog
% Equivalent to: for i in range(1, 6): print(i)
?- between(1, 5, X), write(X), nl, fail ; true.
% Output: 1  2  3  4  5
```
- `between(Low, High, X)` — generates integers from `Low` to `High` on backtracking
- `fail` forces backtracking to get the next value
- `; true` ensures the overall query succeeds after exhausting all values

### 15.2 `forall/2` — For-All Loop
```prolog
% Equivalent to: for x in list: assert action(x) is true
?- forall(member(X, [2, 4, 6]), 0 =:= X mod 2).  % all even?  → true

% Print squares of a list
?- forall(member(X, [1,2,3,4]),
          (Y is X*X, format("~w^2 = ~w~n", [X, Y]))).
```
- `forall(Cond, Action)` — succeeds if `Action` succeeds for **every** solution of `Cond`
- Does NOT collect results — use `findall` for that

### 15.3 `maplist/2,3` — Map Over a List
```prolog
:- use_module(library(apply)).

% Apply a predicate to every element
?- maplist(write, [a, b, c]).           % prints: abc

% Transform every element
double(X, Y) :- Y is X * 2.
?- maplist(double, [1,2,3], Doubled).   % Doubled = [2,4,6]
```
- `maplist(Pred, List)` — calls `Pred(Elem)` for each element
- `maplist(Pred, List, Result)` — transforms each element

### 15.4 `include/3` and `exclude/3` — Filter
```prolog
:- use_module(library(apply)).

positive(X) :- X > 0.
?- include(positive, [-1, 2, -3, 4], Pos).  % Pos = [2, 4]
?- exclude(positive, [-1, 2, -3, 4], Neg).  % Neg = [-1, -3]
```

### 15.5 `foldl/4` — Fold/Reduce
```prolog
:- use_module(library(apply)).

% Sum a list using foldl
add(X, Acc, NewAcc) :- NewAcc is Acc + X.
?- foldl(add, [1,2,3,4,5], 0, Sum).   % Sum = 15
```
- `foldl(Pred, List, V0, V)` — accumulates a result by applying `Pred` to each element

### 15.6 `repeat/0` — While Loop
```prolog
% repeat always succeeds and generates infinite choice points
repeat.
repeat :- repeat.

% While-loop pattern: keep reading until user types 'quit'
read_loop :-
    repeat,
        write('Enter term (quit. to stop): '),
        read(X),
    X == quit, !.   % cut exits the repeat loop when condition met
```
- `repeat` creates an **infinite source of backtracking**
- Combined with `!` to break out when a condition is met
- The "loop body" runs each time Prolog backtracks into `repeat`

---

### Summary — Iteration Techniques

| Need | Use |
|---|---|
| Recurse over a list | Recursive predicate with `[H\|T]` pattern |
| Loop N times | `between(1, N, I)` + `fail ; true` |
| Check all elements satisfy a condition | `forall(Cond, Action)` |
| Transform a list | `maplist(Pred, List, Result)` |
| Filter a list | `include/3` or `exclude/3` |
| Accumulate/reduce | `foldl/4` |
| While loop | `repeat` + `!` |
| If-Then-Else | `( Cond -> Then ; Else )` |

---

## 16. Common Pitfalls

1. **Forgetting the period** `.` at end of each clause → Syntax error
2. **Using `=` for arithmetic** → `X = 3+4` gives `X = 3+4`, NOT 7. Use `is`.
3. **Infinite recursion** → Ensure base case is reached; check order of clauses.
4. **Variable naming** → `x` (lowercase) is an ATOM, not a variable! Use `X`.
5. **Cut abuse** → `!` makes predicates non-logical; use carefully.
6. **Left recursion** → May cause infinite loops; prefer right-recursive definitions.
