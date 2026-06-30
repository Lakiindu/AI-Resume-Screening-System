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

SECTION_HEADINGS = {
    "education": [
        "education", "academic background", "academic qualification",
        "qualifications", "educational background"
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment history", "career history", "leadership & experience",
        "leadership and experience"
    ],
    "projects": [
        "projects", "academic projects", "personal projects",
        "project experience"
    ],
    "certificates": [
        "certificates", "certifications", "licenses", "courses",
        "achievements", "awards"
    ],
    "languages": [
        "languages", "language skills"
    ],
    "skills": [
        "skills", "technical skills", "key skills", "core skills"
    ]
}


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


def normalize_heading(line):
    return (
        line.lower()
        .replace(":", "")
        .replace("&", "and")
        .strip()
    )


def get_heading_map():
    heading_map = {}

    for section, headings in SECTION_HEADINGS.items():
        for heading in headings:
            heading_map[heading.lower().replace("&", "and")] = section

    return heading_map


def detect_section(line):
    normalized_line = normalize_heading(line)
    heading_map = get_heading_map()

    if normalized_line in heading_map:
        return heading_map[normalized_line]

    return None


def extract_sections(text):
    """
    Extracts resume content based on section headings.
    """
    lines = clean_lines(text)

    sections = {
        "education": [],
        "experience": [],
        "projects": [],
        "certificates": [],
        "languages": [],
        "skills": []
    }

    current_section = None

    for line in lines:
        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section
            continue

        if current_section:
            sections[current_section].append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
    }


def extract_email(text):
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text):
    pattern = r"(\+?\d[\d\s\-]{8,}\d)"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_skills(text, skill_section=""):
    combined_text = f"{text} {skill_section}".lower()
    found = []

    for skill in SKILL_KEYWORDS:
        if skill in combined_text:
            found.append(skill)

    return ", ".join(sorted(set(found)))


def fallback_education(text):
    lines = clean_lines(text)
    keywords = [
        "bsc", "bachelor", "degree", "diploma", "higher diploma",
        "university", "institute", "college", "gce", "a/l", "o/l",
        "information technology", "computer science"
    ]

    found = [
        line for line in lines
        if any(keyword in line.lower() for keyword in keywords)
    ]

    return "\n".join(found[:8])


def fallback_experience(text):
    lines = clean_lines(text)
    keywords = [
        "intern", "internship", "trainee", "developer",
        "engineer", "worked", "company", "years", "months"
    ]

    found = [
        line for line in lines
        if any(keyword in line.lower() for keyword in keywords)
    ]

    return "\n".join(found[:8])


def fallback_projects(text):
    lines = clean_lines(text)
    keywords = [
        "project", "system", "application", "website", "web app",
        "management system", "developed", "built"
    ]

    found = [
        line for line in lines
        if any(keyword in line.lower() for keyword in keywords)
    ]

    return "\n".join(found[:10])


def extract_languages(text, language_section=""):
    combined_text = f"{text} {language_section}".lower()
    found = []

    for language in LANGUAGE_KEYWORDS:
        if language in combined_text:
            found.append(language.capitalize())

    return ", ".join(sorted(set(found)))


def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    sections = extract_sections(text)

    education = sections["education"] or fallback_education(text)
    experience = sections["experience"] or fallback_experience(text)
    projects = sections["projects"] or fallback_projects(text)
    certificates = sections["certificates"]
    languages = extract_languages(text, sections["languages"])
    skills = extract_skills(text, sections["skills"])

    return {
        "extracted_text": text,
        "extracted_email": extract_email(text),
        "extracted_phone": extract_phone(text),
        "extracted_skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certificates": certificates,
        "languages": languages
    }