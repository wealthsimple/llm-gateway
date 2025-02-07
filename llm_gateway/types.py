from typing import Any, Dict, TypeAlias

# Common response types
LLMResponse: TypeAlias = Dict[str, Any]
PromptMetadata: TypeAlias = Dict[str, Any]

# Provider-specific types
OpenAIResponse: TypeAlias = Dict[str, Any]
CohereResponse: TypeAlias = Dict[str, Any]
AWSBedrockResponse: TypeAlias = Dict[str, Any]

# Database record types
DBRecord: TypeAlias = Dict[str, Any]
