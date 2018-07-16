.. Hotel Reviews Language Processing documentation master file, created by
   sphinx-quickstart on Wed Jul 11 15:06:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hotel Reviews Language Processing's documentation!
=============================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Requirements
============

| This project uses an external program, called Freeling, to process language : http://nlp.lsi.upc.edu/freeling/
| Check this page to install Freeling on your computer : https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/installation/apis-linux.html
| Notice that to use Python API, Freeling needs to be installed from source with the dedicated options as described in documentation.
| **For now**, only a Linux installation in the default folder */usr/local* is supported, but this should be fixed in next improvements.

| This project also use an embedded sqlite3 database to store results : https://docs.python.org/3/library/sqlite3.html
| The corresponding Python package should already be installed in your Python3 distribution.

Classes
=======

File
----
.. autoclass:: loacore.classes.classes.File
    :members:

Review
------
.. autoclass:: loacore.classes.classes.Review
    :members:

Sentence
--------
.. autoclass:: loacore.classes.classes.Sentence
    :members:

Word
----
.. autoclass:: loacore.classes.classes.Word
    :members:

Synset
------
.. autoclass:: loacore.classes.classes.Synset
    :members:

DepTree
-------
.. autoclass:: loacore.classes.classes.DepTree
    :members:

DepTreeNode
-----------
.. autoclass:: loacore.classes.classes.DepTreeNode
    :members:


Feeding database : *process* package
====================================
This package contains all the necessary modules to perform the processes of new files. Notice that all those processes are automatically handled by the :func:`file_process.add_files()` function.

Raw Processes
--------------

Normalization and review splitting
..................................

- Normalization : conversion to UTF-8 and lower case
- Review splitting : the file text is splitted into reviews

.. automodule:: loacore.process.review_process
    :members:

Freeling Processes
------------------

tokenization
............

.. automodule:: loacore.process.sentence_process
    :members:

lemmatization
.............

.. automodule:: loacore.process.lemma_process
    :members:

disambiguation
..............

.. automodule:: loacore.process.synset_process
    :members:

dependency tree generation
..........................

.. automodule:: loacore.process.deptree_process
    :members:

Feed database
-------------
.. automodule:: loacore.process.file_process
    :members:


Load data from database : *load* package
========================================

Load Files
----------
.. automodule:: loacore.load.file_load
    :members:

Load Reviews
------------
.. automodule:: loacore.load.review_load
    :members:

Load Sentences
--------------
.. automodule:: loacore.load.sentence_load
    :members:

Load Words
----------
.. automodule:: loacore.load.word_load
    :members:

Load Synsets
------------
.. automodule:: loacore.load.synset_load
    :members:

Load Lemmas
-----------
.. automodule:: loacore.load.lemma_load
    :members:

Load DepTrees
-------------
.. automodule:: loacore.load.deptree_load
    :members:


Analyse data : *analysis* package
=================================

Sentiment Analysis
------------------
.. automodule:: loacore.analysis.sentiment_analysis
    :members:

Pattern Recognition
-------------------
.. automodule:: loacore.analysis.pattern_recognition
    :members:

