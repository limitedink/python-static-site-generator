# Python Static Site Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A custom static site generator built in Python, designed to convert Markdown content into a fully functional HTML website. Features recursive directory handling, automatic static asset copying, and support for GitHub Pages deployment with configurable base paths.

## Features

- **Markdown to HTML Conversion**: Parses Markdown files (headings, paragraphs, links, images, code blocks, blockquotes) into clean HTML.
- **Recursive Site Building**: Handles nested directories and generates pages with proper structure.
- **Static Asset Management**: Automatically copies images, CSS, and other assets to the output directory.
- **GitHub Pages Ready**: Supports basepath configuration for subdirectory deployments (e.g., `https://username.github.io/repo-name/`).
- **Customizable Templates**: Uses HTML templates for consistent page layouts.
- **Command-Line Interface**: Easy to run locally or in production builds.

## Demo

Check out the live site: [https://limitedink.github.io/python-static-site-generator/](https://limitedink.github.io/python-static-site-generator/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/limitedink/python-static-site-generator.git
   cd python-static-site-generator
   ```

2. Ensure Python 3.x is installed.

3. No external dependencies required (uses standard libraries like `os` and `shutil`).

## Usage

### Local Development
Run the generator to build the site locally:
```bash
python3 src/main.py
```
- This builds to `./docs/` with default basepath `/`.
- Open `./docs/index.html` in a browser to preview.

### Production Build (for GitHub Pages)
1. Build with the repo basepath:
   ```bash
   ./build.sh
   ```
   - This generates `./docs/` with URLs prefixed for `https://limitedink.github.io/python-static-site-generator/`.

2. Deploy to GitHub Pages:
   - Commit and push `./docs/` (GitHub Pages serves from the `docs/` folder on the `main` branch).
   - Enable in repo Settings > Pages: Source = "main", Folder = "/docs".

### Project Structure
```
python-static-site-generator/
├── src/
│   ├── main.py              # Entry point
│   ├── gencontent.py        # Page generation logic
│   ├── copy_static.py       # Static file copying
│   └── ...                  # Other modules (e.g., markdown_utils.py)
├── content/                 # Markdown source files
├── static/                  # Static assets (images, CSS)
├── template.html            # HTML template
├── build.sh                 # Production build script
├── docs/                    # Generated site (for GitHub Pages)
├── LICENSE                  # MIT License
└── README.md                # This file
```

## How It Works

1. **Content Parsing**: Reads Markdown from `content/`, converts to HTML nodes.
2. **Template Application**: Injects content into `template.html`.
3. **Static Copying**: Recursively copies `static/` to the output dir.
4. **Basepath Handling**: Adjusts links (e.g., `href="/css"` → `href="/repo-name/css"`) for deployment.
5. **Output**: Generates HTML in `./docs/` ready for hosting.

## Technologies Used

- **Python**: Core logic and file handling.
- **Markdown Parsing**: Custom implementation for headings, lists, quotes, etc.
- **HTML Generation**: Builds semantic HTML with proper structure.
- **GitHub Pages**: Free hosting for static sites.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repo.
2. Create a feature branch: `git checkout -b feature-name`.
3. Make changes and test locally.
4. Submit a pull request with a clear description.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
