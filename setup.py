from setuptools import setup 

setup(
    name='DeFiPy',
    version='1.0.0',
    description='tools for interacting with EVM DeFi such as ERC20 tokens and UniswapV2Routers',
    url = 'https:/github.com/bobGSmith/DeFiPy',
    author = 'Bob G Smith',
    author_email = 'bobbyatopk@gmail.com',
    license = 'MIT',
    packages = ['DeFiPy'],
    install_requires = ['web3','PwAES'],
    calssifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience:: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8'
    ] 
)