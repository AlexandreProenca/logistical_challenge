# Smart Cargo Assignment

_Author: Alexandre Proença_ \
_Date: 16/10/2020_ \
_Local: Florianópolis - Brazil_ 

The Python version used on this project is **3.8.5** - available at [python.org](https://www.python.org/downloads/release/python-385/).

### Description

Given a list of trucks and their current locations and a list of cargos and their pickup and delivery locations, ​​find the optimal mapping of trucks to cargos to minimize the overall distances the trucks must travel​​.

Requirements
1. Each truck can only carry up to one cargo.
2. Each truck can only make up to one trip.
3. Some trucks may not be used at all.

The solution should be achieved by running the command below:
   
    $ cargo_truck ​<​cargo_file​>​ ​<​truck_file​>
For example:
    
    $ cargo_truck data/cargo.csv data/truck.csv

The solution should generate a ​`results.csv`​ file in the root of the directory. The first row is the header ​`cargo, truck, distance`​.

Where:
- cargo: the cargo that will be moved.
- truck: the truck that will move the cargo.
- distance: how many **​miles​** the truck will travel, from truck's origin to cargo's origin and to final destination. The distance must consider only one trip, not a round trip. The number must be a float round up to two decimal places.
- Rows must be sorted by distance (ASC)


### Structure of the Repository
Repository structure is a crucial part of project’s architecture, it must be compatible with each kind of application, in this case
a command line application.

    .
    ├── README.md
    ├── Makefile
    ├── app
    │   ├── __init__.py
    │   ├── controllers.py
    │   └── main.py
    ├── assets
    │   ├── BE Challenge.pdf
    │   ├── cargo.csv
    │   └── trucks.csv
    ├── notebooks
    │   └── Developing notes.ipynb
    ├── requirements
    │   ├── requirements-base.in
    │   ├── requirements-dev.in
    │   ├── requirements-dev.txt
    │   ├── requirements-prod.in
    │   └── requirements-prod.txt
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   └── tests.py
    └── tox.ini


| Location|app|
|----------|-------------|
| Propose |The code of interest. | 

| Location |assets|
|----------|:-----:|
| Propose |Files used in development. |

| Location|notebooks|
|--------|:--------:|
| Propose|Notes about algorithm development.| 
 
| Location |requirements|
|----------|:-------------:|
| Propose|Development dependencies.| 

| Location|tests|
|---------|:-----:|
| Propose|Package integration and unit tests.| 

| Location|./Makefile|
|---------|:-----:|
| Propose|Generic management tasks.| 

| Location|./setup.py|
|---------|:-----:|
| Propose|Package and distribution management.| 

### Versioning of application
The application versioning follow Semantic Versioning 2.0.0

    MAJOR version when you make incompatible API changes,
    MINOR version when you add functionality in a backwards compatible manner, and
    PATCH version when you make backwards compatible bug fixes.

### Security cares
    - Modern version of Python
    - Pin dependencies
    - Hash dependencies
    - Add SAST testing using Bandit
    - Dependency analysis tools

### Project development and technical decisions
This shortest path problem can be solved by many manners, a good way to find the shortest distance between two points and preserve the 
original order of input data is check the distance sequencialy, it can be done with a nested FOR loop, but the complexity will be O(n^2),
what is worst case to huge data beacouse iteration grows exponentialy, the good way to search this distance is use a search binary tree, and reduce
complexity to O(kn log n) if n points are **presorted** in each of k dimensions using an O(n log n), but this **presorted** not preserve the
original input data order, but can handle searching faster. So if we run the two solutions we can see some diferences in results beacouse 
some truck came first on the sequancial list than when it came from a binary search tree.
I implemented the two ways, it gives the user an option to work with huge data if input data order preservation is not a problem
, or preserve the original data order if he wants.

I tried use a Kd-Tree, avaliable on `scipy.spatial.cKDTree`, but this library can't bring unique results, we need assign the cargo to the truck and ignore it on the next search, one options is implement kd-tree by hand and mapping busy trucks, other approuch is simpler, and 
can work very well with few and medium records on file, once it works with nested FOR loop in memory, keep in mind of the complexity is O(n^2).\
Thinking about make a professional application that can handle a huge lists of cargo and truck I chossed implement kd-tree by hand, follow below some articles 
that helps me to develop this CLI, also inside of notebook folder you can see my notes and follow my train of thought. 

Building a static k-d tree from n points has the following worst-case complexity:

- Querying an axis-parallel range in a balanced k-d tree takes O(n1−1/k +m) time, where m is the number of the reported points, and k the dimension of the k-d tree.
- Finding 1 nearest neighbour in a balanced k-d tree with randomly distributed points takes O(log n) time on average.

References 

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html
    https://www.geeksforgeeks.org/k-dimensional-tree-set-2-find-minimum/
    https://github.com/tsoding/kdtree-in-python
    https://en.wikipedia.org/wiki/K-d_tree



### Continuous integration
A good way to do automatic deploys is use some service of continuous integration,
I use to work with Travis CI on my public projects it helps me to deploy directly on [Pypi](https://pypi.org/)

CI environment uses separate virtualenv instances for each Python version.
 This means that as soon as you specify language: python in `.travis.yml` your tests will 
 run inside a virtualenv (without you having to explicitly create it). System Python is not 
 used and should not be relied on. If you need to install Python packages, do it via pip and 
 not apt.


### Virtual Environment
The recommended way to install this package is install it inside a virtualenv.

    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate


### Installing
Install all dependency packages, for security reasons was generated packages hashes to avoid install poisoned packages.\
To install this CLI just type commands below in root directory

    $ make

To install development dependencies

    $ make development
 
### How to run the solution
To use the application just use the command line below, the order of files must be respected, the first parameter refers to cargo file and the second parameter refers to truck file, you must use the relative path to both.    
    
    Preserve input order data
    $ cargo_truck <relative/path/cargo.csv> <relative/path/trucks.csv>

    Use to handle huge input data but not preserve input data order 
    $ cargo_truck <relative/path/cargo.csv> <relative/path/trucks.csv> --huge true

### Running tests
To run tests and see the coverage just type command below.

    $ make test

### Contributing
Before commit your changes make sure that you verified the commands below.

    $ make pretty
    $ make secure

Tests and coverage

    $ make test

Rise the app version

    $ bump2version <major>|<minor>|<patch>


If all good feel free to commit and submit your changes :) avoid use push force, let's preserve git history ;)
