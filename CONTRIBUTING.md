# Contributing to Dali

Thank you for contributing to Dali. This document covers how to get involved
and what kinds of contributions are most valuable to the project.

---

## What this project needs most

Dali is a **legal citation integrity standards project**, not a typical
open-source library. The most valuable contributions are:

| Area | What's needed |
|------|--------------|
| **Corpus expansion** | Annotated prompt/citation pairs, especially UK/Commonwealth, Brazil, and adversarial hallucination cases |
| **Ontology review** | Legal practitioners reviewing treatment and proposition ontology definitions for correctness |
| **Parser coverage** | eyecite wrapper improvements, jurisdiction adapter implementations |
| **RFC authorship** | Drafting and reviewing specification changes (see [RFC_PROCESS.md](RFC_PROCESS.md)) |
| **Benchmark replication** | Running the benchmark against new models and sharing results |

Code contributions are welcome but secondary to the above. Annotation quality
and ontology correctness are the core bottlenecks.

---

## Getting started

```bash
git clone https://github.com/yenk/Dali.git
cd Dali
pip install -r requirements.txt
pytest tests/
```

The benchmark runner requires API keys for the models you want to evaluate.
See [docs/examples.md](docs/examples.md) for a walkthrough.

---

## Corpus contributions

Corpus entries live in `synthetic/` (generated probes) and `data/public/`
(annotated real-world citation failures).

Each entry should include:

- `prompt` — the LLM prompt that produced the output
- `llm_output` — the output containing the citation
- `citations` — list of citations with ground-truth annotation
- `expected_verdict` — `supported`, `partially_supported`, or `not_supported`
- `jurisdiction` — jurisdiction code (e.g. `us-fed`, `us-state`, `uk`, `br`)
- `notes` — brief explanation of why this is interesting or tricky

Entries that contain real case names must be verified against CourtListener or
an equivalent authoritative source before submission.

---

## Specification contributions

See [RFC_PROCESS.md](RFC_PROCESS.md). Schema and ontology changes require an RFC.
Documentation and clarification changes do not.

---

## Pull request checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] New corpus entries are annotated with ground-truth verdicts
- [ ] Schema changes have a corresponding RFC (or reference an accepted RFC)
- [ ] No PII in corpus entries (run `corpus/anonymizer.py` if needed)
- [ ] Commit author matches your real identity

---

## What we do not accept

- Changes to Evidence JSON contract semantics without an accepted RFC
- New ontology categories without meeting the minimalism rule in RFC_PROCESS.md
- Corpus entries with unannotated or unverified citations
- Dependencies on proprietary data sources that cannot be redistributed

---

## Academic partnerships

If you are affiliated with a law school, legal research institute, or court
data project and want to contribute corpus data or co-author evaluation
methodology, please open an issue with the label `partnership`. We are
particularly interested in structured collaborations with Stanford CodeX and
Harvard CAP.
