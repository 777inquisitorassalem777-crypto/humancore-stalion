FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "ccos.api:app", "--host", "0.0.0.0", "--port", "8000"]
