# Phase 3: Implementation Roadmap & Technical Details

## 🚀 **Implementation Overview**
**Goal**: Build the Intelligence Engine step-by-step, following TDD principles

**Approach**: Incremental development with continuous testing
**Timeline**: 8 weeks (2 months) with weekly milestones

---

## 📅 **Week-by-Week Implementation Plan**

### **Week 1: Environment Setup & NLP Foundation**
**Goal**: Set up Python ML environment and basic NLP pipeline

#### **Day 1-2: Environment Setup**
```bash
# Create Python virtual environment
python3 -m venv phase3_env
source phase3_env/bin/activate

# Install core dependencies
pip install spacy nltk transformers scikit-learn pandas numpy
pip install requests beautifulsoup4 elasticsearch

# Download spaCy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
```

#### **Day 3-4: Basic NLP Pipeline**
```python
# nlp_engine/query_parser.py
import spacy
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ParsedQuery:
    intent: str
    entities: List[str]
    timeframe: Optional[str]
    filing_type: Optional[str]
    company: Optional[str]
    accounting_concepts: List[str]

class QueryParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.accounting_standards = {
            "ASC 606": "revenue recognition",
            "ASC 860": "transfers and servicing",
            "ASC 842": "leases",
            "ASC 350": "goodwill and intangibles"
        }
    
    def parse_query(self, query: str) -> ParsedQuery:
        """Parse natural language query into structured format"""
        doc = self.nlp(query.lower())
        
        # Extract filing type
        filing_type = self._extract_filing_type(doc)
        
        # Extract timeframe
        timeframe = self._extract_timeframe(doc)
        
        # Extract company names
        company = self._extract_company(doc)
        
        # Extract accounting concepts
        accounting_concepts = self._extract_accounting_concepts(doc)
        
        # Determine intent
        intent = self._classify_intent(doc)
        
        return ParsedQuery(
            intent=intent,
            entities=self._extract_entities(doc),
            timeframe=timeframe,
            filing_type=filing_type,
            company=company,
            accounting_concepts=accounting_concepts
        )
    
    def _extract_filing_type(self, doc) -> Optional[str]:
        """Extract SEC filing type from query"""
        filing_types = ["8-k", "10-k", "10-q", "s-1", "s-3", "424b3"]
        for token in doc:
            if token.text in filing_types:
                return token.text.upper()
        return None
    
    def _extract_timeframe(self, doc) -> Optional[str]:
        """Extract temporal references from query"""
        time_patterns = {
            "past three years": "3years",
            "past year": "1year", 
            "last five": "5filings",
            "within 12 months": "12months"
        }
        
        query_text = doc.text
        for pattern, value in time_patterns.items():
            if pattern in query_text:
                return value
        return None
    
    def _extract_company(self, doc) -> Optional[str]:
        """Extract company names from query"""
        # Use spaCy's named entity recognition
        companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        return companies[0] if companies else None
    
    def _extract_accounting_concepts(self, doc) -> List[str]:
        """Extract accounting standards and concepts"""
        concepts = []
        query_text = doc.text
        
        # Check for accounting standards
        for standard, concept in self.accounting_standards.items():
            if standard.lower() in query_text:
                concepts.append(standard)
                concepts.append(concept)
        
        # Check for specific accounting methods
        methods = ["milestone method", "failed sales", "restatement", "revenue recognition"]
        for method in methods:
            if method in query_text:
                concepts.append(method)
        
        return concepts
    
    def _classify_intent(self, doc) -> str:
        """Classify query intent"""
        query_text = doc.text
        
        if "compare" in query_text:
            return "COMPARE_POLICIES"
        elif "find" in query_text or "search" in query_text:
            return "SEARCH_FILINGS"
        elif "analyze" in query_text:
            return "ANALYZE_CONTENT"
        else:
            return "SEARCH_FILINGS"
```

