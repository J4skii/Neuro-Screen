  🧠 Intelligent Learning Disability Detection and Support System

An interactive web application for **detecting and supporting learning disabilities** (Dyslexia, Dyscalculia, and Working Memory issues) in higher education.  
Built with **Flask + SQLAlchemy + TailwindCSS** and optionally integrated with **Firebase Firestore** for cloud collaboration.

---

   🚀 Features

- **Digital Assessments**
  - Dyslexia test (reading & recognition)
  - Dyscalculia test (numbers & calculations)
  - Memory test (timed image recall grid)

- **Scoring & Result Tracking**
  - Accurate scoring logic for each test
  - Results stored in SQL database
  - Optional dual-write to Firebase Firestore

- **Visual Feedback**
  - Animated charts (Chart.js) on results page
  - Dark/Light mode toggle (persists across sessions)
  - Global Back/Home navigation bar

- **Admin Dashboard**
  - View and filter student results
  - Export results as CSV
  - Secure login with Flask-Login

- **Modern UI**
  - Tailwind CSS design
  - Responsive layout (desktop & mobile)
  - Accessible and student-friendly

---
🛠️ Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML, Jinja2, TailwindCSS, Chart.js
- **Database:** SQLite (local) / PostgreSQL (production via Render)
- **Cloud (optional):** Firebase Firestore for team sync
- **Deployment:** Render (Procfile included)

---
📦 Installation
1. Clone repo
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Create virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate      on Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run locally
bash
Copy
Edit
python app.py
App runs at: http://127.0.0.1:5000

🔑 Environment Variables
Variable	Description
SECRET_KEY	Flask session secret key
DATABASE_URL	SQLAlchemy database URI (e.g., from Render Postgres)
FIREBASE_CREDENTIALS_JSON (optional)	Raw JSON credentials from Firebase service account

☁️ Deploy on Render
Push to GitHub.

Create Render Web Service.

Connect repo, add Procfile:

makefile
Copy
Edit
web: python app.py
Add environment variables:

SECRET_KEY

DATABASE_URL (Render Postgres)

FIREBASE_CREDENTIALS_JSON (optional)

📊 Firebase Integration (Optional)
Enable Firestore in Firebase console.

Create a Service Account → download JSON key.

Store entire JSON as an env variable:

bash
Copy
Edit
export FIREBASE_CREDENTIALS_JSON='{...}'
Results will also sync to Firestore under results/.

👥 Project Team
Team Lead: [Your Name]

Developers: [List team members]

Institution: Durban University of Technology

Module: SODM401 – Software Development Methodologies

📌 Roadmap / Future Enhancements
 Gamified test experience for higher engagement

 Adaptive testing (difficulty scaling)

 Detailed advisor dashboard with trends & insights

 Email notifications for test completions

 Full Firebase Hosting + Authentication
