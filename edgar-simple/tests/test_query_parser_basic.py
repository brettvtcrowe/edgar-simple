import pytest
from nlp_engine.query_parser import QueryParser

class TestQueryParserBasic:
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.parser = QueryParser()
    
    def test_filing_type_extraction_8k(self):
        """Test that 8-K filing type is correctly extracted"""
        query = "Find 8-K filings about restatements"
        result = self.parser.parse_query(query)
        
        assert result.filing_type == "8-K"
        assert result.intent == "SEARCH_FILINGS"
    
    def test_filing_type_extraction_10k(self):
        """Test that 10-K filing type is correctly extracted"""
        query = "Show me 10-K filings from Microsoft"
        result = self.parser.parse_query(query)
        
        assert result.filing_type == "10-K"
        assert result.intent == "SEARCH_FILINGS"
    
    def test_no_filing_type_specified(self):
        """Test handling when no filing type is specified"""
        query = "Find filings about revenue recognition"
        result = self.parser.parse_query(query)
        
        assert result.filing_type is None
        assert result.intent == "SEARCH_FILINGS"
    
    def test_intent_classification_search(self):
        """Test that search intent is correctly classified"""
        query = "Find 8-K filings about restatements"
        result = self.parser.parse_query(query)
        
        assert result.intent == "SEARCH_FILINGS"
    
    def test_intent_classification_compare(self):
        """Test that comparison intent is correctly classified"""
        query = "Compare Microsoft revenue recognition policy"
        result = self.parser.parse_query(query)
        
        assert result.intent == "COMPARE_POLICIES"
