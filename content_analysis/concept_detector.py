from typing import List, Dict
import re

class AccountingConceptDetector:
    """Detect accounting standards and concepts in filing text"""
    
    def __init__(self):
        self.asc_standards = {
            "ASC 606": ["revenue recognition", "contracts", "performance obligations", "revenue from contracts"],
            "ASC 842": ["leases", "right of use", "lease payments", "lease liabilities"],
            "ASC 350": ["goodwill", "intangibles", "impairment"],
            "ASC 860": ["transfers", "servicing", "financial assets"]
        }
    
    def detect_concepts(self, text: str) -> List[Dict[str, str]]:
        """Detect accounting standards and concepts in filing text"""
        detected_concepts = []
        text_lower = text.lower()
        
        for standard, keywords in self.asc_standards.items():
            if self._contains_concept(text_lower, keywords):
                # Find the most relevant concept
                concept = self._find_most_relevant_concept(text_lower, keywords)
                confidence = self._calculate_confidence(text_lower, keywords)
                context = self._extract_context(text, concept)
                
                detected_concepts.append({
                    "standard": standard,
                    "concept": concept,
                    "confidence": confidence,
                    "context": context
                })
        
        return detected_concepts
    
    def _contains_concept(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        # Check if any keyword is present in the text
        return any(keyword in text for keyword in keywords)
    
    def _find_most_relevant_concept(self, text: str, keywords: List[str]) -> str:
        """Find the most relevant concept from the keywords"""
        # Return the first keyword found in the text
        for keyword in keywords:
            if keyword in text:
                return keyword
        return keywords[0]  # Fallback
    
    def _calculate_confidence(self, text: str, keywords: List[str]) -> float:
        """Calculate confidence score for concept detection"""
        # Base confidence from concept presence
        confidence = 0.5
        
        # Boost confidence based on keyword presence
        keyword_matches = sum(1 for keyword in keywords if keyword in text)
        confidence += min(0.5, keyword_matches * 0.1)
        
        # Boost confidence if standard name is mentioned
        if any(standard.lower() in text for standard in ["asc 606", "asc 842", "asc 350", "asc 860"]):
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _extract_context(self, text: str, concept: str, window: int = 100) -> str:
        """Extract context around a concept mention"""
        concept_pos = text.lower().find(concept.lower())
        if concept_pos == -1:
            return ""
        
        start = max(0, concept_pos - window)
        end = min(len(text), concept_pos + len(concept) + window)
        
        return text[start:end].strip()
