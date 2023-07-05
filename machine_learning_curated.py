import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs


def sparkAggregate(
    glueContext, parentFrame, groups, aggs, transformation_ctx
) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = (
        parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs)
        if len(groups) > 0
        else parentFrame.toDF().agg(*aggsFuncs)
    )
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-aj/step_trainer_trusted2/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerTrusted_node1",
)

# Script generated for node Drop Fields
DropFields_node1688597760168 = DropFields.apply(
    frame=StepTrainerTrusted_node1,
    paths=[
        "birthDay",
        "shareWithResearchAsOfDate",
        "registrationDate",
        "customerName",
        "user",
        "email",
        "lastUpdateDate",
        "phone",
        "right_serialNumber",
        "shareWithPublicAsOfDate",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFields_node1688597760168",
)

# Script generated for node Aggregate
Aggregate_node1688597741382 = sparkAggregate(
    glueContext,
    parentFrame=DropFields_node1688597760168,
    groups=["timeStamp", "serialNumber", "z", "sensorReadingTime", "y", "x"],
    aggs=[["right_distanceFromObject", "sum"]],
    transformation_ctx="Aggregate_node1688597741382",
)

# Script generated for node machine_learning_curated
machine_learning_curated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=Aggregate_node1688597741382,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-aj/machine_learning_curated/",
        "partitionKeys": [],
    },
    transformation_ctx="machine_learning_curated_node3",
)

job.commit()
