"""
***************************************************************************************/
    Partially of the following code is developed by Github User JarvisXX, and 2470 Final
    project group uses this code to clean up the Intrepid RAS Log Dataset.

    Title: Parser for Intrepid RAS log Dataset
    Author: Xingyi Wang, arvis_wxy@sjtu.edu.cn
    Date: 2018
    Availability: https://github.com/JarvisXX/Parser-N-Analyzer-for-Intrepid-RAS-log-Dataset

***************************************************************************************/
"""

import json

label = ['RECID', 'MSG_ID', 'COMPONENT', 'SUBCOMPONENT', 'ERRCODE', 'SEVERITY', 'EVENT_TIME', 'FLAGS', 'PROCESSOR', 'NODE', 'BLOCK', 'LOCATION', 'SERIALNUMBER', 'ECID', 'MESSAGE']

pattern = ['-----------', # RECID 11
           '----------', # MSG_ID 10
           '----------------', # COMPONENT 16
           '--------------------', # SUBCOMPONENT 20
           '----------------------------------------', # ERRCODE 40
           '--------', # SEVERITY 8
           '--------------------------', # EVENT_TIME 26
           '----------', # FLAGS 10
           '-----------', # PROCESSOR 11
           '-----------', # NODE 11
           '--------------------------------', # BLOCK 32
           '----------------------------------------------------------------', # LOCATION 64
           '-------------------', # SERIALNUMBER 19
           '-------------------------------', # ECID 31
           '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------']
           # MESSAGE 1024


cnt = 0


def getMessage(line, f):
    msg_prefix_list = ['A DDR ', 'A DMA ', 'A kernel ', 'A Link ', 'A memory ', 'A message ', 'A processor ', 'A script ', 'An ',
                       'ACCESS: ', 'ACCESS_SCOM_STAT: ',
                       'Bootloader ', 'Broken ',
                       'Can no ', 'Cannot ', 'Checksum ', 'CIO service ', 'Collective ', 'Correctable ', 'Could ',
                       'DDR ', 'Detected ', 'DMA SRAM ', 'DMA unit ',
                       'E10000 ', 'ECC-correctable ', 'ECID: ', 'Environment ', 'Error ',
                       'Global ',
                       'Had ', 'HBIST loopback ',
                       'Initialization ', 'Insufficient ', 'Internal ', 'Invalid ', 'IOCard ',
                       'Lbist ', 'Link ', 'L1 data ', 'L1 instruction ', 'L2 snoop ', 'L3 cache ', 'L3 Correctable ', 'L3 directory ', 'L3 machine ',
                       'Machine ', 'Missing bulk ',
                       'Node ',
                       'Power ', 'Problem ',
                       'SerDes ', 'Service ', 'Software ', 'Spurious ', 'Successfully ',
                       'The ', 'There ', 'This ', 'TLB Entry ', 'TLB parity ', 'Torus ',
                       'Unable ',
                       '1.2 power ', '1.5 power ', '1.5V power ', '1.8 Power ', '1.8 power ', '1.8vV power ', '3.3 power ', '5.0 power ']
    # 'The' : 'The global ', 'The microloader ', 'The TNK '
    # 'An' : 'An attempt ', 'An error(s) ', 'An illegal ', 'An oops '
    global cnt
    idx = -1
    # print '-----loop-----'
    line_buf = [] # DEBUG
    while idx < 0:
        # print line
        idx_flag = 0
        idx_min = 2000
        for item in msg_prefix_list:
            idx_tmp = line.find(item)
            if idx_tmp >= 0 and idx_tmp < idx_min:
                idx_flag = 1
                idx_min = idx_tmp
        if idx_flag:
            idx = idx_min
        else:
            line_buf.append(line) # DEBUG
            line = f.readline()
            cnt += 1
            if line.strip() != '' and line.strip()[0] == '2':
                print line_buf # DEBUG
                print 'UNSEEN'
                print cnt
                exit()
        # print idx
        # raw_input()
    msg = line[idx:].strip()
    msg = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
    return msg


