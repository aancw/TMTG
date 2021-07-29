# Copyright (c) 2021 Petruknisme
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

class TMTG(object):
    def __init__(self, args):
        print('Reading CSV file: {}'.format(args.c) )
        
        # Twint cli is writing csv file with tabs delimter
        # but twint library writing csv file with comma delimiter
        try:
            self.DATA = pd.read_csv(args.c)
        except:
            self.DATA = pd.read_csv(args.c, delimiter="\t")
            
        self.ITERATIONS_COUNT = 0
        self.DF = None
        self.iterate_dataframe(self.DATA, 'reply_to')
        self.iterate_dataframe(self.DATA, 'mentions')
        self.write_to_graph(args.g)
        print("Network Graph file is saved to {}".format(args.g))
        
    def iterate_dataframe(self, df_data, column_name):
        df_clean = df_data[df_data[column_name] != '[]']
        self.DF = pd.DataFrame(columns=['username', 'mention'])
        
        for index, row in df_clean.iterrows():
            try:
                mentions = str(row[column_name]).replace('\"', '\'')
                mentions_fix = mentions.replace('\'', '\"')
                json_data = json.loads(mentions_fix)
                for x in json_data:
                    men_user = x['screen_name']
                    self.DF.loc[self.ITERATIONS_COUNT] = [row['username']] + [men_user]
                self.ITERATIONS_COUNT = self.ITERATIONS_COUNT+1
            except: 
                pass
            
    def write_to_graph(self, filename):
        G = nx.from_pandas_edgelist(self.DF, source='username', target='mention')
        nx.write_gexf(G, filename)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='TMTG', 
                                     description='TMTG(Twint Mention to Graph) is tools for converting twint user mentions data to network graph for use in Gephi or others network mapping tools that support GEXF file format.',
                                     usage='%(prog)s -c /path/csvfile.csv -g /path/write-to-file.gexf'
                                     )
    parser.add_argument('-c', help='Twint csv file location', type=str, action='store', required=True)
    parser.add_argument('-g', help='File location for writing graph file', type=str, action='store', required=True)
    parser.add_argument('--csv', help='File location for writing graph file', action='store_true')
    args = parser.parse_args()
    g = TMTG(args)
    
    