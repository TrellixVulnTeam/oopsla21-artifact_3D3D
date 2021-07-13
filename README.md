# OOPSLA 2021 Artifact

## Getting Started

1. [Install Docker](https://docs.docker.com/engine/install/) and start up the 
docker daemon, either 
[manually](https://docs.docker.com/config/daemon/#start-the-daemon-manually)
or through the 
[system utility](https://docs.docker.com/config/daemon/#start-the-daemon-using-operating-system-utilities).

2. Build the docker image (TODO publish image so it can just be downloaded in this step) (this should take 20-30 minutes):

```sh
docker build --tag oopsla21-nader .
```

3. If the image builds successfully, start a docker container like so: 

```sh
docker run -it -p <port>:<port> --cap-add=sys_nice --name artifact oopsla21-nader
```

4. Test that the artifact works by running: 

```sh
python3 ExpDriver.py --figure1 --figure59 --figure7table3
```

This command should complete in under an hour. We explain what it does in more 
detail in the next section. 

## Step by Step Instructions

All of the following commands should be run from the `~/nader/` directory. 
Running all experiments fully takes almost two days to complete. 
We have therefore implemented a fast path that can run all experiments 
(on fewer libraries and applications) and finishes in under an hour. 
Our driver runs the fast path by default, so to run the full version of experiments, 
run: 

```sh
python3 ExpDriver.py [OPTIONS] --full
```

To run the __fast__ path on _all_ experiments, run: 

```sh
python3 ExpDriver.py --all
```

To run the __full__ path on _all_ experiments, run: 

```sh
python3 ExpDriver.py --all --full
```

### Generating results/plots

To run individual experiments, simply replace `--all` with the flag corresponding 
to the desired experiment, found by running: 

```sh
python3 ExpDriver.py --help

  ...
  --figure1           generate figure 1
  --table1            generate table 1
  --figure59          generate figures 5 and 9
  --figure7table3     generate figure 7 and table 3
  --table4            generate table 4
  --figure8           generate figure 8
  ...
```

To generate Figure 7 and Table 3, for example, run the following: 

```sh
python3 ExpDriver --figure7table3 [--full]
```

Expected running times for all experiments on a 
2.3 GHz Dual-Core Intel Core i5 Macbook Pro
are listed here:  

| | Figure 1 | Table 1 | Figures 5 and 9 | Figure 7 and Table 3 | Table 4 | Figure 8 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fast | 20 min | - | 40 min | 2 min | - | - | 1 hr |
| Full | 7 hrs | 20 min | 9 hrs | 20 min | 1 hr | 1 hr | ~19 hrs |

### Viewing results/plots

Some expected output is in `example-results`; you can compare your generated plots to those as a sanity check. 
The above result/plot generalization produces a series of PDFs that can be copied out of the docker container and 
viewed locally. If the container is currently running, get the container ID by running: 

```sh
docker container ps

CONTAINER ID   IMAGE           COMMAND  CREATED  STATUS   PORTS   NAMES
<container_id> oopsla21-nader  ...      ...      ...              artifact
```

If the container is stopped, get the 
container ID by running: 

```sh
docker container ps -a
```

Copy files locally using the `docker cp` cmd: 

```sh
docker cp <container_id>:/home/oopsla21ae/images/<plot>.pdf <local_dest>
```

Where <plot>.pdf is any of the files listed in the below subsections. 

In general, the figures and tables produced here are analogous to the figures and 
tables presented in the paper. We describe how to interpret results below, but 
also refer reviewers to the paper for more detailed information. 

#### Figure 1
  
Files: 

```sh
figure1_all.pdf
figure1_histogram.pdf
figure1_hurt.pdf
figure1_improved.pdf
figure1_insignificantly_affected.pdf
```

Figure 1 results are generated by benchmarking 7 Rust libraries that are in the 
top 250 most downloaded Rust libraries from `crates.io`. These 7 libraries use 
unchecked indexing direct and also come with their own benchmarking suites. 
We compile two versions of each library, one with unchecked indexing and one 
where unchecked indexing is converted to checked indexing, to effectively measure 
the overhead of _checked_ indexing (i.e. bounds checks). 

We find that overhead of checked indexing is not fixed and more specifically, 
that checked indexing does not always hurt performance. `figure1_improved.pdf` 
shows the benchmarks where bounds checks cause speedups, and `figure1_insignificantly_affected.pdf` 
shows benchmarks where bounds checks have no significant effect on performance 
at all. For comparison, `figure1_hurt.pdf` shows the benchmarks where bounds checks 
do hurt performance, and all results are summarized in `figure1_all.pdf` and 
`figure1_histogram.pdf`.

#### Table 1

Table 1 results are generated by benchmarking two versions of a 
[Rust implementation](https://github.com/dropbox/rust-brotli-decompressor) of the 
brotli decompression algorithm in three different contexts. The two versions
of `rust-brotli` are one with unchecked indexing and one where unchecked 
indexing is converted to checked indexing. The three contexts are: 

   * A baseline context: rustc 1.52, compression level = 5
   * A different workload: rustc 1.52, compression level = 11
   * A different compiler: rustc 1.46, compression level = 5

See [this](https://github.com/nataliepopescu/oopsla21-artifact#paper-claims-not-supported-by-artifact) 
section for why our table is missing the `different architecture` column. 

In each context, we effectively measure the overhead of checked indexing by 
benchmarking the two versions of `rust-brotli` and recording the relative 
performance differences. We claim that different contexts further complicate the 
performance impacts of checked indexing. Different checked indexing overheads 
in these different contexts show that this is indeed the case. 

#### Figures 5 and 9

Files: 

```sh
figure5.pdf
figure9.pdf
```

Figure 5 explores the potential heuristics for reintroducing bounds checks. 
Figure 5 is generated by running `rust-brotli` benchmark with only unchecked indexing, 
and iteratively converting them to checked indexing in an order specified by one 
of four heuristics: random, hotness-based, one-checked, and one-unchecked. 
The goal of these different orders is to maximize the amount of unchecked indexing 
converted to checked indexing within a certain threshold (i.e. the farther away from 
random the better). We claim that the hotness heuristic with one-checked at the 
end performs better than the rest. This is shown in the results by an orange line (hotness) that 
hugs the x axis longer than the rest until the light blue (one-checked) line 
surpasses it, thus overall reintroducing more checks while staying below the 
threshold. 

Figure 9 confirms that hotness + one-checked performs better than just hotness 
(and better than random) through a fully-automated run of the heuristic-based 
NADER on `rust-brotli`. The line that hugs the x axis longest introduces the most 
bounds checks within the threshold. 

#### Figure 7 and Table 3

Files: 

```sh
figure7.pdf
table3.pdf
```
  
Figure 7 results are generated by counting unchecked indexing across a set of 
manually, but systematically, chosen applications. Concretely, for each application, 
uses of direct unchecked indexing (within the application itself) and indirect 
unchecked indexing (in the application's dependencies) are counted and displayed as a bar 
chart. We claim that there are _many_ more instances of indirect unchecked indexing than 
there are of direct unchecked indexing: for every direct unchecked indexing operation an 
application uses we calculated there are on average 86 indirect unchecked indexing operations 
in the dependencies! This also supports our claim that unchecked indexing is difficult to 
audit because most of it is in project dependencies. 
  
Table 3 results build off Figure 7 by also including the total number of application dependencies 
and the number of dependencies that have at least one unchecked indexing use. 

#### Table 4

#### Figure 8

Files: 

```sh
figure8.pdf
```
  
Figure 8 confirms that hotness + one-checked performs better than just hotness 
(and better than random) through a fully-automated run of the heuristic-based 
NADER on `COST`. The line that hugs the x axis longest introduces the most 
bounds checks within the threshold. 

### Paper claims _not_ supported by artifact

1. The "Different Architecture" column in Table 1 is not supported by our artifact because 
the reviewers may not have access to two or more different architectures on which to 
run our experiments. 

1. The last column of Table 3 is also not supported by our artifact because it was 
the result of a manual process. We moved forward with applications that had 
reasonable synthetic profiling workloads, although there is room for a more 
rigorous process of elimination here. 

### Functional Badge Requirements
  
- Artifact supports all major claims made by paper (outlined in this document by all of the Figures and Tables)
- Artifact documents detailed steps for result reproduction and lists any potential deviations from what the paper claims
  
Deviations: 
  
- All but Figure 7 and Table 3 are performance results and will vary, but we describe trends and patterns to look for
- A full evaluation takes almost 19 hours, but we offer reviewers a fast path that can complete in about an hour
  
### Reusable Badge Requirements
  
- Future researchers can run this artifact on more libraries and applications by cloning their source code here
- Future researchers building off this artifact can do so by adding new benchmarks and their arguments
- Future researchers can directly modify `Nader.py` to improve its exploration algorithm
- Artifact source code can be reused as separate components much in the same way as the individual plots are generated 
- Others can learn about our benchmarking and large-scale application analysis techniques
- Others can extend the artifact beyond bounds checks to other code patterns by modifying `regexify.py`
