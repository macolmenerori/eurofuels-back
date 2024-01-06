# Create pandas and numpy Lambda Layers

These layers must be created following this procedure, not the same as pytz and openpyxl.

1. On a computer, create a `python` directory.
2. Go to [PyPi pandas download page](https://pypi.org/project/pandas/#files) and download `
pandas-2.1.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` file.
3. Unzip this file with `unzip 
pandas-2.1.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`, 2-3 folders will be generated.
4. Copy these 2-3 folders to the `python` folder.
5. ZIP the `python` directory: `zip -r pandas-layer.zip python`
6. Create a new Layer on AWS with `Runtime: Python 3.9` and `Architecture: x86_64`, upload this ZIP file on creation.

Now the `pandas` layer is created and can be applied on the Lambda Function.

Repeat the same procedure for `numpy` layer. Download the `whl` file from [PyPi numpy downloads page](https://pypi.org/project/numpy/#files), select the file `
numpy-1.26.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.