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

Classes
=======

File
----
.. autoclass:: src.database.classes.classes.File
    :members:

Review
------
.. autoclass:: src.database.classes.classes.Review
    :members:

Sentence
--------
.. autoclass:: src.database.classes.classes.Sentence
    :members:

Word
----
.. autoclass:: src.database.classes.classes.Word
    :members:

Synset
------
.. autoclass:: src.database.classes.classes.Synset
    :members:

DepTree
-------
.. autoclass:: src.database.classes.classes.DepTree
    :members:

DepTreeNode
-----------
.. autoclass:: src.database.classes.classes.DepTreeNode
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

.. automodule:: src.database.process.review_process
    :members:

Freeling Processes
------------------

tokenization
............

.. automodule:: src.database.process.sentence_process
    :members:

lemmatization
.............

.. automodule:: src.database.process.lemma_process
    :members:

disambiguation
..............

.. automodule:: src.database.process.synset_process
    :members:

dependency tree generation
..........................

.. automodule:: src.database.process.deptree_process
    :members:

Feed database
-------------
.. automodule:: src.database.process.file_process
    :members:


Load data from database : *load* package
========================================

Load Files
----------
.. automodule:: src.database.load.file_load
    :members:

Load Reviews
------------
.. automodule:: src.database.load.review_load
    :members:

Load Sentences
--------------
.. automodule:: src.database.load.sentence_load
    :members:

Load Words
----------
.. automodule:: src.database.load.word_load
    :members:

Load Synsets
------------
.. automodule:: src.database.load.synset_load
    :members:

Load Lemmas
-----------
.. automodule:: src.database.load.lemma_load
    :members:

Load DepTrees
-------------
.. automodule:: src.database.load.deptree_load
    :members:


Analyse data : *analysis* package
=================================

Sentiment Analysis
------------------
.. automodule:: src.database.analysis.sentiment_analysis
    :members:

Pattern Recognition
-------------------
.. automodule:: src.database.analysis.pattern_recognition
    :members:

