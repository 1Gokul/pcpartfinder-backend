from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from scraper import it_depot, md_computers, prime_abgb, vedant_computers

description = """
The PCPartFinder API scrapes and finds information about the availability of different PC components in India.

## Sources

- The IT Depot
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

# CORS settings
origins = [
    "https://pcpartfinder.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "PCPartFinder: Go to /docs for documentation."}


@app.get("/api/search/{search_query}", tags=["search"])
async def search(search_query: str):
    if search_query != "null":
        functions = [
            vedant_computers(search_query),
            md_computers(search_query),
            prime_abgb(search_query),
            it_depot(search_query),
        ]
        search_results = await asyncio.gather(*functions)

        return {
            "n_results": sum([len(item["results"]) for item in search_results]),
            "content": search_results,
        }
    else:
        return {
            "n_results": -1,
            "content": {"error": "No search string supplied."},
        }
