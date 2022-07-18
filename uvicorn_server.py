from uvicorn.workers import UvicornWorker


class GunicornUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "auto", "http": "auto", "server_header": False}
