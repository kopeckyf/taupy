"""A Python package to study the theory of dialectical structures
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='taupy',
    version='0.3.0',
    description='A Python package to study the theory of dialectical \
                 structures',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/kopeckyf/taupy',
    author='Felix Kopecky',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Sociology',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',        
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='Argumentation theory, Theory of dialectical structures, \
              Argumentation framework, Agent-based debate model, ABM',

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    #package_dir={'': './'},

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(),
    python_requires='>=3.9, <4',
    install_requires=['sympy>=1.6.2',
                      'dd>=0.5.6',
                      'numpy>=1.19.4',
                      'python_igraph>=0.9.6',
                      'scikit_learn>=0.24.2',
                      'pandas>=1.2.2',
                      'more_itertools>=8.8.0'],

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={
        'Source': 'https://github.com/kopeckyf/taupy/',
        'Bug Reports': 'https://github.com/kopeckyf/taupy/issues',
        'Research group': 'https://debatelab.philosophie.kit.edu/',
    },
)
