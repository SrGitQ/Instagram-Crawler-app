from datetime import datetime, timedelta

def isGreater_24hrs(timedb, timern):
    diff = timern - timedb

    return not (diff < timedelta(hours=24))