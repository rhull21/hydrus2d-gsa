import os
import numpy as np
import xarray as xr
import pandas as pd

def read_item(path):
    return np.genfromtxt(fname=path,  skip_header=2, usecols=(1,2)) #delimiter='\t',

def get_set_from_collection(scheme, section, sample_collection, where_period=None, where_irrigation=None):
    li=  [
        member for member in sorted(sample_collection, key = lambda x: x.attrs['time']) 
            if (
                (member.attrs['scheme']==scheme)  
                and (member.attrs['section']==section) 
            )
        ]
    
    if where_period is not None:
        li = [
                outermember for outermember in 
                    [
                    innermember for innermember in li
                        if (innermember.attrs['time_info']['period'] is not None)
                    ]
                if (where_period in outermember.attrs['time_info']['period'])
            ]

    if where_irrigation is not None: 
        li = [
                outermember for outermember in 
                    [
                    innermember for innermember in li
                        if (innermember.attrs['time_info']['cumulative_irrigation_cm'] is not None)
                    ]
                if (where_irrigation in outermember.attrs['time_info']['cumulative_irrigation_cm'])
            ]

    return li

def get_sets_from_collection(schemes, sections, sample_collection):
    lili = []
    for scheme in schemes:
        for section in sections:
            lili.append(get_set_from_collection(scheme, section, sample_collection))
    return lili


class sample_items():
    
    def __init__(self, sample_name=None, sample_directory=None):
        
        # sample_directory
        if sample_directory is None: 
            self.sample_directory = 'c:/Users/QuinnHull/ownCloud-active jobs/BHP Chile/2150 - BHP Chile - MEL Permeability Testing Program for SHL Ores/Hydrus model/Sulphide AND SCC'
        else:
            self.sample_directory = sample_directory
        
        # sample_name, sample_name_uscroes
        self.sample_name = self.sample_directory.rsplit("/")[-1]
        if sample_name is not None:
            if self.sample_name != sample_name:
                self.sample_name = sample_name
                print("disagreement about sample name")
        self.sample_name_uscores = self.sample_name.replace(" ", "_")

        # raw_data_directory
        self.raw_data_directory=  os.path.join(self.sample_directory,"Raw data")

        # info directory
        self.info_directory = os.path.join(self.raw_data_directory, "info")

        # sample collection
        self.sample_item = self.Sample_Item
    
    def _scandir(self, split1=None, index1=None, split2=None, index2=None):
        li = []
        for filename in os.scandir(self.raw_data_directory):
            if filename.is_file():
                path = filename.path
                if (split1 is not None and index1 is not None and split2 is not None and index2 is not None ):
                    li.append(path.split(split1)[index1].split(split2)[index2])
                else:
                     li.append(path)
        return li

    def get_unique_times(self):

        t_string = self._scandir(split1="Water_Content_",
                                 index1=-1, 
                                 split2="_hours",
                                 index2=0, 
                                )

        t_string = list(set(t_string))
        t_val = [  
                    int(ts.rsplit('_')[-2]) + int(ts.rsplit('_')[-1])/(10**len(ts.rsplit('_')[-1])) # 
                    for ts in t_string
                ]

        self.unique_times = dict(zip(t_string, t_val))

        return self.unique_times

    def get_unique_schemes(self):
        
        scheme_string = self._scandir(split1=self.sample_name_uscores,
                                 index1=-1, 
                                 split2="_Water_Content",
                                 index2=0, 
                                )

        scheme_string = list(set(scheme_string))
        scheme_string.sort()
        self.unique_schemes = dict(zip(scheme_string, 
                                       [i for i in range(1,8)] 
                                       )
                                    )

        return self.unique_schemes

    def get_unique_sections(self):

        sect_string = self._scandir(split1="hours_",
                                 index1=-1, 
                                 split2=".txt",
                                 index2=0, 
                                )

        sect_string = list(set(sect_string))
        sect_string.sort()
        self.unique_sects = dict(zip(sect_string, 
                                       [i for i in range(1,len(sect_string)+1)] 
                                       )
                                    )

        return self.unique_sects

    def get_paths(self):
        self.all_paths = self._scandir()
        return self.all_paths

    def get_time_info(self, info_file="sample_time_info.csv"):
        path = os.path.join(self.info_directory, info_file)
        self.time_info = np.genfromtxt(fname=path, names=True, delimiter=',', dtype=None)
        return self.time_info 

    def make_sample_collection(self):
        self.sample_collection = []
        
        for path in self.all_paths:
            self.sample_collection.append(self.sample_item.create_item(self, path))
    
        return self.sample_collection

    class Sample_Item:

        def extract_time_info_filter(self, item_arr, filter):
            '''
            Adds time info attributes to item
            To Do : Will want to update to make more flexible
            '''
            item_arr.attrs['time_info'] = {
                                        "cumulative_irrigation_cm" : self.time_info['ï»¿cum_irr_cm'][filter], 
                                        "period" : self.time_info['period'][filter]
            }
            return item_arr

        def extract_attr_base(self, path, tp):
            '''
            extracts information about data from parent class based on path to item
            '''
            if tp == 'time': 
                li = [self.unique_times[t] for t in self.unique_times.keys() if path.find(t)>=0 ]
            elif tp == 'section': 
                li = [sect for sect in self.unique_sects.keys() if path.find(sect)>=0 ]
            elif tp == 'scheme': 
                li = [str(self.unique_schemes[schem]) for schem in self.unique_schemes.keys() if path.find(schem)>=0 ]
            return li

        def create_item(self, path):
            # path = self.path
            item = read_item(path)

            item_arr = xr.DataArray(data=item[:,1],
                        name=path,  
                        coords={
                            "distance" : item[:,0]
                            },
                            dims=["distance"],
                            attrs={
                            'path' : path, 
                            'time' : self.sample_item.extract_attr_base(self=self, path=path, tp='time')[0], # extract attributes from list
                            'section' : self.sample_item.extract_attr_base(self=self, path=path, tp='section')[0], 
                            'scheme' : self.sample_item.extract_attr_base(self=self, path=path, tp='scheme')[0], 
                            }
                )

            # add important time info to attributes
            filter = self.time_info[item_arr.attrs['scheme']]==item_arr.attrs['time']
            self.sample_item.extract_time_info_filter(self=self, item_arr=item_arr, filter=filter)

            return item_arr


