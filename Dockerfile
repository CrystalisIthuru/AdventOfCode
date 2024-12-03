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
    
# Install Racket
RUN wget -c https://download.racket-lang.org/installers/8.15/racket-8.15-x86_64-linux-cs.sh && \
    bash racket-8.15-x86_64-linux-cs.sh --dest /usr/ --unix-style && \
    rm -f racket-8.15-x86_64-linux-cs.sh

# Install Racket Packages
RUN raco pkg install --batch --deps search-auto advent-of-code && \
    raco pkg empty-trash

# Setup Advent of Code Session Token
COPY AOC_SESSION /root/.config/aocd/token