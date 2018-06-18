import src.process.normalization as norm
import src.process.tokenization as token
import src.process.lemmatization as lem


def main():
    norm.main()
    token.main()
    lem.main()


if __name__ == "__main__":
    main()