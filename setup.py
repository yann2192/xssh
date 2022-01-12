import setuptools


setuptools.setup(
    name="xssh",
    version="0.1",
    packages=setuptools.find_packages(),
    scripts=["bin/xssh"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["libtmux==0.10.3"],
)
