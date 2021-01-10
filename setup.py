from setuptools import setup


with open("README.md") as readme:
    long_description = readme.read()


with open("requirements.txt") as requirements:
    requirements = requirements.read().split("\n")


setup(
    name="LiteVkApi",
    version="1.2.2",
    description="Библиотека для лекгого написания ботов ВК!",
    packages=["LiteVkApi"],
    author_email="ma_mush@mail.ru",
    zip_safe=False,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements
)
