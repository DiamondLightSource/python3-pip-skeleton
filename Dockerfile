# This file is for use as a devcontainer and a runtime container
# 
# The devcontainer should use the build target and run as root and use podman 
# or docker with user namespaces.
#

FROM python:3.10 as build

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    busybox \
    git \
    net-tools \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && busybox --install

RUN python3 -m venv /virtualenv
ENV PATH=/virtualenv/bin:$PATH

COPY . /project

# verify that the wheel installs and runs with --version
# replace python3-pip-skeleton if the cli command is different from repo name
RUN cd /project && \
    pip install --upgrade pip build && \
    python -m build --sdist --wheel && \
    pip install dist/*.whl && \
    python3-pip-skeleton --version

FROM python:3.10-slim as runtime

COPY --from=build /virtualenv/ /virtualenv/
ENV PATH=/virtualenv/bin:$PATH

ENTRYPOINT ["python3-pip-skeleton"]
CMD ["--version"]
