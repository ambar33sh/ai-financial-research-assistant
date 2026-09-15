from openai import OpenAI

from app.config import get_settings
from app.schemas import Citation, SearchResult


SYSTEM_PROMPT = """You are FinSight AI, a financial research assistant.
Answer only from the supplied evidence. Never invent financial figures, sources, pages, or facts.
If the evidence is insufficient, say that the available documents do not contain enough evidence.
Use concise professional language. Distinguish reported facts from interpretation.
Citations are supplied separately by the application; do not fabricate citation metadata.
"""


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            self.client = None
            return
        kwargs = {"api_key": settings.openai_api_key}
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        self.client = OpenAI(**kwargs)
        self.model = settings.openai_model

    def answer(self, question: str, results: list[SearchResult]) -> tuple[str, list[Citation], str]:
        citations = [Citation(
            source_name=result.source_name,
            page=result.page,
            section=result.section,
            evidence=result.text[:500],
        ) for result in results]
        if not results:
            return "I could not find sufficient evidence in the indexed documents to answer this question.", [], "Insufficient"
        if not self.client:
            return (
                "LLM configuration is not available. The retrieval layer found relevant evidence; "
                "configure OPENAI_API_KEY to generate a grounded natural-language answer.",
                citations,
                "Strong" if results[0].score >= 0.65 else "Moderate",
            )
        evidence = "\n\n".join(
            f"SOURCE: {r.source_name}, PAGE: {r.page}\n{r.text}" for r in results
        )
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"QUESTION:\n{question}\n\nEVIDENCE:\n{evidence}"},
            ],
        )
        answer = response.choices[0].message.content or "No answer was generated."
        strength = "Strong" if results[0].score >= 0.65 else "Moderate"
        return answer, citations, strength