#### **Day 5: Testing Framework**
```python
# tests/test_query_parser.py
import pytest
from nlp_engine.query_parser import QueryParser, ParsedQuery

class TestQueryParser:
    def setup_method(self):
        self.parser = QueryParser()
    
    def test_8k_restatement_query(self):
        """Test parsing of 8-K restatement query"""
        query = "Please find all 8-K filings from the past three years that report a restatement under Item 4.02 related to revenue recognition"
        
        result = self.parser.parse_query(query)
        
        assert result.intent == "SEARCH_FILINGS"
        assert result.filing_type == "8-K"
        assert result.timeframe == "3years"
        assert "restatement" in result.entities
        assert "ASC 606" in result.accounting_concepts
    
    def test_policy_comparison_query(self):
        """Test parsing of policy comparison query"""
        query = "Compare Microsoft's revenue recognition policy disclosures in its last five 10-K filings"
        
        result = self.parser.parse_query(query)
        
        assert result.intent == "COMPARE_POLICIES"
        assert result.filing_type == "10-K"
        assert result.company == "Microsoft"
        assert "revenue recognition" in result.accounting_concepts
```

### **Week 2: Live Data Integration**
**Goal**: Replace mock APIs with live SEC filing data

#### **Day 1-2: SEC API Client Enhancement**
```python
# data_integration/sec_api_client.py
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
        self.headers = {
            "User-Agent": "Regulatory Intelligence Hub - Phase 3 Development"
        }
        self.rate_limit_delay = 0.1  # 10 requests per second
    
    def get_company_filings(self, cik: str, form_type: Optional[str] = None, 
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[FilingContent]:
        """Get company filings with optional filtering"""
        # Respect rate limiting
        time.sleep(self.rate_limit_delay)
        
        # Get company submissions
        submissions_url = f"{self.base_url}/submissions/CIK{cik.zfill(10)}.json"
        response = requests.get(submissions_url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get company data: {response.status_code}")
        
        data = response.json()
        filings = []
        
        for filing in data.get("filings", {}).get("recent", []):
            # Apply filters
            if form_type and filing.get("form") != form_type:
                continue
                
            if start_date and filing.get("filingDate") < start_date:
                continue
                
            if end_date and filing.get("filingDate") > end_date:
                continue
            
            # Get filing content
            filing_content = self._get_filing_content(cik, filing)
            if filing_content:
                filings.append(filing_content)
        
        return filings
    
    def _get_filing_content(self, cik: str, filing: Dict) -> Optional[FilingContent]:
        """Extract content from individual filing"""
        try:
            # Get filing document
            filing_url = f"{self.base_url}/Archives/edgar/data/{cik}/{filing['primaryDocument']}"
            response = requests.get(filing_url, headers=self.headers)
            
            if response.status_code != 200:
                return None
            
            # Extract text content (basic implementation)
            content = self._extract_text_content(response.text)
            
            return FilingContent(
                cik=cik,
                company_name=filing.get("companyName", ""),
                form_type=filing.get("form", ""),
                filing_date=filing.get("filingDate", ""),
                content=content,
                url=filing_url,
                exhibits=self._extract_exhibits(response.text)
            )
            
        except Exception as e:
            print(f"Error getting filing content: {e}")
            return None
    
    def _extract_text_content(self, html_content: str) -> str:
        """Extract text content from HTML filing"""
        # Basic HTML to text extraction
        # In production, use more sophisticated parsing
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _extract_exhibits(self, html_content: str) -> List[str]:
        """Extract exhibit references from filing"""
        # Basic exhibit extraction
        import re
        
        exhibits = re.findall(r'EX-\d+\.\d+', html_content)
        return list(set(exhibits))
```

