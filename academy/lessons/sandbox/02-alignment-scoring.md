# Alignment Scoring

## How It Works

The alignment checker analyzes text against six keyword dimensions — one per ACG Manifesto principle.

```javascript
// The keyword map
const keywords = {
  innovation: ["explore", "verify", "independent", "evidence"],
  quality:    ["test", "validate", "review", "rigorous", "standard"],
  safety:     ["secure", "safe", "harness", "liability", "protect"],
  human:      ["human", "people", "psychological", "wellbeing", "care"],
  consent:    ["transparent", "disclose", "inform", "consent", "know"],
  refuse:     ["refuse", "decline", "ethical", "obligation", "no"],
};

console.log("Dimensions:", Object.keys(keywords).length);
console.log("Total keywords:", Object.values(keywords).flat().length);
```

## Scoring Algorithm

For each dimension, count how many keywords appear in the text. Divide by total keywords in that dimension. Cap at 1.0.

```javascript
function scoreAlignment(text) {
  const t = text.toLowerCase();
  const kw = {
    innovation: ["explore","verify","independent","evidence"],
    quality: ["test","validate","review","rigorous","standard"],
    safety: ["secure","safe","harness","liability","protect"],
    human: ["human","people","psychological","wellbeing","care"],
    consent: ["transparent","disclose","inform","consent","know"],
    refuse: ["refuse","decline","ethical","obligation","no"],
  };

  const scores = {};
  for (const [dim, words] of Object.entries(kw)) {
    const hits = words.filter(w => t.includes(w)).length;
    scores[dim] = Math.min(hits / words.length, 1.0);
  }

  const avg = Object.values(scores).reduce((a,b) => a+b, 0) / 6;
  return { scores, overall: Math.round(avg * 100) / 100, aligned: avg >= 0.3 };
}

// Test it live:
const result = scoreAlignment(
  "We test and validate AI rigorously, protect human wellbeing, " +
  "refuse unsafe systems, and inform users transparently."
);
console.log("Score:", JSON.stringify(result.scores));
console.log("Overall:", result.overall, "Aligned:", result.aligned);
```

## Limitations

This is keyword-density scoring — not semantic understanding. A sentence like "we don't test anything" would still score on "test". For deeper analysis, use the scanner's AI deep scan with a local LLM.

## Extending

Add new dimensions by extending the keyword map. The scoring function is intentionally simple — a foundation for more sophisticated analysis.
