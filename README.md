
# Django REST API with Docker, PostgreSQL, and Swagger Documentation

E-commerce Online Platform project in Django REST API for register, login, managing products, categories, and stocks. It is Dockerized for easy deployment, uses PostgreSQL as the database, and includes Swagger UI for interactive API documentation.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [License](#license)

## Features
- **User Authentication and Registration API**.
- **CRUD operations** for `Product`, `Category`, and `Stock`.
- **API documentation** with Swagger UI and Redoc.
- **Dockerized** for isolated development and deployment.
- **PostgreSQL** for database management.
- **Flexible** many-to-many and one-to-one relationships between models.

## Technologies Used

- **Django** and **Django REST Framework**: Backend framework and API tools.
- **PostgreSQL**: Relational database for reliable data management.
- **Swagger**: API documentation.
- **Docker** and **Docker Compose**: Containerization for easy setup and deployment.

## Project Structure

```
E-commerce-Online-Platform /
│
├── product/                 # Product app (contains models, serializers, views, urls)
├── accounts/                # Accounts app for user management
├── your_project_name/       # Django project settings
├── requirements.txt         # Project dependencies
├── Dockerfile               # Docker configuration for the Django app
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # Project documentation
```

## Setup and Installation

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.

### Step 1: Clone the Repository

```bash
git clone https://github.com/s-nishad/E-commerce-Online-Platform.git
cd E-commerce-Online-Platform
```

### Step 2: Environment Variables

In your Django `settings.py`, config for JWT

```plaintext
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Step 3: Update `settings.py`

In your Django `settings.py`, update the database settings to connect with PostgreSQL:

```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/sparks_db")

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}
```
### Step 4: config `settings.py` for swagger
```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Enter the token with the 'Bearer <your-token>' format.",
        }
    },
    'USE_SESSION_AUTH': False,
}
```


## Running the Project

### Step 1: Build and Start Docker Containers

```bash
docker-compose up --build
```

This command will build the Django and PostgreSQL images, start the containers, and set up the environment.

### Step 2: Apply Migrations

After the containers are running, open a new terminal and run:

```bash
docker-compose exec web python manage.py migrate
```

This command applies migrations to set up the database.

### Step 3: Create a Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

This creates an admin user for accessing the Django admin panel.

### Step 4: Access the Application

- **Django App**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8080`
- **Redoc Documentation**: `http://localhost:8000/api/redocs/`

## API Documentation

Swagger and Redoc are used to generate interactive API documentation:

- **Swagger UI**: Available at `http://localhost:8080`
- **Redoc UI**: Available at `http://localhost:8000/api/redocs/`

## Usage

### Endpoints

- **Product Endpoints**:
  - `POST /api/products/create/`: Create a new product.
  - `GET /api/products/<guid>/`: Retrieve a product by GUID.
  - `PUT /api/products/<guid>/update/`: Update a product by GUID.
  - `DELETE /api/products/<guid>/delete/`: Delete a product by GUID.

- **Category Endpoints**:
  - Add and manage categories through nested serializers within `Product`.

### Example Request

To create a product:

```http
POST /api/products/create/
Content-Type: application/json

{
  "product_name": "Example Product",
  "description": "Product description",
  "price": 100,
  "categories": [
    {"name": "Category1", "description": "Category description"}
  ],
  "stock": {"quantity": 50}
}
```

## License

This project is licensed under the MIT License.