#### **Day 3-4: Content Indexing System**
```python
# data_integration/indexer.py
from elasticsearch import Elasticsearch
from typing import List, Dict
import json

class ContentIndexer:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.index_name = "sec_filings"
    
    def create_index(self):
        """Create Elasticsearch index for SEC filings"""
        mapping = {
            "mappings": {
                "properties": {
                    "cik": {"type": "keyword"},
                    "company_name": {"type": "text"},
                    "form_type": {"type": "keyword"},
                    "filing_date": {"type": "date"},
                    "content": {"type": "text", "analyzer": "standard"},
                    "accounting_concepts": {"type": "keyword"},
                    "industry": {"type": "keyword"},
                    "risk_factors": {"type": "text"}
                }
            }
        }
        
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=mapping)
    
    def index_filing(self, filing_content: FilingContent, 
                     accounting_concepts: List[str] = None,
                     industry: str = None):
        """Index a filing in Elasticsearch"""
        doc = {
            "cik": filing_content.cik,
            "company_name": filing_content.company_name,
            "form_type": filing_content.form_type,
            "filing_date": filing_content.filing_date,
            "content": filing_content.content,
            "url": filing_content.url,
            "accounting_concepts": accounting_concepts or [],
            "industry": industry or "Unknown"
        }
        
        self.es.index(index=self.index_name, body=doc)
    
    def search_filings(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search filings using Elasticsearch"""
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": query}}
                    ]
                }
            }
        }
        
        # Add filters
        if filters:
            for field, value in filters.items():
                if value:
                    search_body["query"]["bool"]["filter"] = [
                        {"term": {field: value}}
                    ]
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        return [hit["_source"] for hit in response["hits"]["hits"]]
```

#### **Day 5: Integration Testing**
```python
# tests/test_data_integration.py
import pytest
from data_integration.sec_api_client import SECAPIClient
from data_integration.indexer import ContentIndexer

class TestDataIntegration:
    def setup_method(self):
        self.api_client = SECAPIClient()
        self.indexer = ContentIndexer()
    
    def test_company_filing_retrieval(self):
        """Test retrieving company filings from SEC API"""
        # Test with a known company (Apple)
        filings = self.api_client.get_company_filings("320193", form_type="8-K", 
                                                    start_date="2024-01-01", end_date="2024-12-31")
        
        assert len(filings) > 0
        assert all(f.form_type == "8-K" for f in filings)
        assert all(f.cik == "320193" for f in filings)
    
    def test_content_extraction(self):
        """Test filing content extraction"""
        filings = self.api_client.get_company_filings("320193", form_type="10-K")
        
        if filings:
            filing = filings[0]
            assert filing.content is not None
            assert len(filing.content) > 100  # Should have substantial content
            assert filing.url is not None
```

### **Week 3: Content Analysis Engine**
**Goal**: Implement accounting concept detection and policy analysis

