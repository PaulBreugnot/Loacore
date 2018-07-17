Loacore : Language and Opinion Analyzer for Comments and Reviews’s documentation![¶](#loacore-language-and-opinion-analyzer-for-comments-and-reviews-s-documentation "Permalink to this headline"){.headerlink} {#loacore-language-and-opinion-analyzer-for-comments-and-reviewss-documentation}
===============================================================================================================================================================================================================

Requirements[¶](#requirements "Permalink to this headline"){.headerlink} {#requirements}
========================================================================

Freeling[¶](#freeling "Permalink to this headline"){.headerlink} {#freeling}
----------------------------------------------------------------

This project uses an external program, called Freeling, to process
language : <http://nlp.lsi.upc.edu/freeling/>

Check this page to install Freeling on your computer :
<https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/installation/apis-linux.html>

Notice that to use Python API, Freeling needs to be installed from
source with the dedicated options as described in documentation.

**For now**, only a Linux installation in the default folder
*/usr/local* is supported, but this should be fixed in next
improvements.

Database[¶](#database "Permalink to this headline"){.headerlink} {#database}
----------------------------------------------------------------

The embedded database used to store results is an sqlite database,
managed with the sqlite3 Python database API :
<https://docs.python.org/3/library/sqlite3.html>

The corresponding Python package should already be installed in your
Python3 distribution.

Utils[¶](#utils "Permalink to this headline"){.headerlink} {#utils}
----------------------------------------------------------

Package `utils` uses a few graphical modules to show results.

-   PrettyTable : <https://pypi.org/project/PrettyTable/>

-   Matplotlib : <https://matplotlib.org/users/installing.html#linux>

-   Tkinter : <https://wiki.python.org/moin/TkInter>

    Module used to generate gui to save pdf for example.

    Even if the package should be included in Python distribution, on
    Linux distributions you might need to install *tk* package through
    your package manager.

Classes[¶](#classes "Permalink to this headline"){.headerlink} {#classes}
==============================================================

File[¶](#file "Permalink to this headline"){.headerlink} {#file}
--------------------------------------------------------

 *class* `loacore.classes.classes.``File`<span class="sig-paren">(</span>*id\_file*, *file\_path*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.File "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_file</strong> (<em>int</em>) – ID_File used in File table</li>
    <li><strong>file_path</strong> (<em>path-like object</em>) – Path used to load file from file system.</li>
    <li><strong>reviews</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <a href="#loacore.classes.classes.Review" class="reference internal" title="loacore.classes.classes.Review"><code class="sourceCode python">Review</code></a>) – File reviews</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

     `load`<span class="sig-paren">(</span>*encoding='windows-1252'*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.File.load "Permalink to this definition"){.headerlink}

    :   Load file from file system using `file_path` and specified
        encoding.

        |             |                                                                                                                             |
        |-------------|-----------------------------------------------------------------------------------------------------------------------------|
        | Parameters: | **encoding** – Source file encoding. Default is set to *windows-1252*, the encoding obtained from .txt conversion in Excel. |
        | Returns:    | file object                                                                                                                 |

Review[¶](#review "Permalink to this headline"){.headerlink} {#review}
------------------------------------------------------------

 *class* `loacore.classes.classes.``Review`<span class="sig-paren">(</span>*id\_review*, *id\_file*, *file\_index*, *review*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.Review "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_review</strong> (<em>int</em>) – ID_Review used id Review table</li>
    <li><strong>id_file</strong> (<em>int</em>) – SQL reference to the corresponding File</li>
    <li><strong>file_index</strong> (<em>int</em>) – Index of the Review in referenced File</li>
    <li><strong>review</strong> (<em>string</em>) – Review represented as a string</li>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <a href="#loacore.classes.classes.Sentence" class="reference internal" title="loacore.classes.classes.Sentence"><code class="sourceCode python">Sentence</code></a>) – Review Sentences</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

Sentence[¶](#sentence "Permalink to this headline"){.headerlink} {#sentence}
----------------------------------------------------------------

 *class* `loacore.classes.classes.``Sentence`<span class="sig-paren">(</span>*id\_sentence*, *id\_review*, *review\_index*, *id\_dep\_tree*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.Sentence "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_sentence</strong> (<em>int</em>) – ID_Sentence used in Sentence table</li>
    <li><strong>id_review</strong> (<em>int</em>) – SQL reference to the corresponding Review</li>
    <li><strong>review_index</strong> (<em>int</em>) – Index of the Sentence in referenced Review</li>
    <li><strong>id_dep_tree</strong> (<em>int</em>) – SQL reference to a possibly associated DepTree</li>
    <li><strong>words</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <a href="#loacore.classes.classes.Word" class="reference internal" title="loacore.classes.classes.Word"><code class="sourceCode python">Word</code></a>) – Sentence Words</li>
    <li><strong>dep_tree</strong> (<a href="#loacore.classes.classes.DepTree" class="reference internal" title="loacore.classes.classes.DepTree"><code class="sourceCode python">DepTree</code></a>) – Possibly associated DepTree</li>
    <li><strong>freeling_sentence</strong> (<code class="sourceCode python">pyfreeling.sentence</code>) – result of <a href="#loacore.classes.classes.Sentence.compute_freeling_sentence" class="reference internal" title="loacore.classes.classes.Sentence.compute_freeling_sentence"><code class="sourceCode python">compute_freeling_sentence()</code></a> when called</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

     `compute_freeling_sentence`<span class="sig-paren">(</span><span class="sig-paren">)</span>[¶](#loacore.classes.classes.Sentence.compute_freeling_sentence "Permalink to this definition"){.headerlink}

    :   Generates a basic `pyfreeling.sentence` instance, converting
        > `words` as `pyfreeling.word` .

        This function is used to process
        [`Sentence`](#loacore.classes.classes.Sentence "loacore.classes.classes.Sentence"){.reference
        .internal} with Freeling.

        > <table>
        > <tbody>
        > <tr class="odd">
        > <td>Example:</td>
        > <td><p>Load <a href="#loacore.classes.classes.Sentence" class="reference internal" title="loacore.classes.classes.Sentence"><code class="sourceCode python">Sentence</code></a> s from database and convert them into Freeling Sentences.</p>
        > <div class="highlight-default notranslate">
        > <div class="highlight">
        > <pre><code>&gt;&gt;&gt; import loacore.load.sentence_load as sentence_load
        > &gt;&gt;&gt; sentences = sentence_load.load_sentences()
        > &gt;&gt;&gt; freeling_sentences = [s.compute_freeling_sentence() for s in sentences]</code></pre>
        > </div>
        > </div></td>
        > </tr>
        > <tr class="even">
        > <td>return:</td>
        > <td><p>generated Freeling Sentence instance</p></td>
        > </tr>
        > <tr class="odd">
        > <td>rtype:</td>
        > <td><p><code class="sourceCode python">pyfreeling.sentence</code></p></td>
        > </tr>
        > </tbody>
        > </table>
        >
     `print_sentence`<span class="sig-paren">(</span>*print\_sentence=True*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.Sentence.print_sentence "Permalink to this definition"){.headerlink}

    :   Convenient way of printing sentences from their word list
        attribute.

        |              |                                                                                                                                |
        |--------------|--------------------------------------------------------------------------------------------------------------------------------|
        | Parameters:  | **print\_sentence** – Can be set to False to compute and return the string corresponding to the sentence, without printing it. |
        | Returns:     | String representation of the sentence                                                                                          |
        | Return type: | string                                                                                                                         |

Word[¶](#word "Permalink to this headline"){.headerlink} {#word}
--------------------------------------------------------

 *class* `loacore.classes.classes.``Word`<span class="sig-paren">(</span>*id\_word*, *id\_sentence*, *sentence\_index*, *word*, *id\_lemma*, *id\_synset*, *PoS\_tag*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.Word "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_word</strong> (<em>int</em>) – ID_Word used in Word table</li>
    <li><strong>id_sentence</strong> (<em>int</em>) – SQL reference to the corresponding Sentence</li>
    <li><strong>sentence_index</strong> (<em>int</em>) – Index of the Word in referenced Sentence</li>
    <li><strong>word</strong> (<em>string</em>) – Word form</li>
    <li><strong>id_lemma</strong> (<em>int</em>) – SQL references to the corresponding Lemma (Table Lemma)</li>
    <li><strong>lemma</strong> (<em>string</em>) – Possibly associated Lemma</li>
    <li><strong>id_synset</strong> (<em>int</em>) – SQL references to corresponding Synset</li>
    <li><strong>synset</strong> (<a href="#loacore.classes.classes.Synset" class="reference internal" title="loacore.classes.classes.Synset"><code class="sourceCode python">Synset</code></a>) – Possibly associated Synset</li>
    <li><strong>PoS_tag</strong> (<em>string</em>) – Possibly associated Part-of-Speech tag</li>
    <li><strong>freeling_word</strong> (<code class="sourceCode python">pyfreeling.word</code>) – result of <a href="#loacore.classes.classes.Word.compute_freeling_word" class="reference internal" title="loacore.classes.classes.Word.compute_freeling_word"><code class="sourceCode python">compute_freeling_word()</code></a> when called</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

     `compute_freeling_word`<span class="sig-paren">(</span><span class="sig-paren">)</span>[¶](#loacore.classes.classes.Word.compute_freeling_word "Permalink to this definition"){.headerlink}

    :   Generates a basic `pyfreeling.word` instance, generated by only
        the word form, even if some analysis could have already been
        realized.

        Moreover, only `loacore.classes.classes.File.load_sentence()`
        (that itself uses this function) should be used, because all
        Freeling analysis work with `pyfreeling.sentence` instances.

Synset[¶](#synset "Permalink to this headline"){.headerlink} {#synset}
------------------------------------------------------------

 *class* `loacore.classes.classes.``Synset`<span class="sig-paren">(</span>*id\_synset*, *id\_word*, *synset\_code*, *synset\_name*, *neg\_score*, *pos\_score*, *obj\_score*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.Synset "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_synset</strong> (<em>int</em>) – ID_Synset used in Synset table</li>
    <li><strong>id_word</strong> (<em>int</em>) – SQL reference to the corresponding Word</li>
    <li><strong>synset_code</strong> (<em>string</em>) – Synset as represented in Freeling (ex : 01123148-a)</li>
    <li><strong>synset_name</strong> (<em>string</em>) – Synset as represent in WordNet and SentiWordNet (ex : good.a.01)</li>
    <li><strong>neg_score</strong> (<em>float</em>) – Negative polarity from SentiWordNet.</li>
    <li><strong>pos_score</strong> (<em>float</em>) – Positive polarity from SentiWordNet.</li>
    <li><strong>obj_score</strong> (<em>float</em>) – Objective polarity from SentiWordNet.</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

    Note

    neg\_score + pos\_score + obj\_score = 1

DepTree[¶](#deptree "Permalink to this headline"){.headerlink} {#deptree}
--------------------------------------------------------------

 *class* `loacore.classes.classes.``DepTree`<span class="sig-paren">(</span>*id\_dep\_tree*, *id\_dep\_tree\_node*, *id\_sentence*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.DepTree "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_dep_tree</strong> (<em>int</em>) – Id_Dep_Tree used in DepTree table</li>
    <li><strong>id_dep_tree_node</strong> (<em>int</em>) – SQL reference to root node (Dep_Tree_Node table)</li>
    <li><strong>id_sentence</strong> (<em>int</em>) – SQL reference to the corresponding Sentence</li>
    <li><strong>root</strong> (<a href="#loacore.classes.classes.DepTreeNode" class="reference internal" title="loacore.classes.classes.DepTreeNode"><code class="sourceCode python">DepTreeNode</code></a>) – Root node</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

     `print_dep_tree`<span class="sig-paren">(</span>*root=None*, *print\_dep\_tree=True*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.DepTree.print_dep_tree "Permalink to this definition"){.headerlink}

    :   <table>
        <tbody>
        <tr class="odd">
        <td>Parameters:</td>
        <td><ul>
        <li><strong>root</strong> (<a href="#loacore.classes.classes.DepTreeNode" class="reference internal" title="loacore.classes.classes.DepTreeNode"><code class="sourceCode python">DepTreeNode</code></a>) – If set, node from which to start to print the tree. self.root otherwise.</li>
        <li><strong>print_dep_tree</strong> (<em>boolean</em>) – Can be set to False to compute and return the string corresponding to the tree, without printing it.</li>
        </ul></td>
        </tr>
        <tr class="even">
        <td>Returns:</td>
        <td><p>String representation of DepTree instance</p></td>
        </tr>
        <tr class="odd">
        <td>Return type:</td>
        <td><p>string</p></td>
        </tr>
        </tbody>
        </table>

DepTreeNode[¶](#deptreenode "Permalink to this headline"){.headerlink} {#deptreenode}
----------------------------------------------------------------------

 *class* `loacore.classes.classes.``DepTreeNode`<span class="sig-paren">(</span>*id\_dep\_tree\_node*, *id\_dep\_tree*, *id\_word*, *label*, *root*<span class="sig-paren">)</span>[¶](#loacore.classes.classes.DepTreeNode "Permalink to this definition"){.headerlink}

:   <table>
    <tbody>
    <tr class="odd">
    <td>Variables:</td>
    <td><ul>
    <li><strong>id_dep_tree_node</strong> (<em>int</em>) – ID_Dep_Tree_Node used in Dep_Tree_Node table</li>
    <li><strong>id_dep_tree</strong> (<em>int</em>) – SQL reference to the corresponding DepTree</li>
    <li><strong>id_word</strong> (<em>int</em>) – SQL reference to corresponding id_word</li>
    <li><strong>word</strong> (<a href="#loacore.classes.classes.Word" class="reference internal" title="loacore.classes.classes.Word"><code class="sourceCode python">Word</code></a>) – Possibly loaded associated word</li>
    <li><strong>label</strong> (<em>string</em>) – Node dependency label. See annex for details.</li>
    <li><strong>root</strong> (<em>boolean</em>) – True if and only if this is the root of the corresponding DepTree</li>
    <li><strong>children</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <a href="#loacore.classes.classes.DepTreeNode" class="reference internal" title="loacore.classes.classes.DepTreeNode"><code class="sourceCode python">DepTreeNode</code></a>) – Node children</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

Feeding database : *process* package[¶](#feeding-database-process-package "Permalink to this headline"){.headerlink} {#feeding-database-process-package}
====================================================================================================================

This package contains all the necessary modules to perform the process
of new files. Notice that all the processes are automatically handled by
the `file_process.add_files()` function.

Raw Processes[¶](#raw-processes "Permalink to this headline"){.headerlink} {#raw-processes}
--------------------------------------------------------------------------

### Normalization and review splitting[¶](#normalization-and-review-splitting "Permalink to this headline"){.headerlink} {#normalization-and-review-splitting}

-   Normalization : conversion to UTF-8 and lower case
-   Review splitting : the file text is splitted into reviews

<span id="module-loacore.process.review_process" class="target"></span>

 `loacore.process.review_process.``add_reviews_from_files`<span class="sig-paren">(</span>*files*, *encoding*<span class="sig-paren">)</span>[¶](#loacore.process.review_process.add_reviews_from_files "Permalink to this definition"){.headerlink}

:   Load argument files from file system and normalize their content.

    Compute Reviews objects and add them to the database.

    Note

    This function should be used only inside the
    `file_process.add_files()` function.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">File</code>) – <code class="sourceCode python">File</code> s to process</li>
    <li><strong>encoding</strong> (<em>String</em>) – Encoding used to load files.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>added <code class="sourceCode python">Review</code> s</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Review</code></p></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.process.review_process.``normalize`<span class="sig-paren">(</span>*text*<span class="sig-paren">)</span>[¶](#loacore.process.review_process.normalize "Permalink to this definition"){.headerlink}

:   Performs raw text normalization.

    -   Convertion to lower case
    -   Review splitting using python regular expressions : each new
        line correspond to a new review

    |              |                                       |
    |--------------|---------------------------------------|
    | Parameters:  | **text** (*string*) – text to process |
    | Returns:     | reviews                               |
    | Return type: | `list` of `string`                    |

Freeling Processes[¶](#freeling-processes "Permalink to this headline"){.headerlink} {#freeling-processes}
------------------------------------------------------------------------------------

<span id="tokenization"></span>

### tokenization[¶](#module-loacore.process.sentence_process "Permalink to this headline"){.headerlink} {#tokenization}

 `loacore.process.sentence_process.``add_sentences_from_reviews`<span class="sig-paren">(</span>*reviews*<span class="sig-paren">)</span>[¶](#loacore.process.sentence_process.add_sentences_from_reviews "Permalink to this definition"){.headerlink}

:   Performs the first Freeling process applied to each normalized
    review.

    Each review is tokenized, and then splitted into sentences, thanks
    to corresponding Freeling modules.

    A representation of the Sentences and their Words (tokens) are then
    added to corresponding tables.

    Note

    This function should be used only inside the
    `file_process.add_files()` function.

    |              |                                                          |
    |--------------|----------------------------------------------------------|
    | Parameters:  | **reviews** (`list` of `Review`) – `Review` s to process |
    | Returns:     | added `Sentence` s                                       |
    | Return type: | `list` of `Sentence`                                     |

<span id="lemmatization"></span>

### lemmatization[¶](#module-loacore.process.lemma_process "Permalink to this headline"){.headerlink} {#lemmatization}

 `loacore.process.lemma_process.``add_lemmas_to_sentences`<span class="sig-paren">(</span>*sentences*, *print\_lemmas=False*<span class="sig-paren">)</span>[¶](#loacore.process.lemma_process.add_lemmas_to_sentences "Permalink to this definition"){.headerlink}

:   Performs a Freeling process to add lemmas to `Word` s.

    However, the argument is actually a sentence to better fit Freeling
    usage.

    Our `Sentence` s will be converted to a Freeling Sentences before
    processing.

    Note

    This function should be used only inside the
    `file_process.add_files()` function.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – <code class="sourceCode python">Sentence</code> s to process</li>
    <li><strong>print_lemmas</strong> (<em>boolean</em>) – If True, print lemmatization results</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

<span id="disambiguation"></span>

### disambiguation[¶](#module-loacore.process.synset_process "Permalink to this headline"){.headerlink} {#disambiguation}

 `loacore.process.synset_process.``add_polarity_to_synsets`<span class="sig-paren">(</span><span class="sig-paren">)</span>[¶](#loacore.process.synset_process.add_polarity_to_synsets "Permalink to this definition"){.headerlink}

:   Adds the positive/negative/objective polarities of all the synsets
    currently in the table Synset, from the SentiWordNet corpus.

    Note

    This function should be used only inside the
    `file_process.add_files()` function.

<!-- -->

 `loacore.process.synset_process.``add_synsets_to_sentences`<span class="sig-paren">(</span>*sentences*, *print\_synsets=False*<span class="sig-paren">)</span>[¶](#loacore.process.synset_process.add_synsets_to_sentences "Permalink to this definition"){.headerlink}

:   Performs a Freeling process to disambiguate words of the sentences
    according to their context (UKB algorithm) linking them to a unique
    synset (if possible).

    Our `Sentence` s are converted to Freeling Sentences before
    processing.

    Notice that even if we may have already computed the Lemmas for
    example, Freeling Sentences generated from our `Sentence` s are “raw
    sentences”, without any analysis linked to their Words. So we make
    all the Freeling process from scratch every time, except
    *tokenization* and *sentence splitting*, to avoid any confusion.

    Note

    This function should be used only inside the
    file\_process.add\_files() function.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – <code class="sourceCode python">Sentence</code> s to process</li>
    <li><strong>print_synsets</strong> (<em>boolean</em>) – If True, print disambiguation results</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

<span id="dependency-tree-generation"></span>

### dependency tree generation[¶](#module-loacore.process.deptree_process "Permalink to this headline"){.headerlink} {#dependency-tree-generation}

 `loacore.process.deptree_process.``add_dep_tree_from_sentences`<span class="sig-paren">(</span>*sentences*, *print\_result=False*<span class="sig-paren">)</span>[¶](#loacore.process.deptree_process.add_dep_tree_from_sentences "Permalink to this definition"){.headerlink}

:   Generates the dependency trees of the specified `Sentence` s and add
    the results to the database.

    Sentences are firstly converted into “raw” Freeling sentences
    (without any analysis) and then all the necessary Freeling processes
    are performed.

    The PoS\_tag of words are also computed and added to the database in
    this function.

    Note

    This function should be used only inside the
    `file_process.add_files()` function.

    Note

    This process can be quite long. (at least a few minutes)

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – <code class="sourceCode python">Sentence</code> s to process</li>
    <li><strong>print_result</strong> (<em>boolean</em>) – Print PoS_tags and labels associated to each <code class="sourceCode python">Word</code></li>
    </ul></td>
    </tr>
    </tbody>
    </table>

<span id="feed-database"></span>

Feed database[¶](#module-loacore.process.file_process "Permalink to this headline"){.headerlink} {#feed-database}
------------------------------------------------------------------------------------------------

 `loacore.process.file_process.``add_files`<span class="sig-paren">(</span>*file\_paths*, *encoding='windows-1252'*<span class="sig-paren">)</span>[¶](#loacore.process.file_process.add_files "Permalink to this definition"){.headerlink}

:   This function performs the full process on all the file\_paths
    specified, and add the results to the corresponding tables.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>file_paths</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">path<span class="op">-</span>like <span class="bu">object</span></code>) – Paths used to load files</li>
    <li><strong>encoding</strong> (<em>String</em>) – Files encoding.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td></td>
    </tr>
    </tbody>
    </table>

    Process and load file from the relative directory *data/raw/*

        file_paths = []
        for dirpath, dirnames, filenames in os.walk(os.path.join('data', 'raw')):
            for name in filenames:
                file_paths.append(os.path.join(dirpath, name))

        file_process.add_files(file_paths)

Load data from database : *load* package[¶](#load-data-from-database-load-package "Permalink to this headline"){.headerlink} {#load-data-from-database-load-package}
============================================================================================================================

<span id="load-files"></span>

Load Files[¶](#module-loacore.load.file_load "Permalink to this headline"){.headerlink} {#load-files}
---------------------------------------------------------------------------------------

 `loacore.load.file_load.``clean_db`<span class="sig-paren">(</span><span class="sig-paren">)</span>[¶](#loacore.load.file_load.clean_db "Permalink to this definition"){.headerlink}

:   Remove all files from database. Implemented references will also
    engender the deletion of all files dependencies in database : all
    the tables will be emptied.

<!-- -->

 `loacore.load.file_load.``load_database`<span class="sig-paren">(</span>*id\_files=\[\]*, *load\_reviews=True*, *load\_sentences=True*, *load\_words=True*, *load\_deptrees=True*<span class="sig-paren">)</span>[¶](#loacore.load.file_load.load_database "Permalink to this definition"){.headerlink}

:   Load the complete database as a `list` of `File` , with all the
    dependencies specified in parameters loaded in them.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_files</strong> – If specified, load only the files with the corresponding ids. Otherwise, load all the files.</li>
    <li><strong>load_reviews</strong> – Specify if Reviews need to be loaded if <code class="sourceCode python">File</code> s.</li>
    <li><strong>load_sentences</strong> – If Reviews have been loaded, specify if Sentences need to be loaded in <code class="sourceCode python">Review</code> s.</li>
    <li><strong>load_words</strong> – If Sentences have been loaded, specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>loaded files</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">File</code></p></td>
    </tr>
    </tbody>
    </table>

    Note

    Among the dependencies, only the load\_deptrees should be set to
    False to significantly reduce processing time if they are not
    needed. Loading other structures is quite fast.

    <table>
    <tbody>
    <tr class="odd">
    <td>Example:</td>
    <td><p>Load files 1,2,3 with only their <code class="sourceCode python">id_file</code> and <code class="sourceCode python">id_path</code>.</p>
    <div class="highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.database.load.file_load as file_load
    &gt;&gt;&gt; files = file_load.load_database(id_files=[1, 2, 3], load_reviews=False)
    &gt;&gt;&gt; print([f.file_path for f in files])
    [&#39;../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_EO.txt&#39;,
    &#39;../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_CC.txt&#39;,
    &#39;../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_GR.txt&#39;]</code></pre>
    </div>
    </div></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load the first 10 files without <code class="sourceCode python">DepTree</code> s.</p>
    <div class="highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.file_load as file_load
    &gt;&gt;&gt; files = load_database(id_files=range(1, 11), load_deptrees=False)
    &gt;&gt;&gt; print(files[3].reviews[8].review)
    que sea mas grande el parqueadero</code></pre>
    </div>
    </div></td>
    </tr>
    <tr class="odd">
    <td>Example:</td>
    <td><p>Load the complete database.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.file_load as file_load
    &gt;&gt;&gt; files = load_database()
    &gt;&gt;&gt; print(len(files))
    33</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.file_load.``remove_files`<span class="sig-paren">(</span>*files*<span class="sig-paren">)</span>[¶](#loacore.load.file_load.remove_files "Permalink to this definition"){.headerlink}

:   Remove specified files from database. Implemented references will
    also engender the deletion of all files dependencies in database.

    |             |                              |
    |-------------|------------------------------|
    | Parameters: | **files** – `list` of `File` |

<span id="load-reviews"></span>

Load Reviews[¶](#module-loacore.load.review_load "Permalink to this headline"){.headerlink} {#load-reviews}
-------------------------------------------------------------------------------------------

 `loacore.load.review_load.``load_reviews`<span class="sig-paren">(</span>*id\_reviews=\[\]*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*<span class="sig-paren">)</span>[¶](#loacore.load.review_load.load_reviews "Permalink to this definition"){.headerlink}

:   Load `Review` s from database.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_reviews</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – If specified, load only the reviews with corresponding ids. Otherwise, load all the reviews.</li>
    <li><strong>load_sentences</strong> (<em>boolean</em>) – Specify if Sentences need to be loaded in <code class="sourceCode python">Review</code> s.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – If Sentences have been loaded, specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded reviews</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Review</code> s</p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load all reviews with sentences and words</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.review_load as review_load
    &gt;&gt;&gt; reviews = review_load.load_reviews(load_sentences=True, load_words=True)
    &gt;&gt;&gt; reviews[0].sentences[0].print_sentence(print_sentence=False)
    &#39;teleferico&#39;</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.review_load.``load_reviews_by_id_files`<span class="sig-paren">(</span>*id\_files*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*<span class="sig-paren">)</span>[¶](#loacore.load.review_load.load_reviews_by_id_files "Permalink to this definition"){.headerlink}

:   Load `Review` s of files specified by their ids.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – Ids of files from which reviews should be loaded.</li>
    <li><strong>load_sentences</strong> (<em>boolean</em>) – Specify if Sentences need to be loaded in <code class="sourceCode python">Review</code> s.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – If Sentences have been loaded, specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded reviews</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Review</code> s</p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load reviews from the first file as “raw” reviews, without <code class="sourceCode python">Sentence</code> s.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.review_load as review_load
    &gt;&gt;&gt; reviews = review_load.load_reviews_by_id_files([1])
    &gt;&gt;&gt; print(reviews[0].review)
    teleferico</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.review_load.``load_reviews_in_files`<span class="sig-paren">(</span>*files*, *load\_sentences=False*, *load\_words=False*, *load\_deptrees=False*<span class="sig-paren">)</span>[¶](#loacore.load.review_load.load_reviews_in_files "Permalink to this definition"){.headerlink}

:   Load `Review` s into corresponding *files*, setting up their
    attribute `reviews`.

    Also return all the loaded reviews.

    Note

    This function is automatically called by `file_load.load_database()`
    when *load\_reviews* is set to `True`. In most of the cases, this
    function should be used to load files and reviews in one go.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">File</code>) – Files in which corresponding reviews will be loaded.</li>
    <li><strong>load_sentences</strong> (<em>boolean</em>) – Specify if Sentences need to be loaded in <code class="sourceCode python">Review</code> s.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – If Sentences have been loaded, specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded reviews</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Review</code> s</p></td>
    </tr>
    </tbody>
    </table>

<span id="load-sentences"></span>

Load Sentences[¶](#module-loacore.load.sentence_load "Permalink to this headline"){.headerlink} {#load-sentences}
-----------------------------------------------------------------------------------------------

 `loacore.load.sentence_load.``load_sentences`<span class="sig-paren">(</span>*id\_sentences=\[\]*, *load\_words=False*, *load\_deptrees=False*<span class="sig-paren">)</span>[¶](#loacore.load.sentence_load.load_sentences "Permalink to this definition"){.headerlink}

:   Load sentences from database.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – If specified, load only the sentences with corresponding ids. Otherwise, load all the sentences.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – Specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded sentences</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load sentences 1,2 and their words.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.database.load.sentence_load as sentence_load
    &gt;&gt;&gt; sentences = sentence_load.load_sentences([1,2], load_words=True)
    &gt;&gt;&gt; sentences[0].print_sentence(print_sentence=False)
    &#39;teleferico&#39;
    &gt;&gt;&gt; sentences[1].print_sentence(print_sentence=False)
    &#39;toboganvy que el agua huela a asufre&#39;</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.sentence_load.``load_sentences_by_id_files`<span class="sig-paren">(</span>*id\_files*, *load\_words=True*, *load\_deptrees=True*<span class="sig-paren">)</span>[¶](#loacore.load.sentence_load.load_sentences_by_id_files "Permalink to this definition"){.headerlink}

:   Ids of files from which sentences should be loaded.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – Ids of files from which reviews should be loaded.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – Specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded sentences</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td></td>
    </tr>
    </tbody>
    </table>

    Load all the sentences from file 1.

        >>> import loacore.load.sentence_load as sentence_load
        >>> sentences = sentence_load.load_sentences_by_id_files([1])
        >>> sentences[0].print_sentence(print_sentence=False)
        'teleferico'

<!-- -->

 `loacore.load.sentence_load.``load_sentences_in_reviews`<span class="sig-paren">(</span>*reviews*, *load\_words=False*, *load\_deptrees=False*<span class="sig-paren">)</span>[¶](#loacore.load.sentence_load.load_sentences_in_reviews "Permalink to this definition"){.headerlink}

:   Load `Sentence` s into corresponding *reviews*, setting up their
    attribute `sentences`.

    Also return all the loaded sentences.

    Note

    This function is automatically called by `file_load.load_database()`
    or `review_load.load_reviews()` when *load\_sentences* is set to
    `True`. In most of the cases, those functions should be used instead
    to load reviews and sentences in one go.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>reviews</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Review</code>) – Reviews in which corresponding sentences should be loaded.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – Specify if Words need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    <li><strong>load_deptrees</strong> (<em>boolean</em>) – If Words have been loaded, specify if DepTrees need to be loaded in <code class="sourceCode python">Sentence</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Loaded sentences</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code></p></td>
    </tr>
    </tbody>
    </table>

<span id="load-words"></span>

Load Words[¶](#module-loacore.load.word_load "Permalink to this headline"){.headerlink} {#load-words}
---------------------------------------------------------------------------------------

 `loacore.load.word_load.``load_words`<span class="sig-paren">(</span>*id\_words=\[\]*, *load\_lemmas=True*, *load\_synsets=True*<span class="sig-paren">)</span>[¶](#loacore.load.word_load.load_words "Permalink to this definition"){.headerlink}

:   Load `Word` s from database.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_words</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – If specified, load only the words with corresponding ids. Otherwise, load all the words.</li>
    <li><strong>load_lemmas</strong> (<em>boolean</em>) – Specify if Lemmas need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    <li><strong>load_synsets</strong> (<em>boolean</em>) – Specify if Synsets need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>loaded words</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Word</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load all words and their lemmas, synsets.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.word_load as word_load
    &gt;&gt;&gt; words = word_load.load_words()
    &gt;&gt;&gt; print([w.word for w in words[0:11]])
    [&#39;teleferico&#39;, &#39;toboganvy&#39;, &#39;que&#39;, &#39;el&#39;, &#39;agua&#39;, &#39;huela&#39;, &#39;a&#39;, &#39;asufre&#39;, &#39;pista&#39;, &#39;de&#39;, &#39;baile&#39;]
    &gt;&gt;&gt; print([w.lemma for w in words[0:11]])
    [&#39;&#39;, &#39;&#39;, &#39;que&#39;, &#39;el&#39;, &#39;agua&#39;, &#39;oler&#39;, &#39;a&#39;, &#39;&#39;, &#39;pista&#39;, &#39;de&#39;, &#39;bailar&#39;]</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.word_load.``load_words_in_dep_trees`<span class="sig-paren">(</span>*dep\_trees*, *load\_lemmas=True*, *load\_synsets=True*<span class="sig-paren">)</span>[¶](#loacore.load.word_load.load_words_in_dep_trees "Permalink to this definition"){.headerlink}

:   Load `Word` s into corresponding *dep\_trees*, setting up the
    attribute `word` of each node.

    Note

    This function is automatically called by `file_load.load_database()`
    when *load\_deptrees* is set to `True`, or by
    `dep_tree.load_deptrees()` when *load\_words* is set to `True`. In
    most of the cases, those functions should be used instead to load
    dep\_trees and words in one go.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>dep_trees</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">DepTree</code>) – DepTrees in which corresponding words should be loaded.</li>
    <li><strong>load_lemmas</strong> (<em>boolean</em>) – Specify if Lemmas need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    <li><strong>load_synsets</strong> (<em>boolean</em>) – Specify if Synsets need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    </ul></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.word_load.``load_words_in_sentences`<span class="sig-paren">(</span>*sentences*, *load\_lemmas=True*, *load\_synsets=True*<span class="sig-paren">)</span>[¶](#loacore.load.word_load.load_words_in_sentences "Permalink to this definition"){.headerlink}

:   Load `Word` s into corresponding *sentences*, setting up their
    attribute `words`.

    Also return all the loaded words.

    Note

    This function is automatically called by `file_load.load_database()`
    or `sentence_load.load_sentences()` when *load\_words* is set to
    `True`. In most of the cases, those functions should be used instead
    to load sentences and words in one go.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – Sentences in which corresponding words should be loaded.</li>
    <li><strong>load_lemmas</strong> (<em>boolean</em>) – Specify if Lemmas need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    <li><strong>load_synsets</strong> (<em>boolean</em>) – Specify if Synsets need to be loaded in <code class="sourceCode python">Word</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>loaded words</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Word</code></p></td>
    </tr>
    </tbody>
    </table>

<span id="load-synsets"></span>

Load Synsets[¶](#module-loacore.load.synset_load "Permalink to this headline"){.headerlink} {#load-synsets}
-------------------------------------------------------------------------------------------

 `loacore.load.synset_load.``load_synsets`<span class="sig-paren">(</span>*id\_synsets=\[\]*<span class="sig-paren">)</span>[¶](#loacore.load.synset_load.load_synsets "Permalink to this definition"){.headerlink}

:   Load `Synset` s from database.

    |              |                                                                                                                                   |
    |--------------|-----------------------------------------------------------------------------------------------------------------------------------|
    | Parameters:  | **id\_synsets** (`list` of `Word`) – If specified, load only the synsets with corresponding ids. Otherwise, load all the synsets. |
    | Returns:     | loaded synsets                                                                                                                    |
    | Return type: | `list` of `Synset`                                                                                                                |
    | Example:     |                                                                                                                                   |

    Load all synsets from database.

        >>> import loacore.load.synset_load as synset_load
        >>> synsets = synset_load.load_synsets()
        >>> print(synsets[0].synset_code)
        14845743-n
        >>> print(synsets[0].synset_name)
        water.n.01

<!-- -->

 `loacore.load.synset_load.``load_synsets_in_words`<span class="sig-paren">(</span>*words*<span class="sig-paren">)</span>[¶](#loacore.load.synset_load.load_synsets_in_words "Permalink to this definition"){.headerlink}

:   Load `Synset` s into corresponding *words*, setting up their
    attribute `synset`.

    Also return all the loaded synsets.

    Note

    This function is automatically called by `file_load.load_database()`
    when *load\_words* is set to `True` or by `word_load.load_words()`
    when *load\_synsets* is set to `True`. In most of the cases, those
    functions should be used instead to load words and synsets in one
    go.

    |              |                                                                                       |
    |--------------|---------------------------------------------------------------------------------------|
    | Parameters:  | **words** (`list` of `Word`) – Words in which corresponding synsets should be loaded. |
    | Returns:     | loaded synsets                                                                        |
    | Return type: | `list` of `Synset`                                                                    |

<span id="load-lemmas"></span>

Load Lemmas[¶](#module-loacore.load.lemma_load "Permalink to this headline"){.headerlink} {#load-lemmas}
-----------------------------------------------------------------------------------------

 `loacore.load.lemma_load.``load_lemmas`<span class="sig-paren">(</span>*id\_lemmas=\[\]*<span class="sig-paren">)</span>[¶](#loacore.load.lemma_load.load_lemmas "Permalink to this definition"){.headerlink}

:   Load lemmas from database.

    |              |                                                                                                                               |
    |--------------|-------------------------------------------------------------------------------------------------------------------------------|
    | Parameters:  | **id\_lemmas** (`list` of `int`) – If specified, load only the lemmas with corresponding ids. Otherwise, load all the lemmas. |
    | Returns:     | loaded lemmas                                                                                                                 |
    | Return type: | `list` of `string`                                                                                                            |
    | Example:     |                                                                                                                               |

    Load all lemmas from database.

        >>> import loacore.load.lemma_load as lemma_load
        >>> lemmas = lemma_load.load_lemmas()
        >>> print(len(lemmas))
        103827
        >>> print(lemmas[10])
        bailar

<!-- -->

 `loacore.load.lemma_load.``load_lemmas_in_words`<span class="sig-paren">(</span>*words*<span class="sig-paren">)</span>[¶](#loacore.load.lemma_load.load_lemmas_in_words "Permalink to this definition"){.headerlink}

:   Load lemmas into corresponding *words*, setting up their attribute
    `lemma`.

    Also return all the loaded lemmas.

    Note

    This function is automatically called by `file_load.load_database()`
    when *load\_words* is set to `True` or by `word_load.load_words()`
    when *load\_synsets* is set to `True`. In most of the cases, those
    functions should be used instead to load words and synsets in one
    go.

    |              |                                                                                       |
    |--------------|---------------------------------------------------------------------------------------|
    | Parameters:  | **words** (`list` of `Word`) – Words in which corresponding synsets should be loaded. |
    | Returns:     | loaded lemmas                                                                         |
    | Return type: | `list` of `string`                                                                    |

<span id="load-deptrees"></span>

Load DepTrees[¶](#module-loacore.load.deptree_load "Permalink to this headline"){.headerlink} {#load-deptrees}
---------------------------------------------------------------------------------------------

 `loacore.load.deptree_load.``load_dep_tree_in_sentences`<span class="sig-paren">(</span>*sentences*, *load\_words=True*<span class="sig-paren">)</span>[¶](#loacore.load.deptree_load.load_dep_tree_in_sentences "Permalink to this definition"){.headerlink}

:   Load `DepTree` s into corresponding *sentences*, setting up their
    attribute `dep_tree`.

    Also return all the loaded deptrees.

    Note

    This function is automatically called by `file_load.load_database()`
    or `sentence_load.load_sentences()` when *load\_deptrees* is set to
    `True`. In most of the cases, those functions should be used instead
    to load sentences and deptrees in one go.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – Sentences in which corresponding DepTrees should be loaded.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – Specify if Words need to be loaded in <code class="sourceCode python">DepTree</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>loaded deptrees</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">DepTree</code></p></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.load.deptree_load.``load_dep_trees`<span class="sig-paren">(</span>*id\_dep\_trees=\[\]*, *load\_words=True*<span class="sig-paren">)</span>[¶](#loacore.load.deptree_load.load_dep_trees "Permalink to this definition"){.headerlink}

:   Load `DepTree` s from database.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>id_dep_trees</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">int</span></code>) – If specified, load only the deptrees with corresponding ids. Otherwise, load all the deptrees.</li>
    <li><strong>load_words</strong> (<em>boolean</em>) – Specify if Words need to be loaded in <code class="sourceCode python">DepTree</code> s.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>loaded deptrees</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">DepTree</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td></td>
    </tr>
    </tbody>
    </table>

    Load all deptrees from database : can take a few moments.

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

Analyse data : *analysis* package[¶](#analyse-data-analysis-package "Permalink to this headline"){.headerlink} {#analyse-data-analysis-package}
==============================================================================================================

<span id="sentiment-analysis"></span>

Sentiment Analysis[¶](#module-loacore.analysis.sentiment_analysis "Permalink to this headline"){.headerlink} {#sentiment-analysis}
------------------------------------------------------------------------------------------------------------

 `loacore.analysis.sentiment_analysis.``compute_extreme_files_polarity`<span class="sig-paren">(</span>*files*, *pessimistic=False*<span class="sig-paren">)</span>[¶](#loacore.analysis.sentiment_analysis.compute_extreme_files_polarity "Permalink to this definition"){.headerlink}

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

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">files</code>) – Files to process</li>
    <li><strong>pessimistic</strong> (<em>boolean</em>) – Specify if pessimistic computing should be used. Optimistic is used if set to False.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>IdFile/Scores dictionary</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">dict</span></code> of <code class="sourceCode python"><span class="bu">int</span></code> : <code class="sourceCode python"><span class="bu">tuple</span></code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Compute optimistic and pessimistic polarities and save them as .pdf files using the GUI.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.file_load as file_load
    &gt;&gt;&gt; import loacore.analysis.sentiment_analysis as sentiment_analysis
    &gt;&gt;&gt; from loacore.utils import plot_polarities
    &gt;&gt;&gt; files = file_load.load_database(load_deptrees=False)
    &gt;&gt;&gt; polarities = sentiment_analysis.compute_extreme_files_polarity(files)
    &gt;&gt;&gt; plot_polarities.save_polarity_pie_charts(polarities)
    &gt;&gt;&gt; polarities = sentiment_analysis.compute_extreme_files_polarity(files, pessimistic=True)
    &gt;&gt;&gt; plot_polarities.save_polarity_pie_charts(polarities)</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.analysis.sentiment_analysis.``compute_simple_files_polarity`<span class="sig-paren">(</span>*files*<span class="sig-paren">)</span>[¶](#loacore.analysis.sentiment_analysis.compute_simple_files_polarity "Permalink to this definition"){.headerlink}

:   Perform the easiest sentiment analysis possible : a normalized sum
    of the positive/negative/objective polarities available in all
    synsets of each file.

    Return a dictionnary that map id\_files to a polarity tuple. A
    polarity tuple is a tuple of length 3, with this form :
    (positive\_score, negative\_score, objective\_score)

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><p><strong>files</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">File</code>) – Files to process</p></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>IdFile/Scores dictionary</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">dict</span></code> of <code class="sourceCode python"><span class="bu">int</span></code> : <code class="sourceCode python"><span class="bu">tuple</span></code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Load all files, compute basic polarities, and show results with <code class="sourceCode python">utils.print_polarity_table()</code>.</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.file_load as file_load
    &gt;&gt;&gt; import loacore.analysis.sentiment_analysis as sentiment_analysis
    &gt;&gt;&gt; files = file_load.load_database(load_deptrees=False)
    &gt;&gt;&gt; polarities = sentiment_analysis.compute_simple_files_polarity(files)
    &gt;&gt;&gt; from loacore.utils import plot_polarities
    &gt;&gt;&gt; plot_polarities.print_polarity_table(polarities)
    +-----------------------------------------------------+-----------+-----------+-----------+
    |                         File                        | Pos_Score | Neg_Score | Obj_Score |
    +-----------------------------------------------------+-----------+-----------+-----------+
    |     EncuestaTemporadaBajafinalbalneario2_EO.txt     |   0.000   |   0.000   |   1.000   |
    |     EncuestaTemporadaBajafinalbalneario2_CC.txt     |   0.069   |   0.016   |   0.915   |
    |     EncuestaTemporadaBajafinalbalneario2_GR.txt     |   0.000   |   0.000   |   1.000   |
    |     EncuestaTemporadaBajafinalbalneario2_JA.txt     |   0.060   |   0.065   |   0.875   |
    |     EncuestaTemporadaBajafinalbalneario2_CD.txt     |   0.080   |   0.057   |   0.863   |
    |     EncuestaTemporadaBajafinalbalneario3_JA.txt     |   0.055   |   0.023   |   0.922   |
    |     EncuestaTemporadaBajafinalbalneario3_CD.txt     |   0.019   |   0.022   |   0.958   |
    |     EncuestaTemporadaBajafinalbalneario3_CC.txt     |   0.044   |   0.003   |   0.953   |
    |     EncuestaTemporadaBajafinalbalneario3_GR.txt     |   0.036   |   0.000   |   0.964   |
    ...</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<span id="pattern-recognition"></span>

Pattern Recognition[¶](#module-loacore.analysis.pattern_recognition "Permalink to this headline"){.headerlink} {#pattern-recognition}
--------------------------------------------------------------------------------------------------------------

Patterns recognitions are realized on the dependency trees computed with
Freeling. This means that *parent-child* structures will be matched,
what **don’t necessarily correspond to adjacent words in the original
sentence**.

 `loacore.analysis.pattern_recognition.``general_pattern_recognition`<span class="sig-paren">(</span>*sentences*, *pattern*, *types*<span class="sig-paren">)</span>[¶](#loacore.analysis.pattern_recognition.general_pattern_recognition "Permalink to this definition"){.headerlink}

:   Recognize a general pattern, compound of PoS\_tags and dependency
    labels, in the DepTrees associated to specified sentences.

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – Sentences to process</li>
    <li><strong>pattern</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">list</span></code> of :obj`string`) – A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the label that will match at position i. ex : <em>pattern = [[‘V’], [‘cc’, ‘ci’, ‘cd’]]</em> will match all the <em>Verb/complement</em> structures.</li>
    <li><strong>types</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">string</code>. Allowed value are ‘PoS_tag’ and ‘label’. Otherwise, nothing will match.) – Specify what type of match to use, such that <em>types[i]</em> specifies if elements of <em>pattern[i]</em> have to be condidered as PoS_tag or label. Notice that types is unidimensional, whereas pattern can be 2 dimensional : this means that for consistency reason, we assume that all the tags that can match in a position <em>i</em> are of the same nature.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Matching patterns in specified sentences, as node tuples.</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">tuple</span></code> of <code class="sourceCode python">DepTreeNode</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Find all the Verb(PoS_tag)/complement(label) patterns in file 28(_PQRS.txt).</p>
    <p>(classically, a negation that applies to the parent verb)</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.sentence_load as sentence_load
    &gt;&gt;&gt; sentences = sentence_load.load_sentences_by_id_files([28])
    &gt;&gt;&gt; import loacore.analysis.pattern_recognition as pattern_recognition
    &gt;&gt;&gt; patterns = pattern_recognition.general_pattern_recognition(sentences, [[&#39;V&#39;], [&#39;cc&#39;, &#39;ci&#39;, &#39;cc&#39;]], [&#39;PoS_tag&#39;, &#39;label&#39;])
    &gt;&gt;&gt; patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
    ( parece : VMIP3S0 : sentence, me : None : ci )
    ( promueven : VMIP3P0 : S, en : None : cc )
    ( atiende : VMIP3S0 : S, de : None : cc )
    ( atiende : VMIP3S0 : S, como : None : cc )
    ( atiendan : VMSP3P0 : S, de : None : cc )
    ( atiende : VMIP3S0 : S, en : None : cc )
    ( viniera : VMSI3S0 : S, con : None : cc )
    ( orientar : VMN0000 : S, en : None : cc )
    ( orientar : VMN0000 : S, al : None : cc )
    ( poner : VMN0000 : S, le : None : ci )
    ( poner : VMN0000 : S, a : None : ci )
    ( establecer : VMN0000 : S, uun : None : cc )
    ...</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

<!-- -->

 `loacore.analysis.pattern_recognition.``label_patterns_recognition`<span class="sig-paren">(</span>*sentences*, *pattern*<span class="sig-paren">)</span>[¶](#loacore.analysis.pattern_recognition.label_patterns_recognition "Permalink to this definition"){.headerlink}

:   Recognize a dependency label pattern in the DepTrees associated to
    specified sentences.

    Labels used for Spanish can be found there :

    > -   <http://clic.ub.edu/corpus/webfm_send/20>
    > -   <http://clic.ub.edu/corpus/webfm_send/18>
    > -   <http://clic.ub.edu/corpus/webfm_send/49>

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – Sentences to process</li>
    <li><strong>pattern</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">list</span></code> of :obj`string`) – A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the label that will match at position i. ex : <em>pattern = [[‘sentence’, ‘v’], [‘</em>’]]* could be used to find all the dependency functions that could follow <em>sentence</em> of <em>v</em> function.</li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Matching patterns in specified sentences, as node tuples.</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">tuple</span></code> of <code class="sourceCode python">DepTreeNode</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Find all node to which a verbal modifier is applied in file 28 (_PQRS.txt).</p>
    <p>(classically, a negation that applies to the parent verb)</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.sentence_load as sentence_load
    &gt;&gt;&gt; sentences = sentence_load.load_sentences_by_id_files([28])
    &gt;&gt;&gt; import loacore.analysis.pattern_recognition as pattern_recognition
    &gt;&gt;&gt; patterns = pattern_recognition.label_patterns_recognition(sentences, [[&#39;*&#39;], [&#39;mod&#39;]])
    &gt;&gt;&gt; patterns_str = pattern_recognition.print_patterns(patterns, label_display=True)
    ( bajar : ao, ya : mod )
    ( bajar : ao, no : mod )
    ( podia : S, tampoco : mod )
    ( quiere : ao, no : mod )
    ( dejan : S, no : mod )
    ...</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

    Note

    This function can also be used to recognize unigram patterns.

    > **Example :** Find all the nodes with dependency label ‘suj’ in
    > file 28 (\_PQRS.txt)
    >
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

<!-- -->

 `loacore.analysis.pattern_recognition.``pos_tag_patterns_recognition`<span class="sig-paren">(</span>*sentences*, *pattern*<span class="sig-paren">)</span>[¶](#loacore.analysis.pattern_recognition.pos_tag_patterns_recognition "Permalink to this definition"){.headerlink}

:   Recognize a PoS\_tag pattern in the DepTrees associated to specified
    sentences.

    PoS\_tags corresponding to each language can be found there :
    <https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/tagsets.html>

    <table>
    <tbody>
    <tr class="odd">
    <td>Parameters:</td>
    <td><ul>
    <li><strong>sentences</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python">Sentence</code>) – Sentences to process</li>
    <li><p><strong>pattern</strong> (<code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">list</span></code> of :obj`string`) –</p>
    <p>A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the PoS_tags that will match at position i. ex : <em>pattern = [[‘V’], [‘A’, ‘NC’]]</em> recognizes verbs followed by an adjective or a common noun.</p>
    <div class="admonition note">
    <p>Note</p>
    <p>Matches are performed with the beginning of the PoS_tag, according to the length of the specified tags. For example, ‘A’ will match ‘AQ0CS00’, ‘AQ0MS00’…</p>
    </div></li>
    </ul></td>
    </tr>
    <tr class="even">
    <td>Returns:</td>
    <td><p>Matching patterns in specified sentences, as node tuples.</p></td>
    </tr>
    <tr class="odd">
    <td>Return type:</td>
    <td><p><code class="sourceCode python"><span class="bu">list</span></code> of <code class="sourceCode python"><span class="bu">tuple</span></code> of <code class="sourceCode python">DepTreeNode</code></p></td>
    </tr>
    <tr class="even">
    <td>Example:</td>
    <td><p>Find all Noun/Adjective patterns in file 28 (_PQRS.txt).</p>
    <div class="last highlight-default notranslate">
    <div class="highlight">
    <pre><code>&gt;&gt;&gt; import loacore.load.sentence_load as sentence_load
    &gt;&gt;&gt; sentences = sentence_load.load_sentences_by_id_files([28])
    &gt;&gt;&gt; import loacore.analysis.pattern_recognition as pattern_recognition
    &gt;&gt;&gt; patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, [[&#39;N&#39;], [&#39;A&#39;]])
    &gt;&gt;&gt; patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True)
    ( manera : NCFS000, grosera : AQ0FS00 )
    ( manera : NCFS000, igual : AQ0CS00 )
    ( señora : NCFS000, irrespetuosa : AQ0FS00 )
    ( zona : NCFS000, visible : AQ0CS00 )
    ( manera : NCFS000, grosera : AQ0FS00 )
    ( espacio : NCMS000, mejor : AQ0CS00 )
    ( atencion : NCFS000, mejor : AQ0CS00 )
    ...</code></pre>
    </div>
    </div></td>
    </tr>
    </tbody>
    </table>

    Note

    This function can also be used to recognize unigram patterns.

    > **Example :** Find all verbs in file 28 (\_PQRS.txt)
    >
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

### [Table Of Contents](#) {#table-of-contents}

-   [Loacore : Language and Opinion Analyzer for Comments and Reviews’s
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

### Related Topics {#related-topics}

-   [Documentation overview](#)

### This Page {#this-page}

-   [Show Source](_sources/index.rst.txt)

### Quick search {#quick-search}

©2018, Universidad Tecnológica de Pereira. \| Powered by [Sphinx
1.7.5](http://sphinx-doc.org/) & [Alabaster
0.7.11](https://github.com/bitprophet/alabaster) \| [Page
source](_sources/index.rst.txt)
