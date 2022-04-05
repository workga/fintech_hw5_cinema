# Cinema API
This is API for Cinema web application

### Features
- Base authentication
- Pydantic validation
- Swagger documentation
- Pagination
- Movies filters: substring, year, top

### Endpoints
You can see API documentation in swagger using url:
```
/docs
```

### Usage

Create venv:
```bash
    make venv
```

Create or recreate database
```bash
    make recreate
```

Run application:
```bash
    make up
```

Build docker image:
```bash
make docker-build
```

Run docker container:
```bash
make docker-run
```

### Development
Run tests:
```bash
    make test
```

Run linters:
```bash
    make lint
```

Run formatters:
```bash
    make format
```