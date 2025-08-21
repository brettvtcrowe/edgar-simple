import pytest
from nlp_engine.query_parser import QueryParser

class TestQueryParserExtended:
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.parser = QueryParser()
    
    def test_timeframe_extraction_past_three_years(self):
        """Test extraction of 'past three years' timeframe"""
        query = "Find 8-K filings from the past three years"
        result = self.parser.parse_query(query)
        
        assert result.timeframe == "3years"
        assert result.filing_type == "8-K"
    
    def test_timeframe_extraction_last_five(self):
        """Test extraction of 'last five' timeframe"""
        query = "Show me the last five 10-K filings from Apple"
        result = self.parser.parse_query(query)
        
        assert result.timeframe == "5filings"
        assert result.filing_type == "10-K"
    
    def test_timeframe_extraction_within_12_months(self):
        """Test extraction of 'within 12 months' timeframe"""
        query = "Find filings within 12 months of acquisition"
        result = self.parser.parse_query(query)
        
        assert result.timeframe == "12months"
    
    def test_company_extraction_microsoft(self):
        """Test extraction of company name 'Microsoft'"""
        query = "Show me Microsoft's 10-K filings"
        result = self.parser.parse_query(query)
        
        assert result.company == "Microsoft"
        assert result.filing_type == "10-K"
    
    def test_company_extraction_apple(self):
        """Test extraction of company name 'Apple'"""
        query = "Find Apple's 8-K filings about restatements"
        result = self.parser.parse_query(query)
        
        assert result.company == "Apple"
        assert result.filing_type == "8-K"
    
    def test_no_timeframe_specified(self):
        """Test handling when no timeframe is specified"""
        query = "Find 8-K filings about restatements"
        result = self.parser.parse_query(query)
        
        assert result.timeframe is None
    
    def test_no_company_specified(self):
        """Test handling when no company is specified"""
        query = "Find 10-K filings about revenue recognition"
        result = self.parser.parse_query(query)
        
        assert result.company is None
