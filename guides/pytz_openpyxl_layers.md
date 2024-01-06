# Create pytz and openpyxl Lambda Layers

These layers must be created following this procedure, not the same as pandas and numpy.

1. On a computer, create a `python` directory.
2. Inside this directory install locally `pytz`: `pip3 install pytz -t .`
3. ZIP the `python` directory: `zip -r pytz-layer.zip python`
4. Create a new Layer on AWS with `Runtime: Python 3.9` and `Architecture: x86_64`, upload this ZIP file on creation.

Now the `pytz` layer is created and can be applied on the Lambda Function.

Repeat the same procedure for `openpyxl` layer.