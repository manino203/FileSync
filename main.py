import file_sync
from arg_parser import setup_parser

if __name__ == "__main__":
    try:
        args = setup_parser()
        file_sync.run(args.source, args.replica, args.interval, args.log_file, args.delta_encoding)
    except (KeyboardInterrupt, PermissionError) as e:
        if isinstance(e, PermissionError):
            print(f"Cannot perform sync because access is denied: {e.filename}")
