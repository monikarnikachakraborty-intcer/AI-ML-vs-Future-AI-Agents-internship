# AI-ML-vs-Future-AI-Agents-internship
Author- Monikarnika Chakraborty

# Students Database CRUD Application

A robust Python backend application built to manage student records natively using **FastAPI** for API routing and **SQLite** for robust persistent storage.

## 🚀 Features
- **Full CRUD Management:** Completely supports Creating, Reading, Updating, and Deleting student profiles.
- **Robust Data Validation:** Strong schema constraints powered by Pydantic (including type-safe email validation).
- **Persistent Storage:** Standalone local SQLite integration requiring zero infrastructure setups.

## 🛠️ Prerequisites
Ensure you have **Python 3.8+** configured on your local workstation.

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <repo-folder-name>
   ```

2. **Install application dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend development environment:**
   ```bash
   uvicorn main:app --reload
   ```

The application server will spin up locally on: `http://127.0.0.1:8000`

## 📑 API Interactive Dashboard
Once the local server is operating, access the self-documenting interactive dashboard to view, mock, and test endpoints live:
- **Swagger UI Docs:** [http://127.0.0](http://127.0.0)

## 📡 Exposed Target Endpoints
- `POST /students` - Register/Add a new student profile.
- `GET /students` - Query and list all records (supports optional `?course=` filtering).
- `GET /students/{student_id}` - Extract a specific student dossier.
- `PUT /students/{student_id}` - Update existing profile attributes dynamically.
- `DELETE /students/{student_id}` - Permanently drop a student record.

