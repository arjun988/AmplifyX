# Squid Session Management System 🦑

## Overview 🌟
The **Squid Session Management System** is a powerful backend system designed to securely store user preferences, track user activities, and manage sessions in the Squid app. It allows for a seamless user experience by enabling personalization through saved preferences such as theme, notifications, and language, and efficiently tracks user session data like pages visited, session start times, and duration. Whether you're accessing from a mobile device or desktop, Squid ensures your preferences and activity are always in sync! 🌐🔄

## Key Features 🚀

- **User Preferences**: Securely store and manage user preferences (theme, notifications, language) via cookies for persistence across sessions.
- **Session Tracking**: Maintain detailed session data for logged-in users, including pages visited and session duration.
- **Cross-Device Syncing**: Automatically sync preferences and session data across devices for authenticated users. 🖥️📱
- **Activity Logging**: Track user actions within the session (e.g., "clicked on Settings", "viewed dashboard").
- **Pagination**: Support for pagination of session and activity logs to handle large datasets efficiently.

## Technologies Used 💻

- **Backend**: 
  - Flask (Python web framework)
  - Flask-PyMongo (MongoDB integration)
  - Flask-Bcrypt (Password hashing)
  - Express-session (for session management)
- **Frontend**: React (for building the user interface)
- **Database**: MongoDB (for storing user data and session logs)

## Requirements ⚙️

- Python 3.x
- Flask
- Flask-PyMongo
- Flask-Bcrypt
- MongoDB (local or cloud service)

## Installation 📥

### Backend Setup 🏗️

1. **Clone this repository**:
    ```bash
    git clone https://github.com/arjun988/AmplifyX.git
    cd AmplifyX
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the necessary dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB**:
   - Install MongoDB locally or use a cloud MongoDB service (e.g., MongoDB Atlas).
   - Update the `MONGO_URI`with your connection string.

5. **Run the Flask app**:
    ```bash
    cd backend
    python run.py
    ```

   The backend will be available at `http://127.0.0.1:5000/`.

---

### Frontend Setup (React) 🔥

1. **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2. **Install frontend dependencies**:
    ```bash
    npm install
    ```

3. **Run the React app**:
    ```bash
    npm start
    ```

   The frontend will be available at `http://localhost:3000/`.

---

## API Endpoints 📡

### User Preferences
- **POST** `/api/preferences`: Save user preferences.
  - Request Body:
    ```json
    {
      "theme": "dark",
      "notifications": "enabled",
      "language": "English"
    }
    ```

- **GET** `/api/preferences`: Retrieve saved user preferences.

### Session Management
- **POST** `/api/session`: Start a new session (initialize).
- **GET** `/api/session`: Fetch session details (e.g., pages visited, start time, duration).
  - Supports pagination with `page` and `per_page` query parameters.

- **POST** `/api/session/page`: Log a page visit during the session.
  - Request Body:
    ```json
    {
      "page": "dashboard"
    }
    ```

- **DELETE** `/api/session`: End the current session.

### Authentication Routes
- **POST** `/api/register`: Register a new user.
- **POST** `/api/login`: Log in an existing user.
- **POST** `/api/logout`: Log out the current user.

### Activity Logging
- **GET** `/api/activities`: Retrieve user activities, with pagination support for `page` and `per_page` query parameters.

---

## System Behavior ⚙️

- **Session Expiration**: Sessions expire after 30 minutes of inactivity to enhance security.
- **Preferences**: Preferences are stored in cookies with the following secure configurations:
  - `HttpOnly`: Prevents client-side JavaScript access.
  - `Secure`: Only enabled in production over HTTPS.
  - `SameSite`: Restricts third-party cookie access.

- **Error Handling**: 
  - Returns appropriate HTTP status codes for errors (e.g., `400 Bad Request`, `401 Unauthorized`).
  - Validates request bodies for required fields to ensure data integrity.

---

## Bonus Features 🎁

- **Cross-Device Syncing**: Preferences and session data sync seamlessly across all devices for authenticated users. Whether on mobile or desktop, your experience is always consistent! 🌍
- **Activity Tracking**: Detailed logging of user activities, including page visits, updates to preferences, and more.
- **Pagination Support**: Efficient handling of large logs with pagination for session and activity data.

