import os
import sys
import json
from datetime import datetime
from groq import Groq
import httpx
MODEL = "llama-3.3-70b-versatile"
USAGE = "Usage: python radar.py <maturity_model_file> <rules_file.txt> <swagger_file>"

def die(msg, code=1):
    print(msg, file=sys.stderr, flush=True)
    sys.exit(code)

if len(sys.argv) != 4:
    die(f"{USAGE}")
print(sys.argv)

maturity_model_file, rules_file, swagger_file = sys.argv[1], sys.argv[2], sys.argv[3]

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    die("GROQ_API_KEY is missing")

client = Groq(api_key=api_key)

def read(path, label):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        die(f" {label} not found at '{path}'.")
    except Exception as e:
        die(f"Error reading {label} '{path}': {e}")

model_def = read(maturity_model_file, "maturity_model definition")
rules = read(rules_file, "Rules file")
swagger_content = read(swagger_file, "Swagger file")

combined_prompt = f"""
You are an **API Architecture and Governance Expert** acting as the evaluation engine of the **API Maturity Radar** .

Your mission is to analyze the provided **OpenAPI specification** in the context of:
1. The defined **Maturity Model** (levels, criteria)
2. The detailed ** Validation Rules**

and produce a structured JSON assessment report showing the determined maturity level and all rule violations.

--- MATURITY MODEL DEFINITION ---
{model_def}
--- END MODEL DEFINITION ---

--- VALIDATION RULES ---
{rules}
--- END VALIDATION RULES ---

--- SWAGGER / OPENAPI CONTENT ---
{swagger_content}
--- END SWAGGER CONTENT ---

**III. REQUIRED OUTPUT FORMAT**
Evaluate the given API’s maturity level according to the supplied rules and maturity model.

- First, assess compliance with each validation rule.
- Then, determine which maturity level the API achieves based on the model criteria.
- Finally, produce a clear analytical summary explaining how rule compliance and API design influenced the final maturity score.

{{
  "Assessment Date": "{datetime.now().strftime('%Y-%m-%d')}",
  "Maturity Level": "[ Level 0/1/2/3]",
  "Final Maturity Level": "[Final Assigned Level Name/Number from your Model]",
  "Analysis Summary": "A concise, single-paragraph summary explaining how the model level and the compliance audit resulted in the Final Maturity Level.",
  "Governance Compliance": {{
    "Total Rules Checked": 0,
    "Total Violations Found": 0,
    "Violations List": [
      {{
        "Rules Violated": "Requirement X.X: [Short Name]",
        "Reason & Location": "Specific path, schema, or property violating the rules."
      }}
    ]
  }}
}}
"""


try:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": combined_prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
        timeout=120,
    )

    content = resp.choices[0].message.content

    parsed = json.loads(content)
    print(content)
    print(json.dumps(parsed, ensure_ascii=False), flush=True)

except json.JSONDecodeError as e:
    die(f"Model returned non-JSON in JSON mode:\n{content}\n\n error: {e}")
except httpx.HTTPError as e:
    die(f"Network error: {e}")
except Exception as e:
    err_msg = getattr(e, "message", str(e))
    die(f" error occurred: {err_msg}")
