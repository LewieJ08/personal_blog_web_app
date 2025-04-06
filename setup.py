from setuptools import setup, find_packages

setup(
    name="personal_blog_web_app",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask"
    ],  
    entry_points={  
        "console_scripts": [
            "personal-blog=personal_blog_web_app.app:app.run" 
        ]
    },
    author="Lewie Jackson",
    author_email="LewieJ08@gmail.com",
    description="A simple web app that allows the user to view articles, with added admin features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LewieJ08/personal_blog_web_app",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)