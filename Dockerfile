FROM rockylinux:8.9

# Install System Packages
RUN dnf update --assumeyes && \
    dnf install -y \
        git \
        vim \
        wget \
        zip && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# Install Miniconda
COPY environment.yml environment.yml
RUN wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    rm -f Miniconda3-latest-Linux-x86_64.sh && \
    /root/miniconda3/condabin/conda update -y conda && \
    /root/miniconda3/condabin/conda init bash && \
    /root/miniconda3/condabin/conda env create -y -f environment.yml && \
    /root/miniconda3/condabin/conda clean --all -y