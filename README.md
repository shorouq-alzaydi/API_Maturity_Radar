# API Maturity Radar

**API Maturity Radar** is a lightweight tool that analyzes **OpenAPI/Swagger specification** against a set of **validation rules** and a **maturity model**.  
It produces a structured **JSON report** that summarizes API's current maturity level and identifies violations.

This tool uses the **Groq Llama-3.3-70B model** 

---

## Features

- Evaluates API maturity based on a defined model (e.g., Level 0–3)
- Checks compliance with validation rules
- Returns a structured JSON report
- Works with any OpenAPI 3.x YAML/JSON file
---

## Requirements

- Python **3.9+**
- A valid **Groq API key**

Install dependencies:
```bash
pip install groq httpx
```
Set Groq API key:
```bash
export GROQ_API_KEY="API_key"
```

## Usage

Run the tool with three input files:
```bash
python radar.py <RULES_FILE> <MODEL_FILE> <OPENAPI_FILE> 
```

## Example:
```bash
python radar.py rules.md maturity_model.md api.yaml > report.json
```
## Example Output

### Example Output

```json
{"Assessment Date": "2025-10-24", "Maturity Level": "Level 1", "Final Maturity Level": "Level 1: Resource-Oriented", "Analysis Summary": "The API achieves a maturity level of 1: Resource-Oriented because it represents distinct resources, uses nouns instead of verbs in URLs, and demonstrates basic use of HTTP methods. However, it lacks versioning in the base path, which is a requirement for Level 2. Additionally, while the API uses correct HTTP verbs and status codes, it does not fully comply with all validation rules, such as including a standardized error schema and versioning. Thus, it does not meet the criteria for higher maturity levels.", "Governance Compliance": {"Total Rules Checked": 5, "Total Violations Found": 2, "Violations List": [{"Rules Violated": "Rule 1.2: Versioning", "Reason & Location": "The base path does not include a version segment (e.g., /v1/)."}, {"Rules Violated": "Rule 1.5: Error Schema", "Reason & Location": "Error responses do not include the required schema with code, message, and timestamp."}]}}
