from setuptools import setup, find_packages

setup(
    name='QTicTacToe',
    version='1.0',
    author='Alan D Moore',
    author_email='alandmoore@example.com',
    description='The classic game of noughts and crosses',
    url="http://qtictactoe.example.com",
    license='MIT',
    long_description=open('README.rst', 'r').read(),
    keywords='game multiplayer example pyqt5',
    project_urls={
        'Author Website': 'https://www.alandmoore.com',
        'Publisher Website': 'https://packtpub.com',
        'Source Code': 'https://git.example.com/qtictactoe'
    },
    #packages=['qtictactoe', 'qtictactoe.images'],
    packages=find_packages(),
    install_requires=['PyQt5 >= 5.12'],
    python_requires='>=3.7',
    #extras_require={
    #    "NetworkPlay": ["requests"]
    #},
    #include_package_data=True,
    package_data={
        'qtictactoe.images': ['*.png'],
        '': ['*.txt', '*.rst']
    },
    entry_points={
        'console_scripts': [
            'qtictactoe = qtictactoe:main'
        ]
    }
)
