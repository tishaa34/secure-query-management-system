# Secure Query Management System

Production-grade Python backend for Jira-style query management with workflow enforcement, RBAC, and audit logging.

## Stack

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- JWT mock authentication

## Why Python Instead Of Prisma

The original requirements mentioned NestJS and Prisma, but the final requirement was "everything in python". This implementation keeps the same data model and workflow constraints, but translates the persistence layer into Python-native SQLAlchemy models instead of Prisma.

## Project Structure

```text
app/
  api/
    dependencies.py
    router.py
  core/
    config.py
    enums.py
    exceptions.py
    security.py
  db/
    base.py
    session.py
  modules/
    auth/
      router.py
      schemas.py
      service.py
    users/
      models.py
      repository.py
      schemas.py
      service.py
    queries/
      models.py
      repository.py
      router.py
      schemas.py
      service.py
      workflow.py
    audit/
      models.py
      repository.py
      router.py
      schemas.py
      service.py
  main.py
scripts/
  seed.py
```

## Domain Model

### User

- `id`
- `name`
- `role`
- `created_at`

### Query

- `id`
- `title`
- `description`
- `status`
- `priority`
- `created_by_id`
- `assigned_to_id`
- `created_at`
- `updated_at`

### AuditLog

- `id`
- `query_id`
- `action`
- `performed_by_id`
- `timestamp`

## Workflow Rules

Allowed transitions:

- `NEW -> ASSIGNED`
- `ASSIGNED -> IN_PROGRESS`
- `IN_PROGRESS -> ON_HOLD`
- `IN_PROGRESS -> RESOLVED`
- `ON_HOLD -> IN_PROGRESS`

Special rule:

- assignment of a `NEW` query automatically moves it to `ASSIGNED`

## RBAC Rules

- `USER`: create queries and view only their own queries
- `RESOLVER`: view and update only queries assigned to them
- `ADMIN`: full access including assignment

## API Endpoints

### Auth

- `POST /auth/login`

Request:

```json
{
  "name": "admin"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user_id": 1,
  "role": "ADMIN"
}
```

### Create Query

- `POST /queries`

Request:

```json
{
  "title": "VPN access is failing",
  "description": "Unable to connect since 9 AM",
  "priority": "HIGH"
}
```

Response:

```json
{
  "id": 1,
  "title": "VPN access is failing",
  "description": "Unable to connect since 9 AM",
  "status": "NEW",
  "priority": "HIGH",
  "created_by": {
    "id": 4,
    "name": "reporter1",
    "role": "USER",
    "created_at": "2026-03-29T17:00:00Z"
  },
  "assigned_to": null,
  "created_at": "2026-03-29T17:01:00Z",
  "updated_at": "2026-03-29T17:01:00Z"
}
```

### List Queries

- `GET /queries`

Optional filters:

- `status`
- `priority`

Visibility is role-aware:

- admin gets all queries
- resolver gets assigned queries only
- user gets self-created queries only

### Assign Query

- `PATCH /queries/{id}/assign`

Request:

```json
{
  "assigned_to_id": 2
}
```

Response:

```json
{
  "id": 1,
  "status": "ASSIGNED",
  "assigned_to": {
    "id": 2,
    "name": "resolver1",
    "role": "RESOLVER",
    "created_at": "2026-03-29T17:00:00Z"
  }
}
```

### Update Status

- `PATCH /queries/{id}/status`

Request:

```json
{
  "status": "IN_PROGRESS"
}
```

Response:

```json
{
  "id": 1,
  "status": "IN_PROGRESS"
}
```

### Get Audit Trail

- `GET /queries/{id}/audit`

Response:

```json
[
  {
    "id": 1,
    "query_id": 1,
    "action": "CREATED",
    "performed_by": {
      "id": 4,
      "name": "reporter1",
      "role": "USER",
      "created_at": "2026-03-29T17:00:00Z"
    },
    "timestamp": "2026-03-29T17:01:00Z"
  },
  {
    "id": 2,
    "query_id": 1,
    "action": "ASSIGNED",
    "performed_by": {
      "id": 1,
      "name": "admin",
      "role": "ADMIN",
      "created_at": "2026-03-29T17:00:00Z"
    },
    "timestamp": "2026-03-29T17:02:00Z"
  }
]
```

## Local Setup

1. Create a PostgreSQL database.
2. Copy `.env.example` to `.env` and adjust values.
3. Install dependencies:

```bash
pip install -e .
```

4. Seed mock users:

```bash
python scripts/seed.py
```

5. Run the server:

```bash
uvicorn app.main:app --reload
```

## Seeded Users

- `admin`
- `resolver1`
- `resolver2`
- `reporter1`
- `reporter2`

## Notes

- Authentication is intentionally lightweight for interview/demo use.
- Audit entries are recorded on query creation, assignment, and status changes.
- Workflow rules are enforced in the service layer, not in controllers.
