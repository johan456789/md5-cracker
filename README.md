# md5-cracker

## Usage

### First time setup for both server and worker

1. SSH into it
2. Clone the repo and run setup scripts
  ```shell
  git clone https://github.com/johan456789/md5-cracker src && ./src/setup.sh
  ```
3. Ctrl + D to exit the SSH session
4. SSH into it again. We should automatically conda activate `web` environment and cd into `~/src`. If not, manually do so: `conda activate web && cd ~/src`

### After first time setup

#### Server

```shell
flask run --host=0.0.0.0 --port=5678
```

#### Worker

  - Client1:
  ```shell
  python worker.py -p 12340
  ```
  
  - Client2:
  ```shell
  python worker.py -p 12341
  ```
  
  - Client3:
  ```shell
  python worker.py -p 12342
  ```
