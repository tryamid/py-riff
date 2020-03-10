import setuptools
import subprocess

setuptools.setup(
    name= 'py-riff',
    version= subprocess.check_output(['git', 'describe', '--tags']).strip() \
            .decode('utf-8') \
            .split('-g')[0],
    description= "An encoding only implementation of the RIFF",
    author= "Shantanu Biswas",
    author_email= "bsantanu381@gmail.com",
    packages= [ 'py_riff' ],
    url= "https://github.com/tryamid/py_riff",
    license= "ISC",
    python_requires= ">=3.5"
)
