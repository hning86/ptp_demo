# Use strict local Python target
FROM python:3.13-slim

# Install uv securely
RUN pip install uv

WORKDIR /app

# Copy project files and resolve dependencies purely against standard PyPI
COPY pyproject.toml /app/
RUN uv pip install --system --index-url https://pypi.org/simple -r pyproject.toml || uv pip install --system --index-url https://pypi.org/simple .

# Copy full project source
COPY . /app

# Execute direct entry path
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
