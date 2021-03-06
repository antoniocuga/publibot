# -*- coding: utf-8 -*-
# source http://stackoverflow.com/a/12031316/3605870
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True


def do_capture(tweet_id):
    tweet_id = str(tweet_id)
    outfile = "screenshots/" + tweet_id + ".png"
    s = Screenshot()
    s.capture('https://twitter.com/uterope/status/' + tweet_id, outfile)


def main():
    #tweet_id = 467337666879827968
    tweet_id = sys.argv[1].strip()
    do_capture(tweet_id)


if __name__ == "__main__":
    main()
