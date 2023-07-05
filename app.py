import asyncio
from flask import Flask, render_template, request, jsonify
import string
from time import sleep, time
from utils.constants import CHECK_IN_PERIOD_SEC, PASSWORD_LEN, SHUTDOWN, SIZE_OF_ALPHABET
from utils.network import check_in, close_connections, create_connections, distribute_task, send_to_client  # noqa
from utils.str_num import n_to_nums, nums2str, str2nums

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crack')
async def crack():
    hash = request.args.get('md5')
    num_workers = int(request.args.get('workers'))  # type: ignore
    total = SIZE_OF_ALPHABET ** PASSWORD_LEN
    finished = 0

    start_time = time()
    connections = create_connections(num_workers)
    asyncio.create_task(distribute_task(num_workers, hash))
    password = None
    while not password:
        password, finish_count = await check_in(num_workers)
        if not password:
            finished += finish_count
            print(f'sleep for {CHECK_IN_PERIOD_SEC} secs')
            await asyncio.sleep(CHECK_IN_PERIOD_SEC)
    end_time = time()
    duration = round(end_time - start_time, 2)
    print(f'===\nFound: {password}. It took {duration} seconds.\n===')

    # stop current task among workers
    for worker_id in range(num_workers):
        await send_to_client(worker_id, f'{SHUTDOWN}', listen=False)

    close_connections(connections)
    return jsonify({'password': password, 'duration': duration})


if __name__ == '__main__':
    print(nums2str(list(range(SIZE_OF_ALPHABET))))
    print(str2nums(string.ascii_letters))

    print(n_to_nums(100))
