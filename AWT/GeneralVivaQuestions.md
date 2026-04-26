# 🌐 Advanced Web Technology: General Viva Questions

This guide contains 50 fundamental Web Technology questions that apply universally, regardless of whether you are using Django, Express, React, or Flask.

---

## 📡 Part 1: Internet & HTTP Basics

**1. Q: What is HTTP and how does it work?**
> **A:** HTTP (HyperText Transfer Protocol) is the foundation of data communication on the web. It is a request-response protocol where a client (browser) sends a request to a server, and the server returns a response (like an HTML page or JSON data).

**2. Q: What is the difference between HTTP and HTTPS?**
> **A:** HTTPS is the secure version of HTTP. It uses SSL/TLS encryption to protect data in transit between the client and the server, preventing hackers from intercepting sensitive information like passwords.

**3. Q: What are the most common HTTP Methods?**
> **A:** `GET` (retrieve data), `POST` (submit/create new data), `PUT` (update/replace existing data), `PATCH` (partially update data), and `DELETE` (remove data).

**4. Q: What is the difference between POST and PUT?**
> **A:** `POST` is used to create a completely new record. `PUT` is used to update an existing record by replacing it entirely. `PUT` is idempotent (calling it 10 times has the same effect as calling it once), while `POST` is not (calling it 10 times creates 10 records).

**5. Q: Explain the categories of HTTP Status Codes.**
> **A:**
>
> - **1xx:** Informational
> - **2xx:** Success (200 OK, 201 Created)
> - **3xx:** Redirection (301 Moved Permanently)
> - **4xx:** Client Errors (400 Bad Request, 401 Unauthorized, 404 Not Found)
> - **5xx:** Server Errors (500 Internal Server Error)

**6. Q: What is a RESTful API?**
> **A:** REST (Representational State Transfer) is an architectural style for APIs. It relies on standard HTTP methods (GET, POST, PUT, DELETE), is stateless (no client session data is stored on the server), and exchanges data typically in JSON format.

**7. Q: What does "Stateless" mean in REST?**
> **A:** It means the server does not store any memory of past requests. Every single request from the client must contain all the information the server needs to fulfill it (like an authentication token).

**8. Q: What is JSON?**
> **A:** JSON (JavaScript Object Notation) is a lightweight data-interchange format. It is easy for humans to read and write, and easy for machines to parse and generate. It uses key-value pairs (like Python dictionaries).

**9. Q: What is CORS?**
> **A:** CORS (Cross-Origin Resource Sharing) is a security feature implemented by web browsers. It prevents a malicious website from making API requests to a different domain without permission. The server must explicitly send CORS headers allowing the client's domain to access its data.

**10. Q: How do you fix a CORS error?**
> **A:** The backend server must be configured to accept requests from the frontend's origin. In Express, this is done using the `cors` middleware package. In Django, it's done using `django-cors-headers`.

---

## 🗄️ Part 2: Databases (SQL vs NoSQL)

**11. Q: What is the difference between SQL and NoSQL databases?**
> **A:** SQL databases (PostgreSQL, MySQL) are relational, use structured tables with fixed schemas, and are best for complex queries. NoSQL databases (MongoDB) are non-relational, store data as flexible JSON-like documents, and scale horizontally very well.

**12. Q: What does ACID stand for in databases?**
> **A:** It defines properties that guarantee database transactions are processed reliably.
>
> - **A**tomicity: All or nothing (if part of a transaction fails, the whole thing rolls back).
> - **C**onsistency: Data must be valid according to defined rules.
> - **I**solation: Concurrent transactions don't interfere with each other.
> - **D**urability: Once committed, data is saved permanently, even during power loss.

**13. Q: What is a Primary Key?**
> **A:** A unique identifier for every record (row) in a database table. It cannot be NULL, and no two rows can share the same primary key.

**14. Q: What is a Foreign Key?**
> **A:** A column in one table that links to the primary key of another table. It is used to establish relationships between tables (e.g., linking a `user_id` in an `Orders` table to the `id` in a `Users` table).

**15. Q: What are Database Indexes?**
> **A:** An index is a data structure that improves the speed of data retrieval operations on a table at the cost of slower writes and more storage space. It acts like the index at the back of a book.

