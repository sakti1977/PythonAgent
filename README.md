# PythonAgent

An AI-powered Python code generation agent built with Claude (Anthropic's AI). This tool allows you to generate Python code by simply describing what you want in natural language.

## Features

- 🤖 **AI-Powered Code Generation**: Uses Claude (Haiku/Sonnet models) to generate Python code from natural language requirements
- 💬 **Interactive Mode**: Have back-and-forth conversations to refine generated code
- 💰 **Cost Tracking**: Monitor API usage and costs for each generation
- 🔄 **Retry Logic**: Robust error handling with automatic retries for API issues
- 📁 **Auto-Save**: Automatically saves generated code to output directory
- 🎯 **Command-Line Interface**: Easy-to-use CLI for quick code generation

## Requirements

- Python 3.x
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sakti1977/PythonAgent.git
cd PythonAgent
```

2. Install dependencies:
```bash
pip install anthropic python-dotenv
```

3. Set up your environment variables:
   - Copy the `.env.example` file to create your own `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your-api-key-here` with your actual Anthropic API key:
     ```
     ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
     ```
   - **Important**: The `.env` file is gitignored and will not be committed to version control. Never commit API keys to git!

## Usage

### Basic Usage (CLI)

Generate code by providing a requirement as a command-line argument:

```bash
python agent.py "Create a function to calculate factorial of a number"
```

Specify a custom output filename:

```bash
python agent.py "Create a REST API client class" --filename api_client.py
```

### Default Example

Run without arguments to see the default example:

```bash
python agent.py
```

This will generate a function called `analyze_data` that calculates statistical metrics (mean, median, min, max, count) from a list of numbers.

### Interactive Conversation Mode

For iterative refinement, use the interactive conversation mode:

```python
from agent import run_agent_conversation

run_agent_conversation()
```

Type your requirements, and the agent will respond with code. Type 'quit' to exit.

### Track Generation Costs

To monitor API usage costs:

```python
from agent import generate_code_with_cost

code = generate_code_with_cost("Create a binary search function")
```

## Configuration

The agent supports two Claude models:

- **Fast Model** (default): `claude-haiku-4-5-20251001` - Faster, more cost-effective
- **Strong Model**: `claude-sonnet-4-5-20250929` - More capable for complex tasks

You can configure which model to use in the `generate_code()` function:

```python
from agent import generate_code

# Use fast model (default)
code = generate_code("Your requirement", use_fast_model=True)

# Use strong model
code = generate_code("Your complex requirement", use_fast_model=False)
```

## Example Output

Input requirement:
```
Create a function called 'analyze_data' that:
- Takes a list of numbers as input
- Returns a dictionary with: mean, median, min, max, and count
- Handles empty lists gracefully
```

Generated code will be saved to `output/analyze_data.py` with:
- Clean, well-commented Python code
- Error handling
- Docstrings explaining functionality
- Example usage

## Project Structure

```
PythonAgent/
├── agent.py           # Main agent code
├── output/            # Generated code output directory
├── .env              # API key configuration (create from .env.example, gitignored)
├── .env.example      # Template for environment variables
├── .gitignore        # Git ignore file (includes .env)
└── README.md         # This file
```

## Features in Detail

### Code Generation
- Generates clean, production-ready Python code
- Includes comprehensive docstrings
- Implements proper error handling
- Follows Python best practices

### Retry Logic
- Automatically retries on API overload (529 errors)
- Exponential backoff strategy (2, 4, 8, 16, 32 seconds)
- Handles connection errors gracefully

### Cost Tracking
- Tracks input and output token usage
- Calculates costs based on Haiku pricing ($0.25/M input, $1.25/M output)
- Displays cost information for each generation

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Security

**Important Security Notes:**

- **Never commit your `.env` file** to version control. It contains sensitive API keys.
- The `.env` file is included in `.gitignore` to prevent accidental commits.
- Always use `.env.example` as a template and create your own `.env` file locally.
- If you accidentally committed your API key, you should:
  1. Immediately revoke the exposed API key from your Anthropic account
  2. Generate a new API key
  3. Update your local `.env` file with the new key
  4. Remove the key from git history (consider using `git filter-branch` or tools like BFG Repo-Cleaner)

## License

This project is open source and available under the MIT License.

## Author

Created by sakti1977

## Support

For issues or questions, please open an issue on the GitHub repository.
