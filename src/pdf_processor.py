"""
PDF Processor Module
Handles PDF text extraction and basic processing
"""

import PyPDF2
import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """PDF document processor for text extraction and basic analysis"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, file_path: Path) -> str:
        """
        Extract text from PDF using multiple methods
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            return self._extract_with_pdfplumber(file_path)
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}")
            try:
                # Fallback to PyPDF2
                return self._extract_with_pypdf2(file_path)
            except Exception as e2:
                logger.error(f"PyPDF2 also failed: {e2}")
                raise Exception(f"Could not extract text from PDF: {e2}")
    
    def _extract_with_pdfplumber(self, file_path: Path) -> str:
        """Extract text using pdfplumber (better for tables/complex layouts)"""
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(f"--- Page {page_num} ---\\n{text}\\n")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {e}")
                    continue
        
        return "\\n".join(text_content)
    
    def _extract_with_pypdf2(self, file_path: Path) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        text_content = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text:
                        text_content.append(f"--- Page {page_num} ---\\n{text}\\n")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {e}")
                    continue
        
        return "\\n".join(text_content)
    
    def get_document_info(self, file_path: Path) -> Dict:
        """
        Get basic information about the PDF document
        
        Returns:
            Dictionary with document metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'file_size': file_path.stat().st_size,
                    'file_name': file_path.name
                }
                
                # Try to get metadata
                if pdf_reader.metadata:
                    info.update({
                        'title': pdf_reader.metadata.get('/Title', 'Unknown'),
                        'author': pdf_reader.metadata.get('/Author', 'Unknown'),
                        'subject': pdf_reader.metadata.get('/Subject', 'Unknown'),
                        'creator': pdf_reader.metadata.get('/Creator', 'Unknown'),
                        'producer': pdf_reader.metadata.get('/Producer', 'Unknown'),
                        'creation_date': pdf_reader.metadata.get('/CreationDate', 'Unknown')
                    })
                
                return info
                
        except Exception as e:
            logger.error(f"Error getting document info: {e}")
            return {
                'error': str(e),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size if file_path.exists() else 0
            }
    
    def extract_pages(self, file_path: Path, page_range: Optional[List[int]] = None) -> Dict[int, str]:
        """
        Extract text from specific pages
        
        Args:
            file_path: Path to PDF file
            page_range: List of page numbers to extract (1-indexed)
            
        Returns:
            Dictionary with page number as key and text as value
        """
        pages_content = {}
        
        try:
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                
                if page_range is None:
                    page_range = list(range(1, total_pages + 1))
                
                for page_num in page_range:
                    if 1 <= page_num <= total_pages:
                        try:
                            page = pdf.pages[page_num - 1]  # Convert to 0-indexed
                            text = page.extract_text()
                            pages_content[page_num] = text if text else ""
                        except Exception as e:
                            logger.warning(f"Error extracting page {page_num}: {e}")
                            pages_content[page_num] = f"Error extracting page: {e}"
                    else:
                        logger.warning(f"Page {page_num} out of range (1-{total_pages})")
                        
        except Exception as e:
            logger.error(f"Error extracting pages: {e}")
            raise
        
        return pages_content
    
    def search_in_document(self, file_path: Path, search_term: str) -> List[Dict]:
        """
        Search for a term in the document and return matches with context
        
        Args:
            file_path: Path to PDF file
            search_term: Term to search for
            
        Returns:
            List of dictionaries with match information
        """
        matches = []
        
        try:
            pages_content = self.extract_pages(file_path)
            
            for page_num, content in pages_content.items():
                if search_term.lower() in content.lower():
                    # Find all occurrences in the page
                    lines = content.split('\\n')
                    for line_num, line in enumerate(lines, 1):
                        if search_term.lower() in line.lower():
                            matches.append({
                                'page': page_num,
                                'line': line_num,
                                'text': line.strip(),
                                'context': self._get_context(lines, line_num - 1, 2)
                            })
            
        except Exception as e:
            logger.error(f"Error searching in document: {e}")
            
        return matches
    
    def _get_context(self, lines: List[str], target_line: int, context_size: int = 2) -> str:
        """Get surrounding context for a line"""
        start = max(0, target_line - context_size)
        end = min(len(lines), target_line + context_size + 1)
        
        context_lines = []
        for i in range(start, end):
            prefix = ">>> " if i == target_line else "    "
            context_lines.append(f"{prefix}{lines[i].strip()}")
        
        return "\\n".join(context_lines) 