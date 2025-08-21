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
    
    def get_company_filings(self, cik: str, form_type: Optional[str] = None):
        time.sleep(self.rate_limit_delay)
        try:
            submissions_url = f"{self.base_url}/submissions/CIK{cik.zfill(10)}.json"
            print(f"Making request to: {submissions_url}")
            
            response = requests.get(submissions_url, headers=self.headers)
            print(f"Response status: {response.status_code}")
            print(f"Response content preview: {response.text[:200]}")
            
            if response.status_code != 200:
                print(f"API request failed with status {response.status_code}")
                return []
            
            data = response.json()
            print(f"Successfully parsed JSON, type: {type(data)}")
            
            filings = []
            recent_filings = data.get("filings", {}).get("recent", [])
            print(f"Found {len(recent_filings)} recent filings")
            print(f"Recent filings: {recent_filings}")
            print(f"Data keys: {list(data.keys())}")
            if "filings" in data:
                print(f"Filings keys: {list(data["filings"].keys())}")
            
            for filing in recent_filings:
                print(f"Processing filing: {filing}")
                print(f"Filing type: {type(filing)}")
                if form_type and filing.get("form") != form_type:
                    continue
                
                filing_content = self._get_filing_content(cik, filing)
                if filing_content:
                    filings.append(filing_content)
            
            return filings
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def _get_filing_content(self, cik: str, filing: Dict):
        try:
            filing_url = f"{self.base_url}/Archives/edgar/data/{cik}/{filing["primaryDocument"]}"
            response = requests.get(filing_url, headers=self.headers)
            
            if response.status_code != 200:
                return None
            
            content = self._extract_text_content(response.text)
            
            return FilingContent(
                cik=cik,
                company_name=filing.get("companyName", ""),
                form_type=filing.get("form", ""),
                filing_date=filing.get("filingDate", ""),
                content=content,
                url=filing_url,
                exhibits=[]
            )
            
        except Exception as e:
            return None
    
    def _extract_text_content(self, html_content: str) -> str:
        import re
        text = re.sub(r"<[^>]+>", "", html_content)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
