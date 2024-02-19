/usr/bin/python3 -m venv /usr/bin/mf_python_env
source /usr/bin/mf_python_env/bin/activate
pip install -r requirements.txt

rm -r -f mkdir /mnt/tmp/code;/mnt/tmp/code;cd /mnt/tmp/code; aws s3 cp s3://mf-code-bucket/code.zip .

mkdir /mnt/tmp/mf_python_env;/usr/bin/python3 -m venv /mnt/tmp/mf_python_env;
source /mnt/tmp/mf_python_env/bin/activate;pip3 install pandas;pip3 install mftool;cd /mnt/tmp/code/src;spark-submit --conf spark.pyspark.python='/mnt/tmp/mf_python_env' history_load.py