**16. Q: What is an ORM / ODM?**
> **A:** ORM (Object-Relational Mapper, like Django ORM or SQLAlchemy) and ODM (Object-Document Mapper, like Mongoose) allow developers to interact with a database using Object-Oriented code (Python/JS classes) instead of writing raw SQL/Mongo queries.

**17. Q: What are SQL Joins?**
> **A:** Joins are used to combine rows from two or more tables based on a related column between them (e.g., INNER JOIN, LEFT JOIN, RIGHT JOIN).

**18. Q: What is Database Normalization?**
> **A:** The process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables.

**19. Q: In MongoDB, what is a Collection and a Document?**
> **A:** A Collection in MongoDB is equivalent to a Table in SQL. A Document is a single JSON-like record inside that collection, equivalent to a Row in SQL.

**20. Q: What is the CAP Theorem?**
> **A:** It states that a distributed database system can only guarantee two out of three characteristics at the same time: Consistency, Availability, and Partition tolerance.

---

## 🔒 Part 3: Authentication & Security

**21. Q: What is the difference between Authentication and Authorization?**
> **A:** Authentication verifies *who* you are (logging in with email/password). Authorization determines *what you are allowed to do* (checking if you have admin privileges to delete a post).

**22. Q: What are Cookies?**
> **A:** Small pieces of data stored on the user's browser by the server. They are automatically sent back to the server with every subsequent HTTP request. Used for sessions, tracking, and user preferences.

**23. Q: What is a Session?**
> **A:** A way to store data across multiple HTTP requests. The server stores user data in memory/DB and sends a unique "Session ID" cookie to the browser. The browser sends this ID back so the server remembers who the user is.

**24. Q: What is a JWT (JSON Web Token)?**
> **A:** A stateless authentication mechanism. The server generates an encrypted token containing user data and sends it to the client. The client sends this token in the header of future requests. The server verifies the token's signature without needing to look up a session in the database.

**25. Q: JWT vs Sessions: Which is better?**
> **A:** Sessions are better for traditional server-rendered apps (like Django/EJS) because you can instantly revoke them. JWTs are better for REST APIs and microservices because they are stateless, reducing database load.

**26. Q: What is Password Hashing?**
> **A:** The process of converting a plain-text password into an unreadable string using a one-way mathematical function (like `bcrypt`). Unlike encryption, hashing cannot be reversed. If the database is hacked, the passwords remain safe.

**27. Q: What is Salting?**
> **A:** Adding a unique, random string of characters (the salt) to a password *before* it is hashed. This prevents hackers from using pre-computed "rainbow tables" to crack common passwords.

**28. Q: What is CSRF (Cross-Site Request Forgery)?**
> **A:** An attack where a malicious site tricks a user's browser into making an unwanted request to a trusted site where the user is currently authenticated. Frameworks like Django prevent this using CSRF Tokens generated for every form.

**29. Q: What is XSS (Cross-Site Scripting)?**
> **A:** An attack where a hacker injects malicious JavaScript into a website (e.g., via a comment section). When other users view the page, the script executes in their browser, potentially stealing their cookies. Prevented by escaping/sanitizing user input.

**30. Q: What is SQL Injection?**
> **A:** An attack where malicious SQL statements are inserted into input fields to manipulate the database (e.g., dropping tables or bypassing login). Using ORMs (like Prisma, Mongoose, or Django ORM) automatically prevents this.

---

## 💻 Part 4: Frontend & Browser Mechanics

**31. Q: What is the DOM (Document Object Model)?**
> **A:** A programming interface for web documents. It represents the page so that programs can change the document structure, style, and content. The DOM represents the document as nodes and objects (a tree structure).

**32. Q: What is LocalStorage vs SessionStorage vs Cookies?**
> **A:**
>
> - **LocalStorage:** Stores data in the browser permanently (until manually cleared). Capacity ~5MB. Not sent to server automatically.
> - **SessionStorage:** Stores data only for the duration of the page session (clears when the tab is closed).
> - **Cookies:** Small (4KB), sent to the server automatically with every request. Can have expiration dates.

