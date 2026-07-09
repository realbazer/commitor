from typing import Literal

from pydantic import BaseModel, Field


class CommitMessage(BaseModel):
    type: Literal['feat', 'fix', 'docs', 'style', 'refactor', 'chore'] = Field(
            description="The type of change according to Conventional Commits standard"
        )
    scope: str | None = Field(
        default=None,
        description="The module or component affected (e.g., auth, db, api). Leave None if global or unclear."
        )
    description: str = Field(
            description="A concise summary of changes. Present tense, max 60 chars, NO period at the end."
        )

    def to_string(self, use_emoji: bool = False) -> str:
            emojis = {
                'feat': '✨ ', 'fix': '🐛 ', 'docs': '📝 ',
                'style': '🎨 ', 'refactor': '♻️ ', 'chore': '🚀 '
            }
            prefix = emojis.get(self.type) if use_emoji else ''
            scope_str = f"({self.scope.lower()})" if self.scope else ""
            return f"{prefix}{self.type}{scope_str}: {self.description.lower().strip('.')}"

SYSTEM_PROMPT = "You are an expert Git assistant. Your ONLY task is to analyze the provided `git diff` and extract the structured information needed to fill out the CommitMessage schema. Be extremely precise."
