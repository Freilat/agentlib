# AgentLib

A lightweight framework for building LLM-powered agents with first-class tool support.

## Overview

AgentLib makes it easy to create AI agents that can:
- Maintain conversation context
- Use tools to perform actions
- Integrate with various LLM providers
- Handle multi-turn interactions

## Features

- **Simple Agent Creation**: Define agents with minimal boilerplate
- **Tool Registration System**: Add capabilities with simple decorators
- **LLM Integration**: Support for multiple providers (OpenAI, Google, X.AI, etc.)
- **Conversation Management**: Built-in handling of multi-turn interactions
- **Type Validation**: Automatic validation of tool inputs and outputs

## Installation

```bash
# Clone the repository
git clone https://github.com/jacobstoner/agentlib.git
cd agentlib

# Install in development mode
pip install -e .
```

## Quick Start

```python
from agentlib import BaseAgent

class SimpleAgent(BaseAgent):
    model = 'google/gemini-2.5-flash'
    system = "You are a helpful assistant."

    @BaseAgent.tool
    def get_data(self, query: str = "The search query"):
        """Retrieve information."""
        return f"Results for: {query}"

# Use the agent
agent = SimpleAgent()
response = agent.run("Find information about Python")
```

## Documentation

For detailed usage instructions, see the [tutorial](docs/agentlib.md).

For a complete example, check out the [Todo Agent](examples/todo_agent.py).

## Supported LLM Providers

AgentLib supports multiple LLM providers through API keys:

- OpenAI
- Google
- X.AI
- OpenRouter

### Setting Up API Keys

1. Copy the `.env.example` file to `.env`
2. Add your API keys to the `.env` file

```bash
cp .env.example .env
# Edit .env with your API keys
```


## License

Released under the MIT License. See the [LICENSE](LICENSE) file for details.
