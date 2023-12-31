import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node1688586148416 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-aj/customertrusted/"], "recurse": True},
    transformation_ctx="AmazonS3_node1688586148416",
)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-aj/accelerometer_landing/"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node Customer Privacy Filter
CustomerPrivacyFilter_node1688586227373 = Join.apply(
    frame1=S3bucket_node1,
    frame2=AmazonS3_node1688586148416,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="CustomerPrivacyFilter_node1688586227373",
)

# Script generated for node Drop Fields
DropFields_node1688586557604 = DropFields.apply(
    frame=CustomerPrivacyFilter_node1688586227373,
    paths=[
        "timeStamp",
        "serialNumber",
        "shareWithPublicAsOfDate",
        "birthDay",
        "registrationDate",
        "shareWithResearchAsOfDate",
        "customerName",
        "email",
        "lastUpdateDate",
        "phone",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFields_node1688586557604",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1688586557604,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-aj/", "partitionKeys": []},
    transformation_ctx="S3bucket_node3",
)

job.commit()