#### **Day 1-2: Accounting Concept Detector**
```python
# content_analyzer/accounting_detector.py
import re
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class AccountingConcept:
    standard: str
    concept: str
    confidence: float
    context: str

class AccountingDetector:
    def __init__(self):
        self.accounting_standards = {
            "ASC 606": {
                "concepts": ["revenue recognition", "contract", "performance obligation", "milestone"],
                "keywords": ["revenue", "recognition", "contract", "obligation", "milestone", "progress"]
            },
            "ASC 860": {
                "concepts": ["transfers", "servicing", "factoring", "receivable", "failed sale"],
                "keywords": ["transfer", "servicing", "factoring", "receivable", "sale", "failed"]
            },
            "ASC 842": {
                "concepts": ["lease", "right of use", "lease liability"],
                "keywords": ["lease", "right of use", "liability", "asset"]
            }
        }
        
        self.restatement_patterns = [
            r"restatement",
            r"restate",
            r"Item 4\.02",
            r"material.*error",
            r"accounting.*error"
        ]
    
    def detect_accounting_concepts(self, text: str) -> List[AccountingConcept]:
        """Detect accounting standards and concepts in text"""
        concepts = []
        text_lower = text.lower()
        
        for standard, config in self.accounting_standards.items():
            # Check for standard mention
            if standard.lower() in text_lower:
                # Find related concepts
                for concept in config["concepts"]:
                    if concept in text_lower:
                        # Find context around the concept
                        context = self._find_context(text, concept)
                        confidence = self._calculate_confidence(text, concept, config["keywords"])
                        
                        concepts.append(AccountingConcept(
                            standard=standard,
                            concept=concept,
                            confidence=confidence,
                            context=context
                        ))
        
        return concepts
    
    def detect_restatements(self, text: str) -> List[Dict]:
        """Detect restatement disclosures in text"""
        restatements = []
        text_lower = text.lower()
        
        for pattern in self.restatement_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Extract context around the match
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 200)
                context = text[start:end]
                
                restatements.append({
                    "type": "restatement",
                    "pattern": pattern,
                    "context": context,
                    "position": match.start()
                })
        
        return restatements
    
    def _find_context(self, text: str, concept: str, window: int = 200) -> str:
        """Find context around a concept mention"""
        concept_pos = text.lower().find(concept.lower())
        if concept_pos == -1:
            return ""
        
        start = max(0, concept_pos - window)
        end = min(len(text), concept_pos + len(concept) + window)
        
        return text[start:end].strip()
    
    def _calculate_confidence(self, text: str, concept: str, keywords: List[str]) -> float:
        """Calculate confidence score for concept detection"""
        text_lower = text.lower()
        concept_lower = concept.lower()
        
        # Base confidence from concept presence
        confidence = 0.5 if concept_lower in text_lower else 0.0
        
        # Boost confidence based on keyword presence
        keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
        confidence += min(0.5, keyword_matches * 0.1)
        
        return min(1.0, confidence)
```

#### **Day 3-4: Policy Change Detector**
```python
# content_analyzer/policy_analyzer.py
from difflib import SequenceMatcher
from typing import List, Dict, Tuple
import re

class PolicyAnalyzer:
    def __init__(self):
        self.policy_sections = [
            "revenue recognition",
            "accounting policies",
            "significant accounting policies",
            "critical accounting estimates"
        ]
    
    def compare_policies(self, filing1_content: str, filing2_content: str, 
                        policy_focus: str = None) -> Dict:
        """Compare policies between two filings"""
        # Extract relevant policy sections
        policy1 = self._extract_policy_section(filing1_content, policy_focus)
        policy2 = self._extract_policy_section(filing2_content, policy_focus)
        
        if not policy1 or not policy2:
            return {"error": "Could not extract policy sections"}
        
        # Calculate similarity
        similarity = self._calculate_similarity(policy1, policy2)
        
        # Find specific changes
        changes = self._identify_changes(policy1, policy2)
        
        return {
            "similarity_score": similarity,
            "changes": changes,
            "policy1_length": len(policy1),
            "policy2_length": len(policy2)
        }
    
    def _extract_policy_section(self, content: str, focus: str = None) -> str:
        """Extract policy section from filing content"""
        content_lower = content.lower()
        
        # Look for policy section headers
        for section in self.policy_sections:
            if section in content_lower:
                # Find the section
                start_pos = content_lower.find(section)
                if start_pos != -1:
                    # Extract from start to next major section
                    section_content = self._extract_to_next_section(content, start_pos)
                    return section_content
        
        # If no specific section found, look for focus area
        if focus:
            focus_lower = focus.lower()
            if focus_lower in content_lower:
                start_pos = content_lower.find(focus_lower)
                if start_pos != -1:
                    section_content = self._extract_to_next_section(content, start_pos)
                    return section_content
        
        return ""
    
    def _extract_to_next_section(self, content: str, start_pos: int, 
                                max_length: int = 5000) -> str:
        """Extract content from start position to next major section"""
        # Look for next major section header
        section_headers = ["item", "note", "exhibit", "part"]
        
        end_pos = start_pos + max_length
        for header in section_headers:
            next_header = content.lower().find(header, start_pos + 100)
            if next_header != -1 and next_header < end_pos:
                end_pos = next_header
        
        return content[start_pos:end_pos].strip()
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two policy texts"""
        # Use sequence matcher for similarity
        matcher = SequenceMatcher(None, text1, text2)
        return matcher.ratio()
    
    def _identify_changes(self, text1: str, text2: str) -> List[Dict]:
        """Identify specific changes between two texts"""
        changes = []
        
        # Split into sentences for comparison
        sentences1 = self._split_into_sentences(text1)
        sentences2 = self._split_into_sentences(text2)
        
        # Find added/removed sentences
        for sentence in sentences1:
            if sentence not in sentences2:
                changes.append({
                    "type": "removed",
                    "content": sentence,
                    "action": "removed from newer filing"
                })
        
        for sentence in sentences2:
            if sentence not in sentences1:
                changes.append({
                    "type": "added",
                    "content": sentence,
                    "action": "added in newer filing"
                })
        
        return changes
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Basic sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
```

