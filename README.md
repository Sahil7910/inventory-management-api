# Inventory Management System API

This project is a RESTful API built using Django Rest Framework (DRF) for managing inventory items. The API supports authentication via JWT and optimizes performance using Redis caching for frequently accessed items. The database used is PostgreSQL.

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Logging](#logging)
- [Running Tests](#running-tests)

## Features
- JWT Authentication for secure API access.
- CRUD Operations for managing inventory items.
- Redis Caching to improve response times for frequently accessed data.
- PostgreSQL database for reliable and scalable data storage.
- Comprehensive Unit Tests to ensure code reliability.

## Setup Instructions

### Prerequisites
- Python 3.x installed.
- PostgreSQL database.
- Redis installed and running.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sahil/inventory-management-api.git 
cd inventory-management-api
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv env
source env/bin/activate    # For Linux/Mac 
env\Scripts\activate       # For Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database
```bash
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 5: Configure Redis
```bash
CACHES = { 
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache', 
        'LOCATION': 'redis://127.0.0.1:6379/1', 
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
````
### Step 6: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create a Superuser
```bash
python manage.py createsuperuser
```

### Step 8: Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints
  ### Authentication
   - User Registration: POST /api/users/register/
   - JWT Login: POST /api/token/
   -  Refresh JWT Token: POST /api/token/refresh/

  ### Inventory Management
  - Create Item: POST /api/additems/
  - Get All Items: GET /api/items/
  - Get Item by ID: GET /api/items/{id}/
  - Update Item by ID: PUT /api/items/{id}/update/
  - Delete Item by ID: DELETE /api/items/{id}/delete/

  ### JWT Authentication
  - Add the Authorization: Bearer <access_token> header to requests to access protected endpoints.


    
## Usage Examples
  ### 1. User Registration
  ```bash
        POST /api/users/register/
        {
          "username": "newuser",
           "email": "newuser@example.com",
           "password": "password123"
        }
  ```
 
  ### Response:
  ```bash
    {
    "id": 1,
    "username": "newuser",
    "email": "newuser@example.com"
  }
   ```

### 2. Obtain JWT Token
  ```bash
      POST /api/token/
    {
      "username": "newuser",
      "password": "password123"
    }
  ```

### Response:
```bash
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

### 3. Create an Inventory Item
```bash
POST /api/additems/
Authorization: Bearer <access_token>

{
    "name": "Laptop",
    "description": "A high-performance laptop."
}
```

### Response:
```bash
{
    "id": 1,
    "name": "Laptop",
    "description": "A high-performance laptop",
    "created_at": "2024-09-28T12:34:56.789Z"
}
```

### 4. Get All Inventory Items
```bash
     GET /api/items/
    Authorization: Bearer <access_token> 
```

### Response:
```bash
{
    "id": 1,
    "name": "Laptop",
    "description": "A high-performance laptop",
    "created_at": "2024-09-28T12:34:56.789Z"
}
```

### 5. Get an Inventory Item by ID
```bash
GET /api/items/1/
Authorization: Bearer <access_token>
```

### Response:
```bash
{
    "id": 1,
    "name": "Laptop",
    "description": "A high-performance laptop",
    "created_at": "2024-09-28T12:34:56.789Z"
}
```

###  6. Update an Inventory Item
  ```bash
    PUT /api/items/1/update/
    Authorization: Bearer <access_token>

{
    "name": "Gaming Laptop",
    "description": "A laptop for gaming."
}
```

### Response:
```bash
{
    "id": 1,
    "name": "Gaming Laptop",
    "description": "A laptop for gaming",
    "created_at": "2024-09-28T12:34:56.789Z"
}
```

###  7. Delete an Inventory Item
```bash
DELETE /api/items/1/delete/
Authorization: Bearer <access_token>

{
    "detail": "Item deleted."
}
```

## Logging
The API includes a logging system that captures significant events, such as:

- API Usage: Logs the requests made to the API and the responses returned.
- Errors: Captures any errors that occur during API calls.
- Events: Logs important operations such as item creation, retrieval, updating, and deletion.
  
## Log File Locations:
- logs/inventory_api.log: Contains general logs for API usage and operations.
- logs/error.log: Contains logs specifically for errors encountered during API operation.
- Viewing Logs: You can view the log files in the logs/ directory to monitor API usage and errors.

### Running Tests
```bash
python manage.py test
```

