""" Setup for the pysonicapi package """

import setuptools
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()


setuptools.setup(
    name='pysonicapi',
    version='0.1.1',
    description='Python Wrapper for SonciWall API',
    license='MIT',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Darshit Kothari',
    author_email='kotharidarsh104@gmail.com',
    url='https://github.com/darshitkothari/pysonicapi.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    keywords='sonicwall sonicos rest api firewall networking',
    py_modules=['pyfortiapi']
)