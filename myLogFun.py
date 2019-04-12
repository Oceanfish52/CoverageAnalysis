import numpy as np
import pandas as pd

def log_tran(df,except_col=[]):
    transformed_col=[]
    for col in df.columns:
        if (df[col].skew() > 1) and (col not in except_col):
            df[col] = np.log(df[col])
            df.rename({col:'ln_{}'.format(col)},axis=1,inplace=True)
            transformed_col.append(col)
    return df,transformed_col

def inv_log_tran(df):
    for col in df.columns:
        if col[:2] == 'ln':
            df[col] = np.e**(df[col])
            df.rename({col:col[3:]},axis=1,inplace=True)
    return df

def cor_col(df):
    
    threshold = 0.8
    
    # Absolute value correlation matrix
    corr_matrix = df.corr().abs()
    
    # Upper triangle of correlations
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

    # Select columns with correlations above threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    return to_drop

def get_log_col(df,log_col_lst):
    col_loc = []
    for col in log_col_lst:
        col_loc.append(df.columns.get_loc(col))
    return col_loc

def log_tran_mat(mat,idx):
    mat2=mat.copy()
    for i in idx:
        mat2[i] = np.log(mat2[i])
    return mat2

def inv_log_tran_mat(mat,idx):
    mat2=mat.copy()
    for i in idx:
        mat2[i] = np.e**(mat2[i])
    return mat2