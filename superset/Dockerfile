FROM apache/superset:6.0.0

USER root
RUN uv pip install --python /app/.venv/bin/python \
    "clickhouse-connect==0.15.1" \
    "psycopg2-binary==2.9.11" \
    "pydantic-settings==2.14.2"

COPY entrypoint.sh bootstrap.py exceptions.py superset_config.py /app/ed-store/

ENV PYTHONPATH="/app/ed-store:/app/pythonpath" \
    SUPERSET_CONFIG_PATH="/app/ed-store/superset_config.py"

USER superset
CMD ["bash", "/app/ed-store/entrypoint.sh"]
