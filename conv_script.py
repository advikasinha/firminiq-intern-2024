from pyspark.sql import SparkSession
import os
import glob

spark = SparkSession.builder \
    .appName("JSON to parq conv") \
    .getOrCreate()

#local path, system based, provides paths of the directory containing .gz files in ip_dir
#op_dir is the path for the folder that will contain the converted parquet files.
ip_dir='s3:/api-dev-backup-us/DEV/dev_global_activity/2024/05/23/AWSDynamoDB/'
op_dir='/content/drive/My Drive/parquetfiles/'

subf=[f.path for f in os.scandir(ip_dir) if f.is_dir()] #traverses the subfolders present in 
#AWSDynamoDB so that the latest created subfolder can be accessed
latest_subf=max(subf,key=os.path.getctime)

#data folder(located in the latest created subfolder) being accessed to get the full path
data_f=[f.path for f in os.scandir(latest_subf) if f.is_dir()][0] 

#glue will automatically read all files
#if not use the json_ip as input directory variable
json_ip=glob.glob(os.path.join(data_f,'*.gz'))

try:
    json_df=spark.read.json(data_f)#replace by json_ip if needed

    #file name extraction so that parquet file has the same name
    file_name=os.path.splitext(os.path.basename(data_f))[0]#replace by json_ip if needed

    parq_op=os.path.join(op_dir, f"{file_name}.parquet")

    json_df.write.mode("overwrite").parquet(parq_op) #if file exists in the DF, it is overwritten by the newly converted file


except Exception as e: #to identify faulty file whose conversion couldnt be carried out
    print(f"An error occurred while converting {data_f} to Parquet:{e}")

spark.stop()
#all the json files will still be preserved, a new folder will be created containing all the corresponding parquet files
