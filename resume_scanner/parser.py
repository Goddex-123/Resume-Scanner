"""
Resume Parser Module
Handles PDF and DOCX file parsing and text extraction.
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
import io


class ResumeParser:
    """
    Parses resume files (PDF, DOCX) and extracts text content.
    """
    
    SUPPORTED_FORMATS = ['.pdf', '.docx', '.doc', '.txt']
    
    def __init__(self):
        self.text = ""
        self.metadata = {}
    
    def parse(self, file_path: Optional[str] = None, file_content: Optional[bytes] = None, 
              file_type: Optional[str] = None) -> str:
        """
        Parse a resume file and extract text.
        
        Args:
            file_path: Path to the resume file
            file_content: Raw file bytes (for uploaded files)
            file_type: File extension (required if using file_content)
            
        Returns:
            Extracted text from the resume
        """
        if file_content and file_type:
            return self._parse_from_bytes(file_content, file_type)
        elif file_path:
            return self._parse_from_path(file_path)
        else:
            raise ValueError("Either file_path or (file_content and file_type) must be provided")
    
    def _parse_from_path(self, file_path: str) -> str:
        """Parse resume from file path."""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        with open(path, 'rb') as f:
            content = f.read()
        
        return self._parse_from_bytes(content, suffix)
    
    def _parse_from_bytes(self, content: bytes, file_type: str) -> str:
        """Parse resume from raw bytes."""
        file_type = file_type.lower()
        if not file_type.startswith('.'):
            file_type = '.' + file_type
            
        if file_type == '.pdf':
            self.text = self._parse_pdf(content)
        elif file_type in ['.docx', '.doc']:
            self.text = self._parse_docx(content)
        elif file_type == '.txt':
            self.text = content.decode('utf-8', errors='ignore')
        else:
            raise ValueError(f"Unsupported file format: {file_type}")
        
        self.text = self._clean_text(self.text)
        return self.text
    
    def _parse_pdf(self, content: bytes) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            
            text_parts = []
            pdf_document = fitz.open(stream=content, filetype="pdf")
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text_parts.append(page.get_text())
            
            pdf_document.close()
            return "\n".join(text_parts)
            
        except ImportError:
            raise ImportError("PyMuPDF (fitz) is required for PDF parsing. Install with: pip install PyMuPDF")
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, content: bytes) -> str:
        """Extract text from DOCX using python-docx."""
        try:
            from docx import Document
            
            doc = Document(io.BytesIO(content))
            text_parts = []
            
            for paragraph in doc.paragraphs:
                text_parts.append(paragraph.text)
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text_parts.append(cell.text)
            
            return "\n".join(text_parts)
            
        except ImportError:
            raise ImportError("python-docx is required for DOCX parsing. Install with: pip install python-docx")
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\+\@\#\(\)\/\&]', '', text)
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def get_sections(self) -> Dict[str, str]:
        """
        Identify and extract common resume sections.
        
        Returns:
            Dictionary mapping section names to their content
        """
        sections = {}
        
        section_patterns = {
            'education': r'(?i)(education|academic|qualification|degree)',
            'experience': r'(?i)(experience|employment|work\s*history|career)',
            'skills': r'(?i)(skills|technical\s*skills|expertise|competencies)',
            'projects': r'(?i)(projects|portfolio|work\s*samples)',
            'certifications': r'(?i)(certification|certificate|license)',
            'summary': r'(?i)(summary|objective|profile|about)',
            'contact': r'(?i)(contact|email|phone|address)'
        }
        
        text_lower = self.text.lower()
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                sections[section_name] = True
            else:
                sections[section_name] = False
        
        return sections
    
    def extract_contact_info(self) -> Dict[str, Optional[str]]:
        """
        Extract contact information from resume.
        
        Returns:
            Dictionary with email, phone, and LinkedIn URL
        """
        contact = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None
        }
        
        # Email pattern
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone pattern (various formats)
        phone_match = re.search(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4,6}', self.text)
        if phone_match:
            contact['phone'] = phone_match.group()
        
        # LinkedIn URL
        linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', self.text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        # GitHub URL
        github_match = re.search(r'github\.com/[\w\-]+', self.text, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group()
        
        return contact
