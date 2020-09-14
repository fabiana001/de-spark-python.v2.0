FROM 134635467856.dkr.ecr.us-east-1.amazonaws.com/centos-base:8.20200825.88

ENV PYTHONUNBUFFERED 1


# Add and configure base packages and tools
#RUN dnf -y install gcc autoconf make patch
#
# Add application dependencies (not included in base images)
#RUN dnf -y install python3-devel

COPY . /opt/app
WORKDIR /opt/app/

RUN yum install git -y

RUN pip3 install --upgrade pip

RUN pip3 install git+https://ghe.bcbsnc.com/nttda328/mimic.git --trusted-host pypi.org --trusted-host files.pythonhosted.org

ENTRYPOINT ["python3"]
CMD ["-m", "mimic", "--config", "./config.yaml", "--output", "./generated_data" ]


## comment above two lines and uncomment to get in to the container with /bin/bash
#ENTRYPOINT ["/bin/bash", "-l", "-c"]