def parse(filename):
    f = open(filename, 'r')
    out_f = open(filename + '.json', 'w')
    unsolved_f = open(filename + '_unsolved', 'w')
    global cnt
    legal_cnt = 0
    start = 0
    while True:
        line = f.readline()
        cnt += 1
        if not line:
            break
        if cnt < start:
            continue
        if line.strip() == '':
            continue
        if legal_cnt % 10000 == 0:
            print legal_cnt
        # print cnt
        try:
            if cnt < 274525:
                log = {}
                log['RECID'] = " ".join(line[0:11].split())
                log['MSG_ID'] = " ".join(line[12:22].split())
                log['COMPONENT'] = " ".join(line[23:39].split())
                log['SUBCOMPONENT'] = " ".join(line[40:60].split())
                log['ERRCODE'] = " ".join(line[61:101].split())
                log['SEVERITY'] = " ".join(line[102:110].split())
                log['EVENT_TIME'] = " ".join(line[111:137].split())
                log['FLAGS'] = " ".join(line[138:148].split())
                log['PROCESSOR'] = " ".join(line[149:160].split())
                log['NODE'] = " ".join(line[161:172].split())
                log['BLOCK'] = " ".join(line[173:205].split())
                log['LOCATION'] = " ".join(line[206:270].split())
                log['SERIALNUMBER'] = " ".join(line[271:290].split())
                log['ECID'] = " ".join(line[291:322].split())
                log['MESSAGE'] = " ".join(line[323:].split())
                json.dump(log, out_f)
                out_f.write('\n')
                out_f.flush()
                legal_cnt += 1
            else:
                log = {}
                log['RECID'] = " ".join( line[0:11].split())
                log['MSG_ID'] =" ".join(line[13:23].split())
                log['COMPONENT'] =" ".join(line[26:42].split())
                log['SUBCOMPONENT'] =" ".join(line[45:65].split())
                log['ERRCODE'] =" ".join(line[68:108].split())
                log['SEVERITY'] = " ".join(line[111:119].split())
                log['EVENT_TIME'] =" ".join(line[122:148].split())
                log['FLAGS'] = 'N/A'
                log['NODE'] = 'N/A'
                log['SERIALNUMBER'] = 'N/A'
                log['ECID'] = 'N/A'
                if log['COMPONENT'][:4] == 'MMCS':
                    if log['ERRCODE'][:14] == 'SERVER_STARTED' or log['ERRCODE'][:16] == 'SERVER_RESTARTED' or log['ERRCODE'][:18] == 'SERVER_TERMINATION' or log['ERRCODE'][:17] == 'BGPMASTER_STARTED' or log['ERRCODE'][:17] == 'BGPMASTER_STOPPED':
                        log['PROCESSOR'] = " ".join(''.join([' ' for i in range(11)]).split())# empty.split())
                        log['BLOCK'] = " ".join((" ".join(line[122:148].split())).split())
                        log['LOCATION'] =" ".join(( ''.join([' ' for i in range(64)])).split()) # empty
                        msg = " ".join(line[158:].strip().split())
                        log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
                        log['MESSAGE'] = " ".join(log['MESSAGE'].split())
                    elif log['ERRCODE'][:16] == 'KILL_JOB_TIMEOUT':
                        log['PROCESSOR'] = " ".join((''.join([' ' for i in range(11)])).split()) # empty
                        log['BLOCK'] =" ".join(line[154:186].split())
                        log['LOCATION'] = " ".join((''.join([' ' for i in range(64)])).split()) # empty
                        msg = " ".join(line[258:].strip().split())
                        log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
                        log['MESSAGE'] = " ".join(log['MESSAGE'].split())
                    else:
                        log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
                        log['PROCESSOR'] = " ".join(log['PROCESSOR'].split())
                        log['BLOCK'] = ''.join([' ' for i in range(32)])
                        log['BLOCK'] = " ".join(log['BLOCK'].split())
                        log['LOCATION'] = line[155:219]
                        log['LOCATION'] = " ".join(log['LOCATION'].split())
                        msg = line[224:].strip()
                        log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
                        log['MESSAGE'] = " ".join(log['MESSAGE'].split())
                elif log['COMPONENT'][:9] == 'BAREMETAL' or log['COMPONENT'][:4] == 'CARD' or log['COMPONENT'][:2] == 'MC' or (log['COMPONENT'][:5] == 'DIAGS' and line[151] == ' '):
                    log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
                    log['PROCESSOR'] = " ".join(log['PROCESSOR'].split())
                    log['BLOCK'] = line[154:186]
                    log['BLOCK'] = " ".join(log['BLOCK'].split())
                    log['LOCATION'] = line[189:253]
                    log['LOCATION'] = " ".join(log['LOCATION'].split())
                    log['MESSAGE'] = getMessage(line, f)
                    log['MESSAGE'] = " ".join(log['MESSAGE'].split())
                else:
                    log['PROCESSOR'] = ''.join([' ' for i in range(10)]) + line[151]
                    log['PROCESSOR'] = " ".join(log['PROCESSOR'].split())
                    log['BLOCK'] = line[155:187]
                    log['BLOCK'] = " ".join(log['BLOCK'].split())
                    log['LOCATION'] = line[190:254]
                    log['LOCATION'] = " ".join(log['LOCATION'].split())
                    log['MESSAGE'] = getMessage(line, f)
                    log['MESSAGE'] = " ".join(log['MESSAGE'].split())
                json.dump(log, out_f)
                out_f.write('\n')
                out_f.flush()
                legal_cnt += 1
        except Exception as e:
            print 'Exception:', cnt
            unsolved_f.write(line)
            unsolved_f.write('\n')
            # exit()
    f.close()
    out_f.close()
    unsolved_f.close()


if __name__ == '__main__':
    parse('Intrepid_RAS_0901_0908_scrubbed')