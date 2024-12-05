# gscholar_gui

**gscholar_gui** is a Python-based tool for searching and extracting academic articles from Google Scholar. It provides a graphical interface using PyQt5 and enables users to search for articles based on keywords, filter results by publication year, and export the results to an Excel file.

## Features

- **Search Articles by Keywords**: Search academic articles on Google Scholar using custom keywords.
- **Filter by Publication Date**: Specify a date range to narrow the search to articles published within the given years.
- **View Article Details**: Extract detailed information such as titles, authors, publication years, DOI, citations, methods, field of study, and more.
- **Export Results**: Export the search results to an Excel file for further analysis.
- **User-Friendly Interface**: Easy-to-use GUI built with PyQt5, allowing seamless interaction for users of all levels.

## Installation

### Requirements

To use **gscholar_gui**, ensure you have the following dependencies installed:

- **Python 3.x**
- **PyQt5**: For the graphical user interface (GUI).
- **requests**: For making HTTP requests.
- **beautifulsoup4**: For parsing HTML and extracting data from web pages.
- **pandas** and **openpyxl**: For working with data and exporting to Excel.

### Install Dependencies

1. Clone or download the repository:

```bash
git clone https://github.com/yourusername/gscholar_gui.git
cd gscholar_gui
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv gscholar-env
source gscholar-env/bin/activate  # On Windows use `gscholar-env\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running gscholar_gui

Once you have the dependencies installed, you can run the application:

1. Open a terminal or command prompt.
2. Navigate to the `gscholar_gui` directory.
3. Run the following command:

```bash
python gscholar_gui.py
```

This will launch the graphical interface for **gscholar_gui**, where you can input your search keywords, set filters, and view the results.

## Usage

### 1. Enter Keywords

In the "Keywords" field, input the search terms you want to use. You can combine multiple keywords using `AND` or `OR` for more specific or broad searches.

Example:

- `"machine learning" AND "computer vision"`
- `cancer OR oncology`
-  segmentation; "cell tracking"

### 2. Set Date Range

Set the publication year range for the articles you are searching for. You can adjust the start year and end year.

### 3. Set Number of Pages

Specify how many pages of results you want to retrieve from Google Scholar. Each page typically shows 10 results, so you can choose between 1 to 10 pages.

### 4. Perform Search

Click the **Search** button to start the search. **gscholar_gui** will connect to Google Scholar and retrieve the articles based on your query. The results will be displayed in a table with various fields like:

- Title
- Authors
- Year
- Journal
- Volume (under development)
- Issue (under development)
- Pages (under development)
- Publisher (under development)
- DOI
- Field (under development)
- Methods
- URL
- Citations
- selective Abstract

### 5. Export Results

![image](https://github.com/user-attachments/assets/a740f10a-bcac-49e1-b124-5e2a41776671)

Once the search is complete, you can export the results to an Excel file by clicking the **Export to Excel** button. This will save the results in a `.xlsx` file that you can open and analyze in Excel or other spreadsheet tools.

### 6. Viewing Results

The results will be displayed in a table within the application, where each row corresponds to an article. You will be able to see key details such as the title, authors, year, DOI, and the number of citations.

## Customizing the Search

- **Field Extraction**: **gscholar_gui** attempts to detect the field of study for each article by analyzing its title, abstract, and author information. Common fields include biology, medicine, materials science, and artificial intelligence.
- **Method Extraction**: **gscholar_gui** can extract sentences related to research methods from the article’s abstract. This helps users quickly identify the methods used in the research.

## Acknowledgments

- **PyQt5**: A set of Python bindings for Qt, used to create the GUI.
- **Requests**: A simple HTTP library for making web requests.
- **BeautifulSoup**: A library for parsing HTML, used to extract article data.
- **Google Scholar**: The primary data source for academic articles.
- **Dr. Sreenivas Bhattiprolu (bnsreenu) aka DigitalSreeni**: The program is inspired by the script [Automate Google Search Results to Excel](https://github.com/bnsreenu/python_for_microscopists/blob/master/347-Automate%20Google%20Search%20Results%20to%20Excel/347-Automate%20Google%20Search%20Results%20to%20Excel.py), developed by Dr. Bhattiprolu as part of his Python for Microscopists tutorial series.

## License

**gscholar_gui** is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

We welcome contributions to **gscholar_gui**! If you have suggestions or improvements, feel free to open an issue or submit a pull request. Here's how you can contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## Author

**gscholar_gui** was developed by [Chandrasekar SUBRAMANI NARAYANA]([https://github.com/yourusername](https://github.com/chandrasekarnarayana)).
