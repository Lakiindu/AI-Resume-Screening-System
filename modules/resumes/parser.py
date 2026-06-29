import re
import pdfplumber


SKILL_KEYWORDS = [
    "python", "flask", "django", "mysql", "postgresql", "html", "css",
    "javascript", "bootstrap", "react", "node.js", "machine learning",
    "data analysis", "sql", "git", "github", "api", "nlp", "scikit-learn",
    "java", "php", "laravel", "c++", "figma", "power bi", "excel"
]


SECTION_KEYWORDS = {
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "work experience", "employment history", "internship"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certificates": ["certificates", "certifications", "courses"],
    "languages": ["languages", "language skills"]
}


def extract_text_from_pdf(file_path):
    """
    Reads all text from a PDF resume using pdfplumber.
    """
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_email(text):
    """
    Extracts email address using regex.
    """
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(email_pattern, text)

    return match.group(0) if match else ""


def extract_phone(text):
    """
    Extracts phone number using regex.
    """
    phone_pattern = r"(\+?\d[\d\s\-]{8,}\d)"
    match = re.search(phone_pattern, text)

    return match.group(0) if match else ""


def extract_skills(text):
    """
    Finds matching skills from predefined skill keywords.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return ", ".join(sorted(set(found_skills)))


def clean_lines(text):
    """
    Splits resume text into clean lines.
    """
    lines = text.split("\n")
    return [line.strip() for line in lines if line.strip()]


def find_section_content(text, section_name):
    """
    Extracts content under a section heading.
    Example:
    Education
    BSc in IT
    University name

    Stops when another known section starts.
    """
    lines = clean_lines(text)
    section_aliases = SECTION_KEYWORDS[section_name]

    all_headings = []
    for aliases in SECTION_KEYWORDS.values():
        all_headings.extend(aliases)

    collecting = False
    collected_lines = []

    for line in lines:
        line_lower = line.lower().strip().replace(":", "")

        if line_lower in section_aliases:
            collecting = True
            continue

        if collecting and line_lower in all_headings:
            break

        if collecting:
            collected_lines.append(line)

    return "\n".join(collected_lines[:10])


def parse_resume(file_path):
    """
    Main parser function.
    """
    text = extract_text_from_pdf(file_path)

    parsed_data = {
        "extracted_text": text,
        "extracted_email": extract_email(text),
        "extracted_phone": extract_phone(text),
        "extracted_skills": extract_skills(text),
        "education": find_section_content(text, "education"),
        "experience": find_section_content(text, "experience"),
        "projects": find_section_content(text, "projects"),
        "certificates": find_section_content(text, "certificates"),
        "languages": find_section_content(text, "languages")
    }

    return parsed_data