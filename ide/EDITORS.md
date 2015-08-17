xdt99 Editor Support
====================

The `ide` folder provides plugins for various editors and integrated development
environments (IDEs) that assist developers writing code for the TI 99 home
computer.

Currently, xdt99 supports the following development environments:

 * [GNU Emacs][3]
 * [IntelliJ IDEA][6] (including related IDEs such as PyCharm)

Both IDEs are available for free and run on Linux, Mac OS X, and Windows.
Please refer to the projects' home pages for general information about
installation and usage.  For running Emacs on the Windows platform, we recommend
downloading the precompiled binary `emacs-<version>-bin-i686-pc-mingw.zip` from
the [GNU server][4].

Picking an editor is very much a matter of personal taste.  For new users with
no prior experience with either project we recommend IntelliJ IDEA.


GNU Emacs
---------

The Emacs plugin provides two major modes for editing assembly and TI Extended
BASIC programs.  The assembly mode offers syntax highlighting and editing
assistance, while the BASIC mode is currently limited to syntax highlighting.

Please note that stock Emacs uses relatively simple technology for analyzing
source code, so the level of functionality that xdt99 can offer is limited.  For
advanced features such as semantic navigation or code refactoring please use the
IntelliJ IDEA plugin instead.


### Assembly Programs

Assembly support is provided by the `asm99-mode` major mode.  To activate this
mode, press `M-x` (i.e., press the meta key plus the X key) and enter
`asm99-mode` at the prompt.  Please refer to the installation section on how to
automate this step.

`asm99-mode` highlights known TMS 9900 mnemonics and various assembly constructs
such as registers and strings.  The look and feel of the highlighting can be
customized using the Emacs `font-lock` faces.

The `comment-region` command (typically bound to `C-c ;`) adds the xdt99 comment
character `;` to a range of lines.  Conversely, the `uncomment-region` command
removes a single `;` character from each line.

Two minor modes provide support for smart keyboard navigation.  The
`asm99-smart-tab-mode` minor mode will

 * automatically indent the current line based on the left-most character or
   word, and
 * advance the cursor to the next tab stop position, i.e., label, mnemonic,
   argument, or comment field,

whenever the user hits the `Tab` key.  You may edit the Emacs variable
`tab-stop-list` to adjust the tab stop positions to your liking.

The `asm99-smart-backspace-mode` minor mode will move the cursor back to the
previous tab stop if there is only whitespace between the cursor and the tab
stop.  In other words, the `Backspace` key acts as the inverse of the `Tab` key.

Both minor modes are active for `asm99-mode` by default but may be toggled by
`M-x asm99-smart-tab-mode` or `M-x asm99-smart-backspace-mode`, respectively.


### TI Extended BASIC Programs

TI Extended BASIC support is provided by the `basic99-mode` major mode.  To
activate this mode, press `M-x` and enter `basic99-mode`.  Please refer to the
installation section on how to automate this step.

`basic99-mode` highlights known TI Extended BASIC keywords and various BASIC
constructs such as line numbers and strings.  The look and feel of the
highlighting can be customized using the Emacs `font-lock` faces.

There is currently no additional editor assistance for TI Extended BASIC beyond
the built-in Emacs functionality.


### Installation

Emacs is configured by creating a `.emacs` file in your home directory.  For
Windows-specific information about the home directory, please refer to the
relevant [GNU FAQ item][5].

