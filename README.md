# Auth FastAPI - Authentication System

A comprehensive authentication system built with FastAPI, featuring Clerk integration, role-based access control, and user management.

## 🚀 Features

-   **🔐 Authentication**: JWT-based authentication with Clerk
-   **👥 User Management**: Complete user CRUD operations
-   **🛡️ Role-Based Access**: USER, ADMIN, MODERATOR roles
-   **⚙️ User Settings**: Customizable user preferences
-   **📊 Admin Panel**: User management and role administration
-   **🔄 Modular Architecture**: Clean, scalable code structure

## 🏗️ Architecture

### Project Structure

```
Auth_cleark_fastapi/
├── 📁 auth/                    # Authentication module
├── 📁 users/                   # User management module
├── 📁 user_settings/           # User settings module
├── 📁 configs/                 # Configuration files
└── 📁 exceptions/              # Global exception handling
```

### Key Components

-   **Authentication Factory**: Provider-agnostic authentication
-   **Repository Pattern**: Clean data access layer
-   **DTO Pattern**: Type-safe data transfer
-   **Dependency Injection**: Loose coupling architecture

## 🛠️ Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/DevSargis/Auth-Fast-Api.git
    cd Auth-Fast-Api
    ```

2. **Create virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    ```bash
    cp .env.example .env
    # Edit .env with your Clerk credentials
    ```

## ⚙️ Configuration

### Environment Variables

```bash
AUTH_PROVIDER=clerk
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_API_URL=https://api.clerk.com/v1
DATABASE_URL=postgresql://user:pass@localhost/db
```

## 🚀 Running the Application

### Development

```bash
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once running, access the interactive API documentation:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### Authentication

-   `GET /api/v1/auth/me` - Get current user
-   `GET /api/v1/health` - Health check

### Users

-   `GET /api/v1/users/me` - Get user profile
-   `GET /api/v1/users/me/metadata` - Get user metadata

### Admin (Admin only)

-   `GET /api/v1/admin/users` - Get all users
-   `GET /api/v1/admin/users/search` - Search users
-   `POST /api/v1/admin/users/{id}/set-role` - Set user role
-   `PUT /api/v1/admin/users/{id}/role` - Update user role
-   `POST /api/v1/admin/set-admin` - Set user as admin

### User Settings

-   `GET /api/v1/user-settings/me` - Get user settings
-   `PUT /api/v1/user-settings/me` - Update user settings

## 🔐 Authentication

The system uses Clerk for authentication:

1. **JWT Token Validation**: Secure token verification
2. **Role-Based Access**: Automatic role checking
3. **Admin Protection**: Admin-only endpoint protection
4. **CORS Support**: Cross-origin request handling

## 🏛️ Design Patterns

-   **Factory Pattern**: Authentication provider flexibility
-   **Repository Pattern**: Database abstraction
-   **DTO Pattern**: Clean data flow
-   **Dependency Injection**: Loose coupling

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 📦 Dependencies

-   **FastAPI**: Modern web framework
-   **SQLAlchemy**: Database ORM
-   **Pydantic**: Data validation
-   **Clerk**: Authentication provider
-   **Uvicorn**: ASGI server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@example.com or create an issue in this repository.

---

**Built with ❤️ using FastAPI and Clerk**
