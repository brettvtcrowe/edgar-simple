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
            
            data = response.json()
            filings = []
            recent_filings = data.get("filings", {}).get("recent", {})
            
            if recent_filings and isinstance(recent_filings, dict):
                # Get the parallel arrays
                accession_numbers = recent_filings.get("accessionNumber", [])
                forms = recent_filings.get("form", [])
                filing_dates = recent_filings.get("filingDate", [])
                primary_documents = recent_filings.get("primaryDocument", [])
                
                # Get the number of filings (should be same for all arrays)
                num_filings = len(accession_numbers)
                print(f"Found {num_filings} filings")
                
                # Limit to first 10 for testing
                max_filings = min(10, num_filings)
                
                # Reconstruct each filing object from parallel arrays
                for i in range(max_filings):
                    if i < len(forms):
                        form = forms[i]
                        
                        # Apply form type filter
                        if form_type and form != form_type:
                            continue
                        
                        filing_data = {
                            "accessionNumber": accession_numbers[i] if i < len(accession_numbers) else "",
                            "form": form,
                            "filingDate": filing_dates[i] if i < len(filing_dates) else "",
                            "primaryDocument": primary_documents[i] if i < len(primary_documents) else "",
                            "companyName": data.get("name", "")  # Company name is at the top level
                        }
                        
                        print(f"Processing filing {i}: {form} on {filing_data['filingDate']}")
                        
                        # For now, create FilingContent without fetching actual content
                        filing_content = FilingContent(
                            cik=cik,
                            company_name=filing_data["companyName"],
                            form_type=filing_data["form"],
                            filing_date=filing_data["filingDate"],
                            content="[Content would be fetched here]",  # Skip content fetch for now
                            url=f"{self.base_url}/Archives/edgar/data/{cik}/{filing_data['primaryDocument']}",
                            exhibits=[]
                        )
                        filings.append(filing_content)
            
            return filings
            
        except Exception as e:
            print(f"Error in get_company_filings: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_filing_content(self, cik: str, filing: Dict) -> Optional[FilingContent]:
        # Simplified for now - we'll implement this after basic structure works
        return None
    
    def _extract_text_content(self, html_content: str) -> str:
        import re
        text = re.sub(r"<[^>]+>", "", html_content)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
