# How to Use GAIO with APIs and Open-Source Models

**GAIO v1.0 — Platform Setup Guide**
**Created by Tech Jacks Solutions**

---

## What This Guide Covers

This guide covers using GAIO configurations programmatically — through API calls, local model deployments, and automation workflows. This is the developer path.

---

## API Integration (Anthropic, OpenAI, Google)

The core pattern is the same across all providers: GAIO config goes in the system prompt parameter.

### Anthropic (Claude API)

```python
import anthropic

# Load your GAIO config from file
with open("gaio_config.txt", "r") as f:
    gaio_config = f.read()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    system=gaio_config,
    messages=[
        {"role": "user", "content": "Your question here"}
    ]
)

print(response.content[0].text)
```

### OpenAI (GPT API)

```python
from openai import OpenAI

with open("gaio_config.txt", "r") as f:
    gaio_config = f.read()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": gaio_config},
        {"role": "user", "content": "Your question here"}
    ]
)

print(response.choices[0].message.content)
```

### Google (Gemini API)

```python
import google.generativeai as genai

with open("gaio_config.txt", "r") as f:
    gaio_config = f.read()

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp",
    system_instruction=gaio_config
)

response = model.generate_content("Your question here")
print(response.text)
```

**Note:** Use a thinking/reasoning model variant for best GAIO compliance. Speed-optimized models may deprioritize system prompt instructions.

---

## Local / Open-Source Models

### Ollama

Create a Modelfile that includes your GAIO config as the system prompt:

```
FROM llama3.2

SYSTEM """
[Paste your entire GAIO configuration here]
"""

PARAMETER temperature 0.7
PARAMETER num_ctx 8192
```

Then build and run:

```bash
ollama create gaio-assistant -f Modelfile
ollama run gaio-assistant
```

Every conversation with this model instance will load the GAIO config automatically.

### LM Studio

1. Open LM Studio and load your model
2. Go to the **System Prompt** field in the chat interface
3. Paste your GAIO configuration
4. Save as a preset for reuse

### vLLM / Text Generation Inference

For server deployments, pass the GAIO config as the system message in your API calls. These servers expose OpenAI-compatible endpoints, so the OpenAI code example above works directly — just change the `base_url` to point to your local server.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="your-local-model",
    messages=[
        {"role": "system", "content": gaio_config},
        {"role": "user", "content": "Your question here"}
    ]
)
```

---

## Automation Patterns

### Config-as-File (Recommended)

Store GAIO configs as versioned text files, not hardcoded strings:

```
/configs/
  gaio_cybersecurity_secops_modeA.txt
  gaio_healthcare_clinical_modeA.txt
  gaio_general_modeB.txt
```

Load at runtime based on context:

```python
def get_gaio_config(domain, subdomain=None, mode="A"):
    filename = f"gaio_{domain}"
    if subdomain:
        filename += f"_{subdomain}"
    filename += f"_mode{mode}.txt"
    
    with open(f"configs/{filename}", "r") as f:
        return f.read()

# Usage
config = get_gaio_config("cybersecurity", "secops", "A")
```

Benefits: version-controlled, one-line updates propagate to all calls, different configs for different use cases without code changes.

### Multi-Model with Consistent Guardrails

If your application uses different models for different tasks, GAIO provides consistent behavioral rules across all of them:

```python
# Same GAIO config, different models for different tasks
gaio_config = get_gaio_config("financial", "banking", "A")

# Claude for analysis
analysis = anthropic_client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=gaio_config,
    messages=[{"role": "user", "content": analysis_prompt}]
)

# GPT-4o for summarization
summary = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": gaio_config},
        {"role": "user", "content": summary_prompt}
    ]
)
```

Both models operate under the same anti-fabrication rules, source authority requirements, and escalation triggers — even though they're different providers.

### Gateway / Proxy Integration

If you use an API gateway (LiteLLM, Portkey, Helicone, or a custom proxy), inject the GAIO config at the gateway level:

```python
# Pseudocode for gateway-level injection
def proxy_request(user_message, model, user_context):
    gaio_config = get_gaio_config_for_user(user_context)
    
    # Prepend GAIO config to every request
    messages = [
        {"role": "system", "content": gaio_config},
        {"role": "user", "content": user_message}
    ]
    
    return forward_to_provider(model, messages)
```

This is the enterprise pattern — users never see or manage the config, it's applied transparently based on their role or department.

---

## Config Management Best Practices

**Version your configs.** GAIO output includes a version stamp (e.g., `GAIO v1.0 | Generated 2026-02-13`). Store configs in version control alongside your application code.

**Don't modify configs by hand unless you know the framework.** The widget generates internally consistent configurations — changing one rule can create conflicts with others. If you need to customize, start from the widget output and make targeted edits following the canonical documentation.

**Test after every config change.** Use the Minimum Viable Test set (28 tests in Section 12) or at minimum, the four basic checks: factual question, out-of-scope question, fabrication request, uncertainty admission.

**Monitor compliance in production.** Log model responses alongside the GAIO config version that was active. If you detect fabrication or scope violations in production, you can trace whether the config was loaded, which model was used, and whether drift prevention triggered.

---

## Model Compatibility Notes

| Provider / Model | GAIO Compliance | Notes |
|-----------------|-----------------|-------|
| Claude Sonnet/Opus | Expected high | Strong system prompt adherence |
| GPT-4o | Expected high | Test with your specific config |
| Gemini Thinking Mode | Verified compliant | Must use thinking mode specifically |
| Gemini Fast Mode | Non-compliant | Bypasses system prompt rules |
| Llama 3.2 (local) | Untested | Open-source models vary widely |
| Mixtral (local) | Untested | Larger models likely better compliance |

Compliance varies by model capability. More capable models follow system prompt instructions more reliably. Speed-optimized or smaller models may deprioritize instruction following in favor of faster generation.

---

*GAIO v1.0 — Created and maintained by Tech Jacks Solutions*
*Standard licensed under CC-BY-SA 4.0 | Widget licensed under Apache 2.0*
