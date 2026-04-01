from services.ai_service import analyze_code, parse_ai_response


def check_performance(code: str, filename: str) -> dict:
    prompt = """You are a performance optimization expert.

Analyze the provided code for:
- Inefficient nested loops
- Unnecessary repeated operations
- Memory leaks or excessive memory usage
- Slow database queries (N+1 problems)
- Better built-in alternatives available

Respond ONLY in this exact JSON format, nothing else:
{
    "issues": [
        {
            "severity": "high/medium/low",
            "problem": "clear description of the performance issue",
            "fix": "exact suggestion to improve performance"
        }
    ],
    "summary": "one line summary of performance issues found"
}

If no issues found, return empty issues array."""

    print(f"  Performance checker analyzing {filename}...")
    response = analyze_code(prompt, code)
    result = parse_ai_response(response)
    result["filename"] = filename
    result["agent"] = "Performance Checker"
    
    return result