from setuptools import setup

# 'Import' __version__
exec(open('centmo/_version.py').read())

requirements = [
    'requests>=2.9.1',
]

setup(
    name='centmo',
    version=__version__,  # noqa
    description='Centmo',
    url='http://github.com/lanewinfield/centmo',
    author='Brian Moore (og Zack Hsi)',
    author_email='brian@brianmoore.com',
    license='MIT',
    packages=['centmo'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'centmo = centmo.cli:main',
        ],
    },
)
