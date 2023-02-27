from setuptools import setup, find_packages

setup(
    name='mkdocs-autolinks-posix-plugin',
    version='0.6.1',
    description='MkDocs Autolinks POSIX plugin',
    long_description='An MkDocs plugin that automagically generates relative links between markdown pages',
    keywords='mkdocs',
    url='https://github.com/arterm-sedov/mkdocs-autolinks-plugin',
    download_url='https://github.com/arterm-sedov/mkdocs-autolinks-plugin/releases/download/v_061/mkdocs-autolinks-posix-plugin-0.6.1.tar.gz',
    author='Arterm Sedov, forked from Zach Hannum',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.2.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'autolinks = mkdocs_autolinks_plugin.plugin:AutoLinksPlugin',
        ]
    }
)
