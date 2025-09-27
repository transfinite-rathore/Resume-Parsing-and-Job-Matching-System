# Resume Parsing and Job Matching System

## Overview
The **Resume Parsing and Job Matching System** is a web-based application designed to automate the process of managing job applications. The system allows recruiters to upload job descriptions and receive a ranked list of applicants based on the match between resumes and job requirements. It also enables applicants to upload resumes, which are automatically parsed and scored against relevant job descriptions.

The system leverages **AI-driven keyword matching** and **resume encoding techniques** to calculate compatibility scores, simplifying recruitment and ensuring better candidate-job fit.

---

## Features

### For Applicants:
- Upload resumes in PDF format.
- Automatic extraction of key details from resumes (education, skills, experience).
- Secure authentication and profile management.

### For Recruiters:
- Post job descriptions with role, required experience, and package offered.
- Retrieve a ranked list of resumes matching job criteria.
- Track best-matched resumes with scores for informed hiring decisions.

### Core Functionalities:
- Resume parsing using NLP techniques.
- Keyword-based and encoding-based scoring for job-resume matching.
- Experience-based filtering and ranking.
- Background tasks for resume processing.
- Integration with **Cloudinary** for secure file storage.

---

## Tech Stack
- **Backend:** FastAPI, Python
- **Database:** MongoDB
- **Authentication:** JWT Tokens
- **File Storage:** Cloudinary
- **AI/ML:** NLP-based keyword matching, embedding-based resume scoring
- **Frontend (optional):** HTML/CSS/JS or React for interface

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Resume-Parsing-and-Job-Matching-System.git
   cd Resume-Parsing-and-Job-Matching-System
2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Configure environment variables in .env file:
   ```bash
   MONGO_URI=<your_mongodb_connection_string>
   CLOUD_NAME=<cloudinary_name>
   CLOUD_API_KEY=<cloudinary_api_key>
   CLOUD_API_SECRET=<cloudinary_api_secret>
   SECRET_KEY=<jwt_secret_key>
5. Start the application:
   ```bash
   uvicorn backend:run_app --reload
  
