from setuptools import setup, find_packages

setup(
    name='mkdocs-roamlinks-plugin',
    version='0.1.0',
    description='An MkDocs plugin',
    long_description='An MkDocs plugin that automagically generates relative links and convert roamlike links between markdown pages',
    keywords='mkdocs',
    url= 'https://github.com/Jackiexiao/mkdocs-roamlinks-plugin',
    #download_url='https://github.com/midnightprioriem/mkdocs-autolinks-plugin/archive/v_020.tar.gz',
    author='jackiexiao',
    author_email='707610215@qq.com',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=1.0.4',
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
            'roamlinks = mkdocs_roamlinks_plugin.plugin:RoamLinksPlugin',
        ]
    }
)
