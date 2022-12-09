# md5-cracker

## Usage

Setup video: https://youtu.be/8rBb_UhnVgE

You can either follow gradescope PDF's instructions and use the servers set up by me already, or use the [rspec.xml](https://raw.githubusercontent.com/johan456789/md5-cracker/main/rspec.xml) to set up resources on GENI.
![image](https://user-images.githubusercontent.com/14802181/206642494-4c60532d-2982-4e1d-8f99-9623a9dea938.png)


### First time setup for both server and worker

If you're using the servers readily set up by me, you can skip this section.

1. SSH into it
2. Clone the repo and run setup scripts
    ```shell
    git clone https://github.com/johan456789/md5-cracker src && ./src/setup.sh
    ```
3. Ctrl + D to exit the SSH session
4. SSH into it again. We should automatically conda activate `web` environment and cd into `~/src`. If not, manually do so: `conda activate web && cd ~/src`

If the server is newly reserved on GENI, you need to update the IP addresses [here](https://github.com/johan456789/md5-cracker/blob/main/app.py#L13) to match those on GENI. Use `ifconfig` on workers to see their IP addresses and update `app.py` on server to match them.

### After first time setup

#### Server

```shell
flask run --host=0.0.0.0 --port=5678
```

#### Worker

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

### Accessing using a web browser

Video demo: https://youtu.be/ZheDjTzCoqE
