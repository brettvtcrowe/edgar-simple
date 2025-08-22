import spacy
from typing import Dict, List
from dataclasses import dataclass
import re

@dataclass
class FilingAnalysis:
    """Structured analysis of SEC filing content"""
    sections: Dict[str, str]
    accounting_concepts: List[Dict[str, str]]
    policies: List[Dict[str, str]]
    risk_factors: List[Dict[str, str]]
    summary: str

class DocumentParser:
    """Parse SEC filing HTML content and extract key information"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if spaCy model not available
            self.nlp = None
    
    def parse_filing_content(self, html_content: str) -> FilingAnalysis:
        """Parse SEC filing HTML content and extract key information"""
        # Extract text content from HTML
        text_content = self._extract_text_content(html_content)
        
        # Extract sections based on headers
        sections = self._extract_sections(html_content)
        
        # Create summary from text content
        summary = text_content[:1000] if len(text_content) > 1000 else text_content
        
        return FilingAnalysis(
            sections=sections,
            accounting_concepts=[],
            policies=[],
            risk_factors=[],
            summary=summary
        )
    
    def _extract_text_content(self, html_content: str) -> str:
        """Extract text content from HTML filing"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_sections(self, html_content: str) -> Dict[str, str]:
        """Extract sections based on HTML headers"""
        sections = {}
        
        # Find all header tags and their content
        header_pattern = r'<h([1-6])[^>]*>(.*?)</h\1>'
        headers = re.findall(header_pattern, html_content, re.IGNORECASE | re.DOTALL)
        
        # Sort headers by position in document
        header_positions = []
        for level, header_text in headers:
            pos = html_content.find(f'<h{level}')
            if pos != -1:
                header_positions.append((pos, level, header_text))
        
        header_positions.sort(key=lambda x: x[0])
        
        for i, (start_pos, level, header_text) in enumerate(header_positions):
            # Clean header text
            clean_header = re.sub(r'<[^>]+>', '', header_text).strip()
            
            # Find end position (next header or end of document)
            if i + 1 < len(header_positions):
                end_pos = header_positions[i + 1][0]
            else:
                end_pos = len(html_content)
            
            # Extract section content (from after the header to the next header)
            # Find the end of the current header tag
            header_end = html_content.find('</h', start_pos)
            if header_end != -1:
                # Find the closing tag
                tag_end = html_content.find('>', header_end)
                if tag_end != -1:
                    content_start = tag_end + 1
                else:
                    content_start = start_pos
            else:
                content_start = start_pos
            
            # Extract content between this header and the next
            section_content = html_content[content_start:end_pos]
            
            # Clean section content and extract text
            section_text = self._extract_text_content(section_content)
            sections[clean_header] = section_text
        
        return sections
