from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from googlesearch import search
from bs4 import BeautifulSoup
import requests


class WebScraperInput(BaseModel):
    """Input schema for WebScraperTool."""
    query: str = Field(..., description="The search query to use for web scraping.")
    num_results: int = Field(5, description="Number of search results to consider.")

class WebScraperTool(BaseTool):
    name: str = "Web Scraper Tool"
    description: str = (
        "Useful for scraping web pages and extracting relevant information based on a search query."
    )
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, query: str, num_results: int) -> str:
        results = search(query, num_results=num_results)
        scraped_data = []
        for url in results:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes

                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text(separator=' ', strip=True)
                scraped_data.append(f"URL: {url} \nContent: {text_content}")
            except requests.exceptions.RequestException as e:
                scraped_data.append(f"Error scraping {url}: {e}")
        
        return "\n\n".join(scraped_data)