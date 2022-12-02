from setuptools import setup, find_packages

setup(name="server_chat",
      version="0.0.1",
      description="Server 'Async chat' application",
      author="Sergey Karnaukhov",
      author_email="s_karn_v@mail.ru",
      packages=find_packages(),
      install_requires=['sqlalchemy', ]
      )

# python setup.py sdist bdist wheel
