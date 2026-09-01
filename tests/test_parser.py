"""
Unit tests for ResumeParser and ResumeDocument.
"""

import pytest
from resume_scanner.parser import ResumeParser, ResumeDocument


def test_txt_parsing_utf8():
    parser = ResumeParser()
    sample = (
        "Alex Rivera\n"
        "Email: alex.rivera@example.com | Phone: +1-555-234-5678\n"
        "EXPERIENCE\n"
        "Senior Security Analyst - 2021 to 2024\n"
        "- Configured Splunk SIEM alerts reducing MTTR by 35%.\n"
        "EDUCATION\n"
        "B.S. in Computer Science, 2020\n"
        "SKILLS\n"
        "Python, Wireshark, Metasploit\n"
    )
    doc = parser.parse_document(file_content=sample.encode("utf-8"), file_type="txt")
    assert isinstance(doc, ResumeDocument)
    assert "Alex Rivera" in doc.raw_text
    assert doc.page_count == 1
    assert not doc.is_scanned


def test_legacy_doc_rejection():
    parser = ResumeParser()
    binary_doc_content = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 100
    with pytest.raises(ValueError) as excinfo:
        parser.parse_document(file_content=binary_doc_content, file_type="doc")
    assert "Legacy binary .doc" in str(excinfo.value)
    assert ".docx" in str(excinfo.value)


def test_contact_info_extraction_robustness():
    parser = ResumeParser()
    parser.text = (
        "John Doe\n"
        "Email: john.doe@cybersec.org\n"
        "Mobile: (555) 432-8765\n"
        "LinkedIn: https://www.linkedin.com/in/johndoe-cyber\n"
        "GitHub: https://github.com/johndoe-dev\n"
        "Years of experience: 2018-2022\n"
    )
    info = parser.extract_contact_info()
    assert info["email"] == "john.doe@cybersec.org"
    assert info["phone"] == "(555) 432-8765"
    assert "linkedin.com/in/johndoe-cyber" in info["linkedin"]
    assert "github.com/johndoe-dev" in info["github"]
    # Verify that the date range 2018-2022 was NOT parsed as a phone number
    assert info["phone"] != "2018-2022"


def test_section_content_extraction():
    parser = ResumeParser()
    parser.text = (
        "Jane Smith\n"
        "SUMMARY\n"
        "Experienced frontend engineer specializing in React and TypeScript.\n"
        "WORK EXPERIENCE\n"
        "- Senior Frontend Engineer at TechCorp (2021 - Present)\n"
        "- Web Developer at WebStudio (2018 - 2021)\n"
        "EDUCATION\n"
        "B.S. in Software Engineering, 2018\n"
        "TECHNICAL SKILLS\n"
        "React, Next.js, TypeScript, Tailwind CSS\n"
    )
    sections = parser.get_sections()
    assert sections.get("summary") is True
    assert sections.get("experience") is True
    assert sections.get("education") is True
    assert sections.get("skills") is True

    exp_content = parser.get_section_content("experience")
    assert "Senior Frontend Engineer at TechCorp" in exp_content
