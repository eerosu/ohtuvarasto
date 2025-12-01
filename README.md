# ohtuvarasto

A warehouse management system with both CLI and web interfaces.

## Features

- Create and manage warehouses
- Add content to warehouses
- Remove content from warehouses
- Edit warehouse properties
- Web UI with professional, trustworthy design

## Installation

```bash
pip install flask pytest
```

Or with the project dependencies:

```bash
pip install -e .
```

## Usage

### Web Interface

Start the Flask web application:

```bash
cd src
python app.py
```

Then open your browser to http://localhost:5000

### Command Line Interface

Run the example CLI application:

```bash
cd src
python index.py
```

## Running Tests

```bash
cd src
python -m pytest tests/
```

## Development

The warehouse logic is in `src/varasto.py`. The web interface is built with Flask in `src/app.py`.

For production deployment, use a production WSGI server like Gunicorn instead of the Flask development server.