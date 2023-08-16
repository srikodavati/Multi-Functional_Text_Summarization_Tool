
# Text Summarization

Implementation of a text summarization tool to help users quickly identify and understand the main points of a document without having to read through the entire document. The tool will be available as a web extension.

## Major Functions
**Text summarization**: Taking a long article or text document linked to the web page and generating a summary that captures the main points of document.

**Customization**: Altering the length of the summary generated.

**Topic Tag generation**: Analyzing the document and generating relevant tags and keywords that reflect the main topics covered in the document.

**Sentiment Analysis**: Analysis of the author’s sentiment in the document.

**Citation generation**: Generate citation for the document.

**Translation**: Translation of the summary in 8 different languages.

## Getting Started

## Clone Project Repository 

You can clone the project repository using the following command

```
git clone https://github.com/vydanasindhu/textsummarization.git
```

## Run the application

### Create virtual env

You need to install virtualenv and then activate the environment. Use the following command to do the same. After cloning the repository, pip3 install virtualenv command should be executed only once. There is no need to run the command every time you use the tool.

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

### Install requirements

To run the tool, a few libraries must be installed. All requirements are specified in the requirements.txt file. Requirements have to installed only once. There is no need to run the command every time the tool is used. To install the requirements, run the following command.

```
pip3 install -r requirements.txt
```

### Upload the extension to your browser
The web extension must be loaded into your browser from local files. Depending on the browser you’re using, this can be done in a variety of ways. Here are the general steps for doing it in Google Chrome.
1) Open Chrome and enter chrome://extensions in the address bar to go to the Extension Management page.
2) Enable Developer Mode by clicking the toggle button in the top right corner.
3) Click the "Load unpacked" button and select the directory containing the unpacked extension(the cloned Git folder).
4) If the extension is successfully loaded, it will appear in the list of extensions,
### Run Python server

The tool sends an API request to sum- marizer.py when we use it, so the python server must be running to handle the API requests. So, whenever you want to use the extension, use the following command.

```
python summarizer.py
```

### Deactivate Environment 

Deactive the environment after using the tool. Use the following command to deactivate
```
deactivate
```

### Common Issues and Solutions:
1) If you encounter a certificate verification error (CERTIFICATE_VERIFY_FAILED) while using the tool, run the following command:

```
/Applications/Python\ 3.x/Install\ Certificates.command
```
Replace "3.x" with the version number of Python you are using (e.g.,
3.7, 3.8, 3.9).









