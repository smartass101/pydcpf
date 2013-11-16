from distutils.core import setup

setup(name = "pydcpf",
      version = "1.3",
      description = "Python device communications protocol framework",
      long_description = "A framework for rapid implementation of communications protocols in Python focusing on speed, modular flexibility and extensibility.",
      url="https://github.com/smartass101/pydcpf",
      packages = ["pydcpf", "pydcpf.interfaces", "pydcpf.appliances", "pydcpf.protocols"],
      author='Ondrej Grover',
      author_email='ondrej.grover@gmail.com',
      requires = ["pyserial"],
      classifiers = [
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
          ],
        
      )
