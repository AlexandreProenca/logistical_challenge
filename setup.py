import re
import os

from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames) for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])

    return {package: filepaths}


setup(
    name='cargo_assignments',
    version=get_version('app'),
    url="https://github.com/AlexandreProenca/cargo_assignments",
    license='MIT',
    description='Given a list of trucks and their current locations and a list of cargos and their pickup and delivery '
        'locations, ​​find the optimal mapping of trucks to cargos to minimize the overall distances the trucks '
        'must travel​​.',
    author='Alexandre Proença',
    author_email='alexandre.proenca@hotmail.com.br',
    packages=get_packages('app'),
    install_requires=['typer', 'geopy'],
    entry_points={
        'console_scripts': [
            'cargo_truck=app.main:main',
        ],
    },
    zip_safe=False,
    keywords='Cargo Assignments',
    package_data={
        'app': ['*.py'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
