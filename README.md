# ReferralAPI

This is a simple RESTful API service for a referral system, which allows users to create and manage referral codes, register with a referral code, and retrieve information about referrals.

## Features

- **User Registration and Authentication**: Users can register and authenticate via JWT and OAuth 2.0.
- **Referral Code Management**:
   - Authenticated users can create and delete their referral code.
   - Only one active referral code can exist per user at a time.
   - A valid expiration date must be set when creating a referral code.
- **Referral Code Retrieval**: Retrieve a referral code by email address of the referrer.
- **Referral Registration**: Users can register using a referral code.
- **Referral Information**: Get information about referrals based on the referrer’s ID.
- **API Documentation**: The API provides a UI documentation using Swagger or ReDoc.
- **In-Memory Caching**: Caching for referral codes is implemented using the cachetools library.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/stepkacorporation/ReferralAPI.git
   cd ReferralAPI
   ```

2. Set up environment variables by creating the `.env file` in the `docker/dev/` directory. You can use the provided example file (`docker/dev/.env-example`) as a reference.

3. Build and start the development containers:

   ```bash
   ./scripts/dev/up.sh -d --build
   ```

## Usage

### Docker Commands

- **Start development containers**:

   ```bash
   ./scripts/dev/up.sh
   ``` 
   You can pass additional arguments like `-d --build` for detached mode or rebuilding containers.

- **Stop and remove containers**:

   ```bash
   ./scripts/dev/down.sh
   ``` 
   You can pass `-v` to remove volumes.

- **Create a new Alembic migration**:

   ```bash
   ./scripts/dev/new_migration.sh "migration message"
   ``` 
  
- **Apply Alembic migrations**:

   ```bash
   ./scripts/dev/migrate.sh
   ```
  
## API Documentation

The API documentation is available through Swagger or ReDoc. Once the application is running, you can access the documentation at the following URLs:

- Swagger UI: http://localhost:8000/docs
- ReDoc UI: http://localhost:8000/redoc
