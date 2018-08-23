import loacore.conf as conf


def change_external_dir():
    import loacore.utils.db as db
    db.download_db(db_name="new", forced=True)
    conf.set_external_conf("C:\\Users\\PaulBreugnot\\Freeling\\")


def check_conf():
    import loacore


def test_download_db():
    import loacore.utils.db as db
    db.download_db(db_name="full_uci_imdb")


def main():
    # change_external_dir()
    # check_conf()
    test_download_db()


if __name__ == "__main__":
    main()
