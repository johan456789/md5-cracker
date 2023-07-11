# Distributed MD5 Cracker

- Supports uppercase and lowercase English characters
- Distributes tasks among worker nodes

## Usage

### Server

```shell
flask run --host=0.0.0.0 --port=5678
```

### Workers

  - worker1 (client1):
    ```shell
    python worker.py -p 12340
    ```
  
  - worker2 (client2):
    ```shell
    python worker.py -p 12341
    ```
  
  - worker3 (client3):
    ```shell
    python worker.py -p 12342
    ```

Video demo: https://youtu.be/ZheDjTzCoqE

## Testing

### Run all tests

```shell
pytest
```

### Run a specific testcase

```shell
pytest -k test_testcase
```

### Get test coverage

```shel
pytest --cov=directory
```
