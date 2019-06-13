import json
import pandas as pd
import numpy as np

def default(o):
    if isinstance(o, np.int64): return int(o)  
    #raise TypeError

def find_key(rqd, target_key):
    for key in rqd:
        target_col = rqd[key]["top"].loc[rqd[key]["top"]['query']==target_key]
        if target_col.empty is False:
            return target_col.loc[:,"value"].values
        #else:
        #    return None
        #print(rqd[key]["rising"].loc[rqd[key]["rising"]['query']==target_key])

def find_relative(keys, filted, rqd, interval=0.2):
    black_list = np.zeros(keys.shape, dtype=bool)
    # Find the index of the maximum value in N dimension array
    index = np.unravel_index(np.argmax(filted, axis=None), filted.shape)
    # Find the index of the maximum value in N dimension array
    max_value = filted[index]
    lower_bound = max_value - interval
    #print("max_value= ",max_value)
    #print("lower_bound= ", lower_bound)
    target_index = index[0]
    #print(abs(corr_matrix[target_index,:]))
    
    # Get index of value in boundary, apply abs to mark +1 and -1 corr are treated equal
    mask = np.argwhere(abs(filted[target_index,:]) > lower_bound)
    # Add into black_list, so they won't be in the next result
    black_list[target_index] = True
    black_list[mask] = True
    # Mark visited
    filted[black_list] = 0
    #print("black=", keys[black_list])
    found_key_list = keys[mask].tolist()
    found_key_list.append(keys[target_index])
    #print("key list= ", found_key_list)
    value_list = []
    for k in found_key_list:
        new_value = find_key(rqd, k[0])
        if new_value is not None:
            value_list.append(new_value[0])
            
    group_list = []
    #print("value=", value_list)
    for n, t in zip(found_key_list, value_list):
        if t is not None:
            group_list = [{"name":n[0], "value":t}for n, t in zip(found_key_list, value_list)]
    if find_key(rqd, keys[target_index]) is not None:
        group_dict = {"name":keys[target_index][0], "value":find_key(rqd, keys[target_index])[0]}
        #print(group_dict)
        group_list.append(group_dict)
    if(len(group_list)>1):
        outter_dict = {'name':'subset', 'children':group_list}
        group_list = outter_dict
    else:
        group_list = group_list[0]
    #print("group=", group_list)
    return lower_bound, group_list

def get_corr_json(corr_result, rqd):
    corr_matrix = corr_result.values
    # Key array
    keys = corr_result.keys().values

    # Clear values in diagnal
    for i in range(corr_matrix.shape[0]):
        corr_matrix[i, i] = 0    
    filted_corr = corr_matrix.copy()

    now_level = 1
    interval = 0.2
    children_parent = []
    while now_level > 0.1:
        lower_bound = now_level - interval
        children = []
        while now_level > lower_bound:
            now_level, g = find_relative(keys, filted_corr, rqd, interval)
            children.append(g)
        sub = {'name':'level'+str(now_level), 'children':children}
        children_parent.append(sub)

    group_list = {'name':'Google Trend', 'children':children_parent}
    return json.dumps(group_list, default=default)
