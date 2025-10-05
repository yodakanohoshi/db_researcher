# Node 20 + Alpine に Python を追加（最小＆シンプル）
FROM node:20-alpine

# apk
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    git

# pip（仮想環境を使用）
RUN python3 -m venv /opt/venv && \
    source /opt/venv/bin/activate && \
    pip install --no-cache-dir \
        pydbml \
        jinja2 \
        pyyaml
ENV PATH="/opt/venv/bin:$PATH"

# npm
RUN npm i -g \
    @dbml/cli \
    @liam-hq/cli \
    vite

# 権限が低いuserにする
RUN adduser -D -u 1001 app && \
    mkdir -p /work && \
    chown -R app:app /work
USER app
WORKDIR /work

# entrypoint
ENTRYPOINT ["bash"]
