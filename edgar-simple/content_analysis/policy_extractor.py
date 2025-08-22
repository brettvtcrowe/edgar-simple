from typing import List, Dict
import re

class PolicyExtractor:
    """Extract policy information from filing text"""
    
    def __init__(self):
        self.policy_keywords = [
            "revenue recognition", "lease accounting", "goodwill", "intangibles",
            "impairment", "transfers", "servicing", "financial assets"
        ]
    
    def extract_policies(self, text: str) -> List[Dict[str, str]]:
        """Extract policy information from filing text"""
        policies = []
        text_lower = text.lower()
        
        # Look for policy sections
        for keyword in self.policy_keywords:
            if keyword in text_lower:
                policy_content = self._extract_policy_section(text, keyword)
                if policy_content:
                    policies.append({
                        "type": keyword.title(),
                        "content": policy_content,
                        "confidence": self._calculate_policy_confidence(text_lower, keyword)
                    })
        
        return policies
    
    def _extract_policy_section(self, text: str, policy_keyword: str) -> str:
        """Extract policy section content around a keyword"""
        text_lower = text.lower()
        keyword_pos = text_lower.find(policy_keyword)
        
        if keyword_pos == -1:
            return ""
        
        # Extract content around the keyword
        start = max(0, keyword_pos - 200)
        end = min(len(text), keyword_pos + len(policy_keyword) + 500)
        
        section_content = text[start:end]
        
        # Clean up the content
        cleaned_content = re.sub(r'\s+', ' ', section_content).strip()
        
        return cleaned_content
    
    def _calculate_policy_confidence(self, text: str, policy_keyword: str) -> float:
        """Calculate confidence score for policy extraction"""
        confidence = 0.5
        
        # Boost confidence if keyword appears multiple times
        keyword_count = text.count(policy_keyword)
        confidence += min(0.3, keyword_count * 0.1)
        
        # Boost confidence if related terms are present
        related_terms = {
            "revenue recognition": ["revenue", "recognition", "contracts", "obligations"],
            "lease accounting": ["lease", "right of use", "liabilities", "assets"],
            "goodwill": ["goodwill", "impairment", "intangibles"],
            "transfers": ["transfers", "servicing", "financial"]
        }
        
        if policy_keyword in related_terms:
            related_count = sum(1 for term in related_terms[policy_keyword] if term in text)
            confidence += min(0.2, related_count * 0.05)
        
        return min(1.0, confidence)
