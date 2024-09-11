import argparse


def setup_parser() -> argparse.Namespace:
    """
        Set up the command-line argument parser.
    """
    parser = argparse.ArgumentParser("Synchronize source folder to replica folder.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("--delta_encoding", action="store_true", help="When this flag is set, "
                                                                      "only the differences between the "
                                                                      "source and destination files will be "
                                                                      "transferred, reducing the total amount of data "
                                                                      "transferred. "
                                                                      "This is especially useful for large files "
                                                                      "where only small portions have "
                                                                      "changed. If not set, the entire file will be "
                                                                      "copied.")

    return parser.parse_args()
