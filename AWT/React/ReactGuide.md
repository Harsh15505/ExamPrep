# ⚛️ React.js Guide: Theory, Cheatsheet & Viva Questions

## 🧠 Section 1 — React.js Theory

### What is React?
React is an open-source JavaScript library developed by Facebook for building user interfaces, primarily for single-page applications (SPAs).
- **Component-Based:** UIs are broken down into small, reusable pieces called components.
- **Declarative:** You describe *what* the UI should look like for a given state, and React automatically updates and renders the right components when your data changes.
- **Virtual DOM:** React creates an in-memory data structure cache (the Virtual DOM), computes the resulting differences (diffing), and then updates the browser's displayed DOM efficiently.

### JSX (JavaScript XML)
JSX is a syntax extension for JavaScript that looks very similar to HTML. It allows you to write HTML structures in the same file as JavaScript code.
- **Rule 1:** Must return a single parent element (e.g., wrap everything in a `<div>` or `<> </>` fragment).
- **Rule 2:** Use `className` instead of `class`.
- **Rule 3:** JavaScript expressions must be wrapped in curly braces `{}`.

### State vs. Props
- **State (`useState`):** Data that is managed *inside* the component. If the state changes, the component re-renders. It is mutable (can be changed).
- **Props (Properties):** Data passed *from a parent component down to a child component*. Props are strictly **read-only** (immutable) inside the child component.

