from fastapi import FastAPI

description = """
The PCPartFinder API scrapes and finds information about the availability of different PC components in India.

## Information Sources

- The IT Depot
- MD Computers
- Vedant Computers
- Prime ABGB
- Amazon India
"""

app = FastAPI(
    title="PCPartFinder",
    description=description,
    version="0.0.1",
    contact={
        "name": "Gokul Viswanath",
        "url": "https://gokulv.netlify.app",
        "email": "viswanath1gokul@gmail.com",
    },
    license_info={
        "name": "GNU GPL 3.0",
        "url": "https://github.com/1Gokul/pcpartfinder-backend/blob/main/LICENSE"
    }
)


@app.get("/")
async def root():
    return {"message": "PCPartFinder - Go to /docs for more information."}
