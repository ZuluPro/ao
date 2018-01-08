import time
import threading


def delay(wait, func, *args, **kwargs):
    def background_func(*args, **kwargs):
        time.sleep(wait)
        func(*args, **kwargs)
    thread = threading.Thread(target=background_func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
