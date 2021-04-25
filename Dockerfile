FROM continuumio/miniconda3

WORKDIR /home/biolib

RUN conda install -c bioconda --yes anarci scikit-learn pandas numpy lightgbm\
    && \
    conda clean -afy

RUN wget https://biolib-public-assets.s3-eu-west-1.amazonaws.com/finalized_model.sav
RUN apt-get update -y
RUN apt-get install python2 -y
RUN python2 -m pip install numpy
COPY . .

ENTRYPOINT [ "python", "src/predict.py" ]

