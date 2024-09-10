# Web image converter and optimizer

This tool is designed to optimize and convert images for use on the web. It can process and optimize images in JPG, WEBP, PNG and HEIC formats, and save the resulting file as JPG or WEBP. 

## Usage

The -h (--help) switch is used to display help.

*Required parameters:*
- input_dir - source directory
- output_dir - destination directory

*Optional parameters:*
- --max_size - max image size (height or width, default 1600)
- --conversion - conversion type (webp or jpg, default webp)

### Example of use:

```imagemin.py ./src ./dist --max_size=1200```

Converts images from "src" directory into "dist" directory, to webp format, with max size limited to 1200px (width or height, the ratio is kept).
