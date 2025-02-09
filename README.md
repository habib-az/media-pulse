# Windsurf Project - FastAPI & Supabase

A FastAPI backend application connected to Supabase for managing windsurf-related data.

## Features

- REST API endpoints for windsurf data management
- Supabase integration for secure data storage
- Real-time data updates
- Authentication and authorization

## Prerequisites

- Python 3.8+
- Supabase account and project credentials

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/windsurf-project.git
   cd windsurf-project
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once running, access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License
