
.. figure:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/Banner400.png
    :align: center
    :target: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal

Simple Rich Trading Journal
###########################

Simple Rich Trading Journal (srtj) is a journal for your private trading portfolio. The application
runs as a local server and the user interface can be called up in a browser.

**NOTE:** `For (Windows) Edge Users`_, `Required System Rights`_

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/Main.png
    :align: center

✨ The project was realized with the opensource packages from plotly_ and CodeMirror_.


.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/cc.png
    :align: right
    :width: 100px
    :target: https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1

This work is licensed under `CC BY-NC-ND 4.0`_.

Development Status
******************

    0.6.1 #2  (`current note`_)

``srtj`` will be released in beta status until the functionality of all features has been confirmed.
This means that the code may change significantly in the future and the functionality of all
features is not guaranteed.

``srtj`` is being developed under linux, tests under windows are still pending.

**Bug reports, feature requests, ideas or questions?**
    Create an issue or write me a message to `srccircumflex-srtj@outlook.com`_.


Table of Contents
*****************

→ `All Contents`_

- `Install and Run`_
    - `Required System Rights`_
    - `Upgrade and Migration`_
    - `Demo`_

- `The Journal`_
    - `General Information`_
    - `Records`_
    - `General Editing Features`_
    - `Additional Editing Interfaces`_
    - `Filtering, Indexing and Scopes`_
    - `Highlighting, Marking and Categorization`_

- `Environs and Profiles`_
    - `Trading-Journals.srtj Files`_
    - `Creating a Sub-Profile`_
    - `Runtime Configurations - Hierarchy`_

- `Your Display Environ (GUI)`_
    - `For (Windows) Edge Users`_
    - `ShowCase Browser (beta)`_

- `Nice to Know`_
    - `General`_
    - `Bug Notes`_
    - `Version History`_
    - `Whats Next`_

→ `All Contents`_

Install and Run
***************

- Install the latest version of the `Python interpreter`_. At least version 3.10 is required.

- Then, open a terminal/cmd/shell
  (the program name ``python`` could be different depending on the operating system or
  version, e.g. ``python3.10`` or ``py``).

- ``srtj`` is added to the Python Package Index. Use the module ``pip`` to install it:

.. code::

    python -m pip install SimpleRichTradingJournal --upgrade

This installs all the required packages and creates the shell command

.. code::

    srtj

At the first startup, ``srtj`` creates a working directory named ``Trading-Journals.srtj``
and the file ``.srtj`` in your home directory. In ``.srtj`` the path to ``Trading-Journals.srtj``
is saved in which the profiles of ``srtj`` are saved.

  For more information on the directory structure, file handling, personalization's and profiles,
  see `Environs and Profiles`_.

For a user-defined root directory in which ``Trading-Journals.srtj`` is to be created, execute:

.. code::

    srtj install <your root directory>

After start by

.. code::

    srtj

the following message is displayed in the terminal:

.. code::

    Dash is running on http://127.0.0.1:8050/

     * Serving Flask app 'Simple Rich Trading Protocol'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:8050
    Press CTRL+C to quit


The user interface can now be called up via the link in a browser.

↑ `Table of Contents`_

Required System Rights
======================

    See also `srtj upgrade all`_, `Trading-Journals.srtj Files`_, `Creating a Sub-Profile`_

``srtj`` creates symlinks when installing, creating sub-profiles and executing
the ``upgrade`` directive. Administrative rights may be required for this. Execute
``srtj`` in an appropriate shell (run as administrator / sudo).

If the error occurs when creating a sub-profile, it will not be fully created,
``srtj`` **will not register this**.
Run ``srtj upgrade / <profile>`` in a shell with administrative rights to repair the profile.

If the error occurs during installation, the *Trading-Journals.srtj* folder in the installation directory
should be completely deleted before running it again in a shell with administrative rights.


Upgrade and Migration
=====================

``srtj upgrade all``
--------------------

  See also `Trading-Journals.srtj Files`_, `Required System Rights`_

Since version 0.5 the command line directive ``upgrade all`` is available.

.. code::

    srtj upgrade all

This updates all `server files`_, `configuration templates`_ and profile
files that do not yet exist.
Activated configuration files are generally not affected, new attributes
may have to be updated manually (the changes are mentioned in the update notes).
However, it is possible that requests will be submitted for this purpose, among others.

