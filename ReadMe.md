# Example of a project ReadMe (User's guide)
Start with a simple description of what your project does and who might want to use it.     

# Installation 
- use pip to install the required third party packages:  `pip -r requirements.txt`

# Usage
Describe how to run your app
- From a IDE you can just run the relevant .py file. If you don't have a IDE, open a terminal,cd to the appropriate folder and type in python <.py file>

- `main.py`: run it in the project root folder, so it can import from the testpack folder
- `testpak.py`: can be run from any folder once it's been installed locally

# Code Examples
If your project code is meant to be integrated into python code, you should list at least a few usage examples that can be copy/pasted and run. For more complex cases, consider writing a separate tutorial (put it and its code into a separate folder called tutorial).
Here, I'll just show how to use one of the functions that my package defines:

```
# use the evenOdd function
from testpak import evenOdd
x = int(input("Enter a number:"))
print(x, "is",  evenOdd(x))
```

# Known issues
List any known bugs and limitations

# Acknowledgments
If some project was instrumental in helping you with this project, consider listing it here.

