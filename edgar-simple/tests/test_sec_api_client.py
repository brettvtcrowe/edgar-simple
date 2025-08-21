import pytest
from data_integration.sec_api_client import SECAPIClient, FilingContent

class TestSECAPIClient:
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.client = SECAPIClient()
    
    def test_company_filing_retrieval_apple(self):
        """Test retrieving Apple filings from SEC API"""
        filings = self.client.get_company_filings("320193", form_type="8-K")
        
        assert len(filings) > 0
        assert all(f.cik == "320193" for f in filings)
        assert all(f.form_type == "8-K" for f in filings)
    
    def test_filing_content_extraction(self):
        """Test that filing content is properly extracted"""
        filings = self.client.get_company_filings("320193", form_type="10-K")
        
        if filings:
            filing = filings[0]
            assert filing.content is not None
            assert len(filing.content) > 100
            assert filing.url is not None
            assert filing.company_name is not None
