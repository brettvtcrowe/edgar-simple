import pytest
from data_integration.sec_api_client import SECAPIClient, FilingContent

class TestSECAPIClient:
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.client = SECAPIClient()
    
    def test_company_filing_retrieval_apple(self):
        """Test retrieving Apple's filings from SEC API"""
        # Apple's CIK: 320193
        # Test without form type filter first
        filings = self.client.get_company_filings("320193")
        
        assert len(filings) > 0
        assert all(f.cik == "320193" for f in filings)
        
        # Test with specific form type
        eight_k_filings = self.client.get_company_filings("320193", form_type="8-K")
        # Should have some 8-K filings based on the debug output
        if eight_k_filings:
            assert all(f.form_type == "8-K" for f in eight_k_filings)
    
    def test_company_filing_retrieval_microsoft(self):
        """Test retrieving Microsoft's filings from SEC API"""
        # Microsoft's CIK: 789019
        filings = self.client.get_company_filings("789019", form_type="10-K")
        
        assert len(filings) > 0
        assert all(f.cik == "789019" for f in filings)
        assert all(f.form_type == "10-K" for f in filings)
    
    def test_filing_content_extraction(self):
        """Test that filing content is properly extracted"""
        filings = self.client.get_company_filings("320193", form_type="10-K")
        
        if filings:
            filing = filings[0]
            assert filing.content is not None
            assert len(filing.content) > 100  # Should have substantial content
            assert filing.url is not None
            assert filing.company_name is not None
    
    def test_date_filtering(self):
        """Test that date filtering works correctly"""
        # Get filings from 2024
        filings = self.client.get_company_filings(
            "320193", 
            form_type="8-K",
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        if filings:
            for filing in filings:
                assert filing.filing_date >= "2024-01-01"
                assert filing.filing_date <= "2024-12-31"
    
    def test_form_type_filtering(self):
        """Test that form type filtering works correctly"""
        # Get only 8-K filings
        filings = self.client.get_company_filings("320193", form_type="8-K")
        
        assert all(f.form_type == "8-K" for f in filings)
    
    def test_rate_limiting_respect(self):
        """Test that rate limiting is respected"""
        import time
        start_time = time.time()
        
        # Make multiple requests
        for _ in range(3):
            self.client.get_company_filings("320193", form_type="8-K")
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should take at least 0.2 seconds (2 * 0.1s rate limit delay)
        assert elapsed >= 0.2
