# BugSearch

A Stack Overflow–style Q&A platform for developers, built with Flask and
MySQL — a team project ("D-BUGGERS": Raja Kumar, Aastha Rajani, Disha
Shiraskar, Esha Patel) for an IIT Delhi web development course.

![BugSearch homepage](docs/screenshots/homepage.png)

## Features

- Post questions and answers, with comments on each
- Upvote/downvote questions and answers, bookmark either
- Tags on questions, and a per-user tag-based profile
- Follow/unfollow other users, reputation and badges (bronze/silver/gold)
- Full auth flow: signup, login, JWT-based password reset via email
- Profile pictures and image uploads
- Optional AI content moderation on posted comments, via the
  [EdenAI](https://www.edenai.co/) text moderation API

## Architecture

- **Backend**: Flask, with `Flask-Login` for sessions, `Flask-Mail` for
  password-reset emails, and `PyJWT` for the reset tokens themselves.
  `app.py` talks to MySQL directly via `mysql-connector-python` — no ORM.
- **Database**: MySQL, 13 tables (`schema.sql`) — `Users`, `Questions`,
  `Answers`, comments/votes/bookmarks for each, `Tags`, and a
  `Followertags` table for the follow graph.
- **Frontend**: server-rendered Jinja templates (`templates/`, 35+ pages)
  over a customized HTML/CSS/JS template, no frontend framework.

## Run it locally

Needs Python 3 and a local MySQL server.

```bash
git clone <this-repo-url>
cd bugsearch
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

mysql -u root -p < schema.sql          # creates the BugSearch database

cp .env.example .env                    # then fill in real values
python app.py                           # -> http://127.0.0.1:5000
```

`.env` needs at minimum `MYSQL_PASSWORD` and `SECRET_KEY`; email-related
features need real `MAIL_*` values, and `EDENAI_API_TOKEN` is optional
(comment moderation just does nothing without it). See `.env.example`
for the full list.

Note: `app.py` connects to MySQL at import time, so the database must
exist and the `.env` values must be correct before running it at all.

## Testing

`tests/` has pytest (`pytest_file.py`), `unittest`-based
(`unittest_file.py`), and Flask-test-client integration
(`integration_test.py`) tests covering the `User` model and the
signup/login/logout flow.

```bash
pytest tests/pytest_file.py
```

## A note on security

The original version of this project had real database, email, and
third-party API credentials hardcoded directly in the source (and in a
committed `.env` file). They've been moved to environment variables
(`.env`, gitignored, see `.env.example`) everywhere they appeared,
including in the archived earlier versions below — but **the old
credentials are still present in this repository's git history** and
should be treated as compromised; rotate them if they're still in use
anywhere.

## `docs/`

- `assignment-brief.pdf` — the original course assignment
- `presentation.pdf` — the team's project demo deck (the homepage
  screenshot above was cropped from this)
- `design/` — ER diagrams, design documentation, and the REST API
  contract (`original-rest-api-design.yaml`) originally planned for this
  project via a Swagger-generated server; the team ended up shipping the
  simpler direct-Flask-template architecture above instead

## `archive/`

Earlier iterations kept for reference:
- `app-earlier-version.py` — an earlier, less complete version of
  `app.py` (uses a non-default MySQL port and imports `fuzzywuzzy` for
  search, later dropped)
- `old-frontend/` and `responsive-frontend/` — earlier UI redesigns
  before the current `templates/`/`static/`
- `link_templates/` — page-flow sketches from early in the project
- `testnewapp-earlier-version.py` — an earlier version of the unit tests
