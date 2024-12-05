from setuptools import setup, find_packages

setup(
    name="gscholar_gui",
    version="1.0.0",
    description="A GUI tool for Google Scholar literature searches",
    author="Chandrasekar SUBRAMANI NARAYANA",
    url="https://github.com/yourusername/gscholar_gui",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.6",
        "requests>=2.32.3",
        "bs4>=4.12.3",
        "beautifulsoup4",
        "pandas>=2.2.3",
        "lxml>=5.3.0",
        "openpyxl>=3.1.5",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "gscholar_gui=gscholar_gui:main",  
        ],
    },
)
