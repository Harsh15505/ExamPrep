FROM apache/spark:3.5.1

# Switch to root to install packages
USER root

# Install required Python libraries + Jupyter
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    networkx \
    jupyter \
    findspark

# Set environment variables so PySpark works inside Jupyter
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PATH="${SPARK_HOME}/bin:${PATH}"

# Create a working directory
RUN mkdir -p /work && chmod 777 /work

WORKDIR /work

# Expose Jupyter port
EXPOSE 8888

USER root
