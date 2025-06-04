# Resume Matcher (FastAPI)

A resume-job description matching API with PDF parsing, NLP (spaCy), and scoring.

## 📦 API Endpoint
`POST /match_resume`

### Form Fields:
- `resume_file`: Upload a PDF
- `job_title`: Text
- `job_content`: Text

### Response:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "match_score": 92.3,
  "interview_scheduled": true
}
