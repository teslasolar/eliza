# ACG Manifesto Scan Rules

The guild's ethical AI principles, enforced as scan rules. Covers verification of AI output, input validation, transparency, error handling, PII protection, and rate limiting.

```python
"""ACG Manifesto scan rules — the guild's ethical AI principles."""

import re
from konomi.meta.rules import Rule, Severity


def get_acg_rules() -> list[Rule]:
    return [
        Rule(
            id="ACG-001",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'ai_model|llm|predict|generate|completion|inference|openai|anthropic|gpt|claude',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'return|yield|send|respond|output|result',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'verif|validat|check|assert|test|review|confirm|sanitize|schema',
                                   d.get("code", ""), re.I))
            ),
            message="AI output used without verification. ACG Principle 2: rigorous verification before production.",
            severity=Severity.ERROR,
            fix="Add verification: validate AI output against schema, known-good reference, or human review.",
            standard="ACG",
        ),
        Rule(
            id="ACG-002",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'request\.|user.*input|form.*data|body\.|params\.|argv|stdin|input\s*\(',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'validat|sanitiz|escape|check|schema|assert|isinstance',
                                   d.get("code", ""), re.I))
            ),
            message="User input without validation. ACG Principle 3: AI systems need same security as traditional software.",
            severity=Severity.ERROR,
            fix="Validate and sanitize all user inputs before processing.",
            standard="ACG",
        ),
        Rule(
            id="ACG-003",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'ai_model|llm|predict|generate|completion|gpt|claude',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'response|reply|send|render|display|output.*user',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'ai.*generat|generated.*ai|powered.*ai|ai.*assist|disclos|transparen',
                                   d.get("code", ""), re.I))
            ),
            message="AI involvement not disclosed to users. ACG Principle 5: transparency is not optional.",
            severity=Severity.WARN,
            fix="Add clear disclosure: 'AI-generated' or 'AI-assisted' labels.",
            standard="ACG",
        ),
        Rule(
            id="ACG-004",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'ai_model|llm|predict|generate|completion|inference',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'try|catch|except|error.*handl|fallback|retry|timeout',
                                   d.get("code", ""), re.I))
            ),
            message="No error handling for AI failures. ACG Principle 3: graceful degradation required.",
            severity=Severity.WARN,
            fix="Wrap AI calls in try/catch with meaningful fallback behavior.",
            standard="ACG",
        ),
        Rule(
            id="ACG-005",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(
                    r'(?:log|print|console\.log|logger)\s*\(.*(?:password|secret|token|ssn|credit.*card)',
                    d.get("code", ""), re.I))
            ),
            message="Logging sensitive/PII data. ACG Principle 4: protect humans — never log PII.",
            severity=Severity.ERROR,
            standard="ACG",
        ),
        Rule(
            id="ACG-006",
            condition=lambda d: (
                d.get("type") == "code" and
                bool(re.search(r'route|endpoint|api|express|flask|fastapi|app\.(get|post)',
                               d.get("code", ""), re.I)) and
                bool(re.search(r'ai|llm|model|predict|generate',
                               d.get("code", ""), re.I)) and
                not bool(re.search(r'rate.*limit|throttl|quota|token.*bucket',
                                   d.get("code", ""), re.I))
            ),
            message="AI endpoint without rate limiting. ACG Principle 3: protect against resource exhaustion.",
            severity=Severity.INFO,
            fix="Add rate limiting to AI-serving endpoints.",
            standard="ACG",
        ),
    ]
```
