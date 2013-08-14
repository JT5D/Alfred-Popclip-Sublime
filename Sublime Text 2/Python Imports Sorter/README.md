python_imports_sorter
======================

Sublime Text 2/3 plugin for organizing imports in your Python source code. 
Rules are described by Guido here: http://www.python.org/dev/peps/pep-0008/#imports


Example 
========
Input
--------

```
  import sys
  import project.module1
  import os
  import django.contrib
  import django.admin
```

When selecting and pressing Cmd + Shift + I  it will format this like this:

Output
-------

```
  import os
  import sys
  
  import django.admin
  import django.contrib
  
  import project.module1
```


Spliting arguments
=================
You can split long-line python keyword arguments into the new lines using additional 
command: split arguments. *This feature is available only for ST3+*

Example:

```
dict(very_long_variable_name=1, even_longer_variable_name=2, additional_param=3)
```

to the form of :
```

dict(
    very_long_variable_name=1, 
    even_longer_variable_name=2, 
    additional_param=3
)
```

Just use command pallete pressing `Super+Shift+P` and chose `split arguments` 
action

Installation
============

Use Sublime Text 2 Package manager. Look for python_imports_sorter
