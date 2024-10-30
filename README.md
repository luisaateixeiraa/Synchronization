# Sync Script

This script synchronizes files between a `source` folder and a `replica` folder at specified intervals.

## Installation

Requires **Python 3.8** or later. To install, clone this repository and ensure Python is installed.

## Usage

Run the following command to start file synchronization:

```bash
python synchronization.py [directory_path] [sync_interval] [log_path]
```
    -directory_path: Path to main directory.
    -sync_interval: Time interval in seconds.
    -log_path: Path to save the log file.

## Example

```bash
python synchronization.py C:\sync_folder 10 C:\sync_folder\logs.txt
```
This example syncs every 10 seconds.