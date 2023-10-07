from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='general_analytics_framework',
    version='0.1.0',
    description='A framework for analytics processes in Python.',
    author='Toby Wilkinson',
    author_email='tobywilkinson3@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)