**Your journal data and caches will not be affected!**

The directive **does not affect the demo profile**. This can only be
reinitialized by ``srtj demo init``, which **deletes all** data and configurations
of the demo!

When ``srtj upgrade all`` should be executed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Generally when it is mentioned in an **update note**.
- When a **different python** version is used / updated.
- If the described files are to be **reset**.

From Versions 0.4 to 0.5
------------------------

After the package update, execute:
``srtj upgrade all``

  See also `srtj upgrade all`_


From Versions <= 0.3 to 0.4
---------------------------

In versions <= 0.3, srtj saved the journal data in project directory
``src/cache`` with name ``tradinglog.pkl`` (sub-profiles with pattern
``tradinglog-<profile>.pkl``).
`Install`_ and `create sub-profiles`_ as described here.
Then replace the `journal.pkl`_ file with the ``tradinglog[-<profile>].pkl`` file.
The same procedure can be used for the ``history.pkl`` files.


↑ `Table of Contents`_

Demo
====

A demo is available for testing purposes.

The demo must be initialized once using the following command:

.. code::

    srtj demo init

You can then call it up directly.
``srtj`` treats the demo like a normal profile, i.e. edits are saved.
Future executions of the ``init`` directive will cause a **reinitialization**.
Remove the ``init`` directive from the command to prevent this.

↑ `Table of Contents`_

The Journal
***********

General Information
===================

- The first record must be a deposit.
- Some columns have a slightly different meaning or function depending on the type of record.
- ITC stands for 'Interests, Taxes and other Costs or Income'.

↑ `Table of Contents`_

Records
=======

Trades
------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/trade_open.png
    :align: center

Enter a value greater than ``0`` in the column *n* and define the cells of the columns
*InvestTime* and *InvestAmount* or *InvestCourse* to open a trade. The value from the
*ITC* column is subtracted or added to the final profit in the calculations.

If a value is entered in *TakeAmount* or *TakeCourse* but not in *TakeTime*, the trade
is still considered to be open, the *Profit* and *Performance* cell is calculated and,
if ``with open`` is active, also the summary footer and a visible side section.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/trade_open_with_take.png
    :align: center

A trade is considered finalized if *TakeTime* is also defined.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/trade_fin.png
    :align: center

Another way to close positions is to give the log a closing instruction.
This can also be used to close several individual positions at once or to close individual
positions only partially.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/close_cmd.png
    :align: center

To do this, enter the appropriate *Name*, a negative number *n*, the *TakeTime*
and the *TakeAmount* or *TakeCourse* in a free row.

Deposits
--------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/deposit.png
    :align: center

Enter a ``0`` in the column *n* and define the cells of the columns *InvestTime* and
*InvestAmount* to define a deposit. The value from the *ITC* column is subtracted or
added to the amount in the calculations.

The column *Profit* contains the sum of the profits of the following trades in relation to
non-exhausted previous or interim deposits. *Performance* is then calculated in relation to
the amount. The value in *Dividend* is calculated like *Profit*.

Entries in the column group *Take* are not accepted, these are defined by the program
based on following payouts. Once the amount has been exhausted, the deposit record
will no longer receive a profit value from that point on.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/deposit_ex.png
    :align: center

Payouts
-------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/payout.png
    :align: center

Enter a ``0`` in the column *n* and define the cells of the columns *TakeTime* and
*TakeAmount* to define a payout. The value from the *ITC* column is subtracted
or added to the amount in the calculations.

Payouts are deducted from the sum of deposits, but not from profits. However, if the
payouts exceed the available money, a ITC record is created from the remaining amount.

Entries in the column group *Invest* are not accepted.

The value in *Performance* represents the rate to the sum of previous deposits.

Dividends
---------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/dividend.png
    :align: center

For a dividend record it is important to enter a *Name* first, then enter a ``0`` in
the column *n* and define the cells of the columns *TakeTime* and *TakeAmount* or
*TakeCourse*.

Entries in the column group *Invest* or column *ITC* are not accepted.

If the dividend is defined in column *TakeCourse*, its amount is calculated with the sum of
column *n* of previous associated trades. The *ITC* column represents the sum of the
*InvestAmount*'s of those trades. This is then used to calculate *Performance* to represent
the dividend rate.

