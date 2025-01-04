from setuptools import setup, find_packages

setup(
    name="mariposa",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "scikit-learn",
        "plotly",
        "pydantic",
        "nltk"
    ],
) 