#### **Day 5: Testing Content Analysis**
```python
# tests/test_content_analysis.py
import pytest
from content_analyzer.accounting_detector import AccountingDetector
from content_analyzer.policy_analyzer import PolicyAnalyzer

class TestContentAnalysis:
    def setup_method(self):
        self.accounting_detector = AccountingDetector()
        self.policy_analyzer = PolicyAnalyzer()
    
    def test_accounting_concept_detection(self):
        """Test detection of accounting concepts"""
        text = "The Company adopted ASC 606 Revenue from Contracts with Customers effective January 1, 2018."
        
        concepts = self.accounting_detector.detect_accounting_concepts(text)
        
        assert len(concepts) > 0
        assert any(c.standard == "ASC 606" for c in concepts)
        assert any("revenue recognition" in c.concept for c in concepts)
    
    def test_restatement_detection(self):
        """Test detection of restatement disclosures"""
        text = "The Company determined that a restatement of previously issued financial statements is required under Item 4.02."
        
        restatements = self.accounting_detector.detect_restatements(text)
        
        assert len(restatements) > 0
        assert any("restatement" in r["type"] for r in restatements)
        assert any("Item 4.02" in r["pattern"] for r in restatements)
    
    def test_policy_comparison(self):
        """Test policy comparison between filings"""
        policy1 = "Revenue is recognized when performance obligations are satisfied."
        policy2 = "Revenue is recognized when performance obligations are satisfied and control transfers to customer."
        
        comparison = self.policy_analyzer.compare_policies(policy1, policy2, "revenue recognition")
        
        assert comparison["similarity_score"] > 0.5
        assert len(comparison["changes"]) > 0
```

### **Week 4: Query Processing Integration**
**Goal**: Integrate NLP pipeline with content analysis and live data

