FROM ubuntu:24.04 AS base

ENV \
	DEBIAN_FRONTEND=noninteractive \
	LANG="C.UTF-8"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

FROM base AS final

RUN set -x \
	&& apt-get update -yq --no-install-recommends \
	&& apt-get install -yq --no-install-recommends \
	build-essential \
	gfortran \
	r-base \
	r-base-dev \
	ca-certificates \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get clean

RUN set -x \
	&& mkdir -p /workdir

WORKDIR /workdir
