# Card-to-Sheba Inquiry Service

A Django REST backend service that accepts a bank card number, validates it,
converts it to its IBAN (Sheba) number through an external provider, and stores
every attempt for auditing. The result is exposed through a versioned REST API.

## Project Overview

This service receives a bank card number from a client and returns the matching
IBAN (Sheba). Before contacting any external service, the card number is
validated locally. Each request — successful or failed — is persisted as an
auditable record with its status, timing, and outcome. Sensitive data is never
stored or logged in full: card numbers are masked and fingerprinted.

The project focuses on backend engineering: a clean layered architecture,
predictable error handling, security of sensitive data, and testability.

## Architecture

The application is organized into clearly separated layers, each with a single
responsibility. A request flows through them top to bottom:

```
API / View        -> HTTP concerns: parse request, basic validation, build response
   |
Service           -> business logic: orchestrates the whole inquiry flow
   |
External Client   -> all communication with the external card-to-Sheba provider
   |
Repository        -> all database reads and writes
   |
PostgreSQL        -> persistent storage
```

- **API / View** — receives the HTTP request, performs request-level validation,
  calls the service, and formats the response. Contains no business logic.
- **Service** — the core of the system. It validates the card, creates the
  inquiry record, calls the external client, processes the result, persists the
  audit data, and returns the outcome.
- **External Client** — isolates all details of talking to the external provider
  (URL, headers, timeout). The service does not know about HTTP.
- **Repository** — isolates database access, so persistence logic can change or
  be tested without touching business logic.

This separation keeps each layer independently testable and gives every part a
single reason to change.

## Requirements

- Python 3.12+
- PostgreSQL 14+
- Git

## Installation

1. Clone the repository and enter the project folder:

```
git clone <repository-url>
cd Main_Django
```

2. Create and activate a virtual environment:

```
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and fill in your own values.

5. Create the PostgreSQL database (matching your `DATABASE_URL`):

```
createdb sheba_db
```

6. Apply the database migrations (see the Database section).

## Environment Variables

Configuration is provided through a `.env` file (never committed to Git).
A template is available in `.env.example`.

| Variable       | Description                                        |
|----------------|----------------------------------------------------|
| `SECRET_KEY`   | Django secret key used for cryptographic signing.  |
| `DEBUG`        | `True` for local development, `False` in production.|
| `DATABASE_URL` | PostgreSQL connection string, e.g. `postgres://user:password@localhost:5432/sheba_db`. |

## Database

The project uses PostgreSQL and Django's migration system. After configuring
`DATABASE_URL`, create all tables by running:

```
python manage.py migrate
```

The project can be set up from an empty database using only the committed
migrations — no manual schema changes are required.

## Running

Start the development server:

```
python manage.py runserver
```

## API Documentation

_To be completed once the API endpoints are implemented._

## Testing

_To be completed once the test suite is implemented._

## Architecture Decisions

- **Layered architecture** — responsibilities are split across API, service,
  external client, and repository layers so each is testable and has a single
  reason to change.
- **UUID primary key** — inquiries are identified by a non-sequential UUID to
  prevent enumeration of other users' requests.
- **Sensitive data handling** — the full card number is never stored or logged.
  Only a masked form and a one-way fingerprint are kept.
- **Configuration via environment** — secrets and environment-specific settings
  are read from a `.env` file using `django-environ`, never hard-coded.
- **PostgreSQL** — chosen for concurrency, data integrity, and production
  suitability.
- **Framework-independent validation** — card validation is a pure function that
  raises a domain exception, so it can be reused and tested without Django.

## Assumptions

- The external card-to-Sheba provider is accessed through an isolated client.
  Because real provider credentials are not available, the client is designed
  against a realistic contract and backed by a fake/mock implementation for
  development and testing.

## Known Limitations

_To be completed._