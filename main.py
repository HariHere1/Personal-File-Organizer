import argparse
import json
import os
import shutil
import sys
import time


DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "categories.json"
)


def load_categories(config_path):
    """Load a category-to-extension JSON file into an extension lookup table."""
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Configuration file not found: {}".format(config_path))
        return None
    except (OSError, json.JSONDecodeError) as error:
        print("Could not read configuration file: {}".format(error))
        return None

    if not isinstance(config, dict):
        print("Invalid configuration: the root must be a JSON object.")
        return None

    categories = {}
    for category, extensions in config.items():
        if (not isinstance(category, str) or not category or
                category in (".", "..") or os.path.basename(category) != category):
            print("Invalid category name: {!r}".format(category))
            return None
        if not isinstance(extensions, list):
            print("Extensions for '{}' must be a list.".format(category))
            return None

        for extension in extensions:
            if not isinstance(extension, str) or not extension.strip():
                print("Each extension must be a non-empty string.")
                return None
            normalized_extension = extension.strip().lower()
            if not normalized_extension.startswith("."):
                normalized_extension = "." + normalized_extension
            categories[normalized_extension] = category

    if not categories:
        print("Invalid configuration: add at least one file extension.")
        return None

    return categories


def validate_path(folder_path):
    """Validate that the provided path exists and is a directory."""
    if os.path.isdir(folder_path):
        print("\nValid path.\n")
        return True

    print("\nInvalid path.")
    return False


def run_dry_run(folder_path, categories):
    """Build and display an in-memory plan of collision-free file moves."""
    print("--- DRY RUN PREVIEW ---")
    planned_moves = []
    simulated_destinations = set()

    for element in os.listdir(folder_path):
        source_file_path = os.path.join(folder_path, element)

        # Ignore subfolders and hidden files such as .env or .DS_Store.
        if not os.path.isfile(source_file_path) or element.startswith("."):
            continue

        filename, extension = os.path.splitext(element)
        category = categories.get(extension.lower(), "Others")
        dest_folder = os.path.join(folder_path, category)
        target_file_path = os.path.join(dest_folder, element)
        count = 1

        # Check both the disk and destinations already reserved in this plan.
        while os.path.exists(target_file_path) or target_file_path in simulated_destinations:
            target_file_path = os.path.join(
                dest_folder, "{} ({}){}".format(filename, count, extension)
            )
            count += 1

        simulated_destinations.add(target_file_path)
        final_name = os.path.basename(target_file_path)
        planned_moves.append({
            "src": source_file_path,
            "dest_folder": dest_folder,
            "dest_file": target_file_path,
            "element": element,
            "category": category,
            "final_name": final_name,
        })

        if final_name != element:
            print("Would move: '{}' -> '{}/' (renamed to '{}')".format(
                element, category, final_name
            ))
        else:
            print("Would move: '{}' -> '{}/'".format(element, category))

    return planned_moves


def execute_moves(planned_moves):
    """Create category folders and execute the approved move plan."""
    print("\n--- EXECUTING MOVES ---")
    category_counts = {}

    for move in planned_moves:
        if not os.path.exists(move["dest_folder"]):
            os.mkdir(move["dest_folder"])

        try:
            shutil.move(move["src"], move["dest_file"])
            category = move["category"]
            category_counts[category] = category_counts.get(category, 0) + 1

            if move["final_name"] != move["element"]:
                print("Moving {} (renamed to {}) to {}".format(
                    move["element"], move["final_name"], category
                ))
            else:
                print("Moving {} to {}".format(move["element"], category))
        except PermissionError:
            print("Warning: {} is locked or open. Skipped.".format(move["element"]))
        except OSError as error:
            print("Error moving {}: {}".format(move["element"], error))

    return category_counts


def print_summary(category_counts):
    """Print the final category-by-category report."""
    print("\n--- Organization Summary ---")
    if not category_counts:
        print("No files were moved.")
        return

    for category_name, file_count in category_counts.items():
        print("{}: {}".format(category_name, file_count))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A safety-first Python file organizer with dry-run previews."
    )
    parser.add_argument(
        "path", nargs="?", default=None,
        help="Path to the directory you want to organize"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview planned moves without changing files"
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Apply changes without asking for confirmation"
    )
    parser.add_argument(
        "--config", default=DEFAULT_CONFIG_PATH,
        help="Path to a JSON category file (default: categories.json)"
    )
    return parser.parse_args()


def main():
    """Run the application controller."""
    args = parse_arguments()
    print("=====================================\nPERSONAL FILE ORGANIZER\n=====================================")

    categories = load_categories(args.config)
    if categories is None:
        sys.exit(1)

    folder_path = args.path
    if not folder_path:
        folder_path = input("\nEnter the folder path to organize: ").strip()

    if not validate_path(folder_path):
        sys.exit(1)

    planned_moves = run_dry_run(folder_path, categories)
    if not planned_moves:
        print("\nNo files to move. Exiting.")
        return

    print("\nTotal files to move: {}".format(len(planned_moves)))
    if args.dry_run:
        print("Dry-run mode active. No files were changed.")
        return

    if args.yes:
        print("Auto-applying changes (-y flag set)...")
        confirmed = True
    else:
        confirmed = input("Apply these changes? (y/n): ").strip().lower() == "y"

    if not confirmed:
        print("Action cancelled. No files were changed.")
        return

    print_summary(execute_moves(planned_moves))


if __name__ == "__main__":
    main()
