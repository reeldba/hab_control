
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license= f.read()

setup(
        name='hab_control',
        version='0.1.0',
        description='Quilliams High Tech Habitat',
        long_description=readme,
        author='Allen Pippin',
        author_email='nottoday@nomail.com',
        url='https://github.com/reeldba/hab_control',
        license=license,
        packages=find_packages(exclude=('tests','docs'))
)
