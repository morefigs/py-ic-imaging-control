from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='py-ic-imaging-control',
      version='1.0',
      description='Python wrapper for the IC Imaging Control SDK from The Imaging Source (TIS)',
      long_description=readme(),
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: GPL-3 License',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering',
                   ],
      keywords='tis imaging source',
      url='https://github.com/zivlab/py-ic-imaging-control',
      author='morefigs',
      author_email='morefigs@gmail.com',
      license='GPL-3',
      packages=['pyicic'],
      )
