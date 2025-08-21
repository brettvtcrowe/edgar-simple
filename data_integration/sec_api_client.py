import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class FilingContent:
    cik: str
    company_name: str
    form_type: str
    filing_date: str
    content: str
    url: str
    exhibits: List[str]

class SECAPIClient:
    
    def __init__(self):
        self.base_url = "https://data.sec.gov"
        self.headers = {"User-Agent": "Regulatory Intelligence Hub - Phase 3 Development"}
        self.rate_limit_delay = 0.1
    
    def get_company_filings(self, cik: str, form_type: Optional[str] = None) -> List[FilingContent]:
        time.sleep(self.rate_limit_delay)
        try:
            submissions_url = f"{self.base_url}/submissions/CIK{cik.zfill(10)}.json"
            print(f"Making request to: {submissions_url}")
            
            response = requests.get(submissions_url, headers=self.headers)
            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API request failed with status {response.status_code}")
                return []
            
            # Try to parse as JSON
            try:
                data = response.json()
                print(f"Successfully parsed JSON")
            except Exception as json_error:
                print(f"Failed to parse JSON: {json_error}")
                return []
            
            filings = []
            recent_filings = data.get("filings", {}).get("recent", {})
            print(f"Found recent filings with keys: {list(recent_filings.keys())[:5]}")
            
            # The SEC API returns parallel arrays - get length from first field
            if recent_filings:
                # Get first field to determine number of filings
                first_field = list(recent_filings.keys())[0]
                num_filings = len(recent_filings[first_field])
                print(f"Number of filings: {num_filings}")
                
                # Limit to 10 for testing
                max_filings = min(num_filings, 10)
                
                for i in range(max_filings):
                    filing_data = {}
                    # Build filing object by getting the i-th element from each field array
                    for field_name in recent_filings.keys():
                        if i < len(recent_filings[field_name]):
                            filing_data[field_name] = recent_filings[field_name][i]
                    
                    print(f"Reconstructed filing {i}: form={filing_data.get('form')}, date={filing_data.get('filingDate')}")
                    
                    # Apply form type filter
                    if form_type and filing_data.get("form") != form_type:
                        continue
                    
                    # Create filing content object
                    filing_content = FilingContent(
                        cik=cik,
                        company_name=data.get("name", ""),
                        form_type=filing_data.get("form", ""),
                        filing_date=filing_data.get("filingDate", ""),
                        content="",  # Simplified for now
                        url=f"{self.base_url}/Archives/edgar/data/{cik}/{filing_data.get('accessionNumber', '').replace('-', '')}/{filing_data.get('primaryDocument', '')}",
                        exhibits=[]
                    )
                    
                    filings.append(filing_content)
                    print(f"Added filing: {filing_content.form_type} on {filing_content.filing_date}")
            
            return filings
            
        except Exception as e:
            print(f"Error in get_company_filings: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_filing_content(self, cik: str, filing: Dict) -> Optional[FilingContent]:
        # Simplified implementation for now
        return None
    
    def _extract_text_content(self, html_content: str) -> str:
        import re
        text = re.sub(r"<[^>]+>", "", html_content)
        text = re.sub(r"\s+", " ", text)
        return text.strip()