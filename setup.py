from setuptools import setup, find_packages

setup(
    name='flaskie',
    version='1.0',
    description='User RESTful API based on Flask-RESTPlus',
    url='https://github.com/asheuh/flaskie',
    author='Brian Mboya',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: All',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages()
)