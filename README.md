# AI-Powered Symptom Checker and Appointment System

A Python-based web application that predicts disease categories based on user symptoms, recommends the most suitable doctor, and allows appointment scheduling.

## Features
- Type symptoms and receive the predicted disease category.
- Recommends the most appropriate specialist doctor.
- Users can book appointments directly through the web app.
- Uses NLP (SpaCy) with synonym mapping and fuzzy matching for accurate symptom detection.
- Flags emergency symptoms automatically.
- Stores and manages user interactions and appointments in Excel for tracking (local file).

## Tech Stack
- **Backend:** Python, Flask
- **Data Processing & NLP:** Pandas, SpaCy, RapidFuzz
- **Storage:** Excel (for appointment tracking)
- **Frontend:** HTML templates (Flask Jinja2)

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/gshankar631/AI-Symptom-Checker.git
cd AI-Symptom-Checker
