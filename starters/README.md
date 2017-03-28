# starter script for BlueSky

Install the script `use_bluesky.sh` (from this directory)
into your `~/bin` folder (or some place in your PATH).
Consider examining and modifying the internal defaults
to suit your installation.

Usage:

	use_bluesky.sh [profile_name]

Command Options

	profile_name : name of existing ipython profile to use (default: $BLUESKY_PROFILE)

Environment Variable(s) (these are optional)

	BLUESKY_BIN_DIR : absolute path to directory containing Python with BlueSky installed

The use_bluesky.sh script has default values for the environment variable(s).

	BLUESKY_BIN_DIR__INTERNAL_DEFAULT : (the first of these to be found, in order)
	                                 "~/Apps/BlueSky/bin"
	                                 or "/APSshare/anaconda3/BlueSky/bin"
	                                 or "." (the fallback default if none of those are found)
	BLUESKY_PROFILE__INTERNAL_DEFAULT : "bluesky"
