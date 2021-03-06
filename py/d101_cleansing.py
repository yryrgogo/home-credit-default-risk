import gc
import numpy as np
import pandas as pd
import sys
import os
HOME = os.path.expanduser('~')
sys.path.append(f"{HOME}/kaggle/data_analysis/library/")
import utils
from utils import logger_func
logger = logger_func()
import eda
from utils import get_categorical_features

key = 'SK_ID_CURR'
target = 'TARGET'


#  app = utils.read_df_pkl(path='../input/clean_app*.p')
#  app[target] = app[target].where(app[target]>=0, np.nan)
#  utils.to_df_pkl(df=app, path='../input', fname='clean_application_train_test')
#  sys.exit()

#==============================================================================
# to pickle
#==============================================================================
def to_pkl():
    app_train = pd.read_csv('../input/application_train.csv')
    app_test = pd.read_csv('../input/application_test.csv')
    app = pd.concat([app_train, app_test], axis=0)
    utils.to_df_pkl(df=app, path='../input', fname='application_train_test')
    app_eda = eda.df_info(app)
    app_eda.to_csv('../eda/application_eda.csv')

    bur = pd.read_csv('../input/bureau.csv')
    utils.to_df_pkl(df=bur, path='../input', fname='bureau')
    bur_eda = eda.df_info(bur)
    bur_eda.to_csv('../eda/bureau_eda.csv')

    pre = pd.read_csv('../input/previous_application.csv')
    utils.to_df_pkl(df=pre, path='../input', fname='previous_application')
    pre_eda = eda.df_info(pre)
    pre_eda.to_csv('../eda/prev_eda.csv')

    ins = pd.read_csv('../input/installments_payments.csv')
    utils.to_df_pkl(df=ins, path='../input', fname='installments_payments')
    ins_eda = eda.df_info(ins)
    ins_eda.to_csv('../eda/install_eda.csv')

    ccb = pd.read_csv('../input/credit_card_balance.csv')
    utils.to_df_pkl(df=ccb, path='../input', fname='credit_card_balance')
    ccb_eda = eda.df_info(ccb)
    ccb_eda.to_csv('../eda/credit_eda.csv')

    pos = pd.read_csv('../input/POS_CASH_balance.csv')
    utils.to_df_pkl(df=pos, path='../input', fname='POS_CASH_balance')
    pos_eda = eda.df_info(pos)
    pos_eda.to_csv('../eda/pos_eda.csv')

#  to_pkl()
#  sys.exit()

#========================================================================
# CLEANSING & PROCESSING
#========================================================================
def clean_app(app):
    logger.info(f'''
    #==============================================================================
    # APPLICATION
    #==============================================================================''')

    app['CODE_GENDER'].replace('XNA', 'F', inplace=True)

    cat_cols = get_categorical_features(df=app, ignore_list=[])
    for col in cat_cols:
        app[col].fillna('XNA', inplace=True)

    ' revo '
    #  revo = 'Revolving loans'
    #  amt_list = ['AMT_ANNUITY', 'AMT_CREDIT', 'AMT_GOODS_PRICE']
    #  for col in amt_list:
    #      app[f'revo_{col}'] = app[col].where(app[f'NAME_CONTRACT_TYPE']==revo, np.nan)
    #      app[col] = app[col].where(app[f'NAME_CONTRACT_TYPE']!=revo, np.nan)

    utils.to_df_pkl(df=app, path='../input', fname='clean_application_train_test')


def clean_bureau(bur):
    logger.info(f'''
    #==============================================================================
    # BUREAU CLEANSING
    #==============================================================================''')

    bur = utils.read_df_pkl(path='../input/bureau*.p')
    bur = bur[bur['CREDIT_CURRENCY']=='currency 1']
    bur['DAYS_CREDIT_ENDDATE'] = bur['DAYS_CREDIT_ENDDATE'].where(bur['DAYS_CREDIT_ENDDATE']>-36000, np.nan)
    bur['DAYS_ENDDATE_FACT'] = bur['DAYS_ENDDATE_FACT'].where(bur['DAYS_ENDDATE_FACT']>-36000, np.nan)
    bur['DAYS_CREDIT_UPDATE'] = bur['DAYS_CREDIT_UPDATE'].where(bur['DAYS_CREDIT_UPDATE']>-36000, np.nan)
    bur = utils.to_df_pkl(df=bur, path='../input', fname='clean_bureau')


def clean_prev(pre):
    logger.info(f'''
    #==============================================================================
    # PREV CLEANSING
    #==============================================================================''')

    cash = 'Cash loans'
    revo = 'Revolving loans'
    pre = utils.read_df_pkl(path='../input/previous*.p')
    pre['AMT_CREDIT'] = pre['AMT_CREDIT'].where(pre['AMT_CREDIT']>0, np.nan)
    pre['AMT_ANNUITY'] = pre['AMT_ANNUITY'].where(pre['AMT_ANNUITY']>0, np.nan)
    pre['AMT_APPLICATION'] = pre['AMT_APPLICATION'].where(pre['AMT_APPLICATION']>0, np.nan)
    pre['CNT_PAYMENT'] = pre['CNT_PAYMENT'].where(pre['CNT_PAYMENT']>0, np.nan)
    pre['AMT_DOWN_PAYMENT'] = pre['AMT_DOWN_PAYMENT'].where(pre['AMT_DOWN_PAYMENT']>0, np.nan)
    pre['RATE_DOWN_PAYMENT'] = pre['RATE_DOWN_PAYMENT'].where(pre['RATE_DOWN_PAYMENT']>0, np.nan)

    pre['DAYS_FIRST_DRAWING']        = pre['DAYS_FIRST_DRAWING'].where(pre['DAYS_FIRST_DRAWING'] <100000, np.nan)
    pre['DAYS_FIRST_DUE']            = pre['DAYS_FIRST_DUE'].where(pre['DAYS_FIRST_DUE']         <100000, np.nan)
    pre['DAYS_LAST_DUE_1ST_VERSION'] = pre['DAYS_LAST_DUE_1ST_VERSION'].where(pre['DAYS_LAST_DUE_1ST_VERSION'] <100000, np.nan)
    pre['DAYS_LAST_DUE']             = pre['DAYS_LAST_DUE'].where(pre['DAYS_LAST_DUE']           <100000, np.nan)
    pre['DAYS_TERMINATION']          = pre['DAYS_TERMINATION'].where(pre['DAYS_TERMINATION']     <100000, np.nan)
    #  pre['SELLERPLACE_AREA']          = pre['SELLERPLACE_AREA'].where(pre['SELLERPLACE_AREA']     <200, 200)

    ignore_list = ['SK_ID_CURR', 'SK_ID_PREV', 'NAME_CONTRACT_TYPE', 'NAME_CONTRACT_STATUS']
    ' revo '
    ' RevolvingではCNT_PAYMENT, AMT系をNULLにする '
    #  for col in pre.columns:
    #      if col in ignore_list:
    #          logger.info(f'CONTINUE: {col}')
    #          continue
    #      pre[f'revo_{col}'] = pre[col].where(pre[f'NAME_CONTRACT_TYPE']==revo, np.nan)
    #      pre[col] = pre[col].where(pre[f'NAME_CONTRACT_TYPE']!=revo, np.nan)

    pre['NAME_TYPE_SUITE'].fillna('XNA', inplace=True)
    pre['PRODUCT_COMBINATION'].fillna('XNA', inplace=True)

    pre = utils.to_df_pkl(df=pre, path='../input', fname='clean_prev')


def clean_pos(pos):
    logger.info(f'''
    #==============================================================================
    # PREV CLEANSING
    #==============================================================================''')

    pos = pos.query("NAME_CONTRACT_STATUS!='Signed' and NAME_CONTRACT_STATUS!='Approved' and NAME_CONTRACT_STATUS!='XNA'")
    pos.loc[(pos.NAME_CONTRACT_STATUS=='Completed') & (pos.CNT_INSTALMENT_FUTURE!=0), 'NAME_CONTRACT_STATUS'] = 'Active'

    pos_0 = pos.query('CNT_INSTALMENT_FUTURE==0')
    pos_1 = pos.query('CNT_INSTALMENT_FUTURE>0')
    pos_0['NAME_CONTRACT_STATUS'] = 'Completed'
    pos_0.sort_values(by=['SK_ID_PREV', 'MONTHS_BALANCE'], ascending=[True, False], inplace=True)
    pos_0.drop_duplicates('SK_ID_PREV', keep='last', inplace=True)
    pos = pd.concat([pos_0, pos_1], ignore_index=True)
    del pos_0, pos_1
    gc.collect()

    utils.to_df_pkl(df=pos, path='../input', fname='clean_pos')


def clean_ins(ins):

    # なぜ0なのかよくわからないし290行しかないので抜いてしまう
    ins = ins.query("AMT_INSTALMENT>0")

    utils.to_df_pkl(df=ins, path='../input', fname='clean_install')


def clean_ccb(ccb):

    amt_cols = [col for col in ccb.columns if col.count('AMT')]
    cnt_cols = [col for col in ccb.columns if col.count('CNT')]
    amt_cnt_cols = list(set(amt_cols+cnt_cols))
    for col in amt_cnt_cols:
        ccb[col].fillna(0, inplace=True)

    utils.to_df_pkl(df=ccb, path='../input', fname='clean_ccb')


if __name__=="__main__":

    #  with utils.timer("To Pickle"):
    #      to_pkl()

    with utils.timer("Cleansing"):

        #  app = utils.read_df_pkl(path='../input/application_train_test*.p')
        #  clean_app(app)
        #  del app
        #  gc.collect()

        bur = utils.read_df_pkl(path='../input/bureau*.p')
        clean_bureau(bur)
        del bur
        gc.collect()

        #  pre = utils.read_df_pkl(path='../input/prev*.p')
        #  clean_prev(pre)
        #  del pre
        #  gc.collect()
        #  pos = utils.read_df_pkl(path='../input/POS*.p')
        #  clean_pos(pos)
        #  del pos
        #  gc.collect()
        #  ins = utils.read_df_pkl(path='../input/install*.p')
        #  clean_ins(ins)
        #  del ins
        #  gc.collect()
        #  ccb = utils.read_df_pkl(path='../input/credit*.p')
        #  clean_ccb(ccb)
        #  del ccb
        #  gc.collect()
