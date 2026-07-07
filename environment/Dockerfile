FROM python:3.13-slim-bookworm@sha256:e4fa1f978c539608a10cdf74700ac32a3f719dfc6e8b6b6001da82deb36302a2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tmux \
        asciinema \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ /app/
COPY scripts/expand_dossier.py /tmp/expand_dossier.py
RUN python3 /tmp/expand_dossier.py && rm /tmp/expand_dossier.py \
    && cp /app/workflow/export_report.py /app/workflow/.export_report.original \
    && chmod a-w /app/workflow/.export_report.original
