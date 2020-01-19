import setuptools
import subprocess

setuptools.setup(
    name= 'py-riff',
    version= subprocess.check_output(['git', 'describe', '--tags']).strip(),
    description= "An encoding only implementation of the RIFF",
    author= "Shantanu Biswas",
    author_email= "bsantanu381@gmail.com",
    py_modules= [
        'py_riff.chunks'
    ],
    url= "https://github.com/tryamid/py_riff",
    license= "ISC",
    python_requires= ">=3.5"
)