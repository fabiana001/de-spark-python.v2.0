Pyspark Bootstrap 

Below is the project structure 


      Pyspark Project/
        │
	    ├── project_name/
	    │
				 ├── function1/
				 ├── function2/
				 ├── start/
				 │
				 ├── __inti__.py
				 └── main.py
			├── __init__.py
	        └── driver.py
	    ├── resources/
	    │
	    ├── data/
			  │
			  ├── Dockerfile/
			  ├── config.yaml
			  └── generate.sh
			├── generated_data/
			└── application.conf
	    ├── tests/
             │
	         ├── function1/
	           │
		       └── test1.py
	         ├── function2/
		     │
		     └── test2.py
	        ├── __init__.py
	        └── conftest.py
	    ├── .coveragerc
	    ├── .gitignore
	    ├── setup.py
	    ├── requirements.txt
	    ├── test_requirements
	    └── README.md


Generate Fake Data :

#To Generate data in docker container and move it back to host manually

docker build -t python-fake-data .

docker run -it python-fake-data

CONTAINER_ID=$(docker ps -alq)

docker cp "$CONTAINER_ID":/opt/app/generated_data .

##Or

just run the shell script generate.sh ./generate.sh in the data director


To create artifacts:
 run below command to generate artifacts
     python setup.py bdist_spark
	 
	 The above will zip the package dependencies and package it self as zip files.
	 To call our main program we will use driver.py file which will be generic
	 
Command to submit :

spark-submit --py-files=package.zip,package-dep.zip driver.py --region=local --configFile=resources/appilcation.conf


with customized log4j

spark-submit --files log4j.properties --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=file:lo
g4j.properties" --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:log4j.properties" --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=file:lo
g4j.properties" --py-files=project_name-0.1.zip,project_name-0.1-deps.zip driver.py --region=local --configFile=C:\work\pysparkTemplate\de-spark-python.v2.0\resources\a
pplication.conf  


Testing :

pytest will be used to do unit testing.

use pytest.ini to configure pytest

use coveragerc to config the coverages to run during pytest

command : pytest --cov-report html --cov=project_name  --html=Reports\pytest.html
