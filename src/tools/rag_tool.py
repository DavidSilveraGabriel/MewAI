from crewai.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import asyncio
from datetime import datetime

class RagToolInput(BaseModel):
    """Input schema for RAG operations"""
    action: str = Field(..., description="Action to perform: store/retrieve")
    content: Optional[str] = Field(None, description="Content to store")
    query: Optional[str] = Field(None, description="Query for retrieval")
    metadata: Optional[dict] = Field(None, description="Additional metadata")

class RagTool(BaseTool):
    name = "rag_database"
    description = "Tool for storing and retrieving information from the knowledge base"
    args_schema: Type[BaseModel] = RagToolInput

    def __init__(self):
        super().__init__()
        self.storage = SupabaseStorage()
        
    def _run(self, action: str, **kwargs) -> str:
        """Synchronous wrapper for async operations"""
        return asyncio.run(self._arun(action, **kwargs))
        
    async def _arun(self, action: str, **kwargs) -> str:
        if action == "store":
            if not kwargs.get("content"):
                raise ValueError("Content is required for store action")
                
            metadata = DocumentMetadata(
                source=kwargs.get("source", "unknown"),
                created_at=datetime.utcnow(),
                topic=kwargs.get("topic", "general"),
                tags=kwargs.get("tags", [])
            )
            
            document_id = await self.storage.store_document(
                content=kwargs["content"],
                metadata=metadata
            )
            return f"Information stored successfully with ID: {document_id}"
            
        elif action == "retrieve":
            if not kwargs.get("query"):
                raise ValueError("Query is required for retrieve action")
                
            # Aquí deberías generar el embedding para la query
            # Usando el modelo que prefieras (OpenAI, HuggingFace, etc.)
            embedding = self._generate_embedding(kwargs["query"])
            
            results = await self.storage.search_similar(
                query=kwargs["query"],
                embedding=embedding,
                limit=kwargs.get("limit", 5)
            )
            
            return self._format_results(results)
            
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using your preferred model
        """
        # Implementar la generación de embeddings
        # Por ejemplo, usando OpenAI o un modelo local
        pass
    
    def _format_results(self, results: List[dict]) -> str:
        """Format search results for output"""
        formatted = ["Search Results:"]
        for idx, result in enumerate(results, 1):
            formatted.append(f"\n{idx}. Content: {result['content'][:200]}...")
            formatted.append(f"   Similarity: {result['similarity']:.2f}")
        return "\n".join(formatted)