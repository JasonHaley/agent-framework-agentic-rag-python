"""
Configuration module for Azure AI Search and OpenAI settings.
"""
import os
from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

@dataclass
class AzureConfig:
    """Configuration for Azure services."""
    
    # Azure AI Search
    search_endpoint: str
    search_api_key: str
    search_index_name: str
    
    # Azure OpenAI
    openai_endpoint: str
    openai_api_version: str
    openai_api_key: str
    chat_model: str
    embedding_model: str
    
    # Credentials
    search_credential: AzureKeyCredential
    
    @classmethod
    def from_env(cls) -> "AzureConfig":
        """Load configuration from environment variables."""
        return cls(
            search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
            search_api_key=os.getenv("AZURE_SEARCH_API_KEY", ""),
            search_index_name=os.getenv("AZURE_SEARCH_INDEX_NAME", ""),
            openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            chat_model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", ""),
            embedding_model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", ""),
            search_credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY", ""))
        )
    
    def validate(self) -> None:
        """Validate that all required configuration is present."""
        if not self.search_endpoint:
            raise ValueError("AZURE_SEARCH_ENDPOINT environment variable is required")
        if not self.search_api_key:
            raise ValueError("AZURE_SEARCH_API_KEY environment variable is required")
        if not self.search_index_name:
            raise ValueError("AZURE_SEARCH_INDEX_NAME environment variable is required")
        if not self.embedding_model:
            raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variable is required")
        if not self.chat_model:
            raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable is required")
        if not self.openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
