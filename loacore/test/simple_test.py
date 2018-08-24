
def main(workers=0):
    import os
    import loacore.utils.db as db
    import loacore.process.file_process as file_process

    # backup = db.database_backup()
    # backup.write_backup()

    db.download_db(db_name="new")
    file_process.add_files([os.path.join(os.path.dirname(__file__), "test_file.txt")], workers=workers)

    # db.restore_db(backup.backup_file, close=True)


if __name__ == "__main__":
    main()
