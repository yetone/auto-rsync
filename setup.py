from setuptools import setup, find_packages


install_requires = []
for line in open('requirements.txt', 'r'):
    install_requires.append(line.strip())

setup(
    name='auto-rsync',
    version='0.0.7',
    keywords=('sync', 'rsync', 'auto rsync', 'auto', 'filesystem'),
    description='Auto RSync by watch filesystem events.',
    url='http://github.com/yetone/auto-rsync',
    license='MIT License',
    author='yetone',
    author_email='yetoneful@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'auto-rsync=auto_rsync:main',
        ],
    },
    zip_safe=False,
    install_requires=install_requires
)
