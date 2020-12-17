## Storage Capacity Checker

This small python script will loop through the Volumes attached to a Mac and create a MacOS notification for each volume that has less storage space than the assigned threshold.

#### SETUP:
Set the constant values as desired:
- *AVAILABLE_SPACE_THRESHOLD* - Amount of available space you want to use as a trigger. ie, 20 would mean any volumes with less than 20% available space are alerted.
- *MINIMUM_DRIVE_SIZE_TO_CHECK_GB* - Minimum size of volumes you want to check in GB. Volumes lower than this won't be checked.
- *VOLUMES_TO_IGNORE* - A list of any volumes you want to ignore entirely.
- *VOLUMES_TO_INCLUDE* - Optionally choose only volumes you want to include. If volumes are added here, all other volumes are ignored.


This script is designed to be used in conjunction with crontab to run every x minutes/hours/days.