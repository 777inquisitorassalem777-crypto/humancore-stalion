FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd -m researcher
USER researcher
WORKDIR /home/researcher
ENTRYPOINT ["humancore"]
CMD ["--cycles", "2000", "--out", "runs/demo"]
