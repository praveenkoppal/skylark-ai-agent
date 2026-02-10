FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY requirements.txt .
COPY app.py .
COPY coordinator.py .
COPY matcher.py .
COPY sheets.py .
COPY conflict_detector.py .
COPY credentials.json .

# Install dependencies using uv (skips externally-managed error)
RUN uv pip install --system --no-cache -r pyproject.toml || uv pip install --system --no-cache --all-extras .

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
