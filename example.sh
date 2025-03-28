#!/bin/bash

# Check if a file path is provided as the first argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path_to_json_file>"
  exit 1
fi

# Read the JSON content from the provided file
JSON_FILE="$1"
if [ ! -f "$JSON_FILE" ]; then
  echo "Error: File '$JSON_FILE' not found!"
  exit 1
fi

# Send the JSON content to the API
curl -X POST -H "Content-Type: application/json" \
--data-binary @"$JSON_FILE" \
http://127.0.0.1:5000/translate_srt