#### **Day 1-2: Query Engine Integration**
```python
# query_engine/query_processor.py
from typing import Dict, List, Any
from nlp_engine.query_parser import QueryParser
from data_integration.sec_api_client import SECAPIClient
from data_integration.indexer import ContentIndexer
from content_analyzer.accounting_detector import AccountingDetector
from content_analyzer.policy_analyzer import PolicyAnalyzer

class QueryProcessor:
    def __init__(self):
        self.query_parser = QueryParser()
        self.api_client = SECAPIClient()
        self.indexer = ContentIndexer()
        self.accounting_detector = AccountingDetector()
        self.policy_analyzer = PolicyAnalyzer()
    
    def process_query(self, natural_language_query: str) -> Dict[str, Any]:
        """Process natural language query end-to-end"""
        try:
            # Step 1: Parse natural language query
            parsed_query = self.query_parser.parse_query(natural_language_query)
            
            # Step 2: Execute query based on intent
            if parsed_query.intent == "SEARCH_FILINGS":
                results = self._search_filings(parsed_query)
            elif parsed_query.intent == "COMPARE_POLICIES":
                results = self._compare_policies(parsed_query)
            elif parsed_query.intent == "ANALYZE_CONTENT":
                results = self._analyze_content(parsed_query)
            else:
                results = {"error": f"Unknown intent: {parsed_query.intent}"}
            
            # Step 3: Format response
            return {
                "query": natural_language_query,
                "parsed_query": parsed_query.__dict__,
                "results": results,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "query": natural_language_query,
                "error": str(e),
                "status": "error"
            }
    
    def _search_filings(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Search for filings based on parsed query"""
        # Get company CIK if specified
        company_cik = None
        if parsed_query.company:
            company_cik = self._get_company_cik(parsed_query.company)
        
        # Determine date range
        date_range = self._parse_timeframe(parsed_query.timeframe)
        
        # Search for filings
        if company_cik:
            # Company-specific search
            filings = self.api_client.get_company_filings(
                company_cik, 
                form_type=parsed_query.filing_type,
                start_date=date_range["start"],
                end_date=date_range["end"]
            )
        else:
            # Industry-wide search (use indexer)
            search_query = " ".join(parsed_query.accounting_concepts)
            filters = {
                "form_type": parsed_query.filing_type,
                "filing_date": date_range
            }
            filings = self.indexer.search_filings(search_query, filters)
        
        # Filter and analyze results
        filtered_filings = self._filter_filings_by_content(filings, parsed_query)
        
        return {
            "total_found": len(filtered_filings),
            "filings": filtered_filings[:10],  # Limit results
            "search_criteria": {
                "company": parsed_query.company,
                "filing_type": parsed_query.filing_type,
                "timeframe": parsed_query.timeframe,
                "concepts": parsed_query.accounting_concepts
            }
        }
    
    def _compare_policies(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Compare policies across filings"""
        if not parsed_query.company:
            return {"error": "Company name required for policy comparison"}
        
        # Get company CIK
        company_cik = self._get_company_cik(parsed_query.company)
        if not company_cik:
            return {"error": f"Company not found: {parsed_query.company}"}
        
        # Get recent filings
        filings = self.api_client.get_company_filings(
            company_cik,
            form_type=parsed_query.filing_type,
            start_date="2020-01-01"  # Default to 4 years
        )
        
        if len(filings) < 2:
            return {"error": "Insufficient filings for comparison"}
        
        # Compare policies
        comparisons = []
        for i in range(len(filings) - 1):
            comparison = self.policy_analyzer.compare_policies(
                filings[i].content,
                filings[i + 1].content,
                "revenue recognition"  # Default focus
            )
            
            comparisons.append({
                "filing1": filings[i].filing_date,
                "filing2": filings[i + 1].filing_date,
                "similarity": comparison.get("similarity_score", 0),
                "changes": comparison.get("changes", [])
            })
        
        return {
            "company": parsed_query.company,
            "filing_type": parsed_query.filing_type,
            "comparisons": comparisons
        }
    
    def _analyze_content(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Analyze filing content for specific concepts"""
        # This would implement content analysis based on query
        # For now, return basic structure
        return {
            "analysis_type": "content_analysis",
            "concepts_requested": parsed_query.accounting_concepts,
            "message": "Content analysis to be implemented"
        }
    
    def _get_company_cik(self, company_name: str) -> str:
        """Get company CIK from name"""
        # Basic implementation - in production, use company database
        company_mapping = {
            "microsoft": "789019",
            "apple": "320193",
            "amazon": "1018724",
            "google": "1652044",
            "alphabet": "1652044"
        }
        
        return company_mapping.get(company_name.lower(), None)
    
    def _parse_timeframe(self, timeframe: str) -> Dict[str, str]:
        """Parse timeframe into date range"""
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        
        if timeframe == "3years":
            start_date = end_date - timedelta(days=3*365)
        elif timeframe == "1year":
            start_date = end_date - timedelta(days=365)
        elif timeframe == "6months":
            start_date = end_date - timedelta(days=180)
        else:
            start_date = end_date - timedelta(days=365)  # Default to 1 year
        
        return {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d")
        }
    
    def _filter_filings_by_content(self, filings: List, parsed_query: ParsedQuery) -> List:
        """Filter filings based on content analysis"""
        filtered = []
        
        for filing in filings:
            # Check if filing contains required concepts
            if hasattr(filing, 'content'):
                content = filing.content
            else:
                content = filing.get('content', '')
            
            # Detect accounting concepts
            concepts = self.accounting_detector.detect_accounting_concepts(content)
            
            # Check if filing matches query requirements
            if self._filing_matches_query(concepts, parsed_query):
                filtered.append(filing)
        
        return filtered
    
    def _filing_matches_query(self, concepts: List, parsed_query: ParsedQuery) -> bool:
        """Check if filing matches query requirements"""
        if not parsed_query.accounting_concepts:
            return True
        
        # Check if any required concepts are present
        required_concepts = set(parsed_query.accounting_concepts)
        detected_concepts = set()
        
        for concept in concepts:
            detected_concepts.add(concept.concept)
            detected_concepts.add(concept.standard)
        
        # Check for overlap
        return bool(required_concepts & detected_concepts)
```

