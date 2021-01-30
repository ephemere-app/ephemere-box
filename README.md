# Ephemere - Box

> Open a secure line

[![GitHub Tag](https://img.shields.io/github/tag/ephemere-app/ephemere-box.svg)](https://github.com/ephemere-app/ephemere-box/releases/latest)
[![GitHub Action CI/CD](https://github.com/ephemere-app/ephemere-box/workflows/CI/CD/badge.svg)](https://github.com/ephemere-app/ephemere-box/actions?query=workflow%3A%22CI%2FCD%22)
[![Coverage Status](https://img.shields.io/codecov/c/github/ephemere-app/ephemere-box)](https://codecov.io/gh/ephemere-app/ephemere-box)
[![License](https://img.shields.io/github/license/ephemere-app/ephemere-box)](https://github.com/ephemere-app/ephemere-box/blob/master/LICENSE)

Store and retrieve end-to-end encrypted and ephemeral messages from
Ephemere using [Redis](https://redis.io).

## Development

Install dependencies:

```bash
pipenv install -d
```

Run QA suite:

```bash
inv qa
```

Run local Redis server:

```bash
docker-compose up -d
```

Run API server:

```bash
cp .example.env .env
honcho start
```

### VSCode

If using VSCode, use the following configuration in `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "ephemere_box",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["--host=0.0.0.0", "--port=8000", "ephemere_box:app"],
      "envFile": "",
      "justMyCode": false
    },
    {
      "name": "tests",
      "type": "python",
      "request": "test",
      "justMyCode": false,
      "env": {
        "CI": "false"
      }
    }
  ]
}
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
