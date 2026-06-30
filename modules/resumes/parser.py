import re
import pdfplumber


SKILL_KEYWORDS = [
    "python", "flask", "django", "mysql", "postgresql", "html", "css",
    "javascript", "bootstrap", "react", "node.js", "machine learning",
    "deep learning", "tensorflow", "pandas", "numpy", "scikit-learn",
    "data analysis", "sql", "git", "github", "api", "rest api", "nlp",
    "java", "php", "laravel", "c++", "figma", "power bi", "excel"
]

LANGUAGE_KEYWORDS = [
    "english", "sinhala", "tamil", "japanese", "hindi", "french"
]

CERTIFICATE_KEYWORDS = [
    "certificate", "certification", "certified", "coursera", "udemy",
    "google", "microsoft", "aws", "cisco", "oracle", "linkedin learning"
]


def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def clean_lines(text):
    return [line.strip() for line in text.split("\n") if line.strip()]


def extract_email(text):
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text):
    pattern = r"(\+?\d[\d\s\-]{8,}\d)"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_skills(text):
    text_lower = text.lower()
    found = []

    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.append(skill)

    return ", ".join(sorted(set(found)))


def extract_education(text):
    lines = clean_lines(text)
    education_lines = []

    keywords = [
        "bsc", "bachelor", "degree", "diploma", "higher diploma",
        "university", "institute", "college", "gce", "a/l", "o/l",
        "information technology", "computer science"
    ]

    for line in lines:
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in keywords):
            education_lines.append(line)

    return "\n".join(education_lines[:8])


def extract_experience(text):
    lines = clean_lines(text)
    experience_lines = []

    keywords = [
        "experience", "intern", "internship", "trainee", "developer",
        "engineer", "worked", "company", "years", "months"
    ]

    for line in lines:
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in keywords):
            experience_lines.append(line)

    return "\n".join(experience_lines[:8])


def extract_projects(text):
    lines = clean_lines(text)
    project_lines = []

    keywords = [
        "project", "system", "application", "website", "web app",
        "management system", "portfolio", "developed", "built"
    ]

    for line in lines:
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in keywords):
            project_lines.append(line)

    return "\n".join(project_lines[:10])


def extract_certificates(text):
    lines = clean_lines(text)
    certificate_lines = []

    for line in lines:
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in CERTIFICATE_KEYWORDS):
            certificate_lines.append(line)

    return "\n".join(certificate_lines[:8])


def extract_languages(text):
    text_lower = text.lower()
    found = []

    for language in LANGUAGE_KEYWORDS:
        if language in text_lower:
            found.append(language.capitalize())

    return ", ".join(sorted(set(found)))


def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    return {
        "extracted_text": text,
        "extracted_email": extract_email(text),
        "extracted_phone": extract_phone(text),
        "extracted_skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certificates": extract_certificates(text),
        "languages": extract_languages(text)
    }