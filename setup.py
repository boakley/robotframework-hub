"""
To push a new version to PyPi, update the version number
in rfhub/version.py and then run the following commands:

    $ python setup.py sdist
    $ python3 -m twine upload dist/*


"""
from setuptools import setup

filename = 'rfhub/version.py'
exec(open(filename).read())

setup(
    name             = 'robotframework-hub',
    version          = __version__,
    author           = 'Bryan Oakley',
    author_email     = 'bryan.oakley@gmail.com',
    url              = 'https://github.com/boakley/robotframework-hub/',
    keywords         = 'robotframework',
    license          = 'Apache License 2.0',
    description      = 'Webserver for robot framework assets',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    zip_safe         = True,
    include_package_data = True,
    install_requires = ['Flask', 'watchdog', 'robotframework', 'tornado'],
    classifiers      = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
        ],
    packages         =[
        'rfhub',
        'rfhub.blueprints',
        'rfhub.blueprints.api',
        'rfhub.blueprints.doc',
        'rfhub.blueprints.dashboard',
        ],
    scripts          =[],
    entry_points={
        'console_scripts': [
            "rfhub = rfhub.__main__:main"
        ]
    }
)