### Component Lifecycle (Functional Components)
Before Hooks, class components had specific lifecycle methods (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`). In modern functional React, **`useEffect`** handles all three phases:
1. **Mounting:** When the component first appears on the screen.
2. **Updating:** When the component's state or props change, causing a re-render.
3. **Unmounting:** When the component is removed from the screen (handled by returning a cleanup function inside `useEffect`).

### 🪝 In-Depth Guide to React Hooks
Hooks were introduced in React 16.8. They allow you to use state and other React features without writing a class component. 
**Rules of Hooks:**
1. **Only call Hooks at the top level:** Do not call them inside loops, conditions, or nested functions.
2. **Only call Hooks from React functional components** (or custom hooks).

#### 1. `useState` — Managing Local Data
- **What it does:** Allows you to add state variables to your component. When the state updates, React automatically re-renders the component to show the new data.
- **When to use it:** Whenever you have data that changes over time and needs to be reflected on the screen (e.g., input field values, toggle switches, shopping cart items).
- **How to use it:**
  ```jsx
  const [count, setCount] = useState(0); 
  // count: current value.
  // setCount: function to update the value.
  // 0: the initial value.
  
  // Usage:
  <button onClick={() => setCount(count + 1)}>Increment</button>
  ```

#### 2. `useEffect` — Handling Side Effects
- **What it does:** Tells React that your component needs to do something *after* render. This includes data fetching, setting up subscriptions, or manually changing the DOM.
- **When to use it:** When you need to interact with the outside world (APIs, LocalStorage, Timers like `setTimeout`).
- **How to use it:** It takes a callback function and an optional dependency array.
  ```jsx
  useEffect(() => {
    // 1. This code runs after render
    document.title = `You clicked ${count} times`;

    // 2. Optional Cleanup function (runs before component unmounts)
    return () => {
      console.log("Cleanup (like clearing a timer) happens here.");
    };
  }, [count]); // 3. Dependency Array: Only re-run if 'count' changes.
  ```
  - **No array:** Runs after *every* render.
  - **`[]` (Empty array):** Runs *exactly once* when the component mounts.
  - **`[state1, state2]`:** Runs when mounting AND whenever `state1` or `state2` changes.

#### 3. `useRef` — Referencing the DOM or Storing Mutable Data
- **What it does:** Returns a mutable object (`{ current: initialValue }`) that persists across renders. **Crucially, updating a ref does NOT trigger a component re-render.**
- **When to use it:** 
  1. To directly access a DOM element (e.g., to automatically focus an input field).
  2. To store a mutable value that you want to keep track of, but don't want to cause a re-render when it changes (like a timer ID).
- **How to use it:**
  ```jsx
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus(); // Directly interacts with the DOM
  };

  return <input ref={inputRef} type="text" />;
  ```

#### 4. `useContext` — Global State (Avoiding Prop Drilling)
- **What it does:** Allows you to subscribe to React context without having to pass props down manually at every single level (prop drilling).
- **When to use it:** For global data that many components need access to, such as the current authenticated user, UI theme (dark/light mode), or preferred language.
- **How to use it:**
  ```jsx
  // 1. Create it (usually in a separate file)
  const ThemeContext = createContext('light');

  // 2. Provide it (in a parent component)
  <ThemeContext.Provider value="dark">
    <ChildComponent />
  </ThemeContext.Provider>

  // 3. Consume it (in any deeply nested child)
  const theme = useContext(ThemeContext); // theme is now "dark"
  ```

#### 5. `useMemo` — Performance Optimization (Caching Values)
- **What it does:** Returns a memoized (cached) value. It only recalculates the value when one of its dependencies has changed.
- **When to use it:** Use it to prevent expensive, heavy calculations from running on every single render.
- **How to use it:**
  ```jsx
  const expensiveCalculation = useMemo(() => {
    return heavyMathFunction(count);
  }, [count]); // Only re-runs heavyMathFunction if 'count' changes.
  ```

#### 6. `useCallback` — Performance Optimization (Caching Functions)
- **What it does:** Returns a memoized callback function. It is very similar to `useMemo`, but instead of caching a *value*, it caches a *function definition*.
- **When to use it:** When passing functions down to highly optimized child components. If you don't use `useCallback`, a brand new function is created on every render, which will cause the child component to re-render unnecessarily.
- **How to use it:**
  ```jsx
  const handleSubmit = useCallback(() => {
    apiCall(data);
  }, [data]); // Function identity stays the same unless 'data' changes.
  ```

---

## ⚡ Section 2 — Quick Revision Cheatsheet

### 🟢 Core Syntax
| Concept | Example |
|---|---|
| **Component Structure** | `function MyComponent() { return <div>Hello</div>; } export default MyComponent;` |
| **JSX JavaScript Injection** | `<h1>{user.name}</h1>` |
| **Styling in JSX** | `<div style={{ backgroundColor: 'red', fontSize: '14px' }}>` |
| **Props Passing** | `<Child title="Hello" count={5} />` |
| **Props Receiving** | `function Child({ title, count }) { ... }` |

### 🎣 Hooks
| Hook | Usage / Example |
|---|---|
| **useState** | `const [count, setCount] = useState(0);` <br> `setCount(count + 1);` |
| **useEffect (Mount)** | `useEffect(() => { console.log("Loaded"); }, []);` |
| **useEffect (Update)** | `useEffect(() => { console.log("Count is now", count); }, [count]);` |
| **useRef (DOM access)** | `const inputRef = useRef(null);` <br> `<input ref={inputRef} />` <br> `inputRef.current.focus();` |

### 🛠️ Common Patterns
| Pattern | Example |
|---|---|
| **Conditional Rendering** | `{isLoggedIn ? <Dashboard /> : <Login />}` |
| **Short-Circuit Logic** | `{showWarning && <WarningMessage />}` |
| **List Rendering (.map)** | `{items.map(item => <li key={item.id}>{item.name}</li>)}` |
| **Event Handling** | `<button onClick={(e) => handleClick(e, id)}>Click</button>` |

---

## 🗣️ Section 3 — Viva Questions & Answers

**1. Q: What is React and who maintains it?**
> **A:** React is an open-source, component-based JavaScript library used for building user interfaces, primarily for single-page applications. It is maintained by Meta (formerly Facebook).

**2. Q: What is the Virtual DOM?**
> **A:** The Virtual DOM is an in-memory, lightweight representation of the actual Real DOM. React compares the Virtual DOM with a snapshot of the previous Virtual DOM (a process called "diffing"). It then computes the minimal number of changes required and updates only those specific parts of the Real DOM, making React highly performant.

**3. Q: What is JSX?**
> **A:** JSX stands for JavaScript XML. It is a syntax extension that allows us to write HTML directly within JavaScript code. Babel later compiles JSX into standard JavaScript `React.createElement()` calls.

**4. Q: Why can't browsers read JSX directly?**
> **A:** Browsers are built to only read regular JavaScript objects. JSX is not valid JavaScript. It must be transformed into standard JavaScript objects (using a transpiler like Babel) before reaching the browser.

**5. Q: What is the difference between State and Props?**
> **A:** Props (Properties) are used to pass data from a parent component to a child component and are read-only (immutable). State is a local data storage that is local to the component only and cannot be passed to other components directly. State is mutable and changes to it trigger a component re-render.

**6. Q: What are React Components?**
> **A:** Components are the building blocks of any React application. They are independent, reusable pieces of UI. There are two main types: Functional Components (modern) and Class Components (legacy).

**7. Q: Why do we need the `key` prop when rendering lists in React?**
> **A:** Keys help React identify which items in a list have changed, been added, or been removed. Providing a unique key (like a database ID) to list elements gives elements a stable identity and optimizes the Virtual DOM diffing process, preventing unnecessary re-renders.

**8. Q: What are React Hooks?**
> **A:** Hooks are functions introduced in React 16.8 that allow you to "hook into" React state and lifecycle features from functional components, eliminating the need to write class components.

**9. Q: Explain the `useState` hook.**
> **A:** `useState` is a hook that allows functional components to manage local state. It returns an array with two values: the current state and a function to update it. When the setter function is called, React automatically re-renders the component to reflect the new state.

**10. Q: Explain the `useEffect` hook.**
> **A:** `useEffect` allows you to perform side effects in functional components, such as data fetching, setting timers, or manually changing the DOM. It takes a callback function and an optional dependency array. It combines the capabilities of `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` from class components.

**11. Q: What happens if you don't pass a dependency array to `useEffect`?**
> **A:** If the dependency array is completely omitted, the `useEffect` callback will run after *every single render* of the component, which can lead to infinite loops if state is updated inside it.

**12. Q: What does passing an empty array `[]` to `useEffect` do?**
> **A:** It tells React that the effect doesn't depend on any values from props or state. Therefore, the effect will only run exactly once, when the component initially mounts (loads) onto the screen.

**13. Q: What is prop drilling and how can you avoid it?**
> **A:** Prop drilling is the process of passing data from a high-level parent component down through multiple layers of intermediate child components just to reach a deeply nested component that actually needs the data. It can be avoided using the Context API (`useContext`) or state management libraries like Redux.

**14. Q: What is the `useRef` hook?**
> **A:** `useRef` returns a mutable reference object whose `.current` property is initialized to the passed argument. Crucially, modifying `.current` does *not* cause a re-render. It is commonly used to directly access DOM elements (like focusing an input field) or storing mutable values across renders without triggering UI updates.

**15. Q: What is conditional rendering?**
> **A:** It is the practice of rendering different UI markup based on certain conditions (usually state or props). This is typically achieved using the logical AND operator (`&&`) for short-circuiting, or the ternary operator (`condition ? trueComponent : falseComponent`).

**16. Q: Why is it bad to mutate state directly (e.g., `state.count = 1`)?**
> **A:** Direct mutation does not notify React that the state has changed. Because React isn't aware of the change, it will not trigger a re-render, and the UI will not update. Always use the setter function provided by `useState` (e.g., `setCount(1)`).

**17. Q: What is a React Fragment (`<> </>`)?**
> **A:** A React Fragment is a pattern that lets you group a list of children without adding extra, unnecessary nodes (like a wrapper `<div>`) to the Real DOM. It helps keep the HTML output clean.

**18. Q: How do you handle forms in React?**
> **A:** Forms in React are typically implemented as "Controlled Components". This means the form data (like the value of an `<input>`) is strictly controlled by React state. The `value` attribute is tied to a state variable, and an `onChange` event handler is used to update the state as the user types.

**19. Q: What is `e.preventDefault()` and why is it used in forms?**
> **A:** In standard HTML, submitting a form causes the browser to reload the page or navigate to a new URL. In a React Single Page Application (SPA), we want to prevent this default behavior so we can handle the submission entirely in JavaScript without losing our current state.

**20. Q: What are Higher-Order Components (HOC)?**
> **A:** An HOC is an advanced technique for reusing component logic. It is a function that takes a component and returns a new component, injecting additional props or wrapping it with extra functionality (e.g., adding authentication checks before rendering a dashboard).

**21. Q: What is the Context API?**
> **A:** The Context API provides a way to share values (like global themes, authenticated user data, or preferred language) between components without having to explicitly pass a prop through every level of the tree.

**22. Q: Explain the spread operator (`...`) as used in React state.**
> **A:** Because state in React should be treated as immutable, the spread operator is used to create a shallow copy of arrays or objects before modifying them. For example: `setTasks([...tasks, newTask])` copies all existing tasks and appends the new one, returning a brand new array to trigger a re-render.

**23. Q: What is the difference between a Functional Component and a Class Component?**
> **A:** Functional components are simpler, written as plain JavaScript functions, and use Hooks to manage state and side effects. Class components require ES6 class syntax, extend `React.Component`, and use specific lifecycle methods. Modern React development strictly favors Functional components.

**24. Q: How is routing handled in React?**
> **A:** React itself does not include routing. It relies on third-party libraries, most commonly `react-router-dom`, to handle navigation between different views or pages without reloading the browser window.

**25. Q: What is Strict Mode in React?**
> **A:** `<React.StrictMode>` is a tool for highlighting potential problems in an application. It does not render any visible UI. It activates additional checks and warnings for its descendants, such as identifying unsafe lifecycles or unexpected side effects. (Note: It causes components to render twice in development mode to catch bugs).
