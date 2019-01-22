from setuptools import setup

setup(
    name='serenity',
    version='0.1',
    description='Serenity API',
    url='http://github.com/weassur/serenity',
    author='Thibaut Fatus',
    author_email='thibaut@weassur.com',
    license='GPL 3.0',
    packages=['serenity'],
    install_requires=['PyJWT', 'requests'],
    zip_safe=False)
