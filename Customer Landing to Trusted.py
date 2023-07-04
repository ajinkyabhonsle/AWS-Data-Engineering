import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={"paths": ["s3://stedi-aj/customer_landing/"], "recurse": True},
    transformation_ctx="S3bucket_node1",
)

# Script generated for node PrivacyFilter
PrivacyFilter_node1688511469862 = Filter.apply(
    frame=S3bucket_node1,
    f=lambda row: (not (row["shareWithResearchAsOfDate"] == 0)),
    transformation_ctx="PrivacyFilter_node1688511469862",
)

# Script generated for node Customer Trusted Zone
CustomerTrustedZone_node1688511827760 = glueContext.write_dynamic_frame.from_options(
    frame=PrivacyFilter_node1688511469862,
    connection_type="s3",
    format="json",
    connection_options={"path": "s3://stedi-aj/customertrusted/", "partitionKeys": []},
    transformation_ctx="CustomerTrustedZone_node1688511827760",
)

job.commit()
