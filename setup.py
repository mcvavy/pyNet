#!/usr/bin/env python3


from setuptools import find_packages, setup


setup(

    ### Metadata

    name='aerofiles',

    version='0.1.0',

    description='waypoint file readers and writers for aviation',

    long_description=...,

    url='https://github.com/Turbo87/aerofiles',

    download_url='https://pypi.python.org/pypi/aerofiles',

    license='MIT',

    author='Tobias Bieniek',
    author_email='tobias.bieniek@gmx.de',

    maintainer='John Doe',
    maintainer_email='john.doe@lavabit.com',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],

    ### Dependencies

    install_requires=[
        'utm',
        'SQLAlchemy>=0.6',
        'BrokenPackage>=0.7,<1.0',
    ],

    dependency_links=[
        'git+https://github.com/Turbo87/utm.git@v0.3.1#egg=utm-0.3.1',
    ],

    ### Contents

    packages=find_packages(exclude=['tests*']),

)
