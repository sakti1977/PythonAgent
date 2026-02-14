import anthropic
import os
import time
import re
import argparse
from dotenv import load_dotenv
from anthropic.types import MessageParam

load_dotenv()

# Centralized Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FAST_MODEL = "claude-haiku-4-5-20251001"
STRONG_MODEL = "claude-sonnet-4-5-20250929"

# Initialize Client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def create_coding_agent():
    return """You are an expert Python developer.

When given a requirement, you will:
1. Write clean, well-commented Python code
2. Include error handling
3. Add a brief docstring explaining what the code does
4. Return ONLY the code block, nothing else

Always wrap your code in ```python ... ``` markers."""


def _make_api_call(messages: list[MessageParam], model: str, max_tokens: int = 1024) -> str:
    """Unified API call method with retry logic."""
    max_retries = 5
    retry_delays = [2, 4, 8, 16, 32]

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=create_coding_agent(),
                messages=messages
            )
            return response

        except anthropic.APIStatusError as e:
            if e.status_code == 529:
                wait_time = retry_delays[attempt]
                print(f"⚠️  Server overloaded. Attempt {attempt + 1}/{max_retries}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except anthropic.APIConnectionError:
            wait_time = retry_delays[attempt]
            print(f"⚠️  Connection error. Attempt {attempt + 1}/{max_retries}. Retrying in {wait_time}s...")
            time.sleep(wait_time)

    raise Exception("❌ Max retries reached. Anthropic API is still overloaded.")


def generate_code(requirement: str, use_fast_model: bool = True) -> str:
    model = FAST_MODEL if use_fast_model else STRONG_MODEL

    print(f"\n🤖 Agent thinking with {model}...")
    print(f"📋 Requirement: {requirement}\n")

    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": f"Write Python code for this requirement:\n\n{requirement}"
        }
    ]

    response = _make_api_call(messages, model)
    return response.content[0].text


def extract_code(response: str) -> str:
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response.strip()


def save_code(code: str, filename: str = "generated_code.py"):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"
    with open(filepath, "w") as f:
        f.write(code)
    print(f"✅ Code saved to: {filepath}")
    return filepath


def run_agent(requirement: str, save: bool = True, filename: str = "generated_code.py"):
    raw_response = generate_code(requirement)
    clean_code = extract_code(raw_response)

    print("=" * 50)
    print("📝 GENERATED CODE:")
    print("=" * 50)
    print(clean_code)
    print("=" * 50)

    if save:
        save_code(clean_code, filename)

    return clean_code


def run_agent_conversation():
    """Have a back-and-forth conversation to refine code."""
    messages = []

    print("🤖 Coding Agent Ready! Type 'quit' to exit.\n")

    while True:
        requirement = input("You: ").strip()
        if requirement.lower() == 'quit':
            break

        messages.append({"role": "user", "content": requirement})

        response = _make_api_call(messages, FAST_MODEL)
        agent_reply = response.content[0].text
        messages.append({"role": "assistant", "content": agent_reply})

        print(f"\nAgent:\n{extract_code(agent_reply)}\n")


def generate_code_with_cost(requirement: str):
    """Track how much each generation costs."""
    messages = [{"role": "user", "content": requirement}]
    response = _make_api_call(messages, FAST_MODEL)

    # Haiku pricing: $0.25/M input, $1.25/M output tokens
    input_cost = (response.usage.input_tokens / 1_000_000) * 0.25
    output_cost = (response.usage.output_tokens / 1_000_000) * 1.25
    total_cost = input_cost + output_cost

    print(f"💰 Cost: ${total_cost:.6f} | Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")

    return response.content[0].text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Coding Agent")
    parser.add_argument("prompt", type=str, nargs="?", help="The coding requirement/prompt")
    parser.add_argument("--filename", type=str, default="generated_code.py", help="Output filename")
    
    args = parser.parse_args()

    if args.prompt:
        run_agent(args.prompt, filename=args.filename)
    else:
        # Fallback to default if no prompt provided via CLI
        my_requirement = """
        Create a function called 'analyze_data' that:
        - Takes a list of numbers as input
        - Returns a dictionary with: mean, median, min, max, and count
        - Handles empty lists gracefully
        """
        run_agent(my_requirement, filename="analyze_data.py")
