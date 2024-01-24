# eurofuels-back

## What's this project about

_eurofuels_ is an improved version of [eurocombustibles](https://github.com/macolmenerori/eurocombustibles), being this the backend part.

Retrieve the fuel prices data from the [EU Weekly Oil Bulletin](https://energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en), store them on an AWS S3 bucket and display it on a webpage.

For retrieving the data, an AWS Lambda function will be used, which will store the data (as a JSON file) on an AWS S3 bucket. The lambda will run periodically triggered by an AWS EventBridge (by CloudWatch) event.

## How to set up the project

### AWS S3 Bucket

1. Create an S3 Bucket on AWS
2. Change _Permissions Policy_ for the following one (to grant public read permission)

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

3. Give public access: disable the _Block public access_ option
4. Change _Object Ownership_ to _Bucket Owner Preferred_
5. Manage ACL (Access Control List): enable _read_ to everyone
6. Add CORS policy (under bucket's permission tab). Without it, data cannot be accessed. It can be in JSON or in XML

```
[
  {
    "AllowedHeaders": ["Authorization"],
    "AllowedMethods": ["GET"],
    "AllowedOrigins": ["*"],
    "MaxAgeSeconds": 3000
  }
]
```

```
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```

7. The AWS S3 Bucket is now set up. Optionally upload the JSON file.

To get the public URL of the file, go to the file and on the _Properties_ tab there it is under _Object URL_.

### AWS Layers

The Lambda function is written in Python and makes use of the following libraries:

- `pandas`
- `numpy` (pandas dependency)
- `pytz` (pandas dependency)
- `openpyxl` (pandas dependency)

These libraries are not installed by default on AWS Python environment, so to set them up a Lambda Layer will be created for each one. These layers will then be applied to the AWS Lambda Function in order to import the libraries.

Follow the following guides to create these layers:

- [pandas and numpy layers](https://github.com/macolmenerori/eurofuels-back/tree/main/guides/pandas_numpy_layers.md)
- [pytz and openpyxl layers](https://github.com/macolmenerori/eurofuels-back/tree/main/guides/pytz_openpyxl_layers.md)

### AWS credentials

On AWS console go to User Settings → Security credentials and create new Access Keys. A `Key_ID` and a `Secret_Key` are generated, save them to be used on the script.

### AWS Lambda

The code in charge of retrieving the data from its source and saving it as a JSON file on the S3 Bucket.

Create a Lambda Function with the following params:

- Runtime: `Python 3.9`
- Architecture: `x86_64`

On the code editor insert the lambda code and click Deploy button to deploy changes.

Set the following environment variables:

- `ACCESS_KEY`: the previously generated `Key_ID`
- `SECRET_KEY`: the previously generated `Secret_Key`
- `BUCKET_NAME`: the name given to the bucket when it was created
- `FILE_NAME`: the name of the JSON file to be saved on the bucket

Now apply the four layers previously created (on the code tab at the bottom).

Everything should be ready now, go to test tab and test that it works okay. Go to the S3 Bucket and check that the _last time modified_ was updated.

### AWS CloudWatch and EventBridge

Here an event will be created that will trigger the execution of the Lambda Function.

1. Go to CloudWatch → Rules → Events and Create Rule
2. Give name, description and select _Schedule_ as _Event Source_
3. It will redirect to EventBridge service, where the _Schedule Pattern_ will be Recurring Schedule → Cron-based
4. Enter the desired cron expression, for example `0 30 8 ? * WED *` (every Wednesday at 08:30)
5. In the _Select targets_ section choose _Lambda function_ as the target type and in the _Function_ dropdown, select the Lambda function.
6. Select to _not retry_ if fail.

Now the Lambda Function will run on the schedule.

[Here](https://freeformatter.com/cron-expression-generator-quartz.html) you can find a useful CRON expression generator.

## Useful links

- [AWS S3 Buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)
- [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
- [AWS Lambda Functions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-functions.html)
- [AWS EventBridge](https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html?icmpid=docs_console_unmapped)
