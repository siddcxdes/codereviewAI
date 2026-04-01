from services.ai_service import analyze_code, parse_ai_response


def detect_bugs(code: str, filename: str) -> dict:
    prompt = """You are an expert software engineer specializing in bug detection.
    
Analyze the provided code for:
- Null pointer / None reference errors
- Division by zero risks
- Logic errors and wrong conditions
- Unhandled edge cases
- Infinite loops

Respond ONLY in this exact JSON format, nothing else:
{
    "issues": [
        {
            "severity": "high/medium/low",
            "problem": "clear description of the bug",
            "fix": "exact suggestion to fix it"
        }
    ],
    "summary": "one line summary of bugs found"
}

If no bugs found, return empty issues array."""

    print(f"Bug detector analyzing {filename}...")
    response = analyze_code(prompt, code)

    result = parse_ai_response(response)

    result["filename"] = filename
    result["agent"] = "Bug Detector"
    
    return result