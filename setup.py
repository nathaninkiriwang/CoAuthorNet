from setuptools import setup, find_packages

setup(
    name='CoAuthorNet',  
    version='0.1.0',
    description='A package for analyzing and visualizing university authorship networks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nathan Inkiriwang, Bryan Ng',
    author_email='nathan.inkiriwang@sydney.edu.au, yizhe.ng@sydney.edu.au',
    url='https://github.com/nathaninkiriwang/CoAuthorNet',  
    packages=find_packages(),
    install_requires=[
        'pandas',
        'networkx',
        'numpy',
        'matplotlib',
        'tqdm',
        'scholarly',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
