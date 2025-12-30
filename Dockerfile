FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir -r requirements.txt; \
    fi

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "src/main.py", "--server.address=0.0.0.0", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
