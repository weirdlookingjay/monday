# Monday.com Clone

A full-featured project management platform clone built with Django and Next.js, implementing core Monday.com functionalities.

## Tech Stack

### Backend
- Django 4.2.20
- Django REST Framework
- Channels for real-time updates
- PostgreSQL database
- JWT Authentication

### Frontend (Coming Soon)
- Next.js 14+
- TailwindCSS
- shadcn/ui components
- Real-time updates with WebSocket

## Features

- [x] Custom User Model with email authentication
- [x] Team Management
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
├── backend/               # Django backend
│   ├── accounts/         # User and Team management
│   ├── boards/           # Board and item management
│   ├── workspace/        # Workspace organization
│   ├── core/            # Shared functionality
│   └── monday_clone/    # Project settings
└── frontend/            # Next.js frontend (coming soon)
```

## Getting Started

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

### Environment Variables

Create a `.env` file in the backend directory with:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## API Documentation

Coming soon...

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
