---
title: |
    Loacore : Language and Opinion Analyzer for Comments and Reviews's
    documentation! --- Loacore : Language and Opinion Analyzer for Comments
    and Reviews documentation
viewport: 'width=device-width, initial-scale=0.9, maximum-scale=0.9'
---

::: {.document}
::: {.documentwrapper}
::: {.bodywrapper}
::: {.body role="main"}
::: {#loacore-language-and-opinion-analyzer-for-comments-and-reviews-s-documentation .section}
Loacore : Language and Opinion Analyzer for Comments and Reviews's documentation![¶](#loacore-language-and-opinion-analyzer-for-comments-and-reviews-s-documentation "Permalink to this headline"){.headerlink}
===============================================================================================================================================================================================================

::: {.toctree-wrapper .compound}
:::
:::

::: {#requirements .section}
Requirements[¶](#requirements "Permalink to this headline"){.headerlink}
========================================================================

::: {#freeling .section}
Freeling[¶](#freeling "Permalink to this headline"){.headerlink}
----------------------------------------------------------------

::: {.line-block}
::: {.line}
This project uses an external program, called Freeling, to process
language : <http://nlp.lsi.upc.edu/freeling/>
:::

::: {.line}
Check this page to install Freeling on your computer :
<https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/installation/apis-linux.html>
:::

::: {.line}
Notice that to use Python API, Freeling needs to be installed from
source with the dedicated options as described in documentation.
:::

::: {.line}
**For now**, only a Linux installation in the default folder
*/usr/local* is supported, but this should be fixed in next
improvements.
:::
:::
:::

::: {#database .section}
Database[¶](#database "Permalink to this headline"){.headerlink}
----------------------------------------------------------------

::: {.line-block}
::: {.line}
The embedded database used to store results is an sqlite database,
managed with the sqlite3 Python database API :
<https://docs.python.org/3/library/sqlite3.html>
:::

::: {.line}
The corresponding Python package should already be installed in your
Python3 distribution.
:::
:::
:::

::: {#utils .section}
Utils[¶](#utils "Permalink to this headline"){.headerlink}
----------------------------------------------------------

Package `utils`{.xref .py .py-mod .docutils .literal .notranslate} uses
a few graphical modules to show results.

-   PrettyTable : <https://pypi.org/project/PrettyTable/>

-   Matplotlib : <https://matplotlib.org/users/installing.html#linux>

-   ::: {.first .line-block}
    ::: {.line}
    Tkinter : <https://wiki.python.org/moin/TkInter>
    :::

    ::: {.line}
    Module used to generate gui to save pdf for example.
    :::

    ::: {.line}
    Even if the package should be included in Python distribution, on
    Linux distributions you might need to install *tk* package through
    your package manager.
    :::
    :::
:::
:::

::: {#classes .section}
Classes[¶](#classes "Permalink to this headline"){.headerlink}
==============================================================

::: {#file .section}
File[¶](#file "Permalink to this headline"){.headerlink}
--------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`File`{.descname}[(]{.sig-paren}*id\_file*, *file\_path*[)]{.sig-paren}[¶](#loacore.classes.classes.File "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_file** (*int*) --       |
    |                                   |     ID\_File used in File table   |
    |                                   | -   **file\_path** (*path-like    |
    |                                   |     object*) -- Path used to load |
    |                                   |     file from file system.        |
    |                                   | -   **reviews** (`list`{.xref .py |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of              |
    |                                   |     [`Review`{.xref .py .py-class |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Review "loacore.classe |
    |                                   | s.classes.Review"){.reference     |
    |                                   |     .internal}) -- File reviews   |
    +-----------------------------------+-----------------------------------+

     `load`{.descname}[(]{.sig-paren}*encoding=\'windows-1252\'*[)]{.sig-paren}[¶](#loacore.classes.classes.File.load "Permalink to this definition"){.headerlink}

    :   Load file from file system using `file_path`{.xref .py .py-attr
        .docutils .literal .notranslate} and specified encoding.

          ------------- ------------------------------------------------------------------------------------------------------------------------------
          Parameters:   **encoding** -- Source file encoding. Default is set to *windows-1252*, the encoding obtained from .txt conversion in Excel.
          Returns:      file object
          ------------- ------------------------------------------------------------------------------------------------------------------------------
:::

::: {#review .section}
Review[¶](#review "Permalink to this headline"){.headerlink}
------------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`Review`{.descname}[(]{.sig-paren}*id\_review*, *id\_file*, *file\_index*, *review*[)]{.sig-paren}[¶](#loacore.classes.classes.Review "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_review** (*int*) --     |
    |                                   |     ID\_Review used id Review     |
    |                                   |     table                         |
    |                                   | -   **id\_file** (*int*) -- SQL   |
    |                                   |     reference to the              |
    |                                   |     corresponding File            |
    |                                   | -   **file\_index** (*int*) --    |
    |                                   |     Index of the Review in        |
    |                                   |     referenced File               |
    |                                   | -   **review** (*string*) --      |
    |                                   |     Review represented as a       |
    |                                   |     string                        |
    |                                   | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     [`Sentence`{.xref .py         |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Sentence "loacore.clas |
    |                                   | ses.classes.Sentence"){.reference |
    |                                   |     .internal}) -- Review         |
    |                                   |     Sentences                     |
    +-----------------------------------+-----------------------------------+
:::

::: {#sentence .section}
Sentence[¶](#sentence "Permalink to this headline"){.headerlink}
----------------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`Sentence`{.descname}[(]{.sig-paren}*id\_sentence*, *id\_review*, *review\_index*, *id\_dep\_tree*[)]{.sig-paren}[¶](#loacore.classes.classes.Sentence "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_sentence** (*int*) --   |
    |                                   |     ID\_Sentence used in Sentence |
    |                                   |     table                         |
    |                                   | -   **id\_review** (*int*) -- SQL |
    |                                   |     reference to the              |
    |                                   |     corresponding Review          |
    |                                   | -   **review\_index** (*int*) --  |
    |                                   |     Index of the Sentence in      |
    |                                   |     referenced Review             |
    |                                   | -   **id\_dep\_tree** (*int*) --  |
    |                                   |     SQL reference to a possibly   |
    |                                   |     associated DepTree            |
    |                                   | -   **words** (`list`{.xref .py   |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of              |
    |                                   |     [`Word`{.xref .py .py-class   |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Word "loacore.classes. |
    |                                   | classes.Word"){.reference         |
    |                                   |     .internal}) -- Sentence Words |
    |                                   | -   **dep\_tree**                 |
    |                                   |     ([`DepTree`{.xref .py         |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.DepTree "loacore.class |
    |                                   | es.classes.DepTree"){.reference   |
    |                                   |     .internal}) -- Possibly       |
    |                                   |     associated DepTree            |
    |                                   | -   **freeling\_sentence**        |
    |                                   |     (`pyfreeling.sentence`{.xref  |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate}) --    |
    |                                   |     result of                     |
    |                                   |     [`compute_freeling_sentence() |
    |                                   | `{.xref                           |
    |                                   |     .py .py-meth .docutils        |
    |                                   |     .literal                      |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Sentence.compute_freel |
    |                                   | ing_sentence "loacore.classes.cla |
    |                                   | sses.Sentence.compute_freeling_se |
    |                                   | ntence"){.reference               |
    |                                   |     .internal} when called        |
    +-----------------------------------+-----------------------------------+

     `compute_freeling_sentence`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#loacore.classes.classes.Sentence.compute_freeling_sentence "Permalink to this definition"){.headerlink}

    :   <div>
        >
        > Generates a basic `pyfreeling.sentence`{.xref .py .py-class
        > .docutils .literal .notranslate} instance, converting
        > `words`{.xref .py .py-attr .docutils .literal .notranslate} as
        > `pyfreeling.word`{.xref .py .py-class .docutils .literal
        > .notranslate} .
        >
        > </div>

        This function is used to process [`Sentence`{.xref .py .py-class
        .docutils .literal
        .notranslate}](#loacore.classes.classes.Sentence "loacore.classes.classes.Sentence"){.reference
        .internal} with Freeling.

        > <div>
        >
        > +-----------------------------------+-----------------------------------+
        > | Example:                          | Load [`Sentence`{.xref .py        |
        > |                                   | .py-class .docutils .literal      |
        > |                                   | .notranslate}](#loacore.classes.c |
        > |                                   | lasses.Sentence "loacore.classes. |
        > |                                   | classes.Sentence"){.reference     |
        > |                                   | .internal} s from database and    |
        > |                                   | convert them into Freeling        |
        > |                                   | Sentences.                        |
        > |                                   |                                   |
        > |                                   | ::: {.highlight-default .notransl |
        > |                                   | ate}                              |
        > |                                   | ::: {.highlight}                  |
        > |                                   |     >>> import loacore.load.sente |
        > |                                   | nce_load as sentence_load         |
        > |                                   |     >>> sentences = sentence_load |
        > |                                   | .load_sentences()                 |
        > |                                   |     >>> freeling_sentences = [s.c |
        > |                                   | ompute_freeling_sentence() for s  |
        > |                                   | in sentences]                     |
        > |                                   | :::                               |
        > |                                   | :::                               |
        > +-----------------------------------+-----------------------------------+
        > | return:                           | generated Freeling Sentence       |
        > |                                   | instance                          |
        > +-----------------------------------+-----------------------------------+
        > | rtype:                            | `pyfreeling.sentence`{.xref .py   |
        > |                                   | .py-class .docutils .literal      |
        > |                                   | .notranslate}                     |
        > +-----------------------------------+-----------------------------------+
        >
        > </div>

     `print_sentence`{.descname}[(]{.sig-paren}*print\_sentence=True*[)]{.sig-paren}[¶](#loacore.classes.classes.Sentence.print_sentence "Permalink to this definition"){.headerlink}

    :   Convenient way of printing sentences from their word list
        attribute.

          -------------- ---------------------------------------------------------------------------------------------------------------------------------
          Parameters:    **print\_sentence** -- Can be set to False to compute and return the string corresponding to the sentence, without printing it.
          Returns:       String representation of the sentence
          Return type:   string
          -------------- ---------------------------------------------------------------------------------------------------------------------------------
:::

::: {#word .section}
Word[¶](#word "Permalink to this headline"){.headerlink}
--------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`Word`{.descname}[(]{.sig-paren}*id\_word*, *id\_sentence*, *sentence\_index*, *word*, *id\_lemma*, *id\_synset*, *PoS\_tag*[)]{.sig-paren}[¶](#loacore.classes.classes.Word "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_word** (*int*) --       |
    |                                   |     ID\_Word used in Word table   |
    |                                   | -   **id\_sentence** (*int*) --   |
    |                                   |     SQL reference to the          |
    |                                   |     corresponding Sentence        |
    |                                   | -   **sentence\_index** (*int*)   |
    |                                   |     -- Index of the Word in       |
    |                                   |     referenced Sentence           |
    |                                   | -   **word** (*string*) -- Word   |
    |                                   |     form                          |
    |                                   | -   **id\_lemma** (*int*) -- SQL  |
    |                                   |     references to the             |
    |                                   |     corresponding Lemma (Table    |
    |                                   |     Lemma)                        |
    |                                   | -   **lemma** (*string*) --       |
    |                                   |     Possibly associated Lemma     |
    |                                   | -   **id\_synset** (*int*) -- SQL |
    |                                   |     references to corresponding   |
    |                                   |     Synset                        |
    |                                   | -   **synset** ([`Synset`{.xref   |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal                      |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Synset "loacore.classe |
    |                                   | s.classes.Synset"){.reference     |
    |                                   |     .internal}) -- Possibly       |
    |                                   |     associated Synset             |
    |                                   | -   **PoS\_tag** (*string*) --    |
    |                                   |     Possibly associated           |
    |                                   |     Part-of-Speech tag            |
    |                                   | -   **freeling\_word**            |
    |                                   |     (`pyfreeling.word`{.xref .py  |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- result of   |
    |                                   |     [`compute_freeling_word()`{.x |
    |                                   | ref                               |
    |                                   |     .py .py-meth .docutils        |
    |                                   |     .literal                      |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Word.compute_freeling_ |
    |                                   | word "loacore.classes.classes.Wor |
    |                                   | d.compute_freeling_word"){.refere |
    |                                   | nce                               |
    |                                   |     .internal} when called        |
    +-----------------------------------+-----------------------------------+

     `compute_freeling_word`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#loacore.classes.classes.Word.compute_freeling_word "Permalink to this definition"){.headerlink}

    :   Generates a basic `pyfreeling.word`{.xref .py .py-class
        .docutils .literal .notranslate} instance, generated by only the
        word form, even if some analysis could have already been
        realized.

        Moreover, only
        `loacore.classes.classes.File.load_sentence()`{.xref .py
        .py-func .docutils .literal .notranslate} (that itself uses this
        function) should be used, because all Freeling analysis work
        with `pyfreeling.sentence`{.xref .py .py-class .docutils
        .literal .notranslate} instances.
:::

::: {#synset .section}
Synset[¶](#synset "Permalink to this headline"){.headerlink}
------------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`Synset`{.descname}[(]{.sig-paren}*id\_synset*, *id\_word*, *synset\_code*, *synset\_name*, *neg\_score*, *pos\_score*, *obj\_score*[)]{.sig-paren}[¶](#loacore.classes.classes.Synset "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_synset** (*int*) --     |
    |                                   |     ID\_Synset used in Synset     |
    |                                   |     table                         |
    |                                   | -   **id\_word** (*int*) -- SQL   |
    |                                   |     reference to the              |
    |                                   |     corresponding Word            |
    |                                   | -   **synset\_code** (*string*)   |
    |                                   |     -- Synset as represented in   |
    |                                   |     Freeling (ex : 01123148-a)    |
    |                                   | -   **synset\_name** (*string*)   |
    |                                   |     -- Synset as represent in     |
    |                                   |     WordNet and SentiWordNet (ex  |
    |                                   |     : good.a.01)                  |
    |                                   | -   **neg\_score** (*float*) --   |
    |                                   |     Negative polarity from        |
    |                                   |     SentiWordNet.                 |
    |                                   | -   **pos\_score** (*float*) --   |
    |                                   |     Positive polarity from        |
    |                                   |     SentiWordNet.                 |
    |                                   | -   **obj\_score** (*float*) --   |
    |                                   |     Objective polarity from       |
    |                                   |     SentiWordNet.                 |
    +-----------------------------------+-----------------------------------+

    ::: {.admonition .note}
    Note

    neg\_score + pos\_score + obj\_score = 1
    :::
:::

::: {#deptree .section}
DepTree[¶](#deptree "Permalink to this headline"){.headerlink}
--------------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`DepTree`{.descname}[(]{.sig-paren}*id\_dep\_tree*, *id\_dep\_tree\_node*, *id\_sentence*[)]{.sig-paren}[¶](#loacore.classes.classes.DepTree "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_dep\_tree** (*int*) --  |
    |                                   |     Id\_Dep\_Tree used in DepTree |
    |                                   |     table                         |
    |                                   | -   **id\_dep\_tree\_node**       |
    |                                   |     (*int*) -- SQL reference to   |
    |                                   |     root node (Dep\_Tree\_Node    |
    |                                   |     table)                        |
    |                                   | -   **id\_sentence** (*int*) --   |
    |                                   |     SQL reference to the          |
    |                                   |     corresponding Sentence        |
    |                                   | -   **root**                      |
    |                                   |     ([`DepTreeNode`{.xref .py     |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.DepTreeNode "loacore.c |
    |                                   | lasses.classes.DepTreeNode"){.ref |
    |                                   | erence                            |
    |                                   |     .internal}) -- Root node      |
    +-----------------------------------+-----------------------------------+

     `print_dep_tree`{.descname}[(]{.sig-paren}*root=None*, *print\_dep\_tree=True*[)]{.sig-paren}[¶](#loacore.classes.classes.DepTree.print_dep_tree "Permalink to this definition"){.headerlink}

    :   +-----------------------------------+-----------------------------------+
        | Parameters:                       | -   **root**                      |
        |                                   |     ([`DepTreeNode`{.xref .py     |
        |                                   |     .py-class .docutils .literal  |
        |                                   |     .notranslate}](#loacore.class |
        |                                   | es.classes.DepTreeNode "loacore.c |
        |                                   | lasses.classes.DepTreeNode"){.ref |
        |                                   | erence                            |
        |                                   |     .internal}) -- If set, node   |
        |                                   |     from which to start to print  |
        |                                   |     the tree. self.root           |
        |                                   |     otherwise.                    |
        |                                   | -   **print\_dep\_tree**          |
        |                                   |     (*boolean*) -- Can be set to  |
        |                                   |     False to compute and return   |
        |                                   |     the string corresponding to   |
        |                                   |     the tree, without printing    |
        |                                   |     it.                           |
        +-----------------------------------+-----------------------------------+
        | Returns:                          | String representation of DepTree  |
        |                                   | instance                          |
        +-----------------------------------+-----------------------------------+
        | Return type:                      | string                            |
        +-----------------------------------+-----------------------------------+
:::

::: {#deptreenode .section}
DepTreeNode[¶](#deptreenode "Permalink to this headline"){.headerlink}
----------------------------------------------------------------------

 *class* `loacore.classes.classes.`{.descclassname}`DepTreeNode`{.descname}[(]{.sig-paren}*id\_dep\_tree\_node*, *id\_dep\_tree*, *id\_word*, *label*, *root*[)]{.sig-paren}[¶](#loacore.classes.classes.DepTreeNode "Permalink to this definition"){.headerlink}

:   +-----------------------------------+-----------------------------------+
    | Variables:                        | -   **id\_dep\_tree\_node**       |
    |                                   |     (*int*) --                    |
    |                                   |     ID\_Dep\_Tree\_Node used in   |
    |                                   |     Dep\_Tree\_Node table         |
    |                                   | -   **id\_dep\_tree** (*int*) --  |
    |                                   |     SQL reference to the          |
    |                                   |     corresponding DepTree         |
    |                                   | -   **id\_word** (*int*) -- SQL   |
    |                                   |     reference to corresponding    |
    |                                   |     id\_word                      |
    |                                   | -   **word** ([`Word`{.xref .py   |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.Word "loacore.classes. |
    |                                   | classes.Word"){.reference         |
    |                                   |     .internal}) -- Possibly       |
    |                                   |     loaded associated word        |
    |                                   | -   **label** (*string*) -- Node  |
    |                                   |     dependency label. See annex   |
    |                                   |     for details.                  |
    |                                   | -   **root** (*boolean*) -- True  |
    |                                   |     if and only if this is the    |
    |                                   |     root of the corresponding     |
    |                                   |     DepTree                       |
    |                                   | -   **children** (`list`{.xref    |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     [`DepTreeNode`{.xref .py      |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}](#loacore.class |
    |                                   | es.classes.DepTreeNode "loacore.c |
    |                                   | lasses.classes.DepTreeNode"){.ref |
    |                                   | erence                            |
    |                                   |     .internal}) -- Node children  |
    +-----------------------------------+-----------------------------------+
:::
:::

::: {#feeding-database-process-package .section}
Feeding database : *process* package[¶](#feeding-database-process-package "Permalink to this headline"){.headerlink}
====================================================================================================================

This package contains all the necessary modules to perform the process
of new files. Notice that all the processes are automatically handled by
the `file_process.add_files()`{.xref .py .py-func .docutils .literal
.notranslate} function.

::: {#raw-processes .section}
Raw Processes[¶](#raw-processes "Permalink to this headline"){.headerlink}
--------------------------------------------------------------------------

::: {#normalization-and-review-splitting .section}
### Normalization and review splitting[¶](#normalization-and-review-splitting "Permalink to this headline"){.headerlink}

-   Normalization : conversion to UTF-8 and lower case
-   Review splitting : the file text is splitted into reviews

[]{#module-loacore.process.review_process .target}

 `loacore.process.review_process.`{.descclassname}`add_reviews_from_files`{.descname}[(]{.sig-paren}*files*, *encoding*[)]{.sig-paren}[¶](#loacore.process.review_process.add_reviews_from_files "Permalink to this definition"){.headerlink}

:   Load argument files from file system and normalize their content.

    Compute Reviews objects and add them to the database.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    `file_process.add_files()`{.xref .py .py-func .docutils .literal
    .notranslate} function.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **files** (`list`{.xref .py   |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of `File`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate}) --    |
    |                                   |     `File`{.xref .py .py-class    |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate} s to process    |
    |                                   | -   **encoding** (*String*) --    |
    |                                   |     Encoding used to load files.  |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | added `Review`{.xref .py          |
    |                                   | .py-class .docutils .literal      |
    |                                   | .notranslate} s                   |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Review`{.xref .py .py-class   |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.process.review_process.`{.descclassname}`normalize`{.descname}[(]{.sig-paren}*text*[)]{.sig-paren}[¶](#loacore.process.review_process.normalize "Permalink to this definition"){.headerlink}

:   Performs raw text normalization.

    -   Convertion to lower case
    -   Review splitting using python regular expressions : each new
        line correspond to a new review

      -------------- --------------------------------------------------------------------------------------------------------------------------
      Parameters:    **text** (*string*) -- text to process
      Returns:       reviews
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `string`{.xref .py .py-obj .docutils .literal .notranslate}
      -------------- --------------------------------------------------------------------------------------------------------------------------
:::
:::

::: {#freeling-processes .section}
Freeling Processes[¶](#freeling-processes "Permalink to this headline"){.headerlink}
------------------------------------------------------------------------------------

::: {#module-loacore.process.sentence_process .section}
[]{#tokenization}

### tokenization[¶](#module-loacore.process.sentence_process "Permalink to this headline"){.headerlink}

 `loacore.process.sentence_process.`{.descclassname}`add_sentences_from_reviews`{.descname}[(]{.sig-paren}*reviews*[)]{.sig-paren}[¶](#loacore.process.sentence_process.add_sentences_from_reviews "Permalink to this definition"){.headerlink}

:   Performs the first Freeling process applied to each normalized
    review.

    Each review is tokenized, and then splitted into sentences, thanks
    to corresponding Freeling modules.

    A representation of the Sentences and their Words (tokens) are then
    added to corresponding tables.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    `file_process.add_files()`{.xref .py .py-func .docutils .literal
    .notranslate} function.
    :::

      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Parameters:    **reviews** (`list`{.xref .py .py-obj .docutils .literal .notranslate} of `Review`{.xref .py .py-class .docutils .literal .notranslate}) -- `Review`{.xref .py .py-class .docutils .literal .notranslate} s to process
      Returns:       added `Sentence`{.xref .py .py-class .docutils .literal .notranslate} s
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `Sentence`{.xref .py .py-class .docutils .literal .notranslate}
      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

::: {#module-loacore.process.lemma_process .section}
[]{#lemmatization}

### lemmatization[¶](#module-loacore.process.lemma_process "Permalink to this headline"){.headerlink}

 `loacore.process.lemma_process.`{.descclassname}`add_lemmas_to_sentences`{.descname}[(]{.sig-paren}*sentences*, *print\_lemmas=False*[)]{.sig-paren}[¶](#loacore.process.lemma_process.add_lemmas_to_sentences "Permalink to this definition"){.headerlink}

:   Performs a Freeling process to add lemmas to `Word`{.xref .py
    .py-class .docutils .literal .notranslate} s.

    However, the argument is actually a sentence to better fit Freeling
    usage.

    Our `Sentence`{.xref .py .py-class .docutils .literal .notranslate}
    s will be converted to a Freeling Sentences before processing.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    `file_process.add_files()`{.xref .py .py-func .docutils .literal
    .notranslate} function.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) --             |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s to process    |
    |                                   | -   **print\_lemmas** (*boolean*) |
    |                                   |     -- If True, print             |
    |                                   |     lemmatization results         |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.process.synset_process .section}
[]{#disambiguation}

### disambiguation[¶](#module-loacore.process.synset_process "Permalink to this headline"){.headerlink}

 `loacore.process.synset_process.`{.descclassname}`add_polarity_to_synsets`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#loacore.process.synset_process.add_polarity_to_synsets "Permalink to this definition"){.headerlink}

:   Adds the positive/negative/objective polarities of all the synsets
    currently in the table Synset, from the SentiWordNet corpus.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    `file_process.add_files()`{.xref .py .py-func .docutils .literal
    .notranslate} function.
    :::

<!-- -->

 `loacore.process.synset_process.`{.descclassname}`add_synsets_to_sentences`{.descname}[(]{.sig-paren}*sentences*, *print\_synsets=False*[)]{.sig-paren}[¶](#loacore.process.synset_process.add_synsets_to_sentences "Permalink to this definition"){.headerlink}

:   Performs a Freeling process to disambiguate words of the sentences
    according to their context (UKB algorithm) linking them to a unique
    synset (if possible).

    Our `Sentence`{.xref .py .py-class .docutils .literal .notranslate}
    s are converted to Freeling Sentences before processing.

    Notice that even if we may have already computed the Lemmas for
    example, Freeling Sentences generated from our `Sentence`{.xref .py
    .py-class .docutils .literal .notranslate} s are "raw sentences",
    without any analysis linked to their Words. So we make all the
    Freeling process from scratch every time, except *tokenization* and
    *sentence splitting*, to avoid any confusion.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    file\_process.add\_files() function.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) --             |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s to process    |
    |                                   | -   **print\_synsets**            |
    |                                   |     (*boolean*) -- If True, print |
    |                                   |     disambiguation results        |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.process.deptree_process .section}
[]{#dependency-tree-generation}

### dependency tree generation[¶](#module-loacore.process.deptree_process "Permalink to this headline"){.headerlink}

 `loacore.process.deptree_process.`{.descclassname}`add_dep_tree_from_sentences`{.descname}[(]{.sig-paren}*sentences*, *print\_result=False*[)]{.sig-paren}[¶](#loacore.process.deptree_process.add_dep_tree_from_sentences "Permalink to this definition"){.headerlink}

:   Generates the dependency trees of the specified `Sentence`{.xref .py
    .py-class .docutils .literal .notranslate} s and add the results to
    the database.

    Sentences are firstly converted into "raw" Freeling sentences
    (without any analysis) and then all the necessary Freeling processes
    are performed.

    The PoS\_tag of words are also computed and added to the database in
    this function.

    ::: {.admonition .note}
    Note

    This function should be used only inside the
    `file_process.add_files()`{.xref .py .py-func .docutils .literal
    .notranslate} function.
    :::

    ::: {.admonition .note}
    Note

    This process can be quite long. (at least a few minutes)
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) --             |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s to process    |
    |                                   | -   **print\_result** (*boolean*) |
    |                                   |     -- Print PoS\_tags and labels |
    |                                   |     associated to each            |
    |                                   |     `Word`{.xref .py .py-class    |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}                 |
    +-----------------------------------+-----------------------------------+
:::
:::

::: {#module-loacore.process.file_process .section}
[]{#feed-database}

Feed database[¶](#module-loacore.process.file_process "Permalink to this headline"){.headerlink}
------------------------------------------------------------------------------------------------

 `loacore.process.file_process.`{.descclassname}`add_files`{.descname}[(]{.sig-paren}*file\_paths*, *encoding=\'windows-1252\'*[)]{.sig-paren}[¶](#loacore.process.file_process.add_files "Permalink to this definition"){.headerlink}

:   This function performs the full process on all the file\_paths
    specified, and add the results to the corresponding tables.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **file\_paths** (`list`{.xref |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `path-like object`{.xref .py  |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate}) -- Paths used  |
    |                                   |     to load files                 |
    |                                   | -   **encoding** (*String*) --    |
    |                                   |     Files encoding.               |
    +-----------------------------------+-----------------------------------+
    | Example:                          |                                   |
    +-----------------------------------+-----------------------------------+

    Process and load file from the relative directory *data/raw/*

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        file_paths = []
        for dirpath, dirnames, filenames in os.walk(os.path.join('data', 'raw')):
            for name in filenames:
                file_paths.append(os.path.join(dirpath, name))

        file_process.add_files(file_paths)
    :::
    :::
:::
:::

::: {#load-data-from-database-load-package .section}
Load data from database : *load* package[¶](#load-data-from-database-load-package "Permalink to this headline"){.headerlink}
============================================================================================================================

::: {#module-loacore.load.file_load .section}
[]{#load-files}

Load Files[¶](#module-loacore.load.file_load "Permalink to this headline"){.headerlink}
---------------------------------------------------------------------------------------

 `loacore.load.file_load.`{.descclassname}`clean_db`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#loacore.load.file_load.clean_db "Permalink to this definition"){.headerlink}

:   Remove all files from database. Implemented references will also
    engender the deletion of all files dependencies in database : all
    the tables will be emptied.

<!-- -->

 `loacore.load.file_load.`{.descclassname}`load_database`{.descname}[(]{.sig-paren}*id\_files=\[\]*, *load\_reviews=True*, *load\_sentences=True*, *load\_words=True*, *load\_deptrees=True*[)]{.sig-paren}[¶](#loacore.load.file_load.load_database "Permalink to this definition"){.headerlink}

:   Load the complete database as a `list`{.xref .py .py-obj .docutils
    .literal .notranslate} of `File`{.xref .py .py-class .docutils
    .literal .notranslate} , with all the dependencies specified in
    parameters loaded in them.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_files** -- If           |
    |                                   |     specified, load only the      |
    |                                   |     files with the corresponding  |
    |                                   |     ids. Otherwise, load all the  |
    |                                   |     files.                        |
    |                                   | -   **load\_reviews** -- Specify  |
    |                                   |     if Reviews need to be loaded  |
    |                                   |     if `File`{.xref .py .py-class |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_sentences** -- If     |
    |                                   |     Reviews have been loaded,     |
    |                                   |     specify if Sentences need to  |
    |                                   |     be loaded in `Review`{.xref   |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    |                                   | -   **load\_words** -- If         |
    |                                   |     Sentences have been loaded,   |
    |                                   |     specify if Words need to be   |
    |                                   |     loaded in `Sentence`{.xref    |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    |                                   | -   **load\_deptrees** -- If      |
    |                                   |     Words have been loaded,       |
    |                                   |     specify if DepTrees need to   |
    |                                   |     be loaded in `Sentence`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | loaded files                      |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `File`{.xref .py .py-class     |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+

    ::: {.admonition .note}
    Note

    Among the dependencies, only the load\_deptrees should be set to
    False to significantly reduce processing time if they are not
    needed. Loading other structures is quite fast.
    :::

    +-----------------------------------+-----------------------------------+
    | Example:                          | Load files 1,2,3 with only their  |
    |                                   | `id_file`{.xref .py .py-attr      |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | and `id_path`{.xref .py .py-attr  |
    |                                   | .docutils .literal .notranslate}. |
    |                                   |                                   |
    |                                   | ::: {.highlight-default .notransl |
    |                                   | ate}                              |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.database.l |
    |                                   | oad.file_load as file_load        |
    |                                   |     >>> files = file_load.load_da |
    |                                   | tabase(id_files=[1, 2, 3], load_r |
    |                                   | eviews=False)                     |
    |                                   |     >>> print([f.file_path for f  |
    |                                   | in files])                        |
    |                                   |     ['../../data/raw/TempBaja/Bal |
    |                                   | neario2/EncuestaTemporadaBajafina |
    |                                   | lbalneario2_EO.txt',              |
    |                                   |     '../../data/raw/TempBaja/Baln |
    |                                   | eario2/EncuestaTemporadaBajafinal |
    |                                   | balneario2_CC.txt',               |
    |                                   |     '../../data/raw/TempBaja/Baln |
    |                                   | eario2/EncuestaTemporadaBajafinal |
    |                                   | balneario2_GR.txt']               |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load the first 10 files without   |
    |                                   | `DepTree`{.xref .py .py-class     |
    |                                   | .docutils .literal                |
    |                                   | .notranslate} s.                  |
    |                                   |                                   |
    |                                   | ::: {.highlight-default .notransl |
    |                                   | ate}                              |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.file_ |
    |                                   | load as file_load                 |
    |                                   |     >>> files = load_database(id_ |
    |                                   | files=range(1, 11), load_deptrees |
    |                                   | =False)                           |
    |                                   |     >>> print(files[3].reviews[8] |
    |                                   | .review)                          |
    |                                   |     que sea mas grande el parquea |
    |                                   | dero                              |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load the complete database.       |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.file_ |
    |                                   | load as file_load                 |
    |                                   |     >>> files = load_database()   |
    |                                   |     >>> print(len(files))         |
    |                                   |     33                            |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.file_load.`{.descclassname}`remove_files`{.descname}[(]{.sig-paren}*files*[)]{.sig-paren}[¶](#loacore.load.file_load.remove_files "Permalink to this definition"){.headerlink}

:   Remove specified files from database. Implemented references will
    also engender the deletion of all files dependencies in database.

      ------------- ---------------------------------------------------------------------------------------------------------------------------------------
      Parameters:   **files** -- `list`{.xref .py .py-obj .docutils .literal .notranslate} of `File`{.xref .py .py-class .docutils .literal .notranslate}
      ------------- ---------------------------------------------------------------------------------------------------------------------------------------
:::

::: {#module-loacore.load.review_load .section}
[]{#load-reviews}

Load Reviews[¶](#module-loacore.load.review_load "Permalink to this headline"){.headerlink}
-------------------------------------------------------------------------------------------

 `loacore.load.review_load.`{.descclassname}`load_reviews`{.descname}[(]{.sig-paren}*id\_reviews=\[\]*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*[)]{.sig-paren}[¶](#loacore.load.review_load.load_reviews "Permalink to this definition"){.headerlink}

:   Load `Review`{.xref .py .py-class .docutils .literal .notranslate} s
    from database.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_reviews** (`list`{.xref |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `int`{.xref .py .py-obj       |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- If          |
    |                                   |     specified, load only the      |
    |                                   |     reviews with corresponding    |
    |                                   |     ids. Otherwise, load all the  |
    |                                   |     reviews.                      |
    |                                   | -   **load\_sentences**           |
    |                                   |     (*boolean*) -- Specify if     |
    |                                   |     Sentences need to be loaded   |
    |                                   |     in `Review`{.xref .py         |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- If Sentences have been     |
    |                                   |     loaded, specify if Words need |
    |                                   |     to be loaded in               |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded reviews                    |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Review`{.xref .py .py-class   |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | s                                 |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load all reviews with sentences   |
    |                                   | and words                         |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.revie |
    |                                   | w_load as review_load             |
    |                                   |     >>> reviews = review_load.loa |
    |                                   | d_reviews(load_sentences=True, lo |
    |                                   | ad_words=True)                    |
    |                                   |     >>> reviews[0].sentences[0].p |
    |                                   | rint_sentence(print_sentence=Fals |
    |                                   | e)                                |
    |                                   |     'teleferico'                  |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.review_load.`{.descclassname}`load_reviews_by_id_files`{.descname}[(]{.sig-paren}*id\_files*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*[)]{.sig-paren}[¶](#loacore.load.review_load.load_reviews_by_id_files "Permalink to this definition"){.headerlink}

:   Load `Review`{.xref .py .py-class .docutils .literal .notranslate} s
    of files specified by their ids.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_files** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `int`{.xref .py .py-obj       |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- Ids of      |
    |                                   |     files from which reviews      |
    |                                   |     should be loaded.             |
    |                                   | -   **load\_sentences**           |
    |                                   |     (*boolean*) -- Specify if     |
    |                                   |     Sentences need to be loaded   |
    |                                   |     in `Review`{.xref .py         |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- If Sentences have been     |
    |                                   |     loaded, specify if Words need |
    |                                   |     to be loaded in               |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded reviews                    |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Review`{.xref .py .py-class   |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | s                                 |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load reviews from the first file  |
    |                                   | as "raw" reviews, without         |
    |                                   | `Sentence`{.xref .py .py-class    |
    |                                   | .docutils .literal                |
    |                                   | .notranslate} s.                  |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.revie |
    |                                   | w_load as review_load             |
    |                                   |     >>> reviews = review_load.loa |
    |                                   | d_reviews_by_id_files([1])        |
    |                                   |     >>> print(reviews[0].review)  |
    |                                   |     teleferico                    |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.review_load.`{.descclassname}`load_reviews_in_files`{.descname}[(]{.sig-paren}*files*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*[)]{.sig-paren}[¶](#loacore.load.review_load.load_reviews_in_files "Permalink to this definition"){.headerlink}

:   Load `Review`{.xref .py .py-class .docutils .literal .notranslate} s
    into corresponding *files*, setting up their attribute
    `reviews`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded reviews.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_reviews* is set to `True`{.xref .py
    .py-obj .docutils .literal .notranslate}. In most of the cases, this
    function should be used to load files and reviews in one go.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **files** (`list`{.xref .py   |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of `File`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate}) --    |
    |                                   |     Files in which corresponding  |
    |                                   |     reviews will be loaded.       |
    |                                   | -   **load\_sentences**           |
    |                                   |     (*boolean*) -- Specify if     |
    |                                   |     Sentences need to be loaded   |
    |                                   |     in `Review`{.xref .py         |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- If Sentences have been     |
    |                                   |     loaded, specify if Words need |
    |                                   |     to be loaded in               |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded reviews                    |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Review`{.xref .py .py-class   |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | s                                 |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.load.sentence_load .section}
[]{#load-sentences}

Load Sentences[¶](#module-loacore.load.sentence_load "Permalink to this headline"){.headerlink}
-----------------------------------------------------------------------------------------------

 `loacore.load.sentence_load.`{.descclassname}`load_sentences`{.descname}[(]{.sig-paren}*id\_sentences=\[\]*, *load\_words=False*, *load\_deptrees=False*[)]{.sig-paren}[¶](#loacore.load.sentence_load.load_sentences "Permalink to this definition"){.headerlink}

:   Load sentences from database.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_sentences**             |
    |                                   |     (`list`{.xref .py .py-obj     |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate} of `int`{.xref  |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate}) -- If |
    |                                   |     specified, load only the      |
    |                                   |     sentences with corresponding  |
    |                                   |     ids. Otherwise, load all the  |
    |                                   |     sentences.                    |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- Specify if Words need to   |
    |                                   |     be loaded in `Sentence`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded sentences                  |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Sentence`{.xref .py .py-class |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load sentences 1,2 and their      |
    |                                   | words.                            |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.database.l |
    |                                   | oad.sentence_load as sentence_loa |
    |                                   | d                                 |
    |                                   |     >>> sentences = sentence_load |
    |                                   | .load_sentences([1,2], load_words |
    |                                   | =True)                            |
    |                                   |     >>> sentences[0].print_senten |
    |                                   | ce(print_sentence=False)          |
    |                                   |     'teleferico'                  |
    |                                   |     >>> sentences[1].print_senten |
    |                                   | ce(print_sentence=False)          |
    |                                   |     'toboganvy que el agua huela  |
    |                                   | a asufre'                         |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.sentence_load.`{.descclassname}`load_sentences_by_id_files`{.descname}[(]{.sig-paren}*id\_files*, *load\_words=True*, *load\_deptrees=True*[)]{.sig-paren}[¶](#loacore.load.sentence_load.load_sentences_by_id_files "Permalink to this definition"){.headerlink}

:   Ids of files from which sentences should be loaded.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_files** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `int`{.xref .py .py-obj       |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- Ids of      |
    |                                   |     files from which reviews      |
    |                                   |     should be loaded.             |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- Specify if Words need to   |
    |                                   |     be loaded in `Sentence`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded sentences                  |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Sentence`{.xref .py .py-class |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          |                                   |
    +-----------------------------------+-----------------------------------+

    Load all the sentences from file 1.

    ::: {.highlight-default .notranslate}
    ::: {.highlight}
        >>> import loacore.load.sentence_load as sentence_load
        >>> sentences = sentence_load.load_sentences_by_id_files([1])
        >>> sentences[0].print_sentence(print_sentence=False)
        'teleferico'
    :::
    :::

<!-- -->

 `loacore.load.sentence_load.`{.descclassname}`load_sentences_in_reviews`{.descname}[(]{.sig-paren}*reviews*, *load\_words=False*, *load\_deptrees=False*[)]{.sig-paren}[¶](#loacore.load.sentence_load.load_sentences_in_reviews "Permalink to this definition"){.headerlink}

:   Load `Sentence`{.xref .py .py-class .docutils .literal .notranslate}
    s into corresponding *reviews*, setting up their attribute
    `sentences`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded sentences.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} or `review_load.load_reviews()`{.xref .py .py-func
    .docutils .literal .notranslate} when *load\_sentences* is set to
    `True`{.xref .py .py-obj .docutils .literal .notranslate}. In most
    of the cases, those functions should be used instead to load reviews
    and sentences in one go.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **reviews** (`list`{.xref .py |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of              |
    |                                   |     `Review`{.xref .py .py-class  |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- Reviews in  |
    |                                   |     which corresponding sentences |
    |                                   |     should be loaded.             |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- Specify if Words need to   |
    |                                   |     be loaded in `Sentence`{.xref |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    |                                   | -   **load\_deptrees**            |
    |                                   |     (*boolean*) -- If Words have  |
    |                                   |     been loaded, specify if       |
    |                                   |     DepTrees need to be loaded in |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Loaded sentences                  |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Sentence`{.xref .py .py-class |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.load.word_load .section}
[]{#load-words}

Load Words[¶](#module-loacore.load.word_load "Permalink to this headline"){.headerlink}
---------------------------------------------------------------------------------------

 `loacore.load.word_load.`{.descclassname}`load_words`{.descname}[(]{.sig-paren}*id\_words=\[\]*, *load\_lemmas=True*, *load\_synsets=True*[)]{.sig-paren}[¶](#loacore.load.word_load.load_words "Permalink to this definition"){.headerlink}

:   Load `Word`{.xref .py .py-class .docutils .literal .notranslate} s
    from database.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_words** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `int`{.xref .py .py-obj       |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- If          |
    |                                   |     specified, load only the      |
    |                                   |     words with corresponding ids. |
    |                                   |     Otherwise, load all the       |
    |                                   |     words.                        |
    |                                   | -   **load\_lemmas** (*boolean*)  |
    |                                   |     -- Specify if Lemmas need to  |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_synsets** (*boolean*) |
    |                                   |     -- Specify if Synsets need to |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | loaded words                      |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Word`{.xref .py .py-class     |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load all words and their lemmas,  |
    |                                   | synsets.                          |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.word_ |
    |                                   | load as word_load                 |
    |                                   |     >>> words = word_load.load_wo |
    |                                   | rds()                             |
    |                                   |     >>> print([w.word for w in wo |
    |                                   | rds[0:11]])                       |
    |                                   |     ['teleferico', 'toboganvy', ' |
    |                                   | que', 'el', 'agua', 'huela', 'a', |
    |                                   |  'asufre', 'pista', 'de', 'baile' |
    |                                   | ]                                 |
    |                                   |     >>> print([w.lemma for w in w |
    |                                   | ords[0:11]])                      |
    |                                   |     ['', '', 'que', 'el', 'agua', |
    |                                   |  'oler', 'a', '', 'pista', 'de',  |
    |                                   | 'bailar']                         |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.word_load.`{.descclassname}`load_words_in_dep_trees`{.descname}[(]{.sig-paren}*dep\_trees*, *load\_lemmas=True*, *load\_synsets=True*[)]{.sig-paren}[¶](#loacore.load.word_load.load_words_in_dep_trees "Permalink to this definition"){.headerlink}

:   Load `Word`{.xref .py .py-class .docutils .literal .notranslate} s
    into corresponding *dep\_trees*, setting up the attribute
    `word`{.xref .py .py-attr .docutils .literal .notranslate} of each
    node.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_deptrees* is set to `True`{.xref .py
    .py-obj .docutils .literal .notranslate}, or by
    `dep_tree.load_deptrees()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_words* is set to `True`{.xref .py .py-obj
    .docutils .literal .notranslate}. In most of the cases, those
    functions should be used instead to load dep\_trees and words in one
    go.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **dep\_trees** (`list`{.xref  |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `DepTree`{.xref .py .py-class |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- DepTrees in |
    |                                   |     which corresponding words     |
    |                                   |     should be loaded.             |
    |                                   | -   **load\_lemmas** (*boolean*)  |
    |                                   |     -- Specify if Lemmas need to  |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_synsets** (*boolean*) |
    |                                   |     -- Specify if Synsets need to |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.word_load.`{.descclassname}`load_words_in_sentences`{.descname}[(]{.sig-paren}*sentences*, *load\_lemmas=True*, *load\_synsets=True*[)]{.sig-paren}[¶](#loacore.load.word_load.load_words_in_sentences "Permalink to this definition"){.headerlink}

:   Load `Word`{.xref .py .py-class .docutils .literal .notranslate} s
    into corresponding *sentences*, setting up their attribute
    `words`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded words.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} or `sentence_load.load_sentences()`{.xref .py .py-func
    .docutils .literal .notranslate} when *load\_words* is set to
    `True`{.xref .py .py-obj .docutils .literal .notranslate}. In most
    of the cases, those functions should be used instead to load
    sentences and words in one go.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- Sentences   |
    |                                   |     in which corresponding words  |
    |                                   |     should be loaded.             |
    |                                   | -   **load\_lemmas** (*boolean*)  |
    |                                   |     -- Specify if Lemmas need to  |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    |                                   | -   **load\_synsets** (*boolean*) |
    |                                   |     -- Specify if Synsets need to |
    |                                   |     be loaded in `Word`{.xref .py |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate} s.              |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | loaded words                      |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `Word`{.xref .py .py-class     |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.load.synset_load .section}
[]{#load-synsets}

Load Synsets[¶](#module-loacore.load.synset_load "Permalink to this headline"){.headerlink}
-------------------------------------------------------------------------------------------

 `loacore.load.synset_load.`{.descclassname}`load_synsets`{.descname}[(]{.sig-paren}*id\_synsets=\[\]*[)]{.sig-paren}[¶](#loacore.load.synset_load.load_synsets "Permalink to this definition"){.headerlink}

:   Load `Synset`{.xref .py .py-class .docutils .literal .notranslate} s
    from database.

      -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Parameters:    **id\_synsets** (`list`{.xref .py .py-obj .docutils .literal .notranslate} of `Word`{.xref .py .py-class .docutils .literal .notranslate}) -- If specified, load only the synsets with corresponding ids. Otherwise, load all the synsets.
      Returns:       loaded synsets
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `Synset`{.xref .py .py-class .docutils .literal .notranslate}
      Example:       
      -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Load all synsets from database.

    ::: {.highlight-default .notranslate}
    ::: {.highlight}
        >>> import loacore.load.synset_load as synset_load
        >>> synsets = synset_load.load_synsets()
        >>> print(synsets[0].synset_code)
        14845743-n
        >>> print(synsets[0].synset_name)
        water.n.01
    :::
    :::

<!-- -->

 `loacore.load.synset_load.`{.descclassname}`load_synsets_in_words`{.descname}[(]{.sig-paren}*words*[)]{.sig-paren}[¶](#loacore.load.synset_load.load_synsets_in_words "Permalink to this definition"){.headerlink}

:   Load `Synset`{.xref .py .py-class .docutils .literal .notranslate} s
    into corresponding *words*, setting up their attribute
    `synset`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded synsets.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_words* is set to `True`{.xref .py .py-obj
    .docutils .literal .notranslate} or by
    `word_load.load_words()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_synsets* is set to `True`{.xref .py
    .py-obj .docutils .literal .notranslate}. In most of the cases,
    those functions should be used instead to load words and synsets in
    one go.
    :::

      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Parameters:    **words** (`list`{.xref .py .py-obj .docutils .literal .notranslate} of `Word`{.xref .py .py-class .docutils .literal .notranslate}) -- Words in which corresponding synsets should be loaded.
      Returns:       loaded synsets
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `Synset`{.xref .py .py-class .docutils .literal .notranslate}
      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

::: {#module-loacore.load.lemma_load .section}
[]{#load-lemmas}

Load Lemmas[¶](#module-loacore.load.lemma_load "Permalink to this headline"){.headerlink}
-----------------------------------------------------------------------------------------

 `loacore.load.lemma_load.`{.descclassname}`load_lemmas`{.descname}[(]{.sig-paren}*id\_lemmas=\[\]*[)]{.sig-paren}[¶](#loacore.load.lemma_load.load_lemmas "Permalink to this definition"){.headerlink}

:   Load lemmas from database.

      -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Parameters:    **id\_lemmas** (`list`{.xref .py .py-obj .docutils .literal .notranslate} of `int`{.xref .py .py-obj .docutils .literal .notranslate}) -- If specified, load only the lemmas with corresponding ids. Otherwise, load all the lemmas.
      Returns:       loaded lemmas
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `string`{.xref .py .py-obj .docutils .literal .notranslate}
      Example:       
      -------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Load all lemmas from database.

    ::: {.highlight-default .notranslate}
    ::: {.highlight}
        >>> import loacore.load.lemma_load as lemma_load
        >>> lemmas = lemma_load.load_lemmas()
        >>> print(len(lemmas))
        103827
        >>> print(lemmas[10])
        bailar
    :::
    :::

<!-- -->

 `loacore.load.lemma_load.`{.descclassname}`load_lemmas_in_words`{.descname}[(]{.sig-paren}*words*[)]{.sig-paren}[¶](#loacore.load.lemma_load.load_lemmas_in_words "Permalink to this definition"){.headerlink}

:   Load lemmas into corresponding *words*, setting up their attribute
    `lemma`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded lemmas.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_words* is set to `True`{.xref .py .py-obj
    .docutils .literal .notranslate} or by
    `word_load.load_words()`{.xref .py .py-func .docutils .literal
    .notranslate} when *load\_synsets* is set to `True`{.xref .py
    .py-obj .docutils .literal .notranslate}. In most of the cases,
    those functions should be used instead to load words and synsets in
    one go.
    :::

      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Parameters:    **words** (`list`{.xref .py .py-obj .docutils .literal .notranslate} of `Word`{.xref .py .py-class .docutils .literal .notranslate}) -- Words in which corresponding synsets should be loaded.
      Returns:       loaded lemmas
      Return type:   `list`{.xref .py .py-obj .docutils .literal .notranslate} of `string`{.xref .py .py-obj .docutils .literal .notranslate}
      -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

::: {#module-loacore.load.deptree_load .section}
[]{#load-deptrees}

Load DepTrees[¶](#module-loacore.load.deptree_load "Permalink to this headline"){.headerlink}
---------------------------------------------------------------------------------------------

 `loacore.load.deptree_load.`{.descclassname}`load_dep_tree_in_sentences`{.descname}[(]{.sig-paren}*sentences*, *load\_words=True*[)]{.sig-paren}[¶](#loacore.load.deptree_load.load_dep_tree_in_sentences "Permalink to this definition"){.headerlink}

:   Load `DepTree`{.xref .py .py-class .docutils .literal .notranslate}
    s into corresponding *sentences*, setting up their attribute
    `dep_tree`{.xref .py .py-attr .docutils .literal .notranslate}.

    Also return all the loaded deptrees.

    ::: {.admonition .note}
    Note

    This function is automatically called by
    `file_load.load_database()`{.xref .py .py-func .docutils .literal
    .notranslate} or `sentence_load.load_sentences()`{.xref .py .py-func
    .docutils .literal .notranslate} when *load\_deptrees* is set to
    `True`{.xref .py .py-obj .docutils .literal .notranslate}. In most
    of the cases, those functions should be used instead to load
    sentences and deptrees in one go.
    :::

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- Sentences   |
    |                                   |     in which corresponding        |
    |                                   |     DepTrees should be loaded.    |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- Specify if Words need to   |
    |                                   |     be loaded in `DepTree`{.xref  |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | loaded deptrees                   |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `DepTree`{.xref .py .py-class  |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.load.deptree_load.`{.descclassname}`load_dep_trees`{.descname}[(]{.sig-paren}*id\_dep\_trees=\[\]*, *load\_words=True*[)]{.sig-paren}[¶](#loacore.load.deptree_load.load_dep_trees "Permalink to this definition"){.headerlink}

:   Load `DepTree`{.xref .py .py-class .docutils .literal .notranslate}
    s from database.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **id\_dep\_trees**            |
    |                                   |     (`list`{.xref .py .py-obj     |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate} of `int`{.xref  |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate}) -- If |
    |                                   |     specified, load only the      |
    |                                   |     deptrees with corresponding   |
    |                                   |     ids. Otherwise, load all the  |
    |                                   |     deptrees.                     |
    |                                   | -   **load\_words** (*boolean*)   |
    |                                   |     -- Specify if Words need to   |
    |                                   |     be loaded in `DepTree`{.xref  |
    |                                   |     .py .py-class .docutils       |
    |                                   |     .literal .notranslate} s.     |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | loaded deptrees                   |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `DepTree`{.xref .py .py-class  |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          |                                   |
    +-----------------------------------+-----------------------------------+

    Load all deptrees from database : can take a few moments.

    ::: {.highlight-default .notranslate}
    ::: {.highlight}
        >>> import loacore.load.deptree_load as deptree_load
        >>> deptrees = deptree_load.load_dep_trees()
        >>> deptree_str = deptrees[500].print_dep_tree()
        instalaciones (sentence, NCFP000, instalación)
            las (spec, None, el)
            agua (sn, NCCS000, agua)
                el (spec, None, el)
                fria (s.a, None, )
                    y (coord, None, y)
                    caliente (grup.a, AQ0CS00, calentar)
                caminata (sn, NCFS000, caminata)
                    la (spec, None, el)
                tranquilidad (sn, NCFS000, tranquilidad)
                    la (spec, None, el)
                servicio (sn, NCMS000, servicio)
                    el (spec, None, el)
    :::
    :::
:::
:::

::: {#analyse-data-analysis-package .section}
Analyse data : *analysis* package[¶](#analyse-data-analysis-package "Permalink to this headline"){.headerlink}
==============================================================================================================

::: {#module-loacore.analysis.sentiment_analysis .section}
[]{#sentiment-analysis}

Sentiment Analysis[¶](#module-loacore.analysis.sentiment_analysis "Permalink to this headline"){.headerlink}
------------------------------------------------------------------------------------------------------------

 `loacore.analysis.sentiment_analysis.`{.descclassname}`compute_extreme_files_polarity`{.descname}[(]{.sig-paren}*files*, *pessimistic=False*[)]{.sig-paren}[¶](#loacore.analysis.sentiment_analysis.compute_extreme_files_polarity "Permalink to this definition"){.headerlink}

:   Performs *extreme* file polarity computation : only the most
    pessimistic or optimistic sense (according to pessimistic argument)
    is considered. Those values tend to show how the disambiguation
    process is important, due to the huge difference between pessimistic
    and optimistic scores.

    Also notice that this function is an interesting example of how
    other processes could be applied to data already computed in
    database. Here, the computed scores of disambiguated synsets are not
    used, and their are computed from the re-computed possible senses
    thanks to freeling.

    Check source code for more detailed explanations about this example.

    Return a dictionnary that map id\_files to a polarity tuple. A
    polarity tuple is a tuple of length 3, with this form :
    (positive\_score, negative\_score, objective\_score)

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **files** (`list`{.xref .py   |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of              |
    |                                   |     `files`{.xref .py .py-obj     |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}) -- Files to    |
    |                                   |     process                       |
    |                                   | -   **pessimistic** (*boolean*)   |
    |                                   |     -- Specify if pessimistic     |
    |                                   |     computing should be used.     |
    |                                   |     Optimistic is used if set to  |
    |                                   |     False.                        |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | IdFile/Scores dictionary          |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `dict`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `int`{.xref .py .py-obj        |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | : `tuple`{.xref .py .py-obj       |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Compute optimistic and            |
    |                                   | pessimistic polarities and save   |
    |                                   | them as .pdf files using the GUI. |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.file_ |
    |                                   | load as file_load                 |
    |                                   |     >>> import loacore.analysis.s |
    |                                   | entiment_analysis as sentiment_an |
    |                                   | alysis                            |
    |                                   |     >>> from loacore.utils import |
    |                                   |  plot_polarities                  |
    |                                   |     >>> files = file_load.load_da |
    |                                   | tabase(load_deptrees=False)       |
    |                                   |     >>> polarities = sentiment_an |
    |                                   | alysis.compute_extreme_files_pola |
    |                                   | rity(files)                       |
    |                                   |     >>> plot_polarities.save_pola |
    |                                   | rity_pie_charts(polarities)       |
    |                                   |     >>> polarities = sentiment_an |
    |                                   | alysis.compute_extreme_files_pola |
    |                                   | rity(files, pessimistic=True)     |
    |                                   |     >>> plot_polarities.save_pola |
    |                                   | rity_pie_charts(polarities)       |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.analysis.sentiment_analysis.`{.descclassname}`compute_simple_files_polarity`{.descname}[(]{.sig-paren}*files*[)]{.sig-paren}[¶](#loacore.analysis.sentiment_analysis.compute_simple_files_polarity "Permalink to this definition"){.headerlink}

:   Perform the easiest sentiment analysis possible : a normalized sum
    of the positive/negative/objective polarities available in all
    synsets of each file.

    Return a dictionnary that map id\_files to a polarity tuple. A
    polarity tuple is a tuple of length 3, with this form :
    (positive\_score, negative\_score, objective\_score)

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | **files** (`list`{.xref .py       |
    |                                   | .py-obj .docutils .literal        |
    |                                   | .notranslate} of `File`{.xref .py |
    |                                   | .py-class .docutils .literal      |
    |                                   | .notranslate}) -- Files to        |
    |                                   | process                           |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | IdFile/Scores dictionary          |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `dict`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `int`{.xref .py .py-obj        |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | : `tuple`{.xref .py .py-obj       |
    |                                   | .docutils .literal .notranslate}  |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Load all files, compute basic     |
    |                                   | polarities, and show results with |
    |                                   | `utils.print_polarity_table()`{.x |
    |                                   | ref                               |
    |                                   | .py .py-func .docutils .literal   |
    |                                   | .notranslate}.                    |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.file_ |
    |                                   | load as file_load                 |
    |                                   |     >>> import loacore.analysis.s |
    |                                   | entiment_analysis as sentiment_an |
    |                                   | alysis                            |
    |                                   |     >>> files = file_load.load_da |
    |                                   | tabase(load_deptrees=False)       |
    |                                   |     >>> polarities = sentiment_an |
    |                                   | alysis.compute_simple_files_polar |
    |                                   | ity(files)                        |
    |                                   |     >>> from loacore.utils import |
    |                                   |  plot_polarities                  |
    |                                   |     >>> plot_polarities.print_pol |
    |                                   | arity_table(polarities)           |
    |                                   |     +---------------------------- |
    |                                   | -------------------------+------- |
    |                                   | ----+-----------+-----------+     |
    |                                   |     |                         Fil |
    |                                   | e                        | Pos_Sc |
    |                                   | ore | Neg_Score | Obj_Score |     |
    |                                   |     +---------------------------- |
    |                                   | -------------------------+------- |
    |                                   | ----+-----------+-----------+     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario2_EO.txt     |   0.00 |
    |                                   | 0   |   0.000   |   1.000   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario2_CC.txt     |   0.06 |
    |                                   | 9   |   0.016   |   0.915   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario2_GR.txt     |   0.00 |
    |                                   | 0   |   0.000   |   1.000   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario2_JA.txt     |   0.06 |
    |                                   | 0   |   0.065   |   0.875   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario2_CD.txt     |   0.08 |
    |                                   | 0   |   0.057   |   0.863   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario3_JA.txt     |   0.05 |
    |                                   | 5   |   0.023   |   0.922   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario3_CD.txt     |   0.01 |
    |                                   | 9   |   0.022   |   0.958   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario3_CC.txt     |   0.04 |
    |                                   | 4   |   0.003   |   0.953   |     |
    |                                   |     |     EncuestaTemporadaBajafi |
    |                                   | nalbalneario3_GR.txt     |   0.03 |
    |                                   | 6   |   0.000   |   0.964   |     |
    |                                   |     ...                           |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+
:::

::: {#module-loacore.analysis.pattern_recognition .section}
[]{#pattern-recognition}

Pattern Recognition[¶](#module-loacore.analysis.pattern_recognition "Permalink to this headline"){.headerlink}
--------------------------------------------------------------------------------------------------------------

Patterns recognitions are realized on the dependency trees computed with
Freeling. This means that *parent-child* structures will be matched,
what **don't necessarily correspond to adjacent words in the original
sentence**.

 `loacore.analysis.pattern_recognition.`{.descclassname}`general_pattern_recognition`{.descname}[(]{.sig-paren}*sentences*, *pattern*, *types*[)]{.sig-paren}[¶](#loacore.analysis.pattern_recognition.general_pattern_recognition "Permalink to this definition"){.headerlink}

:   Recognize a general pattern, compound of PoS\_tags and dependency
    labels, in the DepTrees associated to specified sentences.

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- Sentences   |
    |                                   |     to process                    |
    |                                   | -   **pattern** (`list`{.xref .py |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of `list`{.xref |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     :obj\`string\`) -- A 2        |
    |                                   |     dimensional list of strings   |
    |                                   |     representing patterns. The    |
    |                                   |     patterns list pattern\[i\]    |
    |                                   |     represents the label that     |
    |                                   |     will match at position i. ex  |
    |                                   |     : *pattern = \[\['V'\],       |
    |                                   |     \['cc', 'ci', 'cd'\]\]* will  |
    |                                   |     match all the                 |
    |                                   |     *Verb/complement* structures. |
    |                                   | -   **types** (`list`{.xref .py   |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of              |
    |                                   |     `string`{.xref .py .py-obj    |
    |                                   |     .docutils .literal            |
    |                                   |     .notranslate}. Allowed value  |
    |                                   |     are 'PoS\_tag' and 'label'.   |
    |                                   |     Otherwise, nothing will       |
    |                                   |     match.) -- Specify what type  |
    |                                   |     of match to use, such that    |
    |                                   |     *types\[i\]* specifies if     |
    |                                   |     elements of *pattern\[i\]*    |
    |                                   |     have to be condidered as      |
    |                                   |     PoS\_tag or label. Notice     |
    |                                   |     that types is unidimensional, |
    |                                   |     whereas pattern can be 2      |
    |                                   |     dimensional : this means that |
    |                                   |     for consistency reason, we    |
    |                                   |     assume that all the tags that |
    |                                   |     can match in a position *i*   |
    |                                   |     are of the same nature.       |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Matching patterns in specified    |
    |                                   | sentences, as node tuples.        |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `tuple`{.xref .py .py-obj      |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `DepTreeNode`{.xref .py        |
    |                                   | .py-class .docutils .literal      |
    |                                   | .notranslate}                     |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Find all the                      |
    |                                   | Verb(PoS\_tag)/complement(label)  |
    |                                   | patterns in file 28(\_PQRS.txt).  |
    |                                   |                                   |
    |                                   | (classically, a negation that     |
    |                                   | applies to the parent verb)       |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.sente |
    |                                   | nce_load as sentence_load         |
    |                                   |     >>> sentences = sentence_load |
    |                                   | .load_sentences_by_id_files([28]) |
    |                                   |     >>> import loacore.analysis.p |
    |                                   | attern_recognition as pattern_rec |
    |                                   | ognition                          |
    |                                   |     >>> patterns = pattern_recogn |
    |                                   | ition.general_pattern_recognition |
    |                                   | (sentences, [['V'], ['cc', 'ci',  |
    |                                   | 'cc']], ['PoS_tag', 'label'])     |
    |                                   |     >>> patterns_str = pattern_re |
    |                                   | cognition.print_patterns(patterns |
    |                                   | , PoS_tag_display=True, label_dis |
    |                                   | play=True)                        |
    |                                   |     ( parece : VMIP3S0 : sentence |
    |                                   | , me : None : ci )                |
    |                                   |     ( promueven : VMIP3P0 : S, en |
    |                                   |  : None : cc )                    |
    |                                   |     ( atiende : VMIP3S0 : S, de : |
    |                                   |  None : cc )                      |
    |                                   |     ( atiende : VMIP3S0 : S, como |
    |                                   |  : None : cc )                    |
    |                                   |     ( atiendan : VMSP3P0 : S, de  |
    |                                   | : None : cc )                     |
    |                                   |     ( atiende : VMIP3S0 : S, en : |
    |                                   |  None : cc )                      |
    |                                   |     ( viniera : VMSI3S0 : S, con  |
    |                                   | : None : cc )                     |
    |                                   |     ( orientar : VMN0000 : S, en  |
    |                                   | : None : cc )                     |
    |                                   |     ( orientar : VMN0000 : S, al  |
    |                                   | : None : cc )                     |
    |                                   |     ( poner : VMN0000 : S, le : N |
    |                                   | one : ci )                        |
    |                                   |     ( poner : VMN0000 : S, a : No |
    |                                   | ne : ci )                         |
    |                                   |     ( establecer : VMN0000 : S, u |
    |                                   | un : None : cc )                  |
    |                                   |     ...                           |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

<!-- -->

 `loacore.analysis.pattern_recognition.`{.descclassname}`label_patterns_recognition`{.descname}[(]{.sig-paren}*sentences*, *pattern*[)]{.sig-paren}[¶](#loacore.analysis.pattern_recognition.label_patterns_recognition "Permalink to this definition"){.headerlink}

:   Recognize a dependency label pattern in the DepTrees associated to
    specified sentences.

    Labels used for Spanish can be found there :

    > <div>
    >
    > -   <http://clic.ub.edu/corpus/webfm_send/20>
    > -   <http://clic.ub.edu/corpus/webfm_send/18>
    > -   <http://clic.ub.edu/corpus/webfm_send/49>
    >
    > </div>

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- Sentences   |
    |                                   |     to process                    |
    |                                   | -   **pattern** (`list`{.xref .py |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of `list`{.xref |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     :obj\`string\`) -- A 2        |
    |                                   |     dimensional list of strings   |
    |                                   |     representing patterns. The    |
    |                                   |     patterns list pattern\[i\]    |
    |                                   |     represents the label that     |
    |                                   |     will match at position i. ex  |
    |                                   |     : *pattern = \[\['sentence',  |
    |                                   |     'v'\], \['*'\]\]\* could be   |
    |                                   |     used to find all the          |
    |                                   |     dependency functions that     |
    |                                   |     could follow *sentence* of    |
    |                                   |     *v* function.                 |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Matching patterns in specified    |
    |                                   | sentences, as node tuples.        |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `tuple`{.xref .py .py-obj      |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `DepTreeNode`{.xref .py        |
    |                                   | .py-class .docutils .literal      |
    |                                   | .notranslate}                     |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Find all node to which a verbal   |
    |                                   | modifier is applied in file 28    |
    |                                   | (\_PQRS.txt).                     |
    |                                   |                                   |
    |                                   | (classically, a negation that     |
    |                                   | applies to the parent verb)       |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.sente |
    |                                   | nce_load as sentence_load         |
    |                                   |     >>> sentences = sentence_load |
    |                                   | .load_sentences_by_id_files([28]) |
    |                                   |     >>> import loacore.analysis.p |
    |                                   | attern_recognition as pattern_rec |
    |                                   | ognition                          |
    |                                   |     >>> patterns = pattern_recogn |
    |                                   | ition.label_patterns_recognition( |
    |                                   | sentences, [['*'], ['mod']])      |
    |                                   |     >>> patterns_str = pattern_re |
    |                                   | cognition.print_patterns(patterns |
    |                                   | , label_display=True)             |
    |                                   |     ( bajar : ao, ya : mod )      |
    |                                   |     ( bajar : ao, no : mod )      |
    |                                   |     ( podia : S, tampoco : mod )  |
    |                                   |     ( quiere : ao, no : mod )     |
    |                                   |     ( dejan : S, no : mod )       |
    |                                   |     ...                           |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

    ::: {.admonition .note}
    Note

    This function can also be used to recognize unigram patterns.

    > <div>
    >
    > **Example :** Find all the nodes with dependency label 'suj' in
    > file 28 (\_PQRS.txt)
    >
    > ::: {.highlight-default .notranslate}
    > ::: {.highlight}
    >     >>> import loacore.load.sentence_load as sentence_load
    >     >>> sentences = sentence_load.load_sentences_by_id_files([28])
    >     >>> import loacore.analysis.pattern_recognition as pattern_recognition
    >     >>> patterns = pattern_recognition.label_patterns_recognition(sentences, [['suj']])
    >     >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
    >     ( colmo : NCMS000 : suj )
    >     ( que : None : suj )
    >     ( que : None : suj )
    >     ( tencion : None : suj )
    >     ( señora : NCFS000 : suj )
    >     ( que : None : suj )
    >     ( turista : NCCS000 : suj )
    >     ( ella : None : suj )
    >     ( que : None : suj )
    >     ...
    > :::
    > :::
    >
    > </div>
    :::

<!-- -->

 `loacore.analysis.pattern_recognition.`{.descclassname}`pos_tag_patterns_recognition`{.descname}[(]{.sig-paren}*sentences*, *pattern*[)]{.sig-paren}[¶](#loacore.analysis.pattern_recognition.pos_tag_patterns_recognition "Permalink to this definition"){.headerlink}

:   Recognize a PoS\_tag pattern in the DepTrees associated to specified
    sentences.

    PoS\_tags corresponding to each language can be found there :
    <https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/tagsets.html>

    +-----------------------------------+-----------------------------------+
    | Parameters:                       | -   **sentences** (`list`{.xref   |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     `Sentence`{.xref .py          |
    |                                   |     .py-class .docutils .literal  |
    |                                   |     .notranslate}) -- Sentences   |
    |                                   |     to process                    |
    |                                   | -   **pattern** (`list`{.xref .py |
    |                                   |     .py-obj .docutils .literal    |
    |                                   |     .notranslate} of `list`{.xref |
    |                                   |     .py .py-obj .docutils         |
    |                                   |     .literal .notranslate} of     |
    |                                   |     :obj\`string\`) --            |
    |                                   |                                   |
    |                                   |     A 2 dimensional list of       |
    |                                   |     strings representing          |
    |                                   |     patterns. The patterns list   |
    |                                   |     pattern\[i\] represents the   |
    |                                   |     PoS\_tags that will match at  |
    |                                   |     position i. ex : *pattern =   |
    |                                   |     \[\['V'\], \['A', 'NC'\]\]*   |
    |                                   |     recognizes verbs followed by  |
    |                                   |     an adjective or a common      |
    |                                   |     noun.                         |
    |                                   |                                   |
    |                                   |     ::: {.admonition .note}       |
    |                                   |     Note                          |
    |                                   |                                   |
    |                                   |     Matches are performed with    |
    |                                   |     the beginning of the          |
    |                                   |     PoS\_tag, according to the    |
    |                                   |     length of the specified tags. |
    |                                   |     For example, 'A' will match   |
    |                                   |     'AQ0CS00', 'AQ0MS00'...       |
    |                                   |     :::                           |
    +-----------------------------------+-----------------------------------+
    | Returns:                          | Matching patterns in specified    |
    |                                   | sentences, as node tuples.        |
    +-----------------------------------+-----------------------------------+
    | Return type:                      | `list`{.xref .py .py-obj          |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `tuple`{.xref .py .py-obj      |
    |                                   | .docutils .literal .notranslate}  |
    |                                   | of `DepTreeNode`{.xref .py        |
    |                                   | .py-class .docutils .literal      |
    |                                   | .notranslate}                     |
    +-----------------------------------+-----------------------------------+
    | Example:                          | Find all Noun/Adjective patterns  |
    |                                   | in file 28 (\_PQRS.txt).          |
    |                                   |                                   |
    |                                   | ::: {.last .highlight-default .no |
    |                                   | translate}                        |
    |                                   | ::: {.highlight}                  |
    |                                   |     >>> import loacore.load.sente |
    |                                   | nce_load as sentence_load         |
    |                                   |     >>> sentences = sentence_load |
    |                                   | .load_sentences_by_id_files([28]) |
    |                                   |     >>> import loacore.analysis.p |
    |                                   | attern_recognition as pattern_rec |
    |                                   | ognition                          |
    |                                   |     >>> patterns = pattern_recogn |
    |                                   | ition.pos_tag_patterns_recognitio |
    |                                   | n(sentences, [['N'], ['A']])      |
    |                                   |     >>> patterns_str = pattern_re |
    |                                   | cognition.print_patterns(patterns |
    |                                   | , PoS_tag_display=True)           |
    |                                   |     ( manera : NCFS000, grosera : |
    |                                   |  AQ0FS00 )                        |
    |                                   |     ( manera : NCFS000, igual : A |
    |                                   | Q0CS00 )                          |
    |                                   |     ( señora : NCFS000, irrespetu |
    |                                   | osa : AQ0FS00 )                   |
    |                                   |     ( zona : NCFS000, visible : A |
    |                                   | Q0CS00 )                          |
    |                                   |     ( manera : NCFS000, grosera : |
    |                                   |  AQ0FS00 )                        |
    |                                   |     ( espacio : NCMS000, mejor :  |
    |                                   | AQ0CS00 )                         |
    |                                   |     ( atencion : NCFS000, mejor : |
    |                                   |  AQ0CS00 )                        |
    |                                   |     ...                           |
    |                                   | :::                               |
    |                                   | :::                               |
    +-----------------------------------+-----------------------------------+

    ::: {.admonition .note}
    Note

    This function can also be used to recognize unigram patterns.

    > <div>
    >
    > **Example :** Find all verbs in file 28 (\_PQRS.txt)
    >
    > ::: {.highlight-default .notranslate}
    > ::: {.highlight}
    >     >>> import loacore.load.sentence_load as sentence_load
    >     >>> sentences = sentence_load.load_sentences_by_id_files([28])
    >     >>> import loacore.analysis.pattern_recognition as pattern_recognition
    >     >>> patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, [['V']])
    >     >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
    >     ( parece : VMIP3S0 : sentence )
    >     ( promueven : VMIP3P0 : S )
    >     ( atiende : VMIP3S0 : S )
    >     ( atiendan : VMSP3P0 : S )
    >     ( atiende : VMIP3S0 : S )
    >     ( viniera : VMSI3S0 : S )
    >     ( orientar : VMN0000 : S )
    >     ( contratar : VMN0000 : S )
    >     ( era : VSII3S0 : sentence )
    >     ( argumentando : VMG0000 : gerundi )
    >     ( poner : VMN0000 : S )
    >     ...
    > :::
    > :::
    >
    > </div>
    :::
:::
:::
:::
:::
:::

::: {.sphinxsidebar role="navigation" aria-label="main navigation"}
::: {.sphinxsidebarwrapper}
### [Table Of Contents](#)

-   [Loacore : Language and Opinion Analyzer for Comments and Reviews's
    documentation!](#){.reference .internal}
-   [Requirements](#requirements){.reference .internal}
    -   [Freeling](#freeling){.reference .internal}
    -   [Database](#database){.reference .internal}
    -   [Utils](#utils){.reference .internal}
-   [Classes](#classes){.reference .internal}
    -   [File](#file){.reference .internal}
    -   [Review](#review){.reference .internal}
    -   [Sentence](#sentence){.reference .internal}
    -   [Word](#word){.reference .internal}
    -   [Synset](#synset){.reference .internal}
    -   [DepTree](#deptree){.reference .internal}
    -   [DepTreeNode](#deptreenode){.reference .internal}
-   [Feeding database : *process*
    package](#feeding-database-process-package){.reference .internal}
    -   [Raw Processes](#raw-processes){.reference .internal}
        -   [Normalization and review
            splitting](#normalization-and-review-splitting){.reference
            .internal}
    -   [Freeling Processes](#freeling-processes){.reference .internal}
        -   [tokenization](#module-loacore.process.sentence_process){.reference
            .internal}
        -   [lemmatization](#module-loacore.process.lemma_process){.reference
            .internal}
        -   [disambiguation](#module-loacore.process.synset_process){.reference
            .internal}
        -   [dependency tree
            generation](#module-loacore.process.deptree_process){.reference
            .internal}
    -   [Feed database](#module-loacore.process.file_process){.reference
        .internal}
-   [Load data from database : *load*
    package](#load-data-from-database-load-package){.reference
    .internal}
    -   [Load Files](#module-loacore.load.file_load){.reference
        .internal}
    -   [Load Reviews](#module-loacore.load.review_load){.reference
        .internal}
    -   [Load Sentences](#module-loacore.load.sentence_load){.reference
        .internal}
    -   [Load Words](#module-loacore.load.word_load){.reference
        .internal}
    -   [Load Synsets](#module-loacore.load.synset_load){.reference
        .internal}
    -   [Load Lemmas](#module-loacore.load.lemma_load){.reference
        .internal}
    -   [Load DepTrees](#module-loacore.load.deptree_load){.reference
        .internal}
-   [Analyse data : *analysis*
    package](#analyse-data-analysis-package){.reference .internal}
    -   [Sentiment
        Analysis](#module-loacore.analysis.sentiment_analysis){.reference
        .internal}
    -   [Pattern
        Recognition](#module-loacore.analysis.pattern_recognition){.reference
        .internal}

::: {.relations}
### Related Topics

-   [Documentation overview](#)
:::

::: {role="note" aria-label="source link"}
### This Page

-   [Show Source](_sources/index.rst.txt)
:::

::: {#searchbox style="display: none" role="search"}
### Quick search

::: {.searchformwrapper}
:::
:::
:::
:::

::: {.clearer}
:::
:::

::: {.footer}
©2018, Universidad Tecnológica de Pereira. \| Powered by [Sphinx
1.7.5](http://sphinx-doc.org/) & [Alabaster
0.7.11](https://github.com/bitprophet/alabaster) \| [Page
source](_sources/index.rst.txt)
:::
