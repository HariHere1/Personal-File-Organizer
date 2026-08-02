import os
import shutil
import sys
import time

# Global Configuration Constants
FILE_CATEGORIES = {
    ".png": "Images", ".jpg": "Images", ".jpeg": "Images", ".webp": "Images",
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".mp3": "Audio", ".m4a": "Audio", ".wav": "Audio",
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos"
}


def validate_path(folder_path):

    time.sleep(0.3)
    if os.path.isdir(folder_path):
        time.sleep(0.5)
        print("\nValid path\n")
        time.sleep(0.5)
        return True
    else:
        time.sleep(0.3)
        print("\nInvalid path")
        return False


def run_dry_run(folder_path, categories):

    print("--- DRY RUN PREVIEW ---")
    time.sleep(0.5)
    planned_moves = []
    simulated_destinations = set()

    for element in os.listdir(folder_path):
        source_file_path = os.path.join(folder_path, element)

        # Skip folders and hidden system files
        if not os.path.isfile(source_file_path) or element.startswith('.'):
            continue

        filename, extension = os.path.splitext(element)
        category = categories.get(extension.lower(), "Others")
        dest_path = os.path.join(folder_path, category)

        # Duplicate collision math
        target_file_path = os.path.join(dest_path, element)
        count = 1

        while os.path.exists(target_file_path) or target_file_path in simulated_destinations:
            new_filename = f"{filename} ({count}){extension}"
            target_file_path = os.path.join(dest_path, new_filename)
            count += 1

        simulated_destinations.add(target_file_path)
        final_name = os.path.basename(target_file_path)

        planned_moves.append({
            'src': source_file_path,
            'dest_folder': dest_path,
            'dest_file': target_file_path,
            'element': element,
            'category': category,
            'final_name': final_name
        })

        if final_name != element:
            print(f"Would move: '{element}' --> '{category}/' (Renaming to '{final_name}')")
        else:
            print(f"Would move: '{element}' --> '{category}/'")

        time.sleep(0.15)  # Slight pause between scanning items

    return planned_moves


def execute_moves(planned_moves):

    print("\n--- EXECUTING MOVES ---")
    time.sleep(0.5)
    category_counts = {}

    for move in planned_moves:
        if not os.path.exists(move['dest_folder']):
            os.mkdir(move['dest_folder'])

        try:
            shutil.move(move['src'], move['dest_file'])
            category_counts[move['category']] = category_counts.get(move['category'], 0) + 1

            if move['final_name'] != move['element']:
                print(f"Moving {move['element']} (renamed to {move['final_name']}) to {move['category']}")
            else:
                print(f"Moving {move['element']} to {move['category']}")

            time.sleep(0.3)  # Delay between individual moves

        except PermissionError:
            print(f"{move['element']} is either locked or the file is currently open")
            time.sleep(0.3)
        except Exception as e:
            print(f"Error moving {move['element']} : {e}")
            time.sleep(0.3)

    return category_counts


def print_summary(category_counts):

    time.sleep(0.5)
    print("\n--- Organization Summary ---")
    time.sleep(0.3)

    if not category_counts:
        print("No files were moved.")
        return

    for category_name, file_count in category_counts.items():
        print(f"\n{category_name}: {file_count}")
        time.sleep(0.2)


def main():
    """Main application controller."""
    print("=====================================\n\tPERSONAL FILE ORGANIZER\n=====================================")
    time.sleep(0.3)
    folder_path = input("\nEnter the path of the folder you want to organize & store : ").strip()

    # Step 1: Validate Path
    if not validate_path(folder_path):
        sys.exit()

    # Step 2: Dry Run
    planned_moves = run_dry_run(folder_path, FILE_CATEGORIES)

    time.sleep(0.5)
    if not planned_moves:
        print("\nNo files to move. Exiting.")
        sys.exit()

    # Step 3: Confirmation
    print(f"\nTotal files to move: {len(planned_moves)}")
    time.sleep(0.3)
    confirm = input("Do you want to apply these changes? (y/n): ").strip().lower()

    if confirm != 'y':
        time.sleep(0.3)
        print("Action cancelled. No files were touched.")
        sys.exit()

    # Step 4: Execution & Summary
    category_counts = execute_moves(planned_moves)
    print_summary(category_counts)


# Entry point
if __name__ == "__main__":
    main()