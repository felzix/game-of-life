from setuptools import setup, find_packages

setup(
    name = "GameOfLife Engine",
    version = "0.1",
    packages = find_packages(),
    install_requires=[
        'proxytypes',
        'redis',
        'GameOfLife-Common',
    ],
    author='felzix',
    author_email='felzix@gmail.com',
    entry_points=dict(
        console_scripts=[
            'game-of-life-engine=game_of_life_engine.game_engine:main'
        ],
    ),
)