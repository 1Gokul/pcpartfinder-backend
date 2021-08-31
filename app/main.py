from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
import asyncio

from scraper.components import md_computers, prime_abgb, vedant_computers

description = """
The PCPartFinder API scrapes and finds information about the availability of different PC components in India.

## Sources

- RP Tech
- MD Computers
- Vedant Computers
- Prime ABGB
"""

tags_metadata = [{
    "name": "search",
    "description": "Search and scrape information from the sources."
}]

app = FastAPI(
    title="PCPartFinder",
    description=description,
    version="0.0.1",
    contact={
        "name": "Gokul Viswanath",
        "url": "https://gokulv.netlify.app",
        "email": "viswanath1gokul@gmail.com",
    },
    openapi_tags=tags_metadata,
    license_info={
        "name": "GNU GPL 3.0",
        "url": "https://github.com/1Gokul/pcpartfinder-backend/blob/main/LICENSE"
    }
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/api/search/{search_query}", tags=["search"])
async def search(search_query: str):
    if not search_query:
        raise HTTPException(status_code=400, detail="Search query not provided.")
    else:
        functions = [vedant_computers(search_query), md_computers(search_query), prime_abgb(search_query)]
        search_results = await asyncio.gather(*functions)
        return search_results