# E-Commerce Club Website

## Project Overview
University E-Commerce Club management platform with event registration, admin panel, and content management.

## Tech Stack
- **Frontend**: React, TailwindCSS
- **Backend**: FastAPI, PostgreSQL
- **Authentication**: JWT, bcrypt
- **Deployment**: Vercel (frontend), Railway (backend)
- **Third-party**: Cloudinary, Resend

## Team Members
- [Name] - Backend Lead
- [Name] - Frontend Lead
- [Name] - DevOps & Integration
- [Name] - Full-Stack Support

## Setup Instructions
 
| Task | More details | Is it Done |
|---|---|---|
| Coudinary | Added it to the existing 'package-lock.json' and 'package.json' files in the frontend folder | Done |
| Railway |  |  |

## Project Timeline
Target Completion: December 15, 2024

## Important Links
- [Project Requirements](./docs/requirements.md)
- [API Documentation] (Coming soon)



# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


## Authentication API

### Endpoints

**Public (No Authentication):**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

**Protected (Requires JWT Token):**
- `GET /api/auth/me` - Get current user profile
- `PUT /api/auth/me` - Update profile
- `POST /api/auth/change-password` - Change password
- `DELETE /api/auth/me` - Delete account

### Authentication Flow
1. Register: `POST /api/auth/register`
2. Login: `POST /api/auth/login` (receive JWT token)
3. Use token in header: `Authorization: Bearer <token>`
4. Token expires after 30 minutes

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

### Security Features
- Passwords hashed with bcrypt
- JWT tokens with 30-min expiration
- Account lockout after 5 failed login attempts (15 min)
- Password reset via email

## Event Management API

### Public Endpoints

**List Events**
```http
GET /api/events?page=1&page_size=10
```

**Get Event Details**
```http
GET /api/events/{event_id}
```

**Check Availability**
```http
GET /api/events/{event_id}/availability
```

### User Endpoints (Requires Authentication)

**Register for Event**
```http
POST /api/registrations/
Authorization: Bearer {token}

{
  "event_id": 1
}
```

**View My Registrations**
```http
GET /api/registrations/my-registrations
Authorization: Bearer {token}
```

**Cancel Registration**
```http
DELETE /api/registrations/{registration_id}
Authorization: Bearer {token}
```

### Admin Endpoints (Requires Admin Role)

**Create Event**
```http
POST /api/events/
Authorization: Bearer {admin_token}

{
  "title": "Workshop Title",
  "description": "Event description",
  "event_date": "2024-12-20T18:00:00",
  "event_time": "18:00",
  "location": "Main Hall",
  "capacity": 100,
  "registration_deadline": "2024-12-18T23:59:59"
}
```

**Update Event**
```http
PUT /api/events/{event_id}
Authorization: Bearer {admin_token}
```

**Delete Event**
```http
DELETE /api/events/{event_id}
Authorization: Bearer {admin_token}
```

**View Participants**
```http
GET /api/events/{event_id}/participants
Authorization: Bearer {admin_token}
```