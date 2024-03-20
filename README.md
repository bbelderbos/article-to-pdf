# Turn Pybites articles into PDFs

A quick script to download all Pybites articles and convert them into pdf files.

Steps:

```
$ git clone git@github.com:bbelderbos/article-to-pdf.git
$ cd article-to-pdf

$ mkdir outputs
$ python3 -m venv venv && source venv/bin/activate

(venv) $ python -m pip install -r requirements.txt
(venv) $ python script.py

# all articles should be saved in the outputs directory
```
