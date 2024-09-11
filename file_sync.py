import os
import hashlib
import shutil
import time
from datetime import datetime
from typing import BinaryIO

from logging import log


def perform_sync(src_path: str, dest_path: str, log_path: str, delta_encoding: bool) -> None:
    """
        Perform synchronization between source and destination folders.
    """
    log(f"{datetime.now().strftime('%Y-%d-%m %H:%M:%S')} :", log_path)
    remove_from_dest(src_path, dest_path, log_path)
    copy_from_src(src_path, dest_path, log_path, delta_encoding)
    log("Sync done\n", log_path)


def remove_from_dest(src_path: str, dest_path: str, log_path: str) -> None:
    """
       Remove files and directories from the destination that do not exist in the source.
    """
    for root, dirs, files in os.walk(dest_path):
        src_root = os.path.join(src_path, os.path.relpath(root, dest_path))
        for d in dirs:
            remove_if_not_in_src(root, src_root, d, log_path)
        for f in files:
            remove_if_not_in_src(root, src_root, f, log_path)


def remove_if_not_in_src(root: str, src_root: str, path: str, log_path: str) -> None:
    """
        Remove a file or directory from the destination if it does not exist in the source.
    """
    path_in_dest = os.path.join(root, path)
    path_in_src = os.path.join(src_root, path)
    if not os.path.exists(path_in_src):
        if os.path.isdir(path_in_src):
            os.rmdir(path_in_dest)
            log(f"Removed directory at: {path_in_dest}", log_path)
        else:
            os.remove(path_in_dest)
            log(f"Removed file at: {path_in_dest}", log_path)


def copy_from_src(src_path: str, dest_path: str, log_path: str, delta_encoding: bool) -> None:
    """
        Copy files from the source folder to the destination folder.
    """

    for root, dirs, files in os.walk(src_path):
        dest_root = os.path.join(dest_path, os.path.relpath(root, src_path))
        try:
            os.makedirs(dest_root)
            log(f"Created directory at: {dest_root}", log_path)
        except FileExistsError:
            pass
        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_root, file)
            with open(src_file_path, "rb") as src_file:
                try:
                    with open(dest_file_path, "rb+") as dest_file:
                        copy_file(src_file, dest_file, src_file_path, dest_file_path, log_path, delta_encoding)
                except FileNotFoundError:
                    shutil.copy2(src_file_path, dest_file_path)
                    log(f"Created file at: {dest_file_path}", log_path)


def delta_encoding_copy(src_file: BinaryIO, dest_file: BinaryIO, src_file_path: str, dest_file_path: str) -> bool:
    """
    Copy file data from source to destination using delta encoding. This approach minimizes unnecessary write
    operations.
    """
    updated = False
    chunk_size = 4096
    make_files_same_size(src_file_path, dest_file_path, dest_file)
    for src_chunk, dest_chunk in iter(lambda: (src_file.read(chunk_size), dest_file.read(chunk_size)), (b"", b"")):
        if get_md5_hash(src_chunk) != get_md5_hash(dest_chunk):
            dest_file.seek(-len(src_chunk), 1)
            dest_file.write(src_chunk)
            updated = True
    return updated


def copy_file(src_file: BinaryIO, dest_file: BinaryIO, src_file_path: str, dest_file_path: str, log_path: str,
              delta_encoding: bool) -> None:
    """
        Copy the whole file or update a file, based on the delta_encoding flag, from the source to the destination.
    """
    updated = False
    if delta_encoding:
        updated = delta_encoding_copy(src_file, dest_file, src_file_path, dest_file_path)
    else:
        if get_md5_hash(dest_file.read()) != get_md5_hash(src_file.read()):
            shutil.copy2(src_file_path, dest_file_path)
            updated = True
    if updated:
        log(f"Updated file at: {dest_file_path}", log_path)


def make_files_same_size(src_file_path: str, dest_file_path: str, dest_file: BinaryIO) -> None:
    """
        Function that makes the destination file the same size as the source file to allow copying via delta encoding.
    """
    src_file_size = os.path.getsize(src_file_path)
    dest_file_size = os.path.getsize(dest_file_path)
    if src_file_size < dest_file_size:
        dest_file.truncate(src_file_size)
    elif src_file_size > dest_file_size:
        dest_file.seek(0, 2)
        dest_file.write(b'\x00' * (src_file_size - dest_file_size))
        dest_file.seek(0, 0)


def get_md5_hash(data: bytes) -> str:
    """
        Compute the MD5 hash of the given data.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    return md5_hash.hexdigest()


def run(src_path: str, dest_path: str, delay: int, log_path: str, delta_encoding: bool) -> None:
    """
        Run the synchronization process periodically.
    """
    while True:
        perform_sync(src_path, dest_path, log_path, delta_encoding)
        time.sleep(delay)
