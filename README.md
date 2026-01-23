# LAA GOV.UK Notify Orchestrator

[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/laa_govuk_notify_orchestrator/badge)](https://github-community.service.justice.gov.uk/repository-standards/laa_govuk_notify_orchestrator)

[![Standards Icon]][Standards Link]

This is the API used for Email orchestration between CLA services and GOV.UK Notify.

## Development in a virtual environment

#### 1) Clone the repository

```
git clone https://github.com/ministryofjustice/laa_govuk_notify_orchestrator.git
```

#### 2) Ensure you have the correct Python3 version (3.12)

```
python3 --version
```

If this is below 3.12 please ensure you have installed python3.12 somewhere on your system.

#### 3) Setup and activate a Python virtual environment

```
python3 -m venv env --prompt=\(notify_api\)

source env/bin/activate
```

##### 3.1) Ensure you are running the correct version of Python in your virtual environment

```
python --version

pip --version
```

Ensure both state 'Python 3.12'

#### 4) Update pip and install the required Python dependencies

```
pip install -U pip

pip install -r requirements.txt
```

#### 5) Set up your environment file

```
cp .env.example .env
```

This will setup the service to use RabbitMQ when running via Docker.
To use SQS as the message queue please see `docs/SQS.md`.

#### 6) Launch the service locally without a message queue

```
python manage.py
```

##### If you want the service to run on a port other than 8026 or a host other than 127.0.0.1

```
python manage.py --host 127.0.0.1 --port 8026
```

## Running via Docker

#### Running the service locally with RabbitMQ via Docker

```
./run_local.sh
```

#### Running the service without RabbitMQ via Docker

```
docker-compose down --remove-orphans
docker-compose up
```

## Documentation

Redocly documentation can be found at the root.

Swagger documentation can be found at the **/docs** endpoint.

## Testing

### Unit Testing is performed using pytest

```
pytest
```

[Standards Link]: https://operations-engineering-reports.cloud-platform.service.justice.gov.uk/public-report/laa_govuk_notify_orchestrator "Repo standards badge."
[Standards Icon]: https://img.shields.io/endpoint?labelColor=231f20&color=005ea5&style=for-the-badge&label=MoJ%20Compliant&url=https%3A%2F%2Foperations-engineering-reports.cloud-platform.service.justice.gov.uk%2Fapi%2Fv1%2Fcompliant_public_repositories%2Fendpoint%2Flaa_govuk_notify_orchestrator&logo=data:image/png;base64,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

## Git hooks

Repository uses [MoJ DevSecOps hooks](https://github.com/ministryofjustice/devsecops-hooks) to ensure `pre-commit` git hook is evaluated for series of checks before pushing the changes from staging area. Engineers should ensure `pre-commit` hook is configured and activated.

1. **Installation**:

   Ensure [prek](https://github.com/j178/prek?tab=readme-ov-file#installation) is installed globally

   Linux / MacOS

   ```bash
   curl --proto '=https' --tlsv1.2 -LsSf https://raw.githubusercontent.com/ministryofjustice/devsecops-hooks/e85ca6127808ef407bc1e8ff21efed0bbd32bb1a/prek/prek-installer.sh | sh
   ```

   or

   ```bash
   brew install prek
   ```

   Windows

   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/ministryofjustice/devsecops-hooks/e85ca6127808ef407bc1e8ff21efed0bbd32bb1a/prek/prek-installer.ps1 | iex"
   ```

2. **Activation**

   Execute the following command in the repository directory

   ```bash
   prek install
   ```

3. **Test**

   To dry-run the hook

   ```bash
   prek run
   ```

## 🔧 Configuration

### Exclusion list

One can exclude files and directories by adding them to `exclude` property. Exclude property accepts [regular expression](https://pre-commit.com/#regular-expressions).

Ignore everything under `reports` and `docs` directories for `baseline` hook as an example.

```yaml
   repos:
     - repo: https://github.com/ministryofjustice/devsecops-hooks
       rev: v1.0.0
       hooks:
         - id: baseline
            exclude: |
            ^reports/|
            ^docs/
```

Or one can also create a file with list of exclusions.

```yaml
repos:
  - repo: https://github.com/ministryofjustice/devsecops-hooks
    rev: v1.0.0
    hooks:
      - id: baseline
        exclude: .pre-commit-ignore
```
