from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass
class QueryResult:
    """Structured result of a natural language query"""
    query: str
    parsed_query: Dict[str, Any]
    filings: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    summary: str
    confidence: float
