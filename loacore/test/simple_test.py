import loacore.utils.db as db
import loacore.process.file_process as file_process

backup = db.database_backup()

db.download_db(db_name="new")
file_process.add_files(["test_file.txt"])

db.restore_db(backup)
