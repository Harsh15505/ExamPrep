# ⚠️ OFFLINE EXAM SURVIVAL GUIDE: REQUIREMENTS & SETUP

Since your exam is conducted **without internet access**, you must prepare your machine *today* while you still have a connection. Package managers like `npm` and `pip` will fail tomorrow if they try to fetch tools from the internet.

This document contains everything you need to install today, and how to successfully start and test projects tomorrow while completely offline.

---

## 🐍 1. Django (Python)

### ⬇️ Pre-Install Requirements (Do this TODAY)
You need to install Django globally so it is cached and available offline. Open terminal and run:
1. `pip install django`
2. `pip install psycopg2` (Only if you plan to use PostgreSQL. If using default SQLite, skip this).
3. Ensure **Postman** is installed for testing APIs (if asked to build Django Rest Framework).
4. *Note: If using SQLite, no database setup is required. If using PostgreSQL, ensure pgAdmin/Postgres server is installed and running locally.*

### 🚀 How to Start a New Project (Tomorrow, Offline)
1. **Create Project:** `django-admin startproject exam_project`
2. **Navigate In:** `cd exam_project`
3. **Create App:** `python manage.py startapp myapp`
4. **Register App:** Open `exam_project/settings.py` and add `'myapp'` to the `INSTALLED_APPS` list.
5. **Run Migrations:** `python manage.py migrate` (This creates the local SQLite file).
6. **Create Superuser (Optional):** `python manage.py createsuperuser`

### 🧪 How to Test & Run
1. Start the server: `python manage.py runserver`
2. Open your browser and go to: `http://127.0.0.1:8000`
3. If building an API, open Postman and send GET/POST requests to your configured URLs.

---

## 🟢 2. Express.js / Node.js

### ⬇️ Pre-Install Requirements (Do this TODAY)
You **can** install npm packages globally, but Node.js doesn't automatically look in the global folder when you use `require('express')`. To fix this offline, we use the `npm link` command!

Today, while online, run this to install everything globally:
`npm install -g express mongoose method-override ejs cors dotenv nodemon`

**MongoDB Local:** Ensure **MongoDB Compass** is installed and the local MongoDB server is actively running on your machine (URI: `mongodb://localhost:27017`).

### 🚀 How to Start a New Project (Tomorrow, Offline)
1. **Create Folder:** `mkdir express_exam && cd express_exam`
2. **Initialize:** `npm init -y`
3. **Link Global Packages:** Since you are offline, instead of `npm install`, you will link the global packages you downloaded yesterday into this local folder:
   `npm link express mongoose` (add any other packages you need, like `ejs` or `cors`)
4. **Structure:** Manually create your `app.js` file, and `models/`, `routes/`, `views/` folders.

### 🧪 How to Test & Run
1. Start server: `node app.js` (or `nodemon app.js` if you want auto-reloads).
2. **For REST APIs (Backend only):**
   - Open **Postman**.
   - Create a New Request.
   - For `POST` or `PUT`: Select **Body** -> **raw** -> Select **JSON** from the dropdown.
   - Enter your JSON (e.g., `{"title": "Book 1"}`) and hit Send.
3. **For EJS (Frontend):** Open browser to `http://localhost:3000`.

---

## ⚛️ 3. React.js

### ⬇️ Pre-Install Requirements (Do this TODAY)
**🚨 CRITICAL WARNING:** You CANNOT run `npx create-react-app` tomorrow without internet. It will fail.

**THE OFFLINE HACK:**
Today, right now, run this in your AWT folder:
1. `npx create-react-app blank-react-app`
2. `cd blank-react-app`
3. `npm install`
*Do not delete this folder! This is your golden template.*

### 🚀 How to Start a New Project (Tomorrow, Offline)
1. **DO NOT** use `npx`.
2. Simply **Copy and Paste** the `blank-react-app` folder you made yesterday.
3. Rename the copied folder to whatever the exam question is (e.g., `todo-app`).
4. `cd todo-app`
5. Open VS Code and start writing your code inside `src/App.js` (Note: CRA uses `.js` by default, not `.jsx`).

### 🧪 How to Test & Run
1. Start the React server: `npm start`
2. Open your browser and go to: `http://localhost:3000`
3. Check the browser console (F12 -> Console) for any React errors or warnings.

---

## 🌶️ 4. Flask (Python)

### ⬇️ Pre-Install Requirements (Do this TODAY)
1. Install Flask globally: `pip install flask flask-sqlalchemy`
2. **🚨 CSS WARNING:** In the previous guide, we used a Bootstrap CDN (a web link) for styling. Without internet, that link will fail, and your app will look like plain 1990s HTML. 
   - **Fix:** If you want styling tomorrow, download `bootstrap.min.css` today, or be prepared to write your own basic CSS in a `static/style.css` file.

### 🚀 How to Start a New Project (Tomorrow, Offline)
1. **Create Folder:** `mkdir flask_exam && cd flask_exam`
2. **Create Backend:** Create a file named `app.py`.
3. **Create Folders:**
   - `mkdir templates` (MUST be exactly this name. Put your `.html` files here).
   - `mkdir static` (Put your `.css` or images here).
4. **Database:** If using SQLAlchemy, just write the `db.create_all()` code block in `app.py`. The SQLite `instance/app.db` file will generate automatically when you run the app. No manual setup needed.

### 🧪 How to Test & Run
1. Start the server: `python app.py`
2. Open your browser and go to: `http://127.0.0.1:5000`
3. If an error occurs, look at the terminal output or the detailed Flask debug page in the browser (if `debug=True` is set).

---

## 🛠️ Essential Tools to Verify Today
Before going to sleep, ensure you can open and run these without an internet connection:
- [ ] **VS Code** (Ensure extensions like Prettier and Python/ESLint are active).
- [ ] **Postman** (You can use the desktop app offline without logging in. Just use the 'Scratch Pad' or lightweight API client mode).
- [ ] **MongoDB Compass** (Ensure it connects to `mongodb://localhost:27017` successfully).
- [ ] **pgAdmin** (If you are using PostgreSQL for Django).
