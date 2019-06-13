import time


class Crawler:
    def __init__(self, item):
        self.item = item

    def run(self):
        time.sleep(10)
        return 'http://lmgtfy.com/?q=' + self.item
