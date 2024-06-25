# Grotus Flask App

This is simple flask application for serving machine learning model for Grotus App.

This guide will walk you through the steps to set up a Flask application using a virtual environment (venv) and installing all the necessary dependencies from a requirements file.

## Prerequisites

- Python 3.x installed on your system.

## Setup Instructions

### 1. Clone the Repository

First, clone the repository of your Flask application:

### 2. Create a Virtual Environment

Create a virtual environment inside your project directory. This keeps your project dependencies isolated from the system Python installation:

```console
python -m venv .venv
```

or

```console
py -3 -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment.

```console
venv\Scripts\activate ## if you using cmd
venv\Scripts\Activate ## if you using Powershell
```

### 4. Install Dependencies

Once the virtual environment is activated, install the required dependencies using `pip` and the `requirements.txt` file located in your project directory:

```console
pip install -r requirements.txt
```

### 5. Run the Setup script

Once all the required library installed, you need to run the setup.py to downlaod NLTK punkt

```console
python setup.py
```

### 6. Download the model

You need to download the model by [click here](https://drive.google.com/file/d/1H8p0D6PslbC2-KWOgZTgFWIPRwBoGNp8/view?usp=sharing) and put it on the same directory with `app.py` .

### 7. Run the Flask Application

You are now ready to run your Flask application. Make sure you are in the root directory of your project where `app.py` (or your main Flask application file) is located, and then run:

```python
python app.py
```
