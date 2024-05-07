from pydantic import BaseModel, Field, computed_field
from typing import Dict


class APIResponse(BaseModel):
    response_text: str = Field(
        ..., description="The generated text response from the LLM"
    )
    metadata: Dict[str, Dict] = Field(
        ..., description="Metadata for the sources for the response"
    )

    @computed_field
    @property
    def sources(self) -> str:
        """
        Returns a string representation of the set of volumes extracted from the metadata dictionary.

        :return: A text representation of the set of volumes
        :rtype: str
        """
        return " ".join(set(metadata["volume"] for metadata in self.metadata.values()))
