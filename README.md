# Resume Scanner

A comprehensive AI-powered resume analysis system built with Python, NLP, and Machine Learning.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## 🚀 Features

| Feature                     | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| 📄 **Resume Parsing**       | Extract text from PDF and DOCX files with 95%+ accuracy      |
| 🧠 **NLP Skill Extraction** | Identify technical skills, soft skills, and domain expertise |
| 📊 **ATS Scoring**          | Calculate ATS compatibility score (0-100)                    |
| 🤖 **AI Detection**         | Detect AI-generated content in resumes                       |
| 💼 **Job Matching**         | Match resumes to suitable job roles using TF-IDF             |
| 📈 **Visualizations**       | Interactive charts and analytics dashboard                   |

## 📸 Screenshots

_Coming soon after deployment_

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **NLP:** spaCy, NLTK
- **ML:** scikit-learn (TF-IDF, Cosine Similarity)
- **PDF Parsing:** PyMuPDF, python-docx
- **Web UI:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **Data:** Pandas, NumPy

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Goddex-123/Resume-Scanner.git
cd Resume-Scanner

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py
```

## 🎯 Usage

1. **Launch the app** using `streamlit run app.py`
2. **Upload a resume** (PDF or DOCX format)
3. **View the analysis:**
   - Extracted skills categorized by type
   - ATS compatibility score
   - AI-generated content probability
   - Job role recommendations
4. **Download the report** for future reference

## 📊 How It Works

### Skill Extraction

Uses spaCy NER and custom pattern matching to identify:

- Programming languages (Python, Java, JavaScript, etc.)
- Frameworks (TensorFlow, React, Django, etc.)
- Tools (Git, Docker, AWS, etc.)
- Soft skills (Leadership, Communication, etc.)

### ATS Scoring Algorithm

Evaluates resumes based on:

- Keyword density and relevance
- Section structure (Experience, Education, Skills)
- Format compatibility
- Readability metrics

### AI Content Detection

Analyzes text patterns including:

- Vocabulary diversity (Type-Token Ratio)
- Sentence structure repetition
- Common AI writing patterns
- Perplexity estimation

### Job Matching

Uses TF-IDF vectorization and cosine similarity to:

- Compare resume content with job descriptions
- Rank suitable roles by match percentage
- Identify missing skills for target roles

## 📁 Project Structure

```
Resume-Scanner/
├── app.py                 # Main Streamlit application
├── resume_scanner/        # Core Python package
│   ├── __init__.py
│   ├── parser.py          # PDF/DOCX parsing
│   ├── nlp_engine.py      # NLP and skill extraction
│   ├── ats_scorer.py      # ATS scoring algorithm
│   ├── ai_detector.py     # AI content detection
│   └── job_matcher.py     # Job matching system
├── data/
│   ├── skills_database.json
│   └── job_keywords.json
├── samples/               # Sample resumes for testing
├── requirements.txt
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Soham** - Data Science Enthusiast

---

⭐ Star this repo if you found it useful!
