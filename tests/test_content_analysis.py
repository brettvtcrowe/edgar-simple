import pytest
from content_analysis.document_parser import DocumentParser
from content_analysis.concept_detector import AccountingConceptDetector
from content_analysis.policy_extractor import PolicyExtractor
from content_analysis.risk_analyzer import RiskAnalyzer
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class FilingAnalysis:
    """Structured analysis of SEC filing content"""
    sections: Dict[str, str]
    accounting_concepts: List[Dict[str, str]]
    policies: List[Dict[str, str]]
    risk_factors: List[Dict[str, str]]
    summary: str

class TestDocumentParser:
    """Test document parsing and text extraction"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.parser = DocumentParser()
    
    def test_html_content_extraction(self):
        """Test extraction of text content from HTML filing"""
        html_content = """
        <html>
            <body>
                <h1>Item 1. Business</h1>
                <p>The Company adopted ASC 606 Revenue from Contracts with Customers.</p>
                <h2>Item 1A. Risk Factors</h2>
                <p>Revenue recognition policies may change.</p>
            </body>
        </html>
        """
        
        result = self.parser.parse_filing_content(html_content)
        
        assert result is not None
        assert "ASC 606" in result.sections.get("Item 1. Business", "")
        assert "Revenue from Contracts" in result.sections.get("Item 1. Business", "")
        assert "Item 1A. Risk Factors" in result.sections
        assert "revenue recognition" in result.sections.get("Item 1A. Risk Factors", "").lower()

class TestAccountingConceptDetector:
    """Test accounting concept detection in filing text"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.detector = AccountingConceptDetector()
    
    def test_asc_606_detection(self):
        """Test detection of ASC 606 revenue recognition concepts"""
        text = "The Company adopted ASC 606 Revenue from Contracts with Customers effective January 1, 2018."
        
        concepts = self.detector.detect_concepts(text)
        
        assert len(concepts) > 0
        assert any(c["standard"] == "ASC 606" for c in concepts)
        assert any("contracts" in c["concept"] for c in concepts)
        assert any(c["confidence"] > 0.8 for c in concepts)
    
    def test_asc_842_detection(self):
        """Test detection of ASC 842 lease accounting concepts"""
        text = "The Company adopted ASC 842 Leases which requires recognition of right-of-use assets and lease liabilities."
        
        concepts = self.detector.detect_concepts(text)
        
        assert len(concepts) > 0
        assert any(c["standard"] == "ASC 842" for c in concepts)
        assert any("lease" in c["concept"].lower() for c in concepts)
        assert any("right of use" in c["concept"].lower() for c in concepts)
    
    def test_multiple_concepts_detection(self):
        """Test detection of multiple accounting concepts in same text"""
        text = "The Company adopted ASC 606 for revenue recognition and ASC 842 for lease accounting."
        
        concepts = self.detector.detect_concepts(text)
        
        assert len(concepts) >= 2
        standards = [c["standard"] for c in concepts]
        assert "ASC 606" in standards
        assert "ASC 842" in standards

class TestPolicyExtractor:
    """Test policy information extraction from filing text"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.extractor = PolicyExtractor()
    
    def test_revenue_recognition_policy_extraction(self):
        """Test extraction of revenue recognition policy information"""
        text = """
        Revenue Recognition Policy:
        The Company recognizes revenue when performance obligations are satisfied and control transfers to the customer.
        Revenue is measured at the transaction price allocated to performance obligations.
        """
        
        policies = self.extractor.extract_policies(text)
        
        assert len(policies) > 0
        revenue_policies = [p for p in policies if "revenue" in p["type"].lower()]
        assert len(revenue_policies) > 0
        assert any("performance obligations" in p["content"] for p in revenue_policies)
        assert any("control transfers" in p["content"] for p in revenue_policies)
    
    def test_lease_accounting_policy_extraction(self):
        """Test extraction of lease accounting policy information"""
        text = """
        Lease Accounting:
        The Company recognizes right-of-use assets and lease liabilities for operating leases.
        Lease terms include options to extend when reasonably certain of exercise.
        """
        
        policies = self.extractor.extract_policies(text)
        
        assert len(policies) > 0
        lease_policies = [p for p in policies if "lease" in p["type"].lower()]
        assert len(lease_policies) > 0
        assert any("right-of-use" in p["content"] for p in lease_policies)
        assert any("lease liabilities" in p["content"] for p in lease_policies)

class TestRiskAnalyzer:
    """Test risk factor identification and analysis"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.analyzer = RiskAnalyzer()
    
    def test_risk_factor_identification(self):
        """Test identification of risk factors in filing text"""
        text = """
        Risk Factors:
        Changes in revenue recognition policies could materially affect financial statements.
        Lease accounting changes may impact reported assets and liabilities.
        Regulatory changes could increase compliance costs.
        """
        
        risks = self.analyzer.identify_risks(text)
        
        assert len(risks) >= 3
        risk_types = [r["type"] for r in risks]
        assert any("revenue recognition" in risk_type.lower() for risk_type in risk_types)
        assert any("lease accounting" in risk_type.lower() for risk_type in risk_types)
        assert any("regulatory" in risk_type.lower() for risk_type in risk_types)
    
    def test_risk_severity_assessment(self):
        """Test assessment of risk severity levels"""
        text = "Material changes in accounting policies could significantly impact financial results."
        
        risks = self.analyzer.identify_risks(text)
        
        assert len(risks) > 0
        assert any(r["severity"] in ["high", "medium", "low"] for r in risks)
        assert any("material" in r["content"].lower() for r in risks)

class TestContentAnalysisIntegration:
    """Test integration of all content analysis components"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.parser = DocumentParser()
        self.concept_detector = AccountingConceptDetector()
        self.policy_extractor = PolicyExtractor()
        self.risk_analyzer = RiskAnalyzer()
    
    def test_end_to_end_content_analysis(self):
        """Test complete content analysis pipeline"""
        html_content = """
        <html>
            <body>
                <h1>Item 1. Business</h1>
                <p>The Company adopted ASC 606 Revenue from Contracts with Customers.</p>
                <h2>Item 1A. Risk Factors</h2>
                <p>Changes in revenue recognition policies could materially affect results.</p>
                <h3>Significant Accounting Policies</h3>
                <p>Revenue is recognized when performance obligations are satisfied.</p>
            </body>
        </html>
        """
        
        # Parse document
        analysis = self.parser.parse_filing_content(html_content)
        
        # Extract accounting concepts
        concepts = self.concept_detector.detect_concepts(analysis.summary)
        
        # Extract policies
        policies = self.policy_extractor.extract_policies(analysis.summary)
        
        # Identify risks
        risks = self.risk_analyzer.identify_risks(analysis.summary)
        
        # Verify results
        assert analysis is not None
        assert len(concepts) > 0
        assert len(policies) > 0
        assert len(risks) > 0
        
        # Verify specific content
        assert any("ASC 606" in c["standard"] for c in concepts)
        assert any("revenue recognition" in p["type"].lower() for p in policies)
        assert any("revenue recognition" in r["type"].lower() for r in risks)
