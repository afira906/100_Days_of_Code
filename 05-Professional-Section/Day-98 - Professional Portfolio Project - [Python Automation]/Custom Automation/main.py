import shutil
from pathlib import Path
import logging
from datetime import datetime
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_organizer.log"),
        logging.StreamHandler()
    ]
)


def organize_files(folder_path, dry_run=False, delete_old=False, days_threshold=30):
    """
    Organize files in the specified folder by file type

    Args:
        folder_path (Path): Path to the folder to organize
        dry_run (bool): If True, only show what would be done without actually moving files
        delete_old (bool): If True, delete files older than days_threshold
        days_threshold (int): Number of days after which files are considered old
    """
    # Define file type categories
    file_categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".heic"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".m4v", ".webm"],
        "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".json", ".xml"],
        "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
        "Presentations": [".ppt", ".pptx", ".key", ".odp"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
        "eBooks": [".epub", ".mobi", ".azw3"]
    }

    # Create folders if they don't exist
    for category in file_categories.keys():
        category_path = folder_path / category
        if not category_path.exists() and not dry_run:
            category_path.mkdir()
            logging.info(f"Created folder: {category}")

    # Create an 'Other' folder for uncategorized files
    other_path = folder_path / "Other"
    if not other_path.exists() and not dry_run:
        other_path.mkdir()

    # Organize files
    moved_files_count = 0
    deleted_files_count = 0
    current_time = datetime.now()

    for file_path in folder_path.iterdir():
        # Skip directories and the organizer script itself
        if file_path.is_dir() or file_path.name == __file__:
            continue

        # Check if file is old
        file_mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        file_age = (current_time - file_mod_time).days

        if delete_old and file_age > days_threshold:
            if dry_run:
                logging.info(f"Would delete old file: {file_path.name} ({file_age} days old)")
            else:
                try:
                    file_path.unlink()
                    logging.info(f"Deleted old file: {file_path.name} ({file_age} days old)")
                    deleted_files_count += 1
                except Exception as e:
                    logging.error(f"Error deleting {file_path.name}: {str(e)}")
            continue

        # Get file extension
        file_extension = file_path.suffix.lower()

        # Find the appropriate category for the file
        moved = False
        for category, extensions in file_categories.items():
            if file_extension in extensions:
                category_path = folder_path / category
                try:
                    # Check if file already exists in destination
                    destination = category_path / file_path.name
                    if destination.exists():
                        # Add timestamp to avoid overwriting
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                        destination = category_path / new_name

                    if dry_run:
                        logging.info(f"Would move {file_path.name} to {category}")
                    else:
                        shutil.move(str(file_path), str(destination))
                        logging.info(f"Moved {file_path.name} to {category}")

                    moved_files_count += 1
                    moved = True
                    break
                except Exception as e:
                    logging.error(f"Error moving {file_path.name}: {str(e)}")

        # If file doesn't match any category, move to 'Other'
        if not moved:
            try:
                destination = other_path / file_path.name
                if destination.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                    destination = other_path / new_name

                if dry_run:
                    logging.info(f"Would move {file_path.name} to Other")
                else:
                    shutil.move(str(file_path), str(destination))
                    logging.info(f"Moved {file_path.name} to Other")

                moved_files_count += 1
            except Exception as e:
                logging.error(f"Error moving {file_path.name} to Other: {str(e)}")

    return moved_files_count, deleted_files_count


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by file type")
    parser.add_argument("--folder", "-f", default="~/Downloads",
                        help="Folder to organize (default: ~/Downloads)")
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="Show what would be done without actually doing it")
    parser.add_argument("--delete-old", "-x", action="store_true",
                        help="Delete files older than the specified threshold")
    parser.add_argument("--days", "-t", type=int, default=30,
                        help="Days threshold for deleting old files (default: 30)")

    args = parser.parse_args()

    # Expand user directory and resolve path
    folder_path = Path(args.folder).expanduser().resolve()

    if not folder_path.exists():
        print(f"Error: The folder {folder_path} does not exist.")
        return

    print(f"Organizing files in: {folder_path}")
    if args.dry_run:
        print("DRY RUN: No files will be moved or deleted")
    if args.delete_old:
        print(f"Will delete files older than {args.days} days")

    try:
        moved_count, deleted_count = organize_files(
            folder_path,
            dry_run=args.dry_run,
            delete_old=args.delete_old,
            days_threshold=args.days
        )

        print(f"Organization complete!")
        if not args.dry_run:
            print(f"Moved {moved_count} files")
            if args.delete_old:
                print(f"Deleted {deleted_count} old files")
        else:
            print(f"Would move {moved_count} files")
            if args.delete_old:
                print(f"Would delete {deleted_count} old files")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Script error: {str(e)}")


if __name__ == "__main__":
    main()
