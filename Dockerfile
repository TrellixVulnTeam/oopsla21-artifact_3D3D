FROM ubuntu
ENV WD=/root
SHELL ["/bin/bash", "-c"]
RUN apt-get update
#RUN apt-get -y install cmake
RUN apt-get -y install git
#RUN apt-get -y install g++
#RUN apt-get -y install curl
RUN apt-get -y install wget
RUN apt-get -y install python3-pip
#RUN pip3 install scrapy
RUN pip3 install numpy
RUN pip3 install dash
RUN pip3 install pandas

# Configure and Build LLVM
#WORKDIR ${WD}
#RUN git clone https://github.com/nataliepopescu/llvm-project.git
#WORKDIR ${WD}/llvm-project
#RUN git checkout match-version-from-rust
#RUN mkdir -p build
#WORKDIR ${WD}/llvm-project/build
#RUN cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="/root/.llvm" \
#-DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release ../llvm
#RUN make install-llvm-headers && make -j$(nproc)

# Configure and Build Rust
#WORKDIR ${WD}
#RUN git clone https://github.com/nataliepopescu/rust.git
#COPY ["config.toml", "./rust"]
#WORKDIR ${WD}/rust
#RUN apt-get -y install pkg-config
#RUN apt-get -y install libssl-dev
#RUN python3 x.py build && python3 x.py install && \
#python3 x.py install cargo && python3 x.py doc

# Set up benchmarking framework
WORKDIR ${WD}
RUN git clone https://github.com/nataliepopescu/bencher_scrape.git
WORKDIR ${WD}/bencher_scrape
ENV PATH="/root/.cargo/bin:$PATH"
#RUN cargo install cargo-edit

# Download libraries for Figure 1
ENV F1=fig1
RUN mkdir ${F1}
WORKDIR ${WD}/bencher_scrape/${F1}
# combine-4.5.2
RUN wget www.crates.io/api/v1/crates/combine/4.5.2/download
RUN tar -xzf download && rm download
# string-interner-0.12.2
RUN wget www.crates.io/api/v1/crates/string-interner/0.12.2/download
RUN tar -xzf download && rm download
# prost-0.7.0
RUN wget www.crates.io/api/v1/crates/prost/0.7.0/download
RUN tar -xzf download && rm download
# glam-0.14.0
RUN wget www.crates.io/api/v1/crates/glam/0.14.0/download
RUN tar -xzf download && rm download
# primal-sieve-0.3.1
RUN wget www.crates.io/api/v1/crates/primal-sieve/0.3.1/download
RUN tar -xzf download && rm download
# euc-0.5.3
RUN wget www.crates.io/api/v1/crates/euc/0.5.3/download
RUN tar -xzf download && rm download
# roaring-0.6.5
RUN wget www.crates.io/api/v1/crates/roaring/0.6.5/download
RUN tar -xzf download && rm download
WORKDIR ${WD}/bencher_scrape
