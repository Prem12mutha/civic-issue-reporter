# Civic Issue Reporter

A full-stack web application built with Django for reporting, tracking, and managing civic issues in the Ahmedabad Municipal Corporation (AMC) and Gandhinagar Municipal Corporation (GMC).

## ✨ Features
*   **Premium Glassmorphic UI:** Modern dark theme with interactive elements and animations.
*   **Live Dashboard:** Real-time statistics on total, pending, in-progress, and resolved complaints.
*   **Multi-Step Reporting Form:** Submit complaints with category selection, image upload, and an interactive Leaflet.js map for location pinning.
*   **Public Feed:** Browse community issues with dynamic filters (by status and municipality).
*   **User Authentication:** Secure registration and login system for citizens.
*   **Admin Panel:** Built-in Django admin interface for officials to update complaint statuses.

## 🚀 Getting Started

Follow these instructions to run the project locally on your machine.

### Prerequisites
*   Python 3.10 or higher
*   Git (optional, to clone the repo)

### Installation

1. **Clone the repository** (or download and extract the ZIP file):
   ```bash
   git clone https://github.com/YOUR_USERNAME/civic-issue-reporter.git
   cd civic-issue-reporter
   ```

2. **Create a virtual environment:**
   ```bash
   # On Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. Open your web browser and go to: `http://127.0.0.1:8000/`

## 👤 Admin Access
To access the admin panel and change complaint statuses, you need to create a superuser account:
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account, then log in at `http://127.0.0.1:8000/admin`.

## 🛠️ Tech Stack
*   **Backend:** Python, Django 6.0.4
*   **Database:** SQLite (Default for development)
*   **Frontend:** HTML5, Custom CSS, Bootstrap 5 (Grid & utilities), FontAwesome 6
*   **Mapping:** Leaflet.js (OpenStreetMap)
