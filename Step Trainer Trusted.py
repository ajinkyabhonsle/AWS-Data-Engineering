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

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-aj/accelerometer_trusted_2/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1",
)

# Script generated for node Step Trainer
StepTrainer_node1688594877006 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-aj/step_trainer_landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainer_node1688594877006",
)

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1688594930662 = ApplyMapping.apply(
    frame=StepTrainer_node1688594877006,
    mappings=[
        ("sensorReadingTime", "bigint", "sensorReadingTime", "long"),
        ("serialNumber", "string", "right_serialNumber", "string"),
        ("distanceFromObject", "int", "right_distanceFromObject", "int"),
    ],
    transformation_ctx="RenamedkeysforJoin_node1688594930662",
)

# Script generated for node Join
Join_node1688594901339 = Join.apply(
    frame1=AccelerometerTrusted_node1,
    frame2=RenamedkeysforJoin_node1688594930662,
    keys1=["serialNumber"],
    keys2=["right_serialNumber"],
    transformation_ctx="Join_node1688594901339",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1688595088017 = glueContext.write_dynamic_frame.from_options(
    frame=Join_node1688594901339,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-aj/step_trainer_trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="StepTrainerTrusted_node1688595088017",
)

job.commit()
