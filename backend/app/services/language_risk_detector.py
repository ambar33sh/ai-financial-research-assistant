import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageRiskFlag:
    category: str
    severity: str
    phrase: str
    rationale: str


RULES = (
    ("Going concern", "critical", (r"substantial doubt", r"going concern"), "Management language may indicate uncertainty about the company's ability to continue operating."),
    ("Internal controls", "high", (r"material weakness", r"significant deficiency"), "The filing identifies a weakness or deficiency in internal financial controls."),
    ("Liquidity", "high", (r"liquidity (?:risk|concern|constraints?)", r"liquidity needs", r"liquidity position"), "The filing discusses liquidity pressure or funding needs."),
    ("Litigation", "high", (r"material litigation", r"litigation risk", r"legal proceedings"), "The filing highlights potentially material legal exposure."),
    ("Regulatory", "medium", (r"regulatory risk", r"regulatory uncertainty", r"regulatory changes?"), "Management identifies regulatory uncertainty or potential impact."),
    ("Impairment", "high", (r"impairment charge", r"impairment loss", r"risk of impairment"), "The filing indicates a potential or recognized impairment impact."),
    ("Restructuring", "medium", (r"restructuring charge", r"restructuring costs?", r"restructuring plan"), "The filing discusses restructuring activity or related costs."),
    ("Supply chain", "medium", (r"supply chain disruption", r"supply chain constraints?"), "The filing identifies supply-chain disruption or constraints."),
    ("Customer concentration", "medium", (r"customer concentration", r"concentration of customers?"), "The filing identifies dependence on a concentrated customer base."),
    ("Adverse impact", "medium", (r"may adversely affect", r"could adversely affect", r"materially adversely affect"), "Management explicitly describes a potential adverse impact."),
)


def detect_language_risks(text: str) -> list[LanguageRiskFlag]:
    flags: list[LanguageRiskFlag] = []
    for category, severity, patterns, rationale in RULES:
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                flags.append(LanguageRiskFlag(category, severity, match.group(0), rationale))
                break
    return flags
