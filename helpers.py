
def timestamp2datestring(timestamp,format="%a %b %d %X %Z %Y"):
    import time
    return time.strftime(format,  time.gmtime(timestamp/1000.))