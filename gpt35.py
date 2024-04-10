import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from g4f.client import Client  # Adjust this import to your actual GPT client's import path
import sys

# Assuming you have a configured GPT client that can send requests
client = Client()

def find_files(directory="."):
    """Find the Excel and corresponding text file in the specified directory."""
    for file in os.listdir(directory):
        if file.endswith(".xlsx"):
            excel_file = os.path.join(directory, file)
            txt_file = os.path.splitext(excel_file)[0] + ".txt"
            if os.path.exists(txt_file):
                return excel_file, txt_file
    return None, None

def load_prompt(txt_file):
    """Load the prompt from the text file."""
    with open(txt_file, 'r', encoding='utf-8') as file:
        return file.read().strip()

def process_row(prompt, row_content, row_number, excel_basename, response_dir):
    """Send the row content along with the prompt to the GPT API and save the response."""
    full_prompt = f"{prompt} {row_content}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify your model here
            messages=[{"role": "user", "content": full_prompt}]
        ).choices[0].message.content
        
        response_filename = os.path.join(response_dir, f"{excel_basename}_{row_number}.txt")
        with open(response_filename, 'w', encoding='utf-8') as file:
            file.write(response)
        return True
    except Exception as e:
        print(f"Error processing row {row_number}: {e}")
        return False

def main():
    start_time = datetime.now()
    excel_file, txt_file = find_files()
    if not excel_file or not txt_file:
        print("Excel or text file not found.")
        return
    
    prompt = load_prompt(txt_file)
    dataframe = pd.read_excel(excel_file)
    responses_dir = os.path.splitext(excel_file)[0] + "_responses"
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)

    # Identify the next row to process
    processed_files = os.listdir(responses_dir)
    next_row = max([int(f.split('_')[-1].split('.')[0]) for f in processed_files] + [0])
    total_rows = len(dataframe)
    rows_to_process = total_rows - next_row

    if rows_to_process == 0:
        print("All rows have already been processed.")
        return

    processed_count = 0
    max_requests = 50  # Limit to 50 requests per run

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for index, row in dataframe.iterrows():
            row_number = index + 1
            if row_number <= next_row:
                continue  # Skip already processed rows
            if processed_count >= max_requests:
                break  # Stop after processing 50 rows

            excel_basename = os.path.splitext(os.path.basename(excel_file))[0]
            futures.append(executor.submit(process_row, prompt, row['Text'], row_number, excel_basename, responses_dir))
            processed_count += 1

        # Real-time progress updates moved outside the futures submission loop
        for i, future in enumerate(as_completed(futures)):
            elapsed_time = (datetime.now() - start_time).total_seconds()
            rows_processed = i + 1
            estimated_time_per_row = elapsed_time / rows_processed
            estimated_total_time = estimated_time_per_row * rows_to_process
            estimated_completion_time = start_time + timedelta(seconds=estimated_total_time)
            time_left = estimated_total_time - elapsed_time
            rows_left = rows_to_process - rows_processed

            print(f"\rProgress: {rows_processed}/{rows_to_process} rows processed. Estimated completion: {estimated_completion_time.strftime('%Y-%m-%d %H:%M:%S')}. Time left: {time_left/60:.2f} minutes. Rows left: {rows_left}.", end='')
            sys.stdout.flush()

    print("\nProcessing completed or maximum requests reached. Please rerun to continue.")

if __name__ == "__main__":
    main()
