## Purpose

This repo contains a Django web app, a Node/MongoDB backend microservice, a small Flask sentiment microservice, and a React frontend. These instructions give a concise, actionable primer for an AI coding agent to be productive here: what the pieces are, where to change behavior, and the exact commands and files that are important.

## High-Level architecture 

- Django app: `server/djangoapp/` — hosts views/templates and server-side code. Key file: `restapis.py` (client utilities used by views to call backend services).
- Node/Mongo backend: `server/database/app.js` — Express + Mongoose REST API that serves dealerships and reviews (default port 3030).
- Sentiment microservice: `server/djangoapp/microservices/app.py` — Flask app using NLTK VADER; the Django client expects a sentiment endpoint (default configured in `restapis.py` as 5050).
- React frontend: `server/frontend/` — CRA-based app (dev on 3000, build in `server/frontend/build/`). Django templates in `server/djangoapp/templates/` are the server-rendered UI.

Data flow example:
- Browser → Django views / React → Django `restapis.py` → Node (3030) for dealers/reviews
- Review sentiment: `restapis.py` → sentiment service (expected at 5050) → returns JSON {"sentiment": "positive|neutral|negative"}

## Where to look when making changes

- Change REST client behavior: `server/djangoapp/restapis.py` (use this for consistent backend URLs and error handling).
- Add/inspect seed data: `server/djangoapp/populate.py` (call `initiate()` to seed CarMake/CarModel).
- Node API routes and data model: `server/database/app.js`, `server/database/dealership.js`, `server/database/review.js`.
- Sentiment logic: `server/djangoapp/microservices/app.py` (VADER logic). If sentiment results are unexpected, check VADER lexicon availability.
- Frontend dev/build: `server/frontend/` (use `npm start` for dev, `npm run build` to produce `build/`).

## Exact commands / developer workflows (PowerShell on Windows)

- Activate Django virtualenv and run server:
  cd server;
  .\djangoenv\Scripts\Activate.ps1
  python -m pip install -r requirements.txt
  python manage.py runserver

- Seed Django models (from `server` dir):
  python manage.py shell -c "from djangoapp.populate import initiate; initiate()"

- Run Node/Mongo backend (recommended: docker-compose in `server/database`):
  cd server\database;
  docker-compose up -d
  or locally (needs Mongo available and possible connection string tweak):
  npm install
  node app.js

- Run sentiment microservice (local):
  cd server\djangoapp\microservices
  python -m pip install -r requirements.txt
  ensure NLTK VADER lexicon is installed:
  python -c "import nltk; nltk.download('vader_lexicon')"
  run the app; the Django client expects port 5050 by default — run or map accordingly
  python app.py

- React frontend (dev):
  cd server\frontend
  npm install
  npm start

## Important project-specific notes & conventions

- `restapis.py` centralizes backend URLs and is used throughout Django views — prefer changing endpoint URLs there and use env variables.
- `restapis.py` loads env vars via `python-dotenv`; set `backend_url` and `sentiment_analyzer_url` there or via OS env.
- The Node service (`server/database/app.js`) expects a Mongo host named `mongo_db` (this matches the included docker-compose). If running services manually, update the MONGO connection string accordingly.
- `populate.py` uses Django ORM directly — run it via `manage.py shell` rather than importing from external processes.
- Sentiment analyzer: `restapis.py` defaults to `http://localhost:5050/` while `microservices/app.py` runs Flask default (5000). If you run locally without Docker, start the Flask app on port 5050 or change `restapis.py`.

## Quick API examples (useful when writing code/tests)

- Fetch all dealers: GET http://localhost:3030/fetchDealers (see `server/database/app.js`)
- Fetch dealer reviews: GET http://localhost:3030/fetchReviews/dealer/:id
- Insert review: POST http://localhost:3030/insert_review (expects JSON body)
- Sentiment: GET http://localhost:5050/analyze/<text> → returns JSON {"sentiment": "positive"}

## Tests / CI / missing pieces

- There are no automated tests or CI scripts in the repo. `server/package.json` has no useful scripts. Add tests in the most relevant component (Django tests under `server/djangoapp/tests.py`, Node tests under `server/database/tests`) if required.

## If you change service ports or endpoints

- Update `server/djangoapp/restapis.py` first so all Django views inherit the new settings.
- Update Docker mappings in `server/database/docker-compose.yml` if using Docker.

---
If anything here is unclear or you want me to add more detail (example env files, exact Docker commands for local development, or a checklist for setting up a fresh machine), tell me which area to expand and I'll iterate.
