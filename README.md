# Code Reviewer Recommendation Algorithm

Takes a path to a local git repository, and a list of commit ids in hexidecimal and returns a list of 5 most relevant reccomended reviewers for those commits. 

# Requirements

Firstly, must have [PyGit2](https://www.pygit2.org/install.html) installed
Install with pip:

`$ pip install pygit2`

Supported versions of python:

* Python 3.5 - 3.8
* PyPy 3.5

Python requirements for PyGit2:

* cffi 1.0+
* cached-property

"Libgit2 v0.28.x; binary wheels already include libgit2, so you only need to worry about this if you install the source package"

# Usage 

`review_suggestion.py [-h] repo_path hashes_list [hashes_list ...]`

positional arguments: 
* repo_path Path to local github repository, must not be a path to the repositorys working dir and therefore must end with /.git 
* hashes_list A list of hexidecimal hashes of commits to be included in a review

optional argument: -h, --help show this help message and exit

**Example**: `python3 review_suggestion.py Path/To/Working/Repository/.git 4866b1330bc7c77c0ed0e050e6b99efdeb026448 7b7c1a0135580251990c7866aed39202f9928b1f`