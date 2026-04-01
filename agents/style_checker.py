from services.ai_service import analyze_code, parse_ai_response


def check_style(code: str, filename: str) -> dict:
    """
    Analyzes code for style and readability issues.
    """
    
    prompt = """You are a code quality expert focused on clean code principles.

Analyze the provided code for:
- Non-descriptive variable or function names
- Missing error handling
- Functions that are too long or do too many things
- Missing comments on complex logic
- Code that could be simplified

Respond ONLY in this exact JSON format, nothing else:
{
    "issues": [
        {
            "severity": "high/medium/low",
            "problem": "clear description of the style issue",
            "fix": "exact suggestion to improve it"
        }
    ],
    "summary": "one line summary of style issues found"
}

If no issues found, return empty issues array."""

    print(f" Style checker analyzing {filename}...")
    response = analyze_code(prompt, code)
    result = parse_ai_response(response)
    result["filename"] = filename
    result["agent"] = "Style Checker"
    
    return result