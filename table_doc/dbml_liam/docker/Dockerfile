# docker/Dockerfile
FROM node:20-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    ca-certificates \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN npm i -g @dbml/cli @liam-hq/cli
RUN npm i -g http-server

WORKDIR /work

COPY build_erd.sh /usr/local/bin/build_erd
RUN chmod +x /usr/local/bin/build_erd

CMD ["/bin/bash"]