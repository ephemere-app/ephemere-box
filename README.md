# Ephemere - Box

> Open a secure line

[![GitHub Tag](https://img.shields.io/github/tag/ephemere-app/ephemere-box.svg)](https://github.com/ephemere-app/ephemere-box/releases/latest)
[![GitHub Action CI/CD](https://github.com/ephemere-app/ephemere-box/workflows/CI/CD/badge.svg)](https://github.com/ephemere-app/ephemere-box/actions?query=workflow%3A%22CI%2FCD%22)
[![License](https://img.shields.io/github/license/ephemere-app/ephemere-box)](https://github.com/ephemere-app/ephemere-box/blob/master/LICENSE)

Synchronize end-to-end encrypted and ephemeral messages from
Ephemere using [Socket-io](https://socket.io).

## Build Setup

```
pipenv install -d
inv qa
```

## Docker

### Build

```
docker build -t ephemereapp/ephemere-box:latest .
```

### Run

```
docker run --rm --env-file .env -p 8000:8000 ephemereapp/ephemere-box:latest
```

## License

Licensed under GNU Affero General Public License v3.0 (AGPLv3)

Copyright (c) 2021 - present Romain Clement
