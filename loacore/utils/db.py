
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


def download_db(db_url=None, db_name=None, forced=False, unexisting_db=False):
    """
    Download and replace the current database.
    See https://sourceforge.net/projects/loacore/files/Database/ for available databases.

    The use of :class:`database_backup` as a context manager ensure that the database will be restored if an exception
    occurs (e.g.: Download fail or user interruption)

    :param db_url: An download url to a database file.
    :type db_url: str
    :param db_name: A database name. Possible values : *'new'*, *'full_uci_imdb'*
    :type db_name: str
    """

    import re
    import os
    import urllib.request
    import urllib.error
    from loacore.conf import DB_PATH

    def confirm_delete():
        c = input("Download a database will override current database. Continue? [y/n]")
        if re.fullmatch(r'n|N|no|NO', c) is not None:
            return False
        elif re.fullmatch(r'y|Y|yes|YES', c) is not None:
            return True
        else:
            print("Invalid input.")
            confirm_delete()

    def show_progress(count, block_size, total_size):
        print("\rDownloading... {:.0%}".format(min(count * block_size / total_size, 1)), end="")
        
    def download():
        if os.path.exists(DB_PATH):
            if not forced:
                if confirm_delete():
                    os.remove(DB_PATH)
                else:
                    return
        nonlocal db_url
        if db_url is None:
            if db_name is not None:
                if db_name == "new":
                    db_url = "https://sourceforge.net/projects/loacore/files/Database/new.db/download"
                elif db_name == "full_uci_imdb":
                    db_url = "https://sourceforge.net/projects/loacore/files/Database/full_uci_imdb.db/download"

        if db_url is not None:
                urllib.request.urlretrieve(db_url, DB_PATH, show_progress)
                print("\nDatabase successfully downloaded.")
   
    with database_backup():
        download()
       


class database_backup:
    """
    A context manager that allows to make a backup of the current database, and that restores it if an error occurs during
    the execution of wrapped code.

    Notice that you can also just use this class to make a backup on your local file system using
    :func:`write_backup()`.

    :example:

    Make a persistent manual backup to a local file.

    .. code-block:: python

        >>> from loacore.utils.db import database_backup
        >>> backup = database_backup(path="/home/paulbreugnot/test_backup.db", delete_backup=False)
        >>> backup.write_backup()

    """

    def __init__(self, path=None, delete_backup=True):
        """
        :param path:
            If specified, path of the file to write the backup. Otherwise, a
            `TemporaryFile <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile>`_ is used.
        :type path: |path-like-object|
        :param delete_backup: If path is specified, specify if the generated file should be removed when  __exit__ is
        called.
        :type delete_backup: bool

        """
        self.path = path
        self.delete_backup = delete_backup
        self.backup_file = None

    def write_backup(self, temp=True):
        """
        Write a persistent backup to the file specified at initialization. When this function is used,
        *self.backup_file* potentially needs to be closed manually.
        """

        from loacore.conf import DB_PATH

        if not temp:
            if self.path is None:
                print("No path specified, nothing written.")
            else:
                self.backup_file = open(self.path, mode="w+b")

                self.backup_file.write(open(DB_PATH, mode="w+b").read())
                self.backup_file.flush()
        else:
            from tempfile import TemporaryFile
            self.backup_file = TemporaryFile()
            self.backup_file.write(open(DB_PATH, mode="rb").read())
            self.backup_file.flush()

    def __enter__(self):
        import tempfile
        from loacore.conf import DB_PATH

        if self.path is None:
            self.backup_file = tempfile.TemporaryFile()
        else:
            self.backup_file = open(self.path, mode="w+b")

        self.backup_file.write(open(DB_PATH, mode="w+b").read())
        self.backup_file.flush()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            restore_db(self.backup_file)
        if self.path is not None and self.delete_backup:
            import os
            os.remove(self.path)
        self.backup_file.close()


def restore_db(backup_file, close=False):
    """
    Restore database from the specified backup_file, overriding the current one.

    :param backup_file: A file opened in read and binary mode.
    :type backup_file: :obj:file
    """
    from loacore.conf import DB_PATH

    print("\n==> Restoring database...\n")
    backup_file.seek(0)
    new_db_file = open(DB_PATH, mode='w+b')
    new_db_file.write(backup_file.read())
    new_db_file.close()
    if close:
        backup_file.close()





