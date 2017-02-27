from setuptools import setup

# 'Import' __version__
exec(open('spammo/_version.py').read())

requirements = [
    'requests>=2.9.1',
]

setup(
    name='spammo',
    version=__version__,  # noqa
    description='spammo',
    url='http://github.com/lanewinfield/spammo',
    author='Brian Moore (og Zack Hsi)',
    author_email='brian@brianmoore.com',
    license='MIT',
    packages=['spammo'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'spammo = spammo.cli:main',
        ],
    },
)
