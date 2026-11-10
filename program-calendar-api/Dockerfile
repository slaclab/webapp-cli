FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir .; \
    fi

COPY . .

# Secrets are mounted at /app/secrets by 2-deploy.sh. The app opens these
# files by bare name, so symlink them into WORKDIR.
RUN mkdir -p /app/secrets \
 && ln -sf /app/secrets/credentials.json /app/credentials.json \
 && ln -sf /app/secrets/token.json       /app/token.json \
 && ln -sf /app/secrets/config.json      /app/config.json

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
