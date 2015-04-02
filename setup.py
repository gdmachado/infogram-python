from setuptools import setup

readme  = open('README.rst').read()
history = open('CHANGELOG.md').read()

setup(
    name = 'infogram',
    version = '0.1.1',
    description = 'Unofficial Python library for infogr.am API',
    author = 'Gustavo Machado',
    author_email = 'gdmachado@me.com',
    url = 'https://github.com/gdmachado/infogram-python',
    packages = ['infogram'],
    install_requires = ['requests >= 0.8', 'six >= 1.6'],
    classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent'
    ]
)
