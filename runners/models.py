"""Model registry for the benchmark runner.

Add new models here. Do not change existing entries after a run has
been committed — create a new entry with a new version string instead.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MODELS: dict[str, dict[str, Any]] = {
    "claude-haiku-4-5-20251001": {
        "provider": "anthropic",
        "params": {"temperature": 0.0, "max_tokens": 1024},
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "params": {"temperature": 0.0, "max_tokens": 1024},
    },
}

_BENCHMARK_SYSTEM_PROMPT = (
    "You are a legal research assistant. When asked about cases, statutes, "
    "or academic papers, provide accurate citations including full case names, "
    "reporters, page numbers, years, and URLs where available. "
    "If you are not confident about a citation, say so rather than guessing."
)


def call_model(model_id: str, prompt: str) -> str:
    """Call a model and return its raw text output.

    Raises ValueError for unknown model_id.
    Raises exceptions from the underlying SDK on API errors — callers
    should catch and log them.
    """
    spec = MODELS.get(model_id)
    if spec is None:
        raise ValueError(f"Unknown model: {model_id!r}. Add it to MODELS in models.py.")

    provider = spec["provider"]
    params = spec["params"]

    if provider == "anthropic":
        import anthropic
        import os
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model=model_id,
            system=[
                {
                    "type": "text",
                    "text": _BENCHMARK_SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": prompt}],
            **params,
        )
        return response.content[0].text

    elif provider == "openai":
        import openai
        import os
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": _BENCHMARK_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            **params,
        )
        return response.choices[0].message.content or ""

    else:
        raise ValueError(f"Unknown provider: {provider!r}")
