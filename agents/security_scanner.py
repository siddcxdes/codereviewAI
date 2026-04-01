from services.ai_service import analyze_code, parse_ai_response


def scan_security(code: str, filename: str) -> dict:
    prompt = """You are a cybersecurity expert specializing in code security.

Analyze the provided code for:
- Hardcoded passwords, API keys, or secrets
- SQL injection vulnerabilities
- XSS (Cross-site scripting) risks
- Insecure data handling
- Authentication/authorization issues

Respond ONLY in this exact JSON format, nothing else:
{
    "issues": [
        {
            "severity": "high/medium/low",
            "problem": "clear description of the vulnerability",
            "fix": "exact suggestion to fix it"
        }
    ],
    "summary": "one line summary of security issues found"
}

If no issues found, return empty issues array."""

    print(f"  Security scanner analyzing {filename}...")
    response = analyze_code(prompt, code)
    result = parse_ai_response(response)
    result["filename"] = filename
    result["agent"] = "Security Scanner"
    
    return result