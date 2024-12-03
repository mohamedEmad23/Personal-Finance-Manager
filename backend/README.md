# FastAPI Backend for Personal Finance Manager Project

This is the backend for the Personal Finance Manager project. It is built using FastAPI, a modern Python web framework 
that is fast (high-performance), web-based (based on standard Web APIs), and is based on standard Python type hints.

## Requirements

- Python 3.8 or higher
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- MySQL
- MySQL Connector
- Python-dotenv
- Python-jose
- Passlib
- Requests
- bcrypt

## General Workflow

By default, the dependencies are managed with uv, go and install it (requirements.txt).
After Installing, run the command under the 'Usage' section to start the server in the terminal.


## Installation

```bash
pip install -r requirements.txt
```

## Usage
    
```bash
    uvicorn main:app --reload
```

## Project Structure

Project structure was generated using a simple bash script. The script is located in the root directory of the project and is 
named `structure.sh`.

First line in the script is a shebang line. It tells the system that the script should be executed using bash.
After creating the .sh file, run the command below to make the file executable.

```bash
chmod +x structure.sh
```

To run the script, use the command below:

```bash
./structure.sh
```