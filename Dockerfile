FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
WORKDIR /build

# Create venv, add it to path and install requirements
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install uvicorn server
RUN pip install uvicorn[standard]

# Copy the rest of app
COPY app app
COPY init.sh .
#commented out because vars shouldn't be provided during build process
#env vars should be provided as part of compose file or other deployment method
#COPY .env .

# Create new user to run app process as unprivilaged user
RUN addgroup --gid 1001 --system uvicorn && \
    adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 uvicorn

# Run init.sh script then start uvicorn
RUN chown -R uvicorn:uvicorn /build
CMD bash init.sh && \
    runuser -u uvicorn -- /venv/bin/uvicorn app.main:app --app-dir /build --host 0.0.0.0 --port 8000 --workers 2 --loop uvloop