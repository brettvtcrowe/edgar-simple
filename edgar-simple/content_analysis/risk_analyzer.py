from typing import List, Dict
import re

class RiskAnalyzer:
    """Identify and analyze risk factors in filing text"""
    
    def __init__(self):
        self.risk_keywords = [
            "revenue recognition", "lease accounting", "goodwill", "impairment",
            "regulatory", "compliance", "material", "significant", "impact"
        ]
        
        self.severity_indicators = {
            "high": ["material", "significant", "substantial", "major", "critical"],
            "medium": ["moderate", "considerable", "notable", "important"],
            "low": ["minor", "minimal", "limited", "small"]
        }
    
    def identify_risks(self, text: str) -> List[Dict[str, str]]:
        """Identify risk factors in filing text"""
        risks = []
        text_lower = text.lower()
        
        # Look for risk-related content
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                risk_content = self._extract_risk_content(text, keyword)
                if risk_content:
                    severity = self._assess_risk_severity(text_lower, keyword)
                    risks.append({
                        "type": keyword.title(),
                        "content": risk_content,
                        "severity": severity,
                        "confidence": self._calculate_risk_confidence(text_lower, keyword)
                    })
        
        return risks
    
    def _extract_risk_content(self, text: str, risk_keyword: str) -> str:
        """Extract risk-related content around a keyword"""
        text_lower = text.lower()
        keyword_pos = text_lower.find(risk_keyword)
        
        if keyword_pos == -1:
            return ""
        
        # Extract content around the keyword
        start = max(0, keyword_pos - 300)
        end = min(len(text), keyword_pos + len(risk_keyword) + 300)
        
        risk_content = text[start:end]
        
        # Clean up the content
        cleaned_content = re.sub(r'\s+', ' ', risk_content).strip()
        
        return cleaned_content
    
    def _assess_risk_severity(self, text: str, risk_keyword: str) -> str:
        """Assess the severity level of a risk"""
        # Default to medium severity
        severity = "medium"
        
        # Check for high severity indicators
        for indicator in self.severity_indicators["high"]:
            if indicator in text:
                severity = "high"
                break
        
        # Check for low severity indicators
        if severity != "high":
            for indicator in self.severity_indicators["low"]:
                if indicator in text:
                    severity = "low"
                    break
        
        return severity
    
    def _calculate_risk_confidence(self, text: str, risk_keyword: str) -> float:
        """Calculate confidence score for risk identification"""
        confidence = 0.5
        
        # Boost confidence if keyword appears multiple times
        keyword_count = text.count(risk_keyword)
        confidence += min(0.3, keyword_count * 0.1)
        
        # Boost confidence if severity indicators are present
        severity_indicators = []
        for level_indicators in self.severity_indicators.values():
            severity_indicators.extend(level_indicators)
        
        indicator_count = sum(1 for indicator in severity_indicators if indicator in text)
        confidence += min(0.2, indicator_count * 0.05)
        
        return min(1.0, confidence)
