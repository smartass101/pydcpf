from distutils.core import setup

setup(name = "pydcpf",
      version = "1.1",
      description = "Python device communications protocol framework focusing on speed, modular flexibility and extensibility",
      packages = ["pydcpf", "pydcpf.interfaces", "pydcpf.appliances", "pydcpf.protocols"],
      author='Ondrej Grover',
      author_email='ondrej.grover@gmail.com',
      )
