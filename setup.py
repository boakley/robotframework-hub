from setuptools import setup

execfile('rfhub/version.py')

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
    zip_safe         = False,
    include_package_data = True,
    install_requires = ['Flask', 'watchdog', 'robotframework'],
    classifiers      = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
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
)