A trade belongs to the dividend if the *Name* is identical and it is open at the time of the
dividend. The *Dividend* column of these associated trades is calculated in proportion to the
*InvestAmount*.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/dividend_at_trade.png
    :align: center


Interests, Taxes and other Costs or Income (ITC)
------------------------------------------------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/itc.png
    :align: center

Enter a ``0`` in the column *n* and define the cell of the column *ITC* and
*InvestTime* or *TakeTime* to define a ITC record.

A ITC record is deducted or added to the profit.

Entries in the columns *InvestAmount* or *TakeAmount* are not accepted.

The value in *Performance* represents the rate to the sum of previous deposits.

↑ `Table of Contents`_


General Editing Features
========================

Time specification
------------------

- The time entries in the *InvestTime* and *TakeTime* columns are parsed automatically and
  can be entered according to the following patterns:

    | ``[MM]``
    | ``[hh][MM]``
    | ``[dd][HH][MM]``
    | ``[dd][mm][HH][MM]``
    | ``[dd][mm][yy][HH][MM]``

    With the exception of the last field from the left, all fields must have two digits.
    Characters from ``[ .,:/-]`` are allowed between the fields but are not required. If fields
    are omitted, they are filled from the current date. To apply the current date in full,
    a character from ``[n#0]`` can be entered.

Amount Calculation
------------------

You can enter arithmetic formulas in amount cells.

Supported operants and syntax:
    ============ ==============================================
    ``+``        addition
    ``-``        subtraction
    ``*``        multiplication
    ``/``        division
    ``**``       exponentiation
    ``%``        modulo
    ``&``        bitwise and
    ``|``        bitwise or
    ``^``        bitwise xor
    ``(...)``    calculation in brackets
    ``1 000,1``  international thousands and decimal separator
    ``1.000,1``  non-english thousands and decimal separator
    ``1,000.1``  english thousands and decimal separator
    ============ ==============================================

Copy and Paste
--------------

Functions are implemented but still buggy.

Supported actions:
    ======================== ===========================================================
    ctrl+c                   write a cell content to the clipboard.
    ctrl+x                   write a cell content to the clipboard and delete it from the log.
    ctrl+a, ctrl+y, ctrl+z   write a row to the clipboard.
    ctrl+shift+x             write a row to the clipboard and delete it from the log.
    ctrl+v                   insert the content (if the insertion does not work, move the cursor to another cell and back again and try again).
    ======================== ===========================================================

Until now, the entire log has been recalculated after insertion, which may take more computing time than simply editing a cell.

Currently, the following error may occur temporarily, which leads to the copy function being blocked:
``Uncaught (in promise) DOMException: Clipboard write was blocked due to lack of user activation.``

The feature can be deactivated by `disableCopyPaste`_.

↑ `Table of Contents`_

Additional Editing Interfaces
=============================

Autocompletion
--------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/autoc.png
    :align: left

An autocomplete interface is available for the *Name*, *Symbol*, *ISIN*, *Type*, *Sector*
and *Category* column. Use the key combination ``ctrl+space`` while one of these cells is in focus.

The interface searches for similar entries in the column based on the cell value.
If the cell is empty, press the ``down-arrow`` after calling up the interface.
Click on an entry or select it with ``Enter``. Click anywhere else or press ``Escape``
to close the interface without confirming.


.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

The pool is always created when the page is loaded and is not expanded during editing.


Note Widget
-----------
.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/note.png
    :align: center


The note interface consists of a `dash Markdown component`_ as a display element
(the note sheet) and a `CodeMirror Editor`_ (the note editor).

Get in Touch
~~~~~~~~~~~~

Press ``ctrl+i`` to open the note sheet, if the note editor is not yet open, it will be
opened the next time ``ctrl+i`` is pressed. Otherwise, the note sheet is closed.

``ctrl+shift+i`` has different functions, depending on whether an element of the note
interface is open. If neither the note sheet nor the note editor is open, the key combination
functions as direct access to the note editor. Otherwise, the window position of the elements is switched.

To return the cursor from the note editor to the journal, press ``ctrl+#``. The next time
you press ``ctrl+i``, it jumps back to the note editor.

``esc`` closes all elements of the note interface.

General Syntax Rule
~~~~~~~~~~~~~~~~~~~

The dynamic integration of `cell variables`_ is active by default (`noteCellVariableFormatter`_).
These are processed internally using the `python string format library`_. As the curly brackets
``{}`` are part of their specifications, when using them as characters or in `LaTeX/Mathematics sections`_,
please note that they must be masked by doubling them. This communicates to the formatter
that it is a character and not a command: ``{{`` becomes ``{`` and ``}}`` becomes ``}``.
As the syntax of LaTeX/Mathematics also frequently uses curly brackets, an internal (invisible)
automation is activated by default (`noteMathJaxMasker`_), which masks the curly brackets in LaTeX/Mathematics sections.

Markdown and LaTeX Mathematics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The note interface supports most expressions of the `Markdown language`_, see the
`Markdown Guide`_ for an introduction.

In addition, the rendering of `LaTeX/Mathematics`_ can be activated by `noteMathJax`_.
In the document, the sections that are written in the language must then be delimited by the
character strings ``$$``. Due to the inclusion of various functions, the doubling should
also be used for the inline expression, even if the original documentation provides for a simple ``$``.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/latex.png
    :align: center

Cell Variables
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/cellv.png
    :align: center

The value from a cell in the row can be dynamically included in the document,
for example the time of opening an record via ``{InvestTime}``.

In the file `plugin.py`_ you will find a list of the available fields.

File, Url, Link and Filepath Dropping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/drop.png
    :align: center

A function is implemented and activated by default that recognizes the dropping of files/images,
urls/links and filepaths into the note editor and integrates them into the document in Markdown
language accordingly (`noteFileDropCloner`_).

To ensure that the page can access the file, a copy of the dropped file is created in the asset
folder (this also means that updates to the original file are not applied).
See also `Trading-Journals.srtj Files`_.

**Please note**: For security reasons, all browsers deny access to the file system. Therefore,
links with the ``file:///`` protocol are not functional; hence the implementation of the FileDropClone
feature. Depending on the browser, it is possible to grant access [for certain pages] in various ways.
Here_ is a small excerpt on the topic related to the Firefox browser.

↑ `Table of Contents`_

Filtering, Indexing and Scopes
==============================

There are two different effects when using filters, indexing or scopes.
In the following, *visual* means a purely visual setting of the parameters,
the calculations of the footer and side sections remain unaffected. Whereas a
*real* apply also influences the calculations.

Columns Filter
--------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/table_filter.png
    :align: center

The use of sorting or filtering in columns is purely visual.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

Record Types
------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/type_buttons.png
    :align: center

Filtering with Record Types is purely visual.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

Index by ...
------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/index_by.png
    :align: center

Changing the indexing with the `Index by ...` button is real.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

Quick Search
------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/q_search.png
    :align: left

In the normal state, the Quick Search Entry searches for matches in every cell of a
row and filters purely visually.
However, if the entry is confirmed with ``ctrl+enter``, the filtering becomes real and
matches are only searched in column *Name*.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/s_search.png
    :align: left

From this state, changes in the entry must
always be confirmed with ``ctrl+enter``. In addition, regular expressions are supported
from this state onwards (separate search parameters for multiple *Name*'s with ``|``).
The entry loses its status after it is completely deleted.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

Time Scope
----------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/time_scope.png
    :align: left

A selection of the time scope is real.

About `Scope by ...`
~~~~~~~~~~~~~~~~~~~~

In the `... by Index` status, the time scope is selected based on the indexing according to the
status of the `Index by ...` button.
In the status `... by Both`, based on the values in *InvestTime* and *TakeTime* in each row.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

Calc with open
--------------

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/with_open.png
    :align: left

If the `with open` button is active (default), open positions are included in the calculations of
the footer and side sections.

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/sep.png
    :align: center

↑ `Table of Contents`_

Highlighting, Marking and Categorization
========================================

.. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-main/cat.png
    :align: center

The *Ranking* column is not linked to any internal functions; it is purely used to visualize
an evaluation of the position. All integers between 1 (bad) and incl. 9 (good) are visualized
accordingly.

An record can be marked using the key combination ``ctrl+m`` or ``ctrl+left-click``.
The marking effect in column *Name* is stable, the effect of the entire row can be lost by scrolling
and at the latest after a restart.

``srtj`` provides several columns for the categorization of your positions.
Some are not displayed by default, look in `rconfig.py`_ of your profile.


↑ `Table of Contents`_

Environs and Profiles
*********************

Trading-Journals.srtj Files
===========================

    See also `Install and Run`_, `Required System Rights`_

`journal.pkl`
-------------

This is your journal data as a Python Pickle Object.

`history.pkl`
-------------

Historical data of your journal. The number of entries is
defined by `nHistorySlots`_ (default = 10).

`column-state.pkl` and `column-settings.pkl`
--------------------------------------------

The arrangement of the columns is saved in `column-state.pkl`
if `columnStateCache`_ is activated (default = "global").
The basic settings of the columns are saved in `column-setting.pkl`,
``srtj`` recognizes changes to these and skips loading the cache
during initialization.

`position-colors.pkl`
---------------------

Memory file for position colors of the position chart
when `statisticsUsePositionColorCache`_ is activated (default = "global").

`/files` and `/files/clones`
----------------------------

The `files` folder can be accessed from ``srtj``.
Subfolders can be created here to store files that can be maintained
in the `Note Widget`_, for example. The `clones` subfolder is reserved
for the `File, Url, Link and Filepath Dropping`_ of the `Note Widget`_.

`cleaner.trash` and `cleaner.timestamp`
---------------------------------------

For file system maintenance, a cleaner is active by default,
which removes unused files in `files/clones` and unused entries
in `position-colors.pkl` every `autocleanIntervalS`_ seconds.
`cleaner.timestamp` saves the time of the last cleaning and
`cleaner.trash` is used as a trash can when `noteFileDropClonerFlushTrashing`_
is activated (default = 1). See also `File, Url, Link and Filepath Dropping`_
of the `Note Widget`_.

`#colors.py`, `#plugin.py` and `#rconfig.py`
--------------------------------------------

These files are loaded at startup if the ``#`` is removed from their name.
The attributes of these files are loaded at startup and overwrite the
standard code (see `__env__/...`_). **In order to retain standard attributes,
they must be deleted from the file.**

    See `Runtime Configurations - Hierarchy`_ and the respective file for further information.

`call-gui-engine`
-----------------

This configuration file makes it possible to define a command that is executed
when ``srtj`` is started and to which the url of the srtj-server is passed.

For further information see `call-gui-engine.txt`_.

    See also `Your Display Environ (GUI)`_.


`/%<profile>`
-------------

This folder contains a sub-profile. Its structure corresponds to the main profile,
with the exception of `call-gui-engine`_.

    See also `Creating a Sub-Profile`_.

`/#demo`
--------

This folder contains the demo profile.

    See also `Demo`_.

↑ `Table of Contents`_

Creating a Sub-Profile
======================

    See also `Trading-Journals.srtj Files`_, `Required System Rights`_

A sub-profile can be easily created and called up via the command line:

.. code::

    srtj / 'my second portfolio'


↑ `Table of Contents`_

Runtime Configurations - Hierarchy
==================================

    See also `Trading-Journals.srtj Files`_

Files
-----

`colors.py`_, `plugin.py`_ and `rconfig.py`_ are configuration files ("the configuration files"),
these are provided masked in `Trading-Journals.srtj` and each sub-profile (to activate them,
the ``#`` must be removed from the name).

When ``srtj`` is started, the template configuration files from `__env__/...`_ are loaded first,
then their attributes are overwritten by the configuration files from `Trading-Journals.srtj`
(if available).
If a sub-profile is loaded, its configuration files are loaded at last and the attributes are
overwritten.

Commandline
-----------

In addition, configurations from `rconfig.py`_ can be finally defined via the command line.
The command line parser supports the transfer of lists in python syntax for the definition
of such configurations, note that string types are defined with quotation marks
(otherwise, do not pay attention to these).
Alternatively, only a field of a list can be defined.

.. code::

    srtj colorTheme light scopeByIndex 0 logColOrder [1, 3, 4, 5,2,6,7, 8] logColWidths[2] 100

or

.. code::

    srtj / 'my second portfolio' colorTheme light scopeByIndex 0 logColOrder [1, 3, 4, 5,2,6,7, 8] logColWidths[2] 100

For the demo:

.. code::

    srtj demo colorTheme light scopeByIndex 0 logColOrder [1, 3, 4, 5,2,6,7, 8] logColWidths[2] 100

or

.. code::

    srtj demo init colorTheme light scopeByIndex 0 logColOrder [1, 3, 4, 5,2,6,7, 8] logColWidths[2] 100


↑ `Table of Contents`_


Your Display Environ (GUI)
**************************

As already mentioned, ``srtj`` uses a web engine as a display program.

An automation can be defined via the `call-gui-engine`_ file to execute
a system command that receives the url of the srtj-server.

By default, the system standard browser is called to open a new tab.


For (Windows) Edge Users
========================

The *Microsoft Edge* browser is not compatible as it does not follow the `W3C`_ standards.
Use *Mozilla Firefox* or *Google Chrome* (*Firefox* is recommended) for ``srtj`` instead.
Or use the `ShowCase Browser (beta)`_.


ShowCase Browser (beta)
=======================

  (beta) Compatibility not fully checked!

`call-gui-engine`_ contains a configuration for displaying the ``srtj`` via the
`ShowCase Browser`_ - v3.


↑ `Table of Contents`_



Nice to Know
************

General
=======

- The project has so far only been tested on ``Mozilla Firefox 125.0.2`` on Linux.
- Before the log is (further) edited, large calculations should be completed.
- When calculations are running, ``working...`` is displayed in the tab label.
- The log is recalculated when a defined record is detected or changed.
- Reload the page to reorder all the records.
- Side sections are only calculated if they are visible. If many edits are made, they should be hidden.
- The side section can be hidden by pressing the button in the lower control bar again.
- The bottom control bar is only visible when the mouse is moved over it.
- The size of the side section can be changed: drag/double-click the separator
- Look at `rconfig.py`_
- Look at `plugin.py`_
- If internal errors occur after editing, a red stripe appears.
  This disappears after the next edit without errors.
  If the error cannot be identified, the page should be reloaded.
- Debug by reloading the page.
- After restarting the program in the terminal, the page in the browser must also
  be reloaded. It is best to close the tab and **reopen** it!

Bug Notes
=========

  - All versions below 0.4.3 are defective. Remove the `Trading-Journals.srtj` folder in
    your home directory before you start this version! Make a copy of the journal file
    beforehand to insert it manually after installing version >=0.4.3!

  - Debug by reloading the page.


Version History
===============

0.5.0 #1 (2024-06-19) Your GUI and *<Hypothesis>/Year*

    .. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-u5/about.png

    - srtj now checks the available version at startup and informs about available
      updates in the bottom bar.
    - It is now possible to exit the srtj server from the graphical interface.

    `Your Display Environ (GUI)`_

    - A configuration file is now available that allows a shell command to which the
      url of the srtj-server is passed to be executed at the start.

    .. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-u5/per_y.png

    - New columns and suitable configuration
      `statisticsHypothesisPerDay`_
      added.

    .. image:: https://raw.githubusercontent.com/Simple-Rich-Trading-Journal/docs/main/srtj-u5/c_upd.png

    - The functionality of the course update interval has been optimized.
    - In addition, an update can now also be initiated manually even if
      `coursePluginUpdateInterval`_
      is not activated.

    Fixes:
        - The copy/paste function is a bit more stable.
        - The bug where the cell values are deleted after tab
          navigation during editing is now fixed.
        - `demo` now works as described without the `init` directive.
        - The bug where an error is thrown after canceling an edit
          of an amount cell with an existing value is fixed.
        - The column state caching is now more stable.
        - The configuration `statisticsGroupDefault[2]` is now `0` by default.
        - The file path within the file drop function of the note
          interface has been corrected.

    New version scheme:
        from
            ``major.minor #revision``

                intern:
                    ``'major.minor.revision'``
        to
            ``major.minor.revision #administration-patch``

                intern:
                    ``'major.minor.revision' #administration-patch``
                    (administration-patch internal only as comment)




0.4 #1 (2024-06-08) Relocation
    - Some bugs have been fixed.
    - Columns have been extended.
    - Functions have been added.
    - Demo has been simplified (information in v0.3 is invalid)
    - Command line syntax has been changed.
    - Structure has been fundamentally changed.

0.3 #5 (2024-05-12) @ `srccircumflex/Simple-Rich-Trading-Journal`_
    | `Note Widget`_ implemented

    | Bug fixes, improvements, code maintenance, some **variables and element ids have been renamed**.

        #2
            Module ``config.msg`` created.

        #4
            | Light `colorTheme`_ added.
            | You can now create several journals (see `Creating a Sub-Profile`_).
            | Configurations can now be transferred via the `commandline`_.
            | `Demo`_\ s can now be created for a certain number of years.

        #5
            An bug has been fixed which led to an incorrect calculation of the ITC column of Dividends_.

0.2 #1 (2024-05-05) @ `srccircumflex/Simple-Rich-Trading-Journal`_
    Autocompletion_ implemented

0.1 #1 (2024-04-29) @ `srccircumflex/Simple-Rich-Trading-Journal`_
    Initial Commit


Whats Next
==========

- Export interface.
- Extend documentation.


↑ `Table of Contents`_

All Contents
************

↑ `Table of Contents`_

- `Install and Run`_
    - `Required System Rights`_
    - `Upgrade and Migration`_
        - `srtj upgrade all`_
            - `When srtj upgrade all should be executed`_
        - `From Versions 0.4 to 0.5`_
        - `From Versions <= 0.3 to 0.4`_
    - `Demo`_

- `The Journal`_
    - `General Information`_
    - `Records`_
        - `Trades`_
        - `Deposits`_
        - `Payouts`_
        - `Dividends`_
        - `Interests, Taxes and other Costs or Income (ITC)`_
    - `General Editing Features`_
        - `Time specification`_
        - `Amount Calculation`_
        - `Copy and Paste`_
    - `Additional Editing Interfaces`_
        - `Autocompletion`_
        - `Note Widget`_
            - `Get in Touch`_
            - `General Syntax Rule`_
            - `Markdown and LaTeX Mathematics`_
            - `Cell Variables`_
            - `File, Url, Link and Filepath Dropping`_
    - `Filtering, Indexing and Scopes`_
        - `Columns Filter`_
        - `Record Types`_
        - `Index by ...`_
        - `Quick Search`_
        - `Time Scope`_
            - `About Scope by ...`_
        - `Calc with open`_
    - `Highlighting, Marking and Categorization`_

- `Environs and Profiles`_
    - `Trading-Journals.srtj Files`_
        - `journal.pkl`_
        - `history.pkl`_
        - `column-state.pkl and column-settings.pkl`_
        - `position-colors.pkl`_
        - `/files and /files/clones`_
        - `cleaner.trash and cleaner.timestamp`_
        - `#colors.py, #plugin.py and #rconfig.py`_
        - `call-gui-engine`_
        - `/%<profile>`_
        - `/#demo`_
    - `Creating a Sub-Profile`_
    - `Runtime Configurations - Hierarchy`_
        - `Files`_
        - `Commandline`_

- `Your Display Environ (GUI)`_
    - `For (Windows) Edge Users`_
    - `ShowCase Browser (beta)`_

- `Nice to Know`_
    - `General`_
    - `Bug Notes`_
    - `Version History`_
    - `Whats Next`_

↑ `Table of Contents`_


.. _CC BY-NC-ND 4.0: https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1
.. _srccircumflex-srtj@outlook.com: srccircumflex-srtj@outlook.com
.. _plotly: https://plotly.com/
.. _Python interpreter: https://www.python.org/
.. _W3C: https://www.w3.org/
.. _ShowCase Browser: https://github.com/srccircumflex/ShowCase-Browser

.. _dash Markdown component: https://dash.plotly.com/dash-core-components/markdown
.. _Markdown language: https://en.wikipedia.org/wiki/Markdown
.. _Markdown Guide: https://www.markdownguide.org/
.. _LaTeX/Mathematics: https://en.wikibooks.org/wiki/LaTeX/Mathematics
.. _CodeMirror: https://codemirror.net/5/
.. _CodeMirror Editor: https://codemirror.net/5/
.. _python string format library: https://docs.python.org/3/library/string.html#format-string-syntax
.. _`srccircumflex/Simple-Rich-Trading-Journal`: https://github.com/srccircumflex/Simple-Rich-Trading-Journal

.. _Here: https://github.com/srccircumflex/Simple-Rich-Trading-Journal/blob/master/.repo.doc/~user.js

.. _LaTeX/Mathematics sections: #markdown-and-latex-mathematics
.. _cell variables: #cell-variables

.. _\__env__/...: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__
.. _rconfig.py: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py
.. _plugin.py: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/plugin.py
.. _colors.py: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/colors.py
.. _call-gui-engine.txt: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/call-gui-engine.txt

.. _Install: ./#install-and-run
.. _create sub-profiles: ./#creating-a-sub-profile
.. _journal.pkl: ./#journalpkl
.. _configuration templates: ./#colorspy-pluginpy-and-rconfigpy
.. _server files: ./#files-and-filesclones

.. _current note: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/UPDATE.md



.. _`appHost`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L8
.. _`appPort`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L9
.. _`startupFlushOpenTakeAmount`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L12
.. _`disableCopyPaste`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L13
.. _`disableFooterLifeSignal`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L14
.. _`dateFormat`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L15
.. _`dateFormatFirstDayOfWeek`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L16
.. _`bindKeyCodes`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L18
.. _`colorTheme`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L32
.. _`useDefaultAltColors`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L33
.. _`checkboxLongShortStyling`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L34
.. _`autocleanIntervalS`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L35
.. _`nHistorySlots`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L37
.. _`sideInitBalance`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L42
.. _`gridSideSizeInitScale`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L45
.. _`gridDefWidthScale`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L47
.. _`gridMinWidthScale`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L48
.. _`gridRow3Height`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L49
.. _`bottomBarDistanceBottom`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L50
.. _`bottomBarDistanceRight`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L51
.. _`indexByTakeTime`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L57
.. _`scopeByIndex`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L59
.. _`strictScopeByBoth`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L61
.. _`calcWithOpens`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L68
.. _`logColOrderAssetId`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L75
.. _`logColOrderNote`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L92
.. _`logColOrder`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L107
.. _`logColWidths`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L121
.. _`columnStateCache`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L154
.. _`cellRendererChangeTakeAmount`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L160
.. _`cellRendererChangeTakeCourse`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L161
.. _`cellRendererChangePerformance`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L162
.. _`cellRendererChangeProfit`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L163
.. _`balanceT52W`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L170
.. _`balanceCurrent`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L171
.. _`balanceYears`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L172
.. _`balanceQuarters`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L173
.. _`statisticsGroupDefault`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L178
.. _`statisticsSunMaxDepth`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L189
.. _`statisticsUseSunMaxDepth`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L191
.. _`statisticsIdBySymbol`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L194
.. _`statisticsUsePositionColorCache`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L197
.. _`statisticsPerformanceStepsDefault`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L203
.. _`statisticsPerformanceIntervalDefault`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L205
.. _`statisticsPerformanceFrameDefault`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L207
.. _`statisticsPerformanceRangeDefault`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L209
.. _`statisticsHypothesisPerDay`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L211
.. _`statisticsPerformanceOrder`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L213
.. _`statisticsPerformanceGraphSize`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L236
.. _`statisticsPopGraphSize`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L237
.. _`statisticsOpenPositionsGraphSize`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L238
.. _`statisticsAllPositionsGraphSize`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L239
.. _`notePaperDefaultTransparency`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L246
.. _`noteEditorDefaultTransparency`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L247
.. _`noteFileDropCloner`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L250
.. _`noteFileDropClonerImgAltName`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L258
.. _`noteLinkDropPattern`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L261
.. _`notePathDropPattern`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L263
.. _`noteFileDropClonerFlushTrashing`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L265
.. _`noteMathJax`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L270
.. _`noteCellVariableFormatter`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L274
.. _`noteMathJaxMasker`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L279
.. _`noteUnifying`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L284
.. _`coursePluginUpdateInterval`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L291
.. _`coursePluginUpdateIntervalOn`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L292
.. _`coursePluginUpdateIntervalMs`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L293
.. _`pluginQuickDisable`: https://github.com/Simple-Rich-Trading-Journal/Simple-Rich-Trading-Journal/blob/master/src/SimpleRichTradingJournal/__env__/rconfig.py#L300