**33. Q: What is a Single Page Application (SPA)?**
> **A:** A web application (like React or Vue) that loads a single HTML page. It dynamically updates the content on that page as the user interacts with it, rather than fetching entirely new HTML pages from the server (which is faster and smoother).

**34. Q: What is AJAX?**
> **A:** Asynchronous JavaScript and XML. A set of techniques used to send and retrieve data from a server asynchronously (in the background) without interfering with the display and behavior of the existing page.

**35. Q: What does `async / await` do in JavaScript?**
> **A:** It is syntactic sugar for JavaScript Promises. It allows developers to write asynchronous, non-blocking code (like fetching data from an API) in a way that looks synchronous and is easier to read.

**36. Q: What is the difference between `let`, `const`, and `var`?**
> **A:** `var` is function-scoped and can be re-declared. `let` is block-scoped and can be updated but not re-declared. `const` is block-scoped and cannot be updated or re-declared (though properties of `const` objects can be mutated).

**37. Q: Explain the CSS Box Model.**
> **A:** Every element in web design is a rectangular box. The box model consists of: Content (the text/image), Padding (space around content), Border (line around padding), and Margin (space outside the border).

**38. Q: What are CSS Media Queries?**
> **A:** A CSS technique used to apply different styling rules based on the device's characteristics, primarily screen width. It is the foundation of Responsive Web Design.

**39. Q: What is Webpack / Vite?**
> **A:** They are modern build tools (bundlers) for frontend projects. They take your JavaScript, CSS, and images, optimize them, and bundle them into smaller files that the browser can load faster.

**40. Q: What is the difference between Client-Side Rendering (CSR) and Server-Side Rendering (SSR)?**
> **A:** In CSR (e.g., standard React), the server sends a blank HTML page and JavaScript builds the UI in the browser. In SSR (e.g., Django, EJS, Next.js), the server fully renders the HTML page with data before sending it to the browser.

---

## 🏗️ Part 5: Architecture, Servers, & Deployment

**41. Q: What is MVC Architecture?**
> **A:** Model-View-Controller. A design pattern that separates an application into three logic components:
>
> - **Model:** Handles database logic and data representation.
> - **View:** Handles the frontend UI and HTML rendering.
> - **Controller:** Handles the user input, processes it, and connects the Model to the View.

**42. Q: What is MVT Architecture?**
> **A:** Model-View-Template. This is Django's specific variation of MVC. The "Model" handles the DB, the "Template" handles the HTML UI (equivalent to the 'View' in MVC), and the "View" handles the python business logic (equivalent to the 'Controller' in MVC).

**43. Q: What is a Webhook?**
> **A:** A way for one application to send automated, real-time data to another application when a specific event happens (e.g., Stripe sending a webhook to your server when a payment is successful). Unlike APIs, you don't have to constantly ask (poll) for the data.

**44. Q: What is a Web Server vs an App Server?**
> **A:** A Web Server (like Nginx or Apache) handles raw HTTP requests and serves static files (HTML, CSS, Images). An App Server (like Gunicorn for Python, or Node.js) actually runs the programming logic to generate dynamic responses.

**45. Q: What is Caching?**
> **A:** The process of storing copies of frequently accessed data in a temporary storage location (like Redis or browser cache) so that future requests for that data can be served much faster without hitting the main database.

**46. Q: What is a Reverse Proxy?**
> **A:** A server (like Nginx) that sits in front of one or more backend web servers. It intercepts all incoming requests from the internet, forwards them to the appropriate backend server, and then returns the response. It is used for load balancing, security, and SSL termination.

**47. Q: What is Load Balancing?**
> **A:** Distributing incoming network traffic evenly across a group of backend servers. This ensures no single server becomes overwhelmed, improving responsiveness and availability.

**48. Q: What is CI/CD?**
> **A:** Continuous Integration and Continuous Deployment. A set of practices where code changes are automatically built, tested (CI), and deployed to production servers (CD) multiple times a day.

**49. Q: What is Docker?**
> **A:** A platform that packages an application and all its dependencies (Node versions, libraries) into a standardized unit called a Container. This ensures the app runs exactly the same on any computer or server.

**50. Q: What is an API Endpoint?**
> **A:** A specific URL where an API can be accessed by a client application. For example, `https://api.myapp.com/v1/users` is an endpoint used to interact with user data.
