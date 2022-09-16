def divide_tasks(tasks, numprocs):
    avg = len(tasks) / float(numprocs)
    out = []
    last = 0.0

    while last < len(tasks):
        out.append(tasks[int(last):int(last+avg)])
        last += avg

    out = [el for el in out if el]
    return out
    