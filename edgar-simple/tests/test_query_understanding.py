import pytest

from query_understanding.query_processor import QueryProcessor
from query_understanding.query_result import QueryResult
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class QueryResult:
    """Structured result of a natural language query"""
    query: str
    parsed_query: Dict[str, any]
    filings: List[Dict[str, any]]
    analysis: Dict[str, any]
    summary: str
    confidence: float

class TestQueryProcessor:
    """Test the end-to-end query processing pipeline"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = QueryProcessor()
    
    def test_basic_8k_restatement_query(self):
        """Test basic 8-K restatement query processing"""
        query = "Find all 8-K filings from Apple about restatements"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.query == query
        assert result.parsed_query["filing_type"] == "8-K"
        assert result.parsed_query["company"] == "Apple"
        assert "restatement" in result.parsed_query["keywords"]
        assert len(result.filings) > 0
        assert result.confidence > 0.7

class TestQueryIntegration:
    """Test integration between all Phase 3 components"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = QueryProcessor()
    
    def test_nlp_parser_integration(self):
        """Test that NLP parser is properly integrated"""
        query = "Find 8-K filings about restatements"
        
        result = self.processor.process_query(query)
        
        # Verify NLP parsing worked
        assert result.parsed_query["filing_type"] == "8-K"
        assert "restatement" in result.parsed_query["keywords"]

    def test_asc_606_policy_query(self):
        """Test ASC 606 policy extraction query"""
        query = "What revenue recognition policies does Microsoft disclose in their 10-K filings?"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.parsed_query["filing_type"] == "10-K"
        assert result.parsed_query["company"] == "Microsoft"
        assert "ASC 606" in result.parsed_query["accounting_concepts"]
        assert len(result.analysis["policies"]) > 0
        assert result.confidence > 0.8
    
    def test_risk_factor_analysis_query(self):
        """Test risk factor analysis query"""
        query = "Analyze risk factors in Tesla's recent 8-K filings"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.parsed_query["company"] == "Tesla"
        assert result.parsed_query["filing_type"] == "8-K"
        assert len(result.analysis["risk_factors"]) > 0
        assert result.confidence > 0.7
    
    def test_comparative_analysis_query(self):
        """Test comparative analysis between companies"""
        query = "Compare revenue recognition policies between Apple and Microsoft in their latest 10-K filings"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.parsed_query["intent"] == "COMPARE_POLICIES"
        assert len(result.parsed_query["companies"]) == 2
        assert "Apple" in result.parsed_query["companies"]
        assert "Microsoft" in result.parsed_query["companies"]
        assert result.parsed_query["filing_type"] == "10-K"
        assert len(result.analysis["risk_factors"]) > 0
        assert result.confidence > 0.8
    
    def test_timeframe_filtered_query(self):
        """Test query with timeframe filtering"""
        query = "Find all 8-K filings from the past 3 years that mention lease accounting changes"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.parsed_query["filing_type"] == "8-K"
        assert result.parsed_query["timeframe"] == "3years"
        assert "lease accounting" in result.parsed_query["keywords"]
        assert len(result.filings) > 0
        assert result.confidence > 0.7
    
    def test_complex_multi_criteria_query(self):
        """Test complex query with multiple criteria"""
        query = "Find 10-K filings from technology companies in the past 2 years that discuss ASC 842 lease accounting and have high-risk factors"
        
        result = self.processor.process_query(query)
        
        assert result is not None
        assert result.parsed_query["filing_type"] == "10-K"
        assert result.parsed_query["sector"] == "Technology"
        assert result.parsed_query["timeframe"] == "2years"
        assert "ASC 842" in result.parsed_query["accounting_concepts"]
        assert result.parsed_query["risk_level"] == "high"
        assert len(result.filings) > 0
        assert result.confidence > 0.6

class TestQueryIntegration:
    """Test integration between all Phase 3 components"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.processor = QueryProcessor()
    
    def test_nlp_parser_integration(self):
        """Test that NLP parser is properly integrated"""
        query = "Find 8-K filings about restatements"
        
        result = self.processor.process_query(query)
        
        # Verify NLP parsing worked
        assert result.parsed_query["filing_type"] == "8-K"
        assert "restatement" in result.parsed_query["keywords"]
    
    def test_sec_api_integration(self):
        """Test that SEC API client is properly integrated"""
        query = "Find recent 10-K filings from Apple"
        
        result = self.processor.process_query(query)
        
        # Verify SEC API integration worked
        assert len(result.filings) > 0
        assert all(f["company"] == "Apple" for f in result.filings)
        assert all(f["form_type"] == "10-K" for f in result.filings)
    
    def test_content_analysis_integration(self):
        """Test that content analysis is properly integrated"""
        query = "What accounting standards does Apple discuss in their 10-K filings?"
        
        result = self.processor.process_query(query)
        
        # Verify content analysis worked
        assert len(result.analysis["accounting_concepts"]) > 0
        assert len(result.analysis["policies"]) > 0
    
    def test_end_to_end_pipeline(self):
        """Test complete end-to-end query processing"""
        query = "Find 8-K filings from Apple in the past year that discuss revenue recognition changes"
        
        result = self.processor.process_query(query)
        
        # Verify complete pipeline worked
        assert result is not None
        assert result.parsed_query["company"] == "Apple"
        assert result.parsed_query["filing_type"] == "8-K"
        assert result.parsed_query["timeframe"] == "1year"
        assert "revenue recognition" in result.parsed_query["keywords"]
        assert len(result.filings) > 0
        assert len(result.analysis["accounting_concepts"]) > 0
        assert result.confidence > 0.7
