## ASAR Log Preprocess

This is the repository for data pre-processing for ASAR-Deep-Loglizer. 

Our Intrepid-RAS Blue Gene dataset is done with the help from two open source toolkit, listed at the acknowledgement section.
***
#### References: 
+ [**ICSE'19**] Jieming Zhu, Shilin He, Jinyang Liu, Pinjia He, Qi Xie, Zibin Zheng, Michael R. Lyu. [Tools and Benchmarks for Automated Log Parsing](https://arxiv.org/pdf/1811.03509.pdf). *International Conference on Software Engineering (ICSE)*, 2019.
+ [**DSN'16**] Pinjia He, Jieming Zhu, Shilin He, Jian Li, Michael R. Lyu. [An Evaluation Study on Log Parsing and Its Use in Log Mining](https://jiemingzhu.github.io/pub/pjhe_dsn2016.pdf). *IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)*, 2016.
***
### Dataset 
#### For Blue Gene Intrepid RAS:

The team found that the best results are achieved by parsing on Message section of the Intrepid RAS dataset only. 

```python:
log_foramt = <LineID>,<BLOCK>,<COMPONENT>,<ERRCODE>,<EVENT_TIME>,<LOCATION>,<MESSAGE>,<MSG_ID>,<PROCESSOR>,<RECID>,<SEVERITY>,<SUBCOMPONENT>'
```

#### For Trinity Log Dataset: 

```python:
log_foramt = <user_ID>,<group_ID>,<submit_time>,<start_time>,<dispatch_time>,<queue_time>,<end_time>,<wallclock_limit>,<job_status>,<node_count>,<tasks_requested>
```

### Acknowledgement
***
#### 1. RAS processing 
This part of the code, `DatasetSpecific/ras_parse.py` is developed by Github User [JarvisXX](https://github.com/JarvisXX/). 

And ASAR Team uses this code to clean up the Intrepid RAS Log Dataset.

##### Title:  Parser for Intrepid RAS log Dataset
    
##### Author:Xingyi Wang, [Email](arvis_wxy@sjtu.edu.cn)
##### Date: 2018
##### Availability: [Github](https://github.com/JarvisXX/Parser-N-Analyzer-for-Intrepid-RAS-log-Dataset)

*** 
#### 2.logparser 
logparser is a opensource package developed by [LOGPAI](https://github.com/logpai)

##### Title:  LogParser

##### Author:LogPai
##### Date: 2018

##### Availability: [Github](https://github.com/logpai/logparser)

