import sys
import datetime
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QSpinBox, QTextEdit, QMessageBox, QComboBox, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3
import re
import random

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#from scholarly import scholarly

class ScholarSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Scholar Literature Search")
        self.setGeometry(100, 100, 1200, 800)

        # Main container
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        # Input Section
        self.input_section = QVBoxLayout()

        # Keyword Input
        keyword_layout = QHBoxLayout()
        keyword_label = QLabel("Keywords:")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Enter keywords (use AND, OR for logic)")
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        self.input_section.addLayout(keyword_layout)

        # Date Range Input
        date_layout = QHBoxLayout()
        date_label = QLabel("Date Range:")
        self.start_year_input = QSpinBox()
        self.start_year_input.setRange(1900, 2100)
        self.start_year_input.setValue(2020)
        self.end_year_input = QSpinBox()
        self.end_year_input.setRange(1900, 2100)
        self.end_year_input.setValue(datetime.datetime.now().year)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.start_year_input)
        date_layout.addWidget(QLabel("to"))
        date_layout.addWidget(self.end_year_input)
        self.input_section.addLayout(date_layout)

        # Number of Pages Input
        pages_layout = QHBoxLayout()
        pages_label = QLabel("Number of Pages:")
        self.pages_input = QSpinBox()
        self.pages_input.setRange(1, 10)
        self.pages_input.setValue(2)
        pages_layout.addWidget(pages_label)
        pages_layout.addWidget(self.pages_input)
        self.input_section.addLayout(pages_layout)

        self.layout.addLayout(self.input_section)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)

        # Results Section
        self.results_section = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(16)
        self.results_table.setHorizontalHeaderLabels([
            "Title", "Authors", "Year", "Journal", "Volume", "Issue", "Pages", "Publisher", "DOI", "Field", "Methods", "Keywords", "URL", "Citations", "Abstract", "Page"])
        self.results_section.addWidget(self.results_table)

        self.layout.addLayout(self.results_section)

        # Export Button
        self.export_button = QPushButton("Export to Excel")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Network Manager
        self.network_manager = QNetworkAccessManager()

    def extract_doi(self, text):
        """
        Extract DOI from text or URL:
            DOI pattern starts with 10, followed by 4 to 9 digits, a / (slash), and allowed characters like -, ., _, ;, (), :
        
        """
        doi_pattern = r'10\.\d{4,9}/[-._;()/:\w]+'   # define a regular expression to match the structure of a DOI.
        match = re.search(doi_pattern, text)   # search the input text for the first match of the specified pattern.
        return match.group(0) if match else ""

    
    def extract_cited_by(self, text):
        """
        Extracts the 'Cited by' count from the HTML text using regex.
        """
        cite_pattern = r'Cited by (\d+)'   # define a regular expression to match the structure of a DOI.
        match = re.search(cite_pattern, str(text))   # search the input text for the first match of the specified pattern.
        return match.group(1) if match else ""
    
    def extract_methods(self, abstract):
        """
        Extract potential methods from abstract
        Extract sentences from an abstract containing specific method-related keywords. 
        Return these sentences joined by semicolons as a single string.
        
        """
        method_keywords = ['using', 'method', 'approach', 'technique', 'protocol', 
                          'workflow', 'analysis', 'procedure', 'methodology']
        
        sentences = abstract.split('.')
        method_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in method_keywords):
                method_sentences.append(sentence.strip())
        
        return '; '.join(method_sentences)
    
    def extract_field(self, author_info, title, abstract):
        """Extract potential field of study"""
        fields = {
            'biology': ['biology', 'biological', 'cell', 'molecular', 'genetics', 'neuron', 'brain', 'life sciences'],
            'medicine': ['medical', 'clinical', 'healthcare', 'patient', 'treatment', 'cancer', 'disease'],
            'materials': ['microstructure', 'nanostructure', 'alloy', 'grain size'],
            'microscopy': ['microscopy', 'imaging', 'microscope', 'visualization'],
            'AI': ['machine learning', 'deep learning', 'computer vision']
        }
        
        
        
        text = f"{title} {abstract} {author_info}".lower()
        
        detected_fields = []
        for field, keywords in fields.items():
            if any(keyword in text for keyword in keywords):
                detected_fields.append(field)
        
        return '; '.join(detected_fields) if detected_fields else "Not specified"
    
    def format_search_query(self, keyword, start_year, end_year):
        """
        Format search query with proper logical operators for Google Scholar
        """
        # Remove quotes if they exist and split by OR
        terms = [term.strip(' "\'') for term in keyword.split(' OR ')]
        
        # Format each term
        formatted_terms = []
        for term in terms:
            # If term contains spaces, wrap it in quotes
            if ' ' in term:
                formatted_terms.append(f'"{term}"')
            else:
                formatted_terms.append(term)
        
        # Join terms with OR operator
        query = ' OR '.join(formatted_terms)
        
        # Add date range
        #query += f'&as_ylo=:{start_year}&as_yup:{end_year}'
        
        print(f"Formatted query: {query}")  # Debug print
        return query

    def perform_search(self):
        keywords = self.keyword_input.text()
        start_year = self.start_year_input.value()
        end_year = self.end_year_input.value()
        num_pages = self.pages_input.value()
        keywords = keywords.split(";")
        print(keywords)

        self.status_bar.showMessage("Searching...",5000)
        QMessageBox.information(self, "Search Started", f"Searching for: {keywords}\nDate Range: {start_year}-{end_year}\nPages: {num_pages}")
        
        all_results = []
    
        for keyword in keywords:
            results = self.search_scholar(keyword, start_year, end_year, num_pages)
            if results:
                all_results.extend(results)
            print(f"\nFound {len(results)} total results for {keyword}")
            
            # Add delay between keywords
            if keyword != keywords[-1]:  # If not the last keyword
                delay = random.uniform(30, 60)
                print(f"\nWaiting {delay:.1f} seconds before next search...")
                time.sleep(delay)
                
        if all_results:
            df = pd.DataFrame(all_results)
            
            # Remove duplicates
            initial_count = len(df)
            df = df.drop_duplicates(subset=['Title'])
            final_count = len(df)
            
            print(f"\nFound {initial_count} total results")
            print(f"After removing duplicates: {final_count} results")
            
            # Sort by year
            df = df.sort_values(by=['Year', 'Title'], ascending=[False, True])
            
            # Reorder columns
            columns_order = ["Title", "Authors", "Year", "Journal", "Volume", "Issue", "Pages", "Publisher", "DOI", "Field", "Methods", "Keywords", "URL", "Citations", "Abstract", "Page"]
            df = df[columns_order]
            
        self.display_results(df.to_dict('records'))

        
    def search_scholar(self, keyword, start_year=2020, end_year=2024, num_pages=3):
        results = []
        for page in range(num_pages):
            start_index = page * 10
            query = self.format_search_query(keyword, start_year, end_year)
            
            # URL encode the query properly
            encoded_query = requests.utils.quote(query)
            url = f"https://scholar.google.com/scholar?start={start_index}&q={encoded_query}&as_sdt=0&as_ylo=:{start_year}&as_yhi:{end_year}&hl=en"
            
            print(f"\nSearching for: {keyword} - Page {page + 1}")
            self.status_bar.showMessage(f"\nSearching for: {keyword} - Page {page + 1}", 5000)
            print(f"URL: {url}")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        
            try:
                # Add random delay between pages
                if page > 0:
                    delay = random.uniform(15, 35)
                    print(f"Waiting {delay:.1f} seconds before next page...")
                    self.status_bar.showMessage(f"Waiting {delay:.1f} seconds before next page...")
                    time.sleep(delay)
                    
                response = requests.get(url, headers=headers, verify=False)
                print(f"Status Code: {response.status_code}")
                #self.status_bar.showMessage(f"Status Code: {response.status_code}", 1000)
                

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Debug print
                    print(f"Response content preview: {response.text[:500]}")
                    
                    if "Please show you're not a robot" in response.text:
                        print("CAPTCHA detected. Please try again later.")
                        self.status_bar.showMessage("CAPTCHA detected. Please try again later.", 5000)
                        QMessageBox.critical(self, "CAPTCHA detected","CAPTCHA detected. Please try again later.")
                        return
                    
                    articles = soup.find_all("div", class_="gs_r gs_or gs_scl")
                    print(f"Found {len(articles)} articles on page {page + 1}")
                    self.status_bar.showMessage(f"Found {len(articles)} articles on page {page + 1}", 5000)
                    
                    if not articles:
                        print("No more results found.")
                        self.status_bar.showMessage("No more results found.", 5000)
                        break
                    
                    for idx, article in enumerate(articles, 1):
                        try:
                            #self.status_bar.showMessage(f"\nProcessing article {idx} on page {page + 1}:", 1000)
                            print(f"\nProcessing article {idx} on page {page + 1}:")
                            print(article)
                                                        
                            # Extract basic information
                            title_elem = article.find("h3", class_="gs_rt")
                            author_elem = article.find("div", class_="gs_a")
                            abstract_elem = article.find("div", class_="gs_rs")
                            cite_elem = article.find("div", class_="gs_rs")
                            
                            # Clean and extract title
                            if title_elem:
                                for span in title_elem.find_all("span"):
                                    span.decompose()
                                title = title_elem.get_text(strip=True)
                            else:
                                title = "No title found"
                            
                            # Extract URL and DOI
                            link = title_elem.find("a") if title_elem else None
                            url = link["href"] if link else ""
                            doi = self.extract_doi(url)
                            
                            # Extract author information
                            author_info = author_elem.get_text(strip=True) if author_elem else ""
                            authors = author_info.split('-')[0].strip() if '-' in author_info else ""
                            
                            # Extract journal
                            journal = author_info.split('-')[-1].strip() if '-' in author_info else ""
                            
                            # Extract year
                            year_match = re.search(r'\b(19|20)\d{2}\b', author_info) if author_info else None
                            year = year_match.group(0) if year_match else ""
                            
                            # Extract abstract
                            abstract = abstract_elem.get_text(strip=True) if abstract_elem else ""
                            
                            # Extract methods and field
                            methods = self.extract_methods(abstract)
                            field = self.extract_field(author_info, title, abstract)

                            cite = self.extract_cited_by(article)
                            print(cite)
                            
                            # Store the result
                            result = {
                                "Title": title,
                                "Authors": authors,
                                "Year": year,
                                "Journal": journal,
                                "Volume": 'N/A',
                                "Issue": 'N/A',
                                "Pages": 'N/A',
                                "Publisher": 'N/A',
                                "DOI": doi,
                                "Field": field,
                                "Methods": methods,
                                "Keywords": keyword,
                                "URL": url,
                                "Citations": cite,
                                "Abstract": abstract,
                                "Page": int(page + 1)
                            }
                            print(result)
                            #print(f"Title: {title[:100]}...")
                            #print(f"Authors: {authors[:100]}...")
                            #print(f"Year: {year}")
                            #print(f"Field: {field}")
                            
                            results.append(result)
                            
                        except Exception as e:
                            self.status_bar.showMessage(f"Error processing article {idx} on page {page + 1}: {str(e)}", 5000)
                            print(f"Error processing article {idx} on page {page + 1}: {str(e)}")
                            continue
                    
                else:
                    QMessageBox.critical(self, "Failed Result", f"Failed to get results for page {page + 1}. Status code: {response.status_code}")
                    self.status_bar.showMessage(f"Failed to get results for page {page + 1}. Status code: {response.status_code}", 5000)
                    return
        
            except Exception as e:
                QMessageBox.critical(self, "Search Error", f"Error during search on page {page + 1}: {str(e)}")
                self.status_bar.showMessage("Search failed.", 5000)
                return

        if results == []:
            return None
        return results

    def display_results(self, results):
        self.results_table.setRowCount(len(results))
        for row, result in enumerate(results):
            print(result)
            for col, key in enumerate(["Title", "Authors", "Year", "Journal", "Volume", "Issue", "Pages", "Publisher", "DOI", "Field", "Methods", "Keywords", "URL", "Citations", "Abstract", "Page"]):
                item = QTableWidgetItem(str(result[key]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.results_table.setItem(row, col, item)

        self.status_bar.showMessage(f"Displayed {len(results)} results.", 5000)


    def export_results(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
        if path:
            if not path.endswith('.xlsx'):
                path += '.xlsx'  # Ensure .xlsx extension
            try:
                data = []
                for row in range(self.results_table.rowCount()):
                    data.append([self.results_table.item(row, col).text() for col in range(self.results_table.columnCount())])
    
                df = pd.DataFrame(data, columns=["Title", "Authors", "Year", "Journal", "Volume", "Issue", "Pages", "Publisher", "DOI", "Field", "Methods", "Keywords", "URL", "Citations", "Abstract", "Page"])
                df.to_excel(path, index=False)
                QMessageBox.information(self, "Export Successful", f"Results exported to {path}")
                self.status_bar.showMessage(f"Results exported to {path}", 5000)
            except ImportError as e:
                QMessageBox.critical(self, "Export Error", "Excel export requires the 'openpyxl' library. Please install it using 'pip install openpyxl'.")
                self.status_bar.showMessage("Export failed due to missing dependencies.", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"An unexpected error occurred: {str(e)}")
                self.status_bar.showMessage("Export failed due to an unexpected error.", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScholarSearchApp()
    window.show()
    sys.exit(app.exec_())
