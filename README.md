# python-to-html

## Description

`pretty.py` is a Python program that reads Python code from an input file and generates a well-formatted HTML representation of the code. The output HTML file includes syntax highlighting, line numbers, and other useful features that make it easy to view and understand Python code in a web browser. This tool can be used to showcase Python code in a visually appealing and interactive format, making it easier for developers to navigate, debug, and understand code.

### Key Features
- **Syntax Highlighting**: Displays Python code with syntax highlighting for better readability.
- **Line Numbers**: Includes line numbers alongside the code for easier navigation.
- **Code Statistics**: Generates a summary of the code, such as the number of comments and functions, providing useful insights into the code structure.
- **Rendered Code Block**: The Python code is displayed with enhanced formatting in a web page, making it easy to read.
- **Self-contained HTML Output**: The generated HTML file is self-contained, meaning it doesn’t rely on external JavaScript or CSS files.

## Usage

You can use `pretty.py` on the command line to convert any Python file to HTML. For example:

```bash
python3 pretty.py example.py > example.html
```

For example, if you want to generate a nicely formatted HTML version of the `pretty.py` file itself, you can run the following command:

```bash
python3 pretty.py pretty.py > pretty.html