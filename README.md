# md5-cracker

## Usage

### Server

1. SSH into it
2. Clone the repo and run setup scripts
  ```shell
  git clone https://github.com/johan456789/md5-cracker src && ./src/setup.sh
  ```
3. Run Flask
  ```shell
  flask run --host=0.0.0.0 --port=5678
  ```
  
### Client (worker)

1. SSH into it
2. Clone the repo and run setup scripts
  ```shell
  git clone https://github.com/johan456789/md5-cracker src && ./src/setup.sh
  ```
3. Run `worker.py`
  
  Client1:
  ```shell
  python worker.py -p 12340
  ```
  
  Client2:
  ```shell
  python worker.py -p 12341
  ```
  
  Client3:
  ```shell
  python worker.py -p 12342
  ```
