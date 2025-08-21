import spacy
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ParsedQuery:
    """Data class to hold parsed query results"""
    intent: str
    filing_type: Optional[str]
    timeframe: Optional[str]
    company: Optional[str]
    accounting_concepts: List[str]

class QueryParser:
    """Parse natural language queries into structured format"""
    
    def __init__(self):
        """Initialize the parser with spaCy model"""
        self.nlp = spacy.load("en_core_web_sm")
        self.filing_types = ["8-k", "10-k", "10-q", "s-1", "s-3", "424b3"]
    
    def parse_query(self, query: str) -> ParsedQuery:
        """Parse natural language query into structured format"""
        doc = self.nlp(query.lower())
        
        # Extract filing type
        filing_type = self._extract_filing_type(doc)
        
        # Extract timeframe
        timeframe = self._extract_timeframe(doc)
        
        # Extract company
        company = self._extract_company(doc)
        
        # Classify intent
        intent = self._classify_intent(doc)
        
        # Return parsed query (other fields will be implemented next)
        return ParsedQuery(
            intent=intent,
            filing_type=filing_type,
            timeframe=timeframe,
            company=company,
            accounting_concepts=[]  # Will implement next
        )
    
    def _extract_filing_type(self, doc) -> Optional[str]:
        """Extract SEC filing type from query"""
        # Get the full text and check for filing type patterns
        query_text = doc.text.lower()
        
        # Check for filing types in the text
        for filing_type in self.filing_types:
            if filing_type in query_text:
                return filing_type.upper()
        
        return None
    
    def _extract_timeframe(self, doc) -> Optional[str]:
        """Extract timeframe from query"""
        query_text = doc.text.lower()
        
        # Define time patterns
        time_patterns = {
            "past three years": "3years",
            "past year": "1year", 
            "last five": "5filings",
            "within 12 months": "12months"
        }
        
        # Check for time patterns in the text
        for pattern, value in time_patterns.items():
            if pattern in query_text:
                return value
        
        return None
    
    def _extract_company(self, doc) -> Optional[str]:
        """Extract company name from query"""
        query_text = doc.text.lower()
        
        # Define company name patterns
        company_patterns = {
            "apple": "apple",
            "microsoft": "microsoft",
            "tesla": "tesla",
            "amazon": "amazon",
            "google": "google"
        }
        
        # Check for company name patterns in the text
        for pattern, value in company_patterns.items():
            if pattern in query_text:
                return value.title()
        
        return None
    
    def _classify_intent(self, doc) -> str:
        """Classify query intent - start with simple rule"""
        query_text = doc.text
        
        if "compare" in query_text:
            return "COMPARE_POLICIES"
        else:
            return "SEARCH_FILINGS"
