# pcpartfinder-backend

Backend to pcpartfinder. Scrapes from:

- The IT Depot
- MD Computers
- Vedant Computers
- Prime ABGB

Built with FastAPI.

## Running the server yourself

- Clone the repo
- Create a virtual environment `python3 -m venv .venv`
- Activate it `source .venv/bin/activate`
- Install requirements `pip3 install -r requirements.txt`
- Enter the `app` folder
- Start the server `uvicorn main:app`