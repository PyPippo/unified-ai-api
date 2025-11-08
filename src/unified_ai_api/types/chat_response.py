"""Custom chat response types that are provider-agnostic."""

from typing import Literal, TypeAlias
from pydantic import BaseModel, Field


MessageRole: TypeAlias = Literal['system', 'user', 'assistant']
"""Message roles for chat completion."""


class ChatMessage(BaseModel):
    """A single chat message."""

    role: MessageRole = Field(..., description='The role of the message sender.')
    content: str | None = Field(None, description='The content of the message.')
    name: str | None = Field(None, description='The name of the sender of the message.')
    # tool_calls: list[Any] | None = None
    # tool_call_id: str | None = None

    @classmethod
    def create_message(
        cls, role: MessageRole, content: str | None = None, name: str | None = None
    ) -> 'ChatMessage':
        """Create a ChatMessage object with the specified role and content."""
        
        return cls(role=role, content=content, name=name)


class ChatChoice(BaseModel):
    """A single choice in the chat completion response."""

    index: int
    message: ChatMessage
    finish_reason: str | None = None
    delta: ChatMessage | None = None


class ChatUsage(BaseModel):
    """Token usage information."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class ChatCompletionResponse(BaseModel):
    """
    Unified chat completion response that works with any provider.

    This type replaces OpenAI's ChatCompletion to avoid vendor lock-in
    and provides a consistent interface across different API providers.
    """

    id: str | None = None
    object: str | None = 'chat.completion'
    created: int | None = None
    model: str | None = None
    choices: list[ChatChoice] | None = None
    usage: ChatUsage | None = None
    system_fingerprint: str | None = None

    @classmethod
    def create_response(
        cls,
        id: str | None = None,
        object: str | None = 'chat.completion',
        created: int | None = None,
        model: str | None = None,
        choices: list[ChatChoice] | None = None,
        usage: ChatUsage | None = None,
        system_fingerprint: str | None = None
    ) -> 'ChatCompletionResponse':
        """Create a ChatCompletionResponse object."""

        return cls(
            id=id, object=object, created=created, model=model, 
            choices=choices, usage=usage, system_fingerprint=system_fingerprint
            )

  
    def get_content(self) -> str | None:
        """Get the content of the first choice, if available."""

        if self.choices and len(self.choices) > 0:
            return self.choices[0].message.content
        return None

    def get_role(self) -> MessageRole | None:
        """Get the role of the first choice, if available."""

        if self.choices and len(self.choices) > 0:
            return self.choices[0].message.role
        return None
