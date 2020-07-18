from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='autoplotter',
    version='0.0.1',
    description='Useful tool for GUI Based EDA',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Saurabh Verma',
    author_email='verma.saurabh8010@gmail.com',
    keywords=['EDA', 'Python', 'Plotly','Gui EDA'],
    url='https://github.com/ersaurabhverma/autoplotter',
    download_url='https://pypi.org/project/autoplotter/'
)

install_requires = [
    'dash',
    'plotly',
    'jupyter_dash',
    'dash_bootstrap_components',
    'pandas',
    'dash_table',
    'dash_core_components',
    'dash_html_components',
    'ppscore',
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)