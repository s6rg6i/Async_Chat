from setuptools import setup, find_packages

setup(name="client_chat",
      version="0.0.1",
      description="Client 'Async chat' application",
      author="Sergey Karnaukhov",
      author_email="s_karn_v@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', ]
      )

# python setup.py sdist bdist wheel
