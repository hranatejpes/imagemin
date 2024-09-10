#!/usr/bin/env python3

import os
import sys
import subprocess

def install_and_import(package):
	try:
		__import__(package)
	except ImportError:
		print(f"The '{package}' module is not installed, trying to install...")
		try:
			subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
		except subprocess.CalledProcessError:
			print(f"Error: The '{package}' module cannot be installed. Check permissions and try again.")
			sys.exit(1)

		print(f"The '{package}' module has been installed.")
		globals()[package] = __import__(package)

install_and_import("PIL")
install_and_import("pillow_heif")

from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def resize_and_convert(input_dir, output_dir, conversion_type = "webp", max_size = 1600):
	# Check if source and target directories are set
	if not input_dir or not output_dir:
		print("Error: Source or target directory is not defined.")
		sys.exit(1)

	# Check if source directory exists
	if not os.path.isdir(input_dir):
		print(f"Error: The source directory '{input_dir}' does not exist.")
		sys.exit(1)

	# Check if target directory exists and if not, create it
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# Set conversion type
	if conversion_type.lower() == "webp":
		valid_extensions = ('.jpg', '.jpeg', '.png', '.heic')
		output_extension = ".webp"
	elif conversion_type.lower() == "jpg":
		valid_extensions = ('.webp', '.heic')
		output_extension = ".jpg"
	else:
		print("Error: Conversion type is not valid. Use 'webp' or 'jpg'.")
		sys.exit(1)

	# Go through all files in source directory
	for root, dirs, files in os.walk(input_dir):
		for file in files:
			# Check file type
			if file.lower().endswith(valid_extensions):
				input_path = os.path.join(root, file)

				# Open the image
				try:
					img = Image.open(input_path)

					# Get the dimensions
					width, height = img.size

					# Set the new dimensions with keep an aspect ratio
					if max(width, height) > max_size:
						if width > height:
							new_width = max_size
							new_height = int((max_size / width) * height)
						else:
							new_height = max_size
							new_width = int((max_size / height) * width)
					else:
						new_width, new_height = width, height

					# Resize the image
					img = img.resize((new_width, new_height), Image.LANCZOS)

					# Target path
					output_filename = os.path.splitext(file)[0] + output_extension
					output_path = os.path.join(output_dir, output_filename)

					# Optimize the image
					if conversion_type.lower() == "webp":
						img.save(output_path, "WEBP", quality=85, optimize=True, method=6)
					elif conversion_type.lower() == "jpg":
						img = img.convert("RGB")
						img.save(output_path, "JPEG", quality=85, optimize=True)

					print(f"File '{file}' was successfully converted and save to '{output_filename}'.")

				except Exception as e:
					print(f"Error while processing '{file}': {e}")

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='A script for an image conversion and optimization.')
	parser.add_argument('input_dir', type=str, help='Source (input) directory')
	parser.add_argument('output_dir', type=str, help='Target (output) directory')
	parser.add_argument('--conversion', type=str, choices=['webp', 'jpg'], default='webp', help='Conversion type: "webp" or "jpg" (default: webp)')
	parser.add_argument('--max_size', type=int, default=1600, help='Maximum image size (width or height, default: 1600)')

	args = parser.parse_args()
	resize_and_convert(args.input_dir, args.output_dir, args.conversion, args.max_size)
