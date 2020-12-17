# CRONTAB TO RUN EVERY 6 HOURS ON WEEKDAYS: 0 */6 * * * python3 /path/to/script/storage_capacity_checker.py >/dev/null 2>&1

from os import listdir
import shutil
import subprocess

AVAILABLE_SPACE_THRESHOLD = 20 # Amount of available space you want to use as a trigger. ie, 20 would mean any volumes with less than 20% available space are alerted.
MINIMUM_DRIVE_SIZE_TO_CHECK_GB = 100 # Minimum size of volumes you want to check in GB. Volumes lower than this won't be checked.
VOLUMES_TO_IGNORE = ["IGNORE_ME", "IGNORE_ME_TOO"] # A list of any volumes you want to ignore entirely.
VOLUMES_TO_INCLUDE = [] # Optionally choose only volumes you want to include. If volumes are added here, all other volumes are ignored.

print("Running storage capacity check...")

def main():
  if len(VOLUMES_TO_INCLUDE) > 0:
    print("Using VOLUMES_TO_INCLUDE whitelist...")
    for volume in listdir("/Volumes"):
      if volume in VOLUMES_TO_INCLUDE:
        check_volume(volume)
      else:
        print(f"\t- Ignoring {volume}. Not in VOLUMES_TO_INCLUDE whitelist.")
  else:
    for volume in listdir("/Volumes"):
      check_volume(volume)
  print("Finished!")

    
def is_above_threshold(used_percentage):
  return used_percentage > (100 - AVAILABLE_SPACE_THRESHOLD)


def is_above_minimum_capacity(drive_capacity):
  return drive_capacity > (MINIMUM_DRIVE_SIZE_TO_CHECK_GB * 1073741824)


def is_not_ignored(volume):
  return volume not in VOLUMES_TO_IGNORE


def check_volume(volume):
  storage_stats = shutil.disk_usage("/Volumes/" + volume)
  used_percentage = round((storage_stats.used / storage_stats.total) * 100)

  if is_not_ignored(volume):
    if is_above_minimum_capacity(storage_stats.total) and is_above_threshold(used_percentage):
      print("\t- Storage is getting low on volume: " + volume)
      notification_message = f'display alert "Storage space is getting low (below {AVAILABLE_SPACE_THRESHOLD}%)" message "{volume} has {100 - used_percentage}% remaining"'
      subprocess.run(["osascript", "-e", 'tell application "Finder"', "-e", "activate", "-e", notification_message, "-e", "end tell"])
    else:
      print(f"\t- {volume} is OK, {100 - used_percentage}% available.")
  else:
    print(f"\t- Skipping {volume}, volume is in VOLUMES_TO_IGNORE")

if __name__ == "__main__":
    main()