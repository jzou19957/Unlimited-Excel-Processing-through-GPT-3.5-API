**Getting Started**
Follow these simple steps to use the application:

1. Install Python Requirements: Ensure all the required Python packages are installed by running the following command:
pip install pandas openpyxl requests

2. Prepare Your Files: Place your Excel file and a corresponding text file in the same directory as gpt35.py and gpt35.bat. Make sure both files (Excel and text) have the same name but different extensions (e.g., data.xlsx and data.txt).![d7c275aa4d44d3dc689362d16110604](https://github.com/jzou19957/Unlimited-Excel-Processing-through-GPT-3.5-API/assets/153259165/701378e7-9212-40e3-95e2-d5e51109a93b) .Ensure that in your excel data the first column should be named "Text".

3. Excel File Setup: Populate the first column of your Excel file with the data or text you want GPT 3.5 to analyze. Each row will be sent to GPT 3.5 as an individual request.

4. Text File Setup: The text file (named identically to your Excel file) should contain the prompt or instructions for the GPT 3.5 API. These prompts will direct the AI in crafting responses based on the content of each row in your Excel file.

5. Running the Application: Launch the gpt35.bat file by double-clicking it. The script will automatically start processing the Excel and text file pair.

6. All the responses in txt format for each row of the excel will be saved in the subfolder named after the excel

7. Processing Multiple Excel Files: If you have multiple Excel files, ensure that each one has a corresponding text file with prompts in the same directory. The script will automatically process them one after the other until all paired Excel files are processed.![86f26e17d2b282f993bb9efeec39183](https://github.com/jzou19957/Unlimited-Excel-Processing-through-GPT-3.5-API/assets/153259165/7f349fb7-b140-4917-8fe0-5835c184ae16)

8. In cases of interruption (internet interruption or othe reasons), you do not need to worry about shutting the program down. Every time the code is run again, it will resume from where it was last time until all the excels with txt prompts are finished. 

9. You now have a folder of txt files that are the responses of API requests to each of the row in your excel file. You can proceed to join them together by code or perform any other analyses. 
