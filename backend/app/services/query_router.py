import re


class QueryRouter:
    ANALYTICS_PATTERNS = (
        r"\b(cagr|growth rate|margin|ratio|roe|roa|roic|debt[- ]to[- ]equity|current ratio)\b",
        r"\b(compare|versus|vs\.?|difference between)\b",
    )
    RAG_PATTERNS = (
        r"\b(why|what did|what risks|risk factors|management|explain|according to|mentioned)\b",
    )

    def route(self, query: str) -> str:
        normalized = query.lower()
        analytics = any(re.search(pattern, normalized) for pattern in self.ANALYTICS_PATTERNS)
        rag = any(re.search(pattern, normalized) for pattern in self.RAG_PATTERNS)
        if analytics and rag:
            return "hybrid"
        if analytics:
            return "analytics"
        return "rag"