#### **Day 3-4: API Endpoint Integration**
```python
# server.py (updated for Phase 3)
from query_engine.query_processor import QueryProcessor

# Initialize query processor
query_processor = QueryProcessor()

# New natural language query endpoint
app.post('/api/query/natural', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }
        
        // Process natural language query
        const result = await query_processor.process_query(query);
        
        res.json(result);
        
    } catch (error) {
        console.error('Natural language query error:', error);
        res.status(500).json({ error: 'Query processing failed' });
    }
});
```

#### **Day 5: End-to-End Testing**
```python
# tests/test_end_to_end.py
import pytest
from query_engine.query_processor import QueryProcessor

class TestEndToEnd:
    def setup_method(self):
        self.processor = QueryProcessor()
    
    def test_8k_restatement_query(self):
        """Test complete 8-K restatement query processing"""
        query = "Please find all 8-K filings from the past three years that report a restatement under Item 4.02 related to revenue recognition"
        
        result = self.processor.process_query(query)
        
        assert result["status"] == "success"
        assert result["parsed_query"]["intent"] == "SEARCH_FILINGS"
        assert result["parsed_query"]["filing_type"] == "8-K"
        assert "restatement" in result["parsed_query"]["accounting_concepts"]
    
    def test_policy_comparison_query(self):
        """Test complete policy comparison query processing"""
        query = "Compare Microsoft's revenue recognition policy disclosures in its last five 10-K filings"
        
        result = self.processor.process_query(query)
        
        assert result["status"] == "success"
        assert result["parsed_query"]["intent"] == "COMPARE_POLICIES"
        assert result["parsed_query"]["company"] == "Microsoft"
        assert "revenue recognition" in result["parsed_query"]["accounting_concepts"]
```

---

## 🎯 **Week 4 Success Criteria**

### **Functional Requirements**
- [ ] Natural language queries processed end-to-end
- [ ] Live SEC data integration working
- [ ] Accounting concept detection operational
- [ ] Policy comparison functional
- [ ] API endpoints responding correctly

### **Performance Requirements**
- [ ] Query response time <10 seconds
- [ ] Content analysis accuracy >80%
- [ ] Concept detection precision >85%
- [ ] System stability maintained

### **Testing Requirements**
- [ ] All unit tests passing
- [ ] Integration tests successful
- [ ] End-to-end tests working
- [ ] Performance benchmarks met

---

## 🚀 **Next Steps After Week 4**

### **Phase 3B: Intelligence Engine Enhancement**
1. **Advanced NLP**: Improve query understanding accuracy
2. **Content Analysis**: Enhance accounting concept detection
3. **Performance Optimization**: Improve response times
4. **User Experience**: Add natural language interface to frontend

### **Phase 4 Preparation**
1. **Multi-Source Integration**: Plan comment letters, FASB standards
2. **Advanced Analytics**: Design correlation and trend analysis
3. **Machine Learning**: Plan ML-powered insights
4. **Scalability**: Design for production deployment

---

**Ready to begin Week 1 implementation?** 🚀
