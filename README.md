# Central Company Management System (CCMS)

## نظام الإدارة المركزية للشركات متعددة الفروع

نظام مركزي لإدارة الشركات والفروع والموظفين والمهام والتقارير بشكل آمن ومنظم.

## Features

- JWT Authentication
- Role-Based Authorization
- Company and Branch Management
- Employee Management
- Department Management
- Task Management
- Attendance Management
- Leave Requests
- Reports and CSV Export
- Notifications
- Audit Logs
- Central Dashboard
- Company Data Isolation
- UUID Public Identifiers

## Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT
- bcrypt

### Frontend
- React
- Vite
- Axios
- React Router
- Lucide Icons

## Security

The system provides authentication, authorization, password hashing, company isolation, branch access control, UUID identifiers, and audit logging.

## Project Goal

The goal of CCMS is to provide a secure centralized platform for managing companies and their branches remotely.

## System Architecture

```text
React Frontend
       |
       v
FastAPI REST API
       |
       v
Authentication & Authorization
       |
       v
Service Layer
       |
       v
SQLAlchemy ORM
       |
       v
PostgreSQL Database
Database
The system uses PostgreSQL with SQLAlchemy ORM and Alembic migrations.
Main entities:
Companies
Branches
Users
Departments
Employees
Tasks
Task History
Attendance
Leave Requests
Reports
Notifications
Audit Logs
API Design
The backend provides RESTful API endpoints for:
Authentication
Dashboard
Companies
Branches
Users
Employees
Departments
Tasks
Attendance
Leave Requests
Reports
Notifications
Audit Logs
Interactive API documentation is available through FastAPI Swagger UI.
Access Control
The system separates access according to user roles and company ownership.
Owners can manage company resources.
Employees have restricted access.
Users cannot access resources belonging to another company.
Protected endpoints require authentication.
UUID Security
Public resource identifiers use UUIDs to reduce predictable identifier enumeration.
Internal database relationships continue to use internal identifiers while API resources expose UUIDs where appropriate.
UUIDs are used together with authentication and authorization as an additional security measure.
Testing Results
The system has been tested for:
API availability
Authentication
Authorization
Owner access
Employee restrictions
Company isolation
Cross-company resource protection
UUID-based resource access
Audit logging
All major security tests completed successfully.
Future Development
Planned improvements include:
Advanced dashboard charts
Advanced search and filtering
Responsive mobile interface
Centralized export interface
Production deployment
Maps and branch locations
AI-powered analytics
Advanced monitoring and notifications
Project Status
Current Status: Active Development
The core backend, database, authentication, security, management modules, audit system, reports, and React frontend are implemented and tested.