def write_horizontal(path, li, header=True, write_bool=True, insert_list=['cumulative_irrigation_cm', 'scheme']):

    for l in li:
        if write_bool != True:
            mode='a'
            df = l.to_dataframe().T
            header=False

        else:
            mode='w'
            write_bool=False
            df = l.to_dataframe().T
            header=True
        
        # print(df.index)
        df.insert(loc=0, column=insert_list[0], value=str(l.attrs['time_info'][insert_list[0]][0]))
        df.insert(loc=1, column=insert_list[1],  value=str(l.attrs[insert_list[1]][0]))

        df.to_csv(path, mode=mode, header=header) 

    try:
        pd.DataFrame(columns=[' ' for i in range(len(df.columns))]).to_csv(path, mode=mode) 
    except:
        print(f"No Data in collection ")

def write_horizontal_sheet(section, schemes, sample_collection, where_period=b'Before next ON period', where_irrigation=None, save_dir='',  insert_list=['cumulative_irrigation_cm', 'scheme']):
    
    write_bool = True
    for scheme in schemes:
        # print(scheme, section)
        li = get_set_from_collection(scheme=scheme,section=section,sample_collection=sample_collection, where_period=where_period, where_irrigation=where_irrigation)
        # print(li)
        write_horizontal(path=os.path.join(save_dir,section+'.csv'), li=li, header=True, write_bool=write_bool, insert_list=insert_list)   
        write_bool = False