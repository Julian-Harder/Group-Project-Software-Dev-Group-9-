# docker/Dockerfile.app
# Runtime image for the Mini Bingo CLI

FROM python:3.12-slim

# 1) Set working directory inside the container
WORKDIR /app

# 2) Copy project metadata (for reference / future tools)
COPY pyproject.toml ./

# 3) Copy source code and tests from the repo into the image
COPY src ./src
COPY tests ./tests

# 4) Install pytest so we can run tests inside the container if we want
RUN pip install --no-cache-dir pytest

# 5) Default command: run the Mini Bingo CLI
# (You can also use: CMD ["python", "-m", "mini_bingo"])
CMD ["python", "src/main.py"]
