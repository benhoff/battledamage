from setuptools import setup, find_packages

setup(
        name='battledamage',
        version='0.0.1',
        license='BSD',
        author='Ben Hoff',
        packages=find_packages(),
        install_requires=['numpy',
                          'PyQt5'],

        extras_require={'dev': ['flake8',]},
        )
