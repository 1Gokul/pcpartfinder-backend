from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
import asyncio

from scraper.components import md_computers, prime_abgb, rp_tech, vedant_computers

description = """
The PCPartFinder API scrapes and finds information about the availability of different PC components in India.

## Sources

- RP Tech
- MD Computers
- Vedant Computers
- Prime ABGB
"""

tags_metadata = [
    {"name": "search", "description": "Search and scrape information from the sources."}
]

app = FastAPI(
    title="PCPartFinder",
    description=description,
    version="0.0.1",
    contact={
        "name": "Gokul Viswanath",
        "url": "https://gokulv.netlify.app",
        "email": "viswanath1gokul@gmail.com",
    },
    swagger_favicon_url="https://placekitten.com/200/300",
    openapi_tags=tags_metadata,
    license_info={
        "name": "GNU GPL 3.0",
        "url": "https://github.com/1Gokul/pcpartfinder-backend/blob/main/LICENSE",
    },
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/api/search/{search_query}", tags=["search"])
async def search(search_query: str):
    functions = [
        vedant_computers(search_query),
        md_computers(search_query),
        prime_abgb(search_query),
        rp_tech(search_query),
    ]
    search_results = await asyncio.gather(*functions)

    # search_results is a list of lists. The code below flattens it out.
    return [result for sublist in search_results for result in sublist]
