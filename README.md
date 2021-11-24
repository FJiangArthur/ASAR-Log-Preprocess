# ASAR Log Preprocess


The best results are achieved by saving Message only.

#### For Blue Gene Intrepid RAS Dataset :

```python:
log_foramt = <LineID>,<BLOCK>,<COMPONENT>,<ERRCODE>,<EVENT_TIME>,<LOCATION>,<MESSAGE>,<MSG_ID>,<PROCESSOR>,<RECID>,<SEVERITY>,<SUBCOMPONENT>'
```
#### For Trinity Log Dataset: 

```python:
log_foramt = <user_ID>,<group_ID>,<submit_time>,<start_time>,<dispatch_time>,<queue_time>,<end_time>,<wallclock_limit>,<job_status>,<node_count>,<tasks_requested>
```
***
## Acknowledgement
***
####1. RAS processing 
This part of the code, `DatasetSpecific/ras_parse.py` is developed by Github User [JarvisXX](https://github.com/JarvisXX/). 

And ASAR Team uses this code to clean up the Intrepid RAS Log Dataset.

#####Title:  Parser for Intrepid RAS log Dataset
    
#####Author:Xingyi Wang, [Email](arvis_wxy@sjtu.edu.cn)
#####Date: 2018
#####Availability: [Github](https://github.com/JarvisXX/Parser-N-Analyzer-for-Intrepid-RAS-log-Dataset)
***

####2.logparser 
logparser is a opensource package developed by [LOGPAI](https://github.com/logpai)

#####Title:  LogParser
    
#####Author:LogPai
#####Date: 2018
#####Availability: [Github](https://github.com/logpai/logparser)
***