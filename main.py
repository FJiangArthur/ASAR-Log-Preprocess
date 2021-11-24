import pandas as pd
import numpy as np
import gdown
from parse import parse_util
from DatasetSpecific.ras_parse import parse as process_ras


def save_to_csv(json_input, full_log, msg_only):
    df = pd.read_json(json_input, lines=True)
    df = df[2:]
    df['BLOCK'] = df['BLOCK'].fillna('N/A')
    df['ECID'] = df['ECID'].apply(lambda x: x.replace(r"'", ''))
    df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'], format='%Y-%m-%d-%H.%M.%S.%f', errors='ignore')

    for col in df[['BLOCK', 'PROCESSOR']].columns:
        df[col].apply(lambda x: 'N/A' if x == '' else x)

    # Sort the value
    df.sort_values(by=['BLOCK', 'EVENT_TIME'])
    df['BLOCK_TIME_UNIQUE_ID'] = df['BLOCK'] + '__' + df['EVENT_TIME'].dt.strftime('%Y-%m-%d-%H')

    # This is too fine-grained for logging type
    df['EVENT_TIME'] = df['EVENT_TIME'].dt.strftime('%Y-%m-%d-%H-%M-%S-%f')
    df['FLAGS'] = df['FLAGS'].apply(lambda x: x.replace('-', 'N/A'))
    df['MESSAGE'] = df['MESSAGE'].apply(lambda x: x.replace(r"'", '').replace(r'"', '').replace(",", ';'))
    df['NODE'] = df['FLAGS'].apply(lambda x: x.replace('-', 'N/A'))

    # Save just msg column and block_time_unique_id column for better parsing result
    msg_df = df[['BLOCK_TIME_UNIQUE_ID', 'MESSAGE']]
    msg_df.to_csv(msg_only, sep=',', na_rep='N/A', header=True,
               index=True)

    df.to_csv(full_log, sep=',', na_rep='N/A', header=True, index=True)


def create_labels(output_file, binary=False):
    df = pd.read_csv('Intrepid_RAS_0901_0908_scrubbed_with_unique_id.csv')

    if binary:
        df['label'] = np.where((df['SEVERITY'] == ('ERROR' or 'FATAL')), 'Abnormal', 'Normal')
        print("Converting binary labels")
    else:
        df['label'] = np.where((df['SEVERITY'] == ('ERROR' or 'FATAL')), df['SEVERITY'] + '__' + df['SUBCOMPONENT'],  'Normal')
        print("Converting Multi-class labels")

    label = df[['BLOCK_TIME_UNIQUE_ID','label']]
    label = label.groupby('BLOCK_TIME_UNIQUE_ID')['label'].apply(list).reset_index()

    # TODO: Optimize later
    for index, row in label.iterrows():
        if len(row['label']) > 1:
            if 'Normal' in row['label']:
                row['label'] = [x for x in set(row['label']) if x not in ['Normal', None]]
            else:
                row['label'] = [x for x in set(row['label']) if x not in [None]]

            if len(row['label']) == 0:
                row['label'] = ['Normal']

    label.to_csv(output_file, sep=',', na_rep='N/A', header=True, index=True)


def combine_msg_template(input_file):
    df = pd.read_csv('Intrepid_RAS_0901_0908_scrubbed_with_unique_id.csv')
    df_msg_structured = pd.read_csv('Intrepid_RAS_0901_0908_scrubbed_with_unique_id_msg_only.csv_structured.csv')
    df_msg_structured = df_msg_structured.drop(['LineId', 'LineID'], axis=1)
    df = df[1:len(df_msg_structured)]
    df_merged = pd.concat([df, df_msg_structured], axis=1)
    df_merged.to_csv('Intrepid_RAS_0901_0908_scrubbed_with_unique_id_combined_with_structured_msg.csv', sep=',', na_rep='N/A', header=True, index=False)


if __name__ == '__main__':
    # Getting Intrepid RAS Dataset
    url = 'https://drive.google.com/uc?id=1MipdCgWaYXqNkDRdpoIZ-GCyH83-oHq1'
    output = 'Intrepid_RAS_0901_0908_scrubbed.log'
    gdown.download(url, output, quiet=False)

    # RAS Specific Handling to solve encoding issue
    process_ras(output)

    # Save to csv with complete log and msg only log
    json_input = 'Intrepid_RAS_0901_0908_scrubbed.json'
    full_log = 'Intrepid_RAS.csv'
    msg_only = 'Intrepid_RAS_msg_only.csv'
    save_to_csv(json_input,full_log, msg_only)

    # Actual Parsing on msg only files
    log_format = '<LineID>,<BLOCK_TIME_UNIQUE_ID>,<Content>'
    input_dir = './'
    log_name = 'Intrepid_RAS_msg_only.csv'
    parse_util(input_dir, log_name, [], log_format)

    # Create binary/multiclass label
    create_labels(True,)


