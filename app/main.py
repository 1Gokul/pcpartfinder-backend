from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from dotenv import load_dotenv
from datetime import datetime
import json
import os

import data_manager

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

# Load environment variables from either a .env file(dev) or from the environment(production)
load_dotenv()

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
        search_results = await data_manager.search(search_query)

        return (
            {
                "n_results": sum(
                    [
                        len(value)
                        for result in search_results
                        for value in result.values()
                    ]
                ),
                "content": search_results,
            }
            if search_results
            else {"error": "No results found. Try another search string."}
        )
    else:
        return {
            "n_results": -1,
            "content": {"error": "No search string supplied."},
        }


@app.post("/crawl", tags=["crawler"])
async def crawl(request: Request):
    secret_key = None

    # Check if a request body exists and if there exists a value for the key "update_code"
    try:
        body = await request.json()
        secret_key = body["update_code"]

    # Return a "Bad Request" response if there is no update_code supplied.
    except (json.decoder.JSONDecodeError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No credentials supplied."
        )

    else:
        # If the update_code exists and it matches, start crawling and update the database.
        if secret_key == os.getenv("UPDATE_VERIFICATION_CODE"):
            data_manager.crawl_data()
            return {"success": f"Updating database... Time: {datetime.now()}"}

        # Else if it doesn't match, return a "Forbidden" response.
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect credentials supplied.",
            )
