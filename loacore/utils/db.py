
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
            print("Commit attempt number : " + try_number)
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB failed, retry.", str(try_number)))
            time.sleep(10)
            safe_commit(conn, try_number+1, state_queue, id_process)
        else:
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB commit failed.", " X "))
            print("Commit fail.")


def safe_execute(c, request, try_number, state_queue, id_process,  mark_args=None):
    import os
    import time
    import sqlite3 as sql
    from loacore.utils.status import ProcessState
    from loacore.conf import MAX_DB_COMMIT_ATTEMPTS
    try:
        if mark_args is not None:
            c.execute(request, mark_args)
        else:
            c.execute(request)
    except sql.OperationalError:
        if try_number <= MAX_DB_COMMIT_ATTEMPTS:
            try_number += 1
            print("Execute attempt number : " + try_number)
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB failed, retry.", str(try_number)))
            time.sleep(10)
            safe_execute(c, request, try_number+1, state_queue, id_process, mark_args=mark_args)
        else:
            if state_queue is not None:
                state_queue.put(ProcessState(id_process, os.getpid(), "DB execute failed.", " X "))
            print("Execute fail.")
