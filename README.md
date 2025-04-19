# Monday.com Clone

A full-featured project management platform clone built with Django and Next.js, implementing core Monday.com functionalities.

## Tech Stack

### Backend
- Django 4.2.20
- Django REST Framework
- Channels for real-time updates
- PostgreSQL database
- JWT Authentication
- `/api/users/` endpoint for user info lookup (enables assignee name/email display)

### Frontend
- Next.js 14
- TypeScript
- TailwindCSS
- shadcn/ui components
- Zustand for state management
- Real-time updates (coming soon)

## Features

- [x] Custom User Model with email authentication
- [x] Team Management
- [x] Project (Board) creation from the dashboard UI
- [x] Group creation from the task modal UI
- [x] Tasks can be associated with any project and group
- [x] Projects link in the sidebar for quick access
- [x] Assignee field now displays user name or email (not just ID!) in task modal
- [x] `/api/users/` endpoint for user info
- [x] Client-side authentication with:
  - Protected routes and API endpoints
  - Persistent sessions using cookies
  - Smooth SPA navigation
  - Loading skeletons for better UX
- [ ] Workspaces
- [ ] Boards with multiple views (Table, Kanban, Calendar)
- [ ] Real-time collaboration
- [ ] Automations
- [ ] File attachments
- [ ] Activity tracking
- [ ] Notifications

## Project Structure

```
monday/
├── backend/              # Django backend
│   ├── accounts/         # User and Team management
│   ├── boards/           # Board and item management
│   ├── workspace/        # Workspace organization
│   ├── core/            # Shared functionality
│   └── monday_clone/    # Project settings
└── frontend/            # Next.js frontend
    ├── app/             # Next.js app directory
    ├── components/      # React components
    │   ├── auth/        # Authentication components
    │   ├── layout/      # Layout components
    │   └── ui/          # UI components
    ├── lib/             # Utilities and store
    └── types/           # TypeScript types
```

## Production Readiness

- **All debug panels, logs, and sensitive authentication state displays have been removed from the frontend.**
- The dashboard and all user-facing pages are now production-ready and do not leak sensitive information.
- If you still see debug info, try a hard refresh (Ctrl+Shift+R) or clear your browser cache.

## Recent Changes

- Added ability to create Projects (Boards) from the dashboard UI
- Added ability to create Groups within a project from the task creation modal
- Added a "Projects" link in the sidebar for easier navigation
- Improved task creation flow: tasks must be associated with a project and group

## Getting Started

### Version Control

This project uses git for version control. To get started:

```bash
git init
git add .
git commit -m "Initial commit"
```

For ongoing work:
```bash
git add .
git commit -m "Describe your changes"
git push
```

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

Access the admin interface at: http://localhost:8000/admin

### Frontend Setup

1. Install dependencies:
```bash
pnpm install
```

2. Start development server:
```bash
pnpm dev
```

Access the frontend at: http://localhost:3000

### Environment Variables

Create a `.env` file in the backend directory with:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## Authentication Flow

1. User logs in with email/password
2. Server validates credentials and returns JWT tokens
3. Tokens are stored in HTTP-only cookies
4. Client-side route protection using AuthProvider
5. Protected routes show loading skeletons while checking auth
6. Smooth SPA navigation between public/protected routes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
