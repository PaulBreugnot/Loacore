
def safe_commit(conn, try_number, state_queue, id_process):
    import os
    import time
    import sqlite3 as sql
    from loacore.utils.status import ProcessState
    from loacore.conf import MAX_DB_COMMIT_ATTEMPTS
    try:
        conn.commit()
    except sql.OperationalError:
        if try_number <= MAX_DB_COMMIT_ATTEMPTS:
            try_number += 1
            if id_process is not None:
                print("[Process " + str(id_process) + "] Commit attempt number : " + str(try_number))
            else:
                print("Commit attempt number : " + str(try_number))
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB failed, retry.", str(try_number)))
            time.sleep(10)
            safe_commit(conn, try_number+1, state_queue, id_process)
        else:
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB commit failed.", " X "))
            if id_process is not None:
                print("[Process " + str(id_process) + "] Commit fail.")
            else:
                print("Commit fail.")


def safe_execute(c, request, try_number, state_queue, id_process,  mark_args=None, execute_many=False):
    import os
    import time
    import sqlite3 as sql
    from loacore.utils.status import ProcessState
    from loacore.conf import MAX_DB_COMMIT_ATTEMPTS
    try:
        if mark_args is not None:
            if not execute_many:
                c.execute(request, mark_args)
            else:
                c.executemany(request, mark_args)
        else:
            c.execute(request)
    except sql.OperationalError:
        if try_number <= MAX_DB_COMMIT_ATTEMPTS:
            try_number += 1
            if id_process is not None:
                print("[Process " + str(id_process) + "] Execute attempt number : " + str(try_number))
            else:
                print("Execute attempt number : " + str(try_number))
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB failed, retry.", str(try_number)))
            time.sleep(10)
            safe_execute(c, request, try_number+1, state_queue, id_process, mark_args=mark_args)
        else:
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB execute failed.", " X "))
            if id_process is not None:
                print("[Process " + str(id_process) + "] Execute fail.")
            else:
                print("Execute fail.")


def download_db(db_url):
    import os
    import urllib.request
    from loacore.conf import DB_PATH

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    urllib.request.urlretrieve(db_url, DB_PATH)
