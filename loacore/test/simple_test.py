
def main():
    import loacore.utils.db as db
    import loacore.process.file_process as file_process

    backup = db.database_backup()
    backup.write_backup()

    db.download_db(db_name="new")
    file_process.add_files(["test_file.txt"], workers=0)

    db.restore_db(backup.backup_file, close=True)


if __name__ == "__main__":
    main()
