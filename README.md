# Interview Coach API

![Interview Coach Banner](https://github.com/snehabansal483/backend-repo/blob/main/Screenshots/Ai%20Interview%20Coach.png)

A Flask-based backend API that generates interview questions and answers using Google's Gemini AI, tailored to specific job roles, companies, and candidate backgrounds.

## Features

- 🎯 Generate personalized interview questions based on job role and experience level
- 💡 Get AI-powered suggested answers to interview questions
- 🔍 Context-aware responses considering company and project details
- 🌐 RESTful API endpoints with JSON responses
- 🔒 CORS enabled for frontend integration

## Tech Stack

- **Backend**: Python Flask
- **AI**: Google Gemini API
- **Environment**: Python 3.x
- **Deployment**: Ready for deployment with gunicorn

## Tech Stack Architecture

**Frontend**: 
- 🖥️ Streamlit (Python) - [Live Demo](https://interview-coach-frontend.onrender.com/)
- 🚀 Hosted on Render

**Backend**: 
- ⚙️ Flask REST API - [Live Demo](https://interview-coach-backend.onrender.com/)
- 🚀 Hosted on Render

**AI Core**:
- 🧠 Google's Gemini AI (integrated via backend API)

### Base URL
`https://interview-coach-backend.onrender.com/`

## API Endpoints

1. **Welcome Message**
   - `GET /`
   - Returns API information and available endpoints

2. **Generate Questions**
   - `POST /generate-questions`
   - Parameters:
     - `job_role` (required): The target job position
     - `company_name` (optional): The company name
     - `project` (optional): Relevant project experience
     - `experience_level` (optional): junior/mid-level/senior

3. **Generate Answer**
   - `POST /generate-answer`
   - Parameters:
     - `question` (required): The interview question to answer
     - `job_role` (optional): The target job position
     - `company_name` (optional): The company name
     - `project` (optional): Relevant project experience
     - `context` (optional): Additional context for the answer

## Getting Started

### Prerequisites

- Python 3.7+
- Google Gemini API key (set as environment variable `GEMINI_API_KEY`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/snehabansal483/backend-repo
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Gemini API key:
   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

**Development server:**
```bash
python app.py
```

**Production (using gunicorn):**
```bash
gunicorn app:app
```

The API will be available at `http://localhost:5000`

Ensure your `GEMINI_API_KEY` is set as an environment variable in your production environment.

## Example Requests

**Generate Questions**
```bash
curl -X POST http://localhost:5000/generate-questions   -H "Content-Type: application/json"   -d '{
    "job_role": "Data Scientist",
    "company_name": "Google",
    "project": "machine learning models for customer segmentation",
    "experience_level": "mid-level"
  }'
```

**Generate Answer**
```bash
curl -X POST http://localhost:5000/generate-answer   -H "Content-Type: application/json"   -d '{
    "question": "How would you handle missing data in a dataset?",
    "job_role": "Data Scientist",
    "company_name": "Google",
    "project": "customer segmentation models",
    "context": "Our dataset had 30% missing values in key demographic fields"
  }'
```

## Project Structure
```
 snehabansal483-backend-repo/
    ├── README.md             # Readme file
    ├── app.py                # Main application file
    ├── requirements.txt      # Python dependencies
    └── Screenshots/          # Application screenshots 
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For questions or feedback, please contact Sneha Bansal at snehabansal481@gmail.com
