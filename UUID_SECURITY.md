# UUID Security Strategy

## Overview

The Central Company Management System uses UUID values as public identifiers for API resources.

The goal is to reduce predictable resource enumeration and avoid exposing sequential database identifiers through the public API.

## Current Strategy

UUIDs are implemented as additional unique public identifiers.

The existing integer primary keys and internal foreign keys are preserved to maintain database stability and avoid unnecessary migration risks.

## API Usage

The main API resources expose UUID identifiers for individual resource retrieval and update operations.

Examples include:

- Companies
- Branches
- Departments
- Employees
- Tasks
- Attendance
- Leave Requests
- Reports
- Notifications
- Audit Logs

## Security Benefit

Sequential identifiers such as:

`/companies/1`

can make resource enumeration easier.

UUID-based identifiers such as:

`/companies/dae88118-8b70-451f-b2aa-efbe8746138a`

are significantly less predictable.

UUIDs are therefore used as public resource identifiers while database relationships continue using internal primary keys.

## Important Note

UUIDs are not a replacement for authentication or authorization.

The system still requires:

- Authentication
- Role-based authorization
- Company isolation
- Branch access control
- Secure password hashing
- JWT authentication
- Audit logging

## Future Migration

If the system later requires UUIDs to become the actual database primary keys, this should be implemented as a separate planned migration.

The migration must preserve existing relationships, foreign keys, indexes, and application behavior.

