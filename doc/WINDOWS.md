xdt99 Windows Installation
==========================

In this brief tutorial we guide Windows users through the installation and setup
process.

For most Windows users, installation is a two-step process, as we need to get
both xdt99 and Python 3.


### Python

xdt99 is written in the [Python][1] programming language, which is easy to learn
and available for all major platforms.

If we already have a Python version lower than 3.6.0 installed, we first need to
uninstall it.

We can download Python from the [download page][2], where the latest available
release should be automatically offered to us.  Click on `Download Python 3.x.y`
and then (double-)click the downloaded file to start the Python installer.

In the installation wizard, make sure that option `Add Python to PATH` is
selected, and make note of the installation path, shown under `Install Now`
(alas, we cannot copy & paste it).  We will need this path later on.

To check if the installation was successful, we can open a command prompt (also
known as "DOS box") by opening the Start menu, searching for `cmd.exe`, and
clicking on the program when it shows up in the menu.  In the command prompt,
we type

    python

and hit `Return`.  We should see a response like

    Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (In
    tel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Close the command prompt window again.

Next, we open another command prompt, but this time as administrator.  So again
we open the Windows menu and search for `cmd.exe`.  When the program is shown in
the menu, we right-click on it and select `Run as administrator`.  In the window
that opens, we type

    assoc .py=pythonsource
    ftype pythonsource=<your python path> "%1" %*

Where `<your python path>` is the path we copied during installation.  On my
machine, the Python path is

    C:\Users\ralph\AppData\Local\Programs\Python\Python38-32\python.exe

When done, close the window.

Congratulations, you're running Python now!  Also rest assured that we don't
have to deal with Python again.


### xdt99

Once Python is running, we can proceed to install xdt99, which is even simpler.

We download the latest release `xdt99.zip` from the [project page][3] and unzip
the archive somewhere on our disk, say `c:\ti99\xdt99`.  We don't have to be
administrator for this, unless we would put it in a protected folder.

Again, we open a command prompt (Start > Type `cmd.exe`) and change to the xdt99
directory by typing

    > cd c:\ti99\xdt99

We don't type the `>`, though.  This character (like the Linux `$` used in the
xdt99 manual) merely represents the command prompt presented to us by Windows.

To check if xdt99 is working, we type

    > xas99.py -h

We should see the usage information of the xas99 assembler:

    usage: xas99.py [-h] [-b | -i | -c | -t [<format>] | --embed-xb]
                    [-l <file> [<file> ...] | -ll <file> [<file> ...]] [-5] [-18]
                    [-s] [-n <name>] [-R] [-C] [-L <file>] [-S] [-E <file>] [-q]
                    [-a <addr>] [-I <paths>] [-D <sym=val> [<sym=val> ...]]
                    [-o <file>]
                    [<source> [<source> ...]]
    
    TMS9900 cross-assembler, v3.0.0
    ....

To finalize the installation, we need to add xdt99 to our _command search path_
so that the xdt99 tools are found no matter which directory we are in.

We change the search path by opening Control Panel > System > Advanced System
Settings > Environment Variables.  Note that Control Panel is not shown in the
Win 10 menu, but we can start it by searching for it.
  
Now, in the lower window called `System Variables`, we search for the `Path`
entry, select it, and press `Edit`.  In the window that pops up, we press `New`
and add this line

    c:\ti99\xdt99

or whatever our chosen installation folder is.  We can close all windows by
pressing `OK`.  We then need to _close all `cmd.exe` windows_ for the changes to
take effect.

To test if everything is correct, we open a new command prompt and invoke
`xas99` from a different folder and check that the `xas99` help is shown.

    > cd \
    > xas99.py -h

Finally, we recommend to create a _working folder_ where we store all our files,
such as assembly sources and disk images, we want to use with xdt99.  In this
guide, we will use `c:\ti99\work` as working directory.  

We should never store user files inside the xdt99 installation directory!


First Steps
-----------

In order to use xdt99, we first need to open a command prompt (also called a
_shell_).  In general, this will be `cmd.exe`, but other prompts such as git
bash will also work.  Don't use the PowerShell, though, unless you know what
you're doing.  

The `example` folder in the xdt99 installation directory contains some sample
programs.  To follow the tutorial, we must copy this folder into our working
folder, and then `cd` into it, e.g.,

    > cd C:\ti99\work\example

We can then assemble the source file `ashello.asm` by typing:

    > xas99.py -R ashello.asm
    
`xas99` will print out a warning about some references

    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR

which we can ignore for now.

We now see an additional file, `ashello.obj`:

    > dir ashello.*
     Volume in drive C is OSDisk
     Volume Serial Number is 1234-5678
    
     Directory of C:\ti99\work\examples
    
    19.03.2020  14:34               925 ashello.asm
    19.03.2020  14:40               720 ashello.obj

This file contains _object code_, which can be run with the Editor/Assembler
cart option 3.

Note that in order to repeat a previous command, we can switch to the previous
or next commands by pressing Cursor-Up or Cursor-Down, resp.  If we were to make
a change to `ashello.asm`, we don't have to type

    > xas99.py -R ashello.asm

again, but can simple press the Cursor-Up key once, followed by Return.

Another useful trick when using the command line is _command completion_.  For
example, if we type

    > xas99.py -R ashe
    
and then press the Tab key, the shell will complete the fragment we typed as

    > xas99.py -R ashello.asm

If we keep pressing Tab, the shell will cycle through all other possible
completions:

    > xas99.py -R ashello.obj
    > xas99.py -R ashello_new.asm

and then start at the first option again.  To select one of the suggestions, we
only need to press Return.  Of course, we can also continue typing other parts
of our command.

The command completion will compare the fragment that prefixes the cursor with
all files in the current folder, and suggest those that match the fragment.
Once you get used to completion, it can save a lot of typing.

    
Next Steps
----------

This concludes our Windows setup.  We now recommend to continue with the main
tutorial.  In general, the tutorial will use the `$` character to show which
commands we need to type in.  Should this command _not_ apply to Windows, there
will be an extra line starting with `>`.

For example, when we see this,

    $ ls -l example/
    > dir example
    
we should type `dir example` as Windows users, and here

    $ xas99.py -h
    
we type `xas99.py -h`, since it is valid for all platforms.

For a in-depth introduction to all xdt99 tools, please refer to the main manual.


[1]: https://en.wikipedia.org/wiki/Python_%28programming_language%29
[2]: https://www.python.org/downloads/
[3]: https://github.com/endlos99/xdt99/releases
