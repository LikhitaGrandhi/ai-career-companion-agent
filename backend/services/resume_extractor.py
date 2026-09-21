import re


def extract_email(text: str):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )
    return match.group(0) if match else None


def extract_name(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return None

    # Usually the candidate's name appears near the beginning.
    for line in lines[:8]:
        if (
            len(line.split()) <= 5
            and not any(char.isdigit() for char in line)
            and "@" not in line
            and not any(
                word in line.lower()
                for word in [
                    "resume",
                    "curriculum vitae",
                    "linkedin",
                    "github",
                    "phone",
                    "email"
                ]
            )
        ):
            return line

    return lines[0]


def extract_skills(text: str):
    common_skills = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Express",
        "MongoDB",
        "MySQL",
        "SQL",
        "Git",
        "GitHub",
        "FastAPI",
        "Flask",
        "Django",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Artificial Intelligence",
        "Power BI",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "PyTorch",
        "AWS"
    ]

    found_skills = []

    text_lower = text.lower()

    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_section(text: str, section_names):
    lines = text.splitlines()

    collected = []
    collecting = False

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if any(
            section.lower() in lower_line
            for section in section_names
        ):
            collecting = True
            continue

        if collecting:
            # Stop when another common resume section starts
            if any(
                section in lower_line
                for section in [
                    "education",
                    "experience",
                    "projects",
                    "skills",
                    "certifications",
                    "achievements",
                    "internships",
                    "contact"
                ]
            ):
                break

            collected.append(clean_line)

    return collected


def extract_resume_data(text: str):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_section(
            text,
            ["education", "academic background"]
        ),
        "experience": extract_section(
            text,
            ["experience", "work experience", "internship"]
        ),
        "projects": extract_section(
            text,
            ["projects", "academic projects"]
        ),
        "certifications": extract_section(
            text,
            ["certifications", "certificates"]
        )
    }