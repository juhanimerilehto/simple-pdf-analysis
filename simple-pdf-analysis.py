# PDF Semi-Structured Data Extraction and Analysis with Anthropics Claude API
# Created to search for three types of information for headers and create an Excel file with the results
# Version: 1.0
# Date: 2024-10-15
# Creator: Juhani Merilehto - @juhanimerilehto
# Sponsor: Jyväskylä University of Applied Sciences (JAMK), Likes institute


import os
import fitz  # PyMuPDF for PDF handling
import anthropic
import pandas as pd
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level set to INFO, change to DEBUG for more verbosity
    format='%(asctime)s - %(levelname)s - %(message)s',  # Standard logging format with timestamps
    handlers=[
        logging.FileHandler("script.log"),  # Log to a file called 'script.log'
        logging.StreamHandler()  # Also output logs to the console
    ]
)

# Load environment variables from .env file
load_dotenv()

# Initialize the Anthropic client using the API key from environment variables
client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

logging.info("Script is running")  # Log that the script has started

def extract_and_query_page(pdf_path, page_number, api_key, max_tokens=4000):  # Adjusted max_tokens default to 4000
    # Open the PDF document
    with fitz.open(pdf_path) as doc:
        page = doc.load_page(page_number)  # Load the specific page
        text = page.get_text()  # Extract text from the page
        logging.info(f"Extracting text from page {page_number+1}/{len(doc)}")  # Log page extraction progress
        logging.debug(f"Extracted text: {text[:50]}")  # Log first 50 characters of the extracted text for debugging
        response = query_claude_api(text, api_key, max_tokens)  # Query the Claude API with extracted text
        # Assuming 'response' is a list of 'ContentBlock' objects, extract the first text element
        if response and hasattr(response[0], 'text'):  # Check if the response has the 'text' attribute
            return response[0].text  # Return the text if it's available
        else:
            logging.warning("Response is not as expected or missing 'text' attribute")  # Log unexpected responses
            return ""  # Return empty string if response is not as expected

# Query the Claude API using provided text and the system's API key
def query_claude_api(text, api_key, max_tokens=4000):  # Adjusted max_tokens to 4000 to match input limits
    # System prompt to set the context for Claude
    system_prompt = "You are an AI assistant helping to organize data from a PDF file."
    
    # User-specific prompt to instruct Claude on how to analyze the text
    human_prompt = f"""Analyze the following text from a PDF report and extract the name, business ID, and personnel count.

Text:
{text}

Present your findings in a structured format with each entry separated by commas. Each entry should list the name, business ID, and personnel count, in that order.
Format your response as: Name, business ID, personnel 
There is no need for additional information other than the columns. When encountering more than one personnel count, use the number that focuses on the sport, not the whole organization.
On personnel count information, those that are licence holders and sport practitioners, should be the priority numbers, i.e. "lisenssit".

If there is no information on business ID, then mark it as "NA". Full names of clubs are prioritized over i.e., acronyms.
If the data is missing business ID or the personnel count, mark them as NA.
The order should be the same as the original text.
The format MUST HAVE the three columns and ONLY the three columns. Be extremely accurate or I will lose my job!"""

    # The message structure for the API
    messages = [
        {"role": "user", "content": human_prompt}
    ]

    try:
        # Call the Claude API with the prompt and message
        response = client.messages.create(
            model="claude-3-opus-20240229",
            system=system_prompt,  # Send the system prompt to set the context
            messages=messages,  # Send the user prompt
            max_tokens=max_tokens  # Limit the response to a certain number of tokens (adjusted to 4000)
        )
        return response.content  # Return the full response content from Claude
    except Exception as e:
        logging.error(f"Error in API response: {e}")  # Log the error in case of API failure
        return f"Error in API response: {e}"  # Return the error message as the response

# Parse the Claude response and convert it into a DataFrame-friendly format
def parse_claude_response_to_dataframe(response_content, all_data):
    lines = response_content.strip().split('\n')  # Split response into lines
    for line in lines:
        if line:  # Ensure line is not empty
            # Split by commas and keep only the first three elements: Name, business ID, personnel 
            data = [element.strip() for element in line.split(',')][:3]
            all_data.append(data)  # Append the parsed data to the list
    return all_data  # Return the updated list

# Process all PDF files in the input folder and output results to Excel
def process_pdfs(input_folder, output_folder, api_key, max_tokens=4000):  # max_tokens set to 4000 for input/output control
    for filename in sorted(os.listdir(input_folder)):  # Iterate over all files in the input folder
        if filename.lower().endswith('.pdf'):  # Process only PDF files
            pdf_path = os.path.join(input_folder, filename)  # Construct full path to PDF file
            all_data = []  # Initialize list to accumulate data from all pages
            logging.info(f"Processing PDF file: {filename}")  # Log the start of processing for the file
            with fitz.open(pdf_path) as doc:  # Open the PDF file
                for page_number in range(len(doc)):  # Iterate over all pages in the document
                    # Extract text from each page and query the Claude API
                    response_content = extract_and_query_page(pdf_path, page_number, api_key, max_tokens)
                    # Parse API response and add it to the accumulated data
                    all_data = parse_claude_response_to_dataframe(response_content, all_data)

            # Once all pages are processed, create a DataFrame from the accumulated data
            df = pd.DataFrame(all_data, columns=['Name', 'business ID', 'personnel'])
            
            # Sanitize the filename for Excel file creation (remove unwanted characters)
            sanitized_filename = filename.replace('.PDF', '').replace('.pdf', '')
            sanitized_filename = sanitized_filename.replace("+", "_").replace(",", "").replace(" ", "_")
            excel_filename = sanitized_filename + '.xlsx'  # Define the Excel filename
            excel_path = os.path.join(output_folder, excel_filename)  # Define the path for saving the Excel file
            
            # Save the DataFrame to an Excel file
            df.to_excel(excel_path, index=False)
            
            logging.info(f"Processed {filename} and saved Excel file to {excel_path}")  # Log the successful file save

# Configuration and execution using environment variables
api_key = os.getenv('ANTHROPIC_API_KEY')  # Retrieve API key from environment variables
input_folder = os.getenv('PDF_INPUT_FOLDER', './PDFs')  # Default input folder is './PDFs' if not set
output_folder = os.getenv('EXCEL_OUTPUT_FOLDER', './ExcelFiles')  # Default output folder is './ExcelFiles' if not set
max_tokens = int(os.getenv('MAX_TOKENS', 4000))  # Set the token limit from environment or default to 4000

# Ensure the output directory exists; if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Start processing the PDFs
process_pdfs(input_folder, output_folder, api_key, max_tokens)
