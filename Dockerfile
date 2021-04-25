FROM continuumio/miniconda3

WORKDIR /home/biolib

RUN apt-get install python-pip
RUN pip install numpy
RUN conda install -c bioconda --yes anarci scikit-learn pandas numpy lightgbm\
    && \
    conda clean -afy

RUN wget https://biolib-public-assets.s3-eu-west-1.amazonaws.com/finalized_model.sav
COPY . .

ENTRYPOINT [ "python", "src/predict.py" ]

