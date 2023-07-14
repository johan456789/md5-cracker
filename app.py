import os
import asyncio
from typing import List
from flask import Flask, render_template, request, jsonify
from subprocess import Popen
import time
from argparse import ArgumentParser
from utils import get_free_ports, set_env_vars
from utils.constants import SHUTDOWN, SIZE_OF_ALPHABET
from utils.network import Network
from config import get_config


def create_app(config, network):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/crack')
    async def crack():
        CHECK_IN_PERIOD_SEC = int(os.environ.get('CHECK_IN_PERIOD_SEC'))  # type: ignore
        PASSWORD_LEN = int(os.environ.get('PASSWORD_LEN'))  # type: ignore

        hash = request.args.get('md5')
        total_work = SIZE_OF_ALPHABET ** PASSWORD_LEN
        finished = 0

        start_time = time.time()
        asyncio.create_task(network.distribute_task(hash))
        password = None
        while not password:
            password, finish_count = await network.check_in()
            if not password:
                finished += finish_count
                print(f'sleep for {CHECK_IN_PERIOD_SEC} secs')
                await asyncio.sleep(CHECK_IN_PERIOD_SEC)
                print(f'Progress: {round(finished / total_work * 100, 2)}%')
            else:
                print('Progress: 100%')
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        print(f'===\nFound: {password}. It took {duration} seconds.\n===')

        return jsonify({'password': password, 'duration': duration})

    return app


def teardown(network):
    async def helper():
        # stop current task among workers
        for worker_id in range(int(os.getenv('MAX_NUM_WORKERS'))):  # type: ignore
            await network.send_to_client(worker_id, f'{SHUTDOWN}', listen=False)
        network.close_connections()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(helper())


def main():
    parser = ArgumentParser()
    parser.add_argument('--mode', type=str, default='dev')  # dev/prod
    args = parser.parse_args()
    config = get_config(args.mode)
    set_env_vars(config)
    print(os.environ.get('CONFIG_TYPE'))

    # find available port
    # TODO: load port settings from env vars for prod
    MAX_NUM_WORKERS = int(os.environ.get('MAX_NUM_WORKERS'))  # type: ignore
    ports = get_free_ports(MAX_NUM_WORKERS)

    # start workers on available ports
    print(f'starting workers on {ports}')
    worker_processes: List[Popen[bytes]] = []
    for i in range(MAX_NUM_WORKERS):
        worker_process = Popen(['python', 'worker.py', '-p', str(ports[i])])
        worker_processes.append(worker_process)
    time.sleep(1)  # TODO wait for workers to be ready using retries instead of sleep

    # start server
    network = Network(ports)
    try:
        network.create_connections()
        app = create_app(config, network)
        app.template_folder = os.path.join(os.getcwd(), 'templates')
        app.run(port=5678, debug=True, use_reloader=False)
    finally:
        async def shutdown_workers():
            # stop current task among workers
            for worker_id in range(int(os.getenv('MAX_NUM_WORKERS'))):  # type: ignore
                await network.send_to_client(worker_id, f'{SHUTDOWN}', listen=False)
            network.close_connections()

        asyncio.run(shutdown_workers())  # run asynchronous functions in a simple, single-threaded manner

        for process in worker_processes:
            process.kill()


if __name__ == '__main__':
    main()
