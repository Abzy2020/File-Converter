## File-Converter
Convert files to different formats

Need to create a ConvertAPI account and set API_SECRET, API_KEY, and TOKEN environment variables
The TOKEN must be generated through the command line like so:

python converter.py -t

Convert a File:

python converter.py <file_path> <fmt_before_convert> <fmt_after_convert> <new_file_name>