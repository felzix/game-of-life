from setuptools import setup, find_packages

setup(
    name = "GameOfLife Web Server",
    version = "0.1",
    packages = find_packages(),
    install_requires=[
        'flask',
        'flask-wtf',
        'proxytypes',
        'redis',
        'wtforms',

        'GameOfLife-Common',
    ],
    author='felzix',
    author_email='felzix@gmail.com',
    entry_points=dict(
        console_scripts=[
            'game-of-life-web-server=game_of_life_web_server.web_server:main'
        ],
    ),
)