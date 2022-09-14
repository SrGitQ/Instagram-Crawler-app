from datetime import datetime, timedelta

def isGreater_24hrs(timedb, timern):
    diff = timern - timedb

    if diff < timedelta(hours=24):
        return False

    return True