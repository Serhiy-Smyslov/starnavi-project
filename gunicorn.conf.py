import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn_server.GunicornUvicornWorker'
keepalive = 40
