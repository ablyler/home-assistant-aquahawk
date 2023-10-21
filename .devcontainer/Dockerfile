FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# install direnv
RUN apt-get update && \
    apt-get install --no-install-recommends -y direnv && \
    rm -rf /var/lib/apt/lists/*