"""Routing helpers for reaching every model through OpenRouter.

OpenRouter fronts OpenAI, Anthropic and Google behind one OpenAI-compatible
Responses API, so a single client and a single protocol replace the three
native SDKs. Only two things differ from talking to OpenAI directly: model ids
are namespaced by provider, and the thinking level travels as the standard
``reasoning.effort`` field for every provider.
"""

from llm import Llm, model_base_name

# Keyed by the model name without its thinking/effort suffix. Verified against
# the OpenRouter catalogue; note that it spells the versions with dots and has
# no dated gpt-5.4 snapshot.
_SLUGS: dict[str, str] = {
    "gpt-5.4-mini": "openai/gpt-5.4-mini",
    "gpt-5.4-2026-03-05": "openai/gpt-5.4",
    "gpt-5.5": "openai/gpt-5.5",
    "gpt-5.6-sol": "openai/gpt-5.6-sol",
    "gpt-5.6-terra": "openai/gpt-5.6-terra",
    "claude-sonnet-4-6": "anthropic/claude-sonnet-4.6",
    "claude-opus-5": "anthropic/claude-opus-5",
    "claude-opus-4-8": "anthropic/claude-opus-4.8",
    "claude-fable-5": "anthropic/claude-fable-5",
    "gemini-3-flash-preview": "google/gemini-3-flash-preview",
    "gemini-3.1-pro-preview": "google/gemini-3.1-pro-preview",
    "gemini-3.5-flash": "google/gemini-3.5-flash",
    "gemini-3.6-flash": "google/gemini-3.6-flash",
}


def openrouter_slug(model: Llm) -> str:
    base = model_base_name(model)
    if base not in _SLUGS:
        raise ValueError(f"No OpenRouter model id for {model.value}")
    return _SLUGS[base]


def openrouter_reasoning_effort(model: Llm) -> str | None:
    """Read the effort out of the model label, e.g. "(medium effort)".

    The labels use "thinking" for OpenAI/Gemini and "effort" for Claude, and
    "no thinking" means the request should carry no reasoning field at all.
    """
    value = model.value
    if "(" not in value:
        return None
    effort = value.split("(", 1)[1].rstrip(")").split()[0]
    return None if effort == "no" else effort
