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
{
  "assessment_date": "2025-10-24",
  "determined_rmm_level": "Level 2",
  "final_maturity_level": "Standardized REST",
  "overall_analysis_summary": "The API follows REST principles and implements versioning, but lacks hypermedia features required for Level 3.",
  "governance_compliance": {
    "total_requirements_checked": 5,
    "total_violations_found": 1,
    "violations_list": [
      {
        "requirement_violated": "Rule 1.3: Error Schema",
        "reasoning_and_location": "Error responses do not include a standardized schema."
      }
    ]
  }
}
