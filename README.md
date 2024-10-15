

# Simple PDF Analyzer

**Version 1.0**
### Creator: Juhani Merilehto - @juhanimerilehto - Jyväskylä University of Applied Sciences (JAMK), Likes institute

## Overview

Simple PDF Analyzer was created for anayzing Data from semi-structured content, and is a Python-based tool that processes PDF files page-by-page. It extracts relevant information
such as  names, Business ID, and Personnel counts - provided that they are enough explicitly stated; and formats them into structured Excel files. The tool utilizes the Claude API by Anthropic for natural language understanding and data extraction from the text in PDFs.

## Features

- **PDF Text Extraction**: Extracts text from multi-page PDF files.
- **AI-Powered Data Extraction**: Uses Anthropic's Claude API to analyze text and extract specific information.
- **Excel Output**: Converts the extracted data into clean Excel files, making it easy to work with.
- **Logging**: Detailed logs for tracking the process and diagnosing any issues.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/juhanimerilehto/simple-pdf-analysis.git
   cd simple-pdf-analysis
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory to store your API key and folders configuration:

   ```
   ANTHROPIC_API_KEY=your_api_key_here
   PDF_INPUT_FOLDER=./PDFs  # (Optional, default is ./PDFs)
   EXCEL_OUTPUT_FOLDER=./ExcelFiles  # (Optional, default is ./ExcelFiles)
   MAX_TOKENS=4000  # (Optional, default is 4000)
   ```

## Usage

1. Place your PDF files into the folder specified in the `.env` file (default: `./PDFs`).
2. Run the script:

   ```bash
   python simple-pdf-analysis.py
   ```

3. After processing, Excel files with extracted data will be saved in the specified output folder (default: `./ExcelFiles`).

## Logging

The script generates detailed logs in `script.log` to help monitor the progress and debug any issues.

## Configuration

You can configure the following environment variables in the `.env` file:

- **ANTHROPIC_API_KEY**: Your API key for the Claude API.
- **PDF_INPUT_FOLDER**: Folder where input PDFs are located (default: `./PDFs`).
- **EXCEL_OUTPUT_FOLDER**: Folder where output Excel files will be saved (default: `./ExcelFiles`).
- **MAX_TOKENS**: Token limit for API responses (default: 4000).

## Contributions

We welcome contributions! Feel free to fork the repository and submit pull requests.

## Credits

- **Juhani Merilehto (@juhanimerilehto)** – Project Lead and Developer
- **JAMK Likes** – Organization sponsor, providing use case and requirements for data analysis.

## License

This project is licensed for free use under the condition that proper credit is given to Juhani Merilehto (@juhanimerilehto). You are free to use, modify, and distribute this project, provided that you mention the original author and do not hold him liable for any consequences arising from the use of the software.