Extensions are generally placed into the Emacs `site-lisp` directory or into
your local `.emacs.d` directory.  When using a non-standard directory, you need
to add its location to your library path in your `.emacs` config file, e.g.,

    (add-to-list 'load-path "~/.emacs.d/")

To activate the xdt99 extension for Emacs, add

    (autoload 'asm99-mode "xdt99-mode" "TMS 9900 Assembly Mode" t)
    (autoload 'basic99-mode "xdt99-mode" "TI Extended BASIC Mode" t)

to your `.emacs` file.

The xdt99 Emacs extension has been tested with Emacs 24, but other reasonably
recent versions of Emacs should also work.


### Customization

You can associate arbitrary file extensions to the major modes provided by
xdt99:

    (setq auto-mode-alist
      (append '(("\\.a99$" . asm99-mode)    ; .a99 -> assembly
                ("\\.asm$" . asm99-mode)    ; .asm -> assembly
                ("\\.b99$" . basic99-mode)  ; .b99 -> TI BASIC
                ("\\.xb$" . basic99-mode)   ; .xb  -> TI BASIC
               ) auto-mode-alist))

Alternatively you can use `M-x asm99-mode` and `M-x basic99-mode` to activate or
deactivate each mode for the active buffer.

To permanently disable the smart tab and/or smart backspace minor modes, add one
or both of these lines to your `.emacs` file:

    (asm99-smart-tab-mode 0)
    (asm99-smart-backspace-mode 0)
    
You can always use `M-x asm99-smart-tab-mode` and `M-x
asm99-smart-backspace-mode` to activate or deactivate each minor mode for the
active buffer.


IDEA IntelliJ
-------------

The xdt99 IDEA plugin extends IntelliJ's advanced code assistance functionality
to TI 99 assembly and Extended BASIC programs.


### Assembly Programs

The xdt99 IDEA plugin provides semantic syntax highlighting for TMS 9900
assembly programs, including `xas99` extensions.  Unlike the simple
pattern-based Emacs colorizer, the IDEA plugin understands the TMS 9900
instruction set and reports syntactic errors visually.

The plugin also tracks labels used throughout the program and supports
navigation, usage lists, and semantic renaming for them.

If the cursor is positioned on any label, pressing `Ctrl+B` or selecting
Navigate > Declaration from the menu will move the cursor to the definition of
the label.  Conversely, pressing `Ctrl+Alt+B` or selecting Navigate >
Implementations will show all usages of the label.

Pressing `Shift+F6` or selecting Refactor > Rename from the menu will
consistently rename all occurrences of the label that the cursor is positioned
on.  Renaming is "safe", i.e., renaming the label `SAMPLE` will not affect
labels `SAMPLE1` or `ASAMPLE`, nor will it change strings or comments containing
the word `SAMPLE`.

Line comments, i.e., comments starting with `*` in the first column, introduce
code blocks that can be collapsed and expanded using the `+` and `-` boxes next
to the editor window.

Pressing `Ctrl+/` or selecting Code > Comment with Line Comment from the menu
will quickly commment out a block of code.  Repeating this step will uncomment
the block again.

Finally, the `Tab` key moves the cursor to the beginning of the next assembly
instruction field.


### TI Extended BASIC Programs

The xdt99 IDEA plugin provides semantic syntax highlighting for TI BASIC and TI
Extended BASIC programs.  The plugin understands most of the TI Extended BASIC
syntax and reports many syntactic errors visually.  Note, however, that semantic
checks are not supported, so nonsensical statements such as

    10 CALL CLEAR(1):: CALL HCHAR(#1,"A"):: OPTION BASE 99

that would throw runtime errors are not marked as erroneous.

The plugin tracks BASIC line numbers and variable names and supports navigation,
usage lists, and semantic renaming for them.  Please refer to the Assembly
section on how to use these features.

Note that refactoring line numbers changes line numbers consistently across a
program without affecting integer values, strings, or comments.  For example, if
the cursor is positioned on `10` in line 20

    10 IF RND>0.5 THEN A=INT(A/10) :: GOTO 10
    20 ON A GO TO 110,10,310
	40 IF A<10 THEN 10 ELSE A=10 :: PRINT "SET TO 10"

renaming might change the program to

    15 IF RND>0.5 THEN A=INT(A/10) :: GOTO 15
    20 ON A GO TO 110,15,310
	40 IF A<10 THEN 15 ELSE A=10 :: PRINT "SET TO 10"

without affecting the integer value `10` in lines 10 and 40.  Thus, line number
refactoring works similarly to the `RESEQUENCE` command in TI BASIC.

Similarly, refactoring variable names changes the name of a variable
consistently across a program without affecting other variables or strings that
may contain the original variable name.  Refactoring is thus safer than a simple
global search and replace operation.


### Installation

To install the plugin in your IDEA-based IDE, open the Settings menu and select
the Plugins tab.  Choose "Install plugin from disk" and select the
`xdt99-idea.jar` file.

The xdt99 IDEA plugin has been tested with IntelliJ IDEA Community Edition
Version 14 and PyCharm Community Edition Version 4.5, but other reasonably
recent versions should also work.


### Customization

The xdt99 IDEA plugin provides two customization tabs for xdt99 on the general
Settings dialog for IDEA.

On the Settings > Editor > Colors & Fonts > xdt99 tabs, you can customize the
color scheme used by the syntax highlighter for assembly and BASIC programs.

On the Settings > Editor > Code Style > xdt99 tab, you can customize the tab
stop positions for assembly programs.

Note that IDEA also supports different keymaps, including Eclipse and Emacs key
bindings.

By default, the xdt99 IDEA plugin associates file extensions `.a99` and `.b99`
with TI assembly and TI Extended BASIC, respectively.  To register additional
extensions, add them in the Settings > Editor > File Types tab.


Contact Information
-------------------

The xdt99 Editor Support is part of the [TI 99 Cross-Development Tools][1].  The
tools are released under the GNU GPL, in the hope that TI 99 enthusiasts may
find them useful.

Please email feedback and bug reports to the developer at <xdt99dev@gmail.com>
or use the issue tracker on the project [GitHub page][2].


[1]: http://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99
[3]: http://www.gnu.org/software/emacs
[4]: http://ftp.gnu.org/gnu/emacs/windows
[5]: http://www.gnu.org/software/emacs/manual/html_node/emacs/Windows-HOME.html
[6]: http://www.jetbrains.com/idea
