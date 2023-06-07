# Tides
---
This is very much a work in progress.

The aim is to create a tool that will give local tide times for the next few days, along with a weather forecast.

---

- It's currently a POC in a Jupyter Notebook, py_Tides_v1.ipynb

Here's the plan, courtesy of ChatGPT:

1) Reorganize and Document the Code: Go through your Notebook and make sure the code is organized logically. Group related cells together and make sure each cell or group of cells is well-commented so that someone reading your code (including future you) can understand what each part of the code is supposed to do.

2) Replace the API Call: You mentioned that one part of your code is not working because it depends on an API that was only being used as a trial. You'll need to replace this API call with a different data source. This could be another API, a local data file, or something else depending on what data you need. You may need to adjust the rest of your code to handle the data from the new source.

3) Remove Jupyter-Specific Code: Jupyter Notebooks allow you to write code that wouldn't work in a regular Python script. For example, you might be using magic commands (like %matplotlib inline) or relying on the order of cell execution. You'll need to rewrite these parts of your code so that they work in a normal Python script.

4) Convert Notebook to Python Script: After you've made the above changes, you can convert your Notebook to a Python script using nbconvert:

jupyter nbconvert --to script Your_Notebook.ipynb

5) Structure Your Script: In a Jupyter Notebook, it's okay to have a lot of top-level code (i.e., code not inside a function or class), but in a Python script, it's good practice to wrap your code in functions or classes. This makes your code more modular, easier to read, and easier to test.

6) Error Handling and Logging: In a Jupyter Notebook, you can just look at the output of each cell to see if something went wrong. In a Python script, it's important to include proper error handling (using try/except blocks) and logging so that you can understand what's happening when you run your script.

7) Test Your Script: Finally, make sure to test your script thoroughly. Make sure all the functionality of your original Notebook is working as expected in the Python script.

ChatGPT also suggested that the rambling Notebook code would be better condensed down in a format something like what is in Tides.py