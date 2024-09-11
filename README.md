# Folder Synchronization Tool

## Overview

This Python program synchronizes two folders: a source folder and a replica folder. It ensures that the replica folder maintains a full, identical copy of the source folder. Synchronization is performed periodically, and all file operations are logged both to a log file and to the console. The program supports delta encoding to optimize the synchronization of large files by only transferring the differences between the source and destination files.

## Features

- **One-Way Synchronization**: The replica folder will be modified to exactly match the source folder.
- **Periodic Synchronization**: Synchronization is performed at regular intervals.
- **Logging**: File creation, copying, and removal operations are logged to a file and printed to the console.
- **Delta Encoding**: Minimizes data transfer by only sending changes (optional).
- **Command-Line Arguments**: Paths for source and destination folders, synchronization interval, and log file path are provided via command-line arguments.

## Installation

To use this tool, you need Python 3.x installed on your machine. This tool relies only on built-in libraries, so no additional installation is required.

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/manino203/FileSync.git
   
2. **Run the script:**
    ```bash
   python main.py <source_folder> <replica_folder> <interval_in_seconds> <log_file_path> [--delta_encoding]