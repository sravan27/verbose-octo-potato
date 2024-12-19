from setuptools import setup, find_packages

setup(
    name="zlm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "streamlit",
        "nltk",
        "openai"
    ],
    author="Your Name",
    description="Your custom description",
    url="https://github.com/sravan27/verbose-octo-potato",
)
