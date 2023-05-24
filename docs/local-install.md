![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Local Install

> If you would prefer to run things locally, you can do that as well.

## Setup Development Environment

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Since we are using Python 3.9, you may need to specify the version of python when creating the virtual environment:

```bash
python3.9 -m venv venv
```

To exit the Python Virtual Environment, type the following into terminal:

```bash
deactivate
```

## Authenticate with ClearML

> We are using [ClearML](https://app.clear.ml/) as a tool to evaluate trained models, so you'll need to connect your account:

After installing all the Python dependencies, you can connect to your ClearML account in terminal: 

NOTE: You only need to do this once.  If you are not sure if you have done this already, check for a `~/clearml.conf` file.

```bash
clearml-init
```

## Windows WSL:

> You will likely need to run this command before you can run the install process ( replace `3.9` in `python3.9-venv` with your machines version of python )

```bash
sudo apt install python3.9-venv
```

---

[![Previous Step](https://img.shields.io/badge/README-121212.svg?logo=github&style=for-the-badge)](../README.md) &nbsp; [![Next Step](https://img.shields.io/badge/Next_Step-1aa0db.svg?logo=github&style=for-the-badge)](./downloading-assets.md)
