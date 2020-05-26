# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:51:06 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
ref:https://medium.com/open-machine-learning-course/open-machine-learning-course-topic-9-time-series-analysis-in-python-a270cb05e0b3
    https://blog.csdn.net/jh1137921986/article/details/90257764
    https://www.cnblogs.com/tianqizhi/p/9277376.html
"""
#time series analysis
import os,itertools,math
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import statsmodels.tsa.api as smt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA

from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error
def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
from sklearn.model_selection import TimeSeriesSplit # you have everything done for you
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from matplotlib.pylab import style

style.use('ggplot')   
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

tscv = TimeSeriesSplit(n_splits=5)
def timeseries_train_test_split(X, y, test_size):
    """
        Perform train-test split with respect to time series structure
    """
    
    # get the index after which test set starts
    test_index = int(len(X)*(1-test_size))
    
    X_train = X.iloc[:test_index]
    y_train = y.iloc[:test_index]
    X_test = X.iloc[test_index:]
    y_test = y.iloc[test_index:]
    
    return X_train, X_test, y_train, y_test

def plotModelResults(model, X_train, X_test,y_train,y_test, plot_intervals=False, plot_anomalies=False, scale=1.96):
    """
        Plots modelled vs fact values, prediction intervals and anomalies
    
    """
    
    prediction = model.predict(X_test)
    
    plt.figure(figsize=(15, 7))
    plt.plot(prediction, "g", label="prediction", linewidth=2.0)
    plt.plot(y_test.values, label="actual", linewidth=2.0)
    
    if plot_intervals:
        cv = cross_val_score(model, X_train, y_train, 
                                    cv=tscv, 
                                    scoring="neg_mean_squared_error")
        #mae = cv.mean() * (-1)
        deviation = np.sqrt(cv.std())
        
        lower = prediction - (scale * deviation)
        upper = prediction + (scale * deviation)
        
        plt.plot(lower, "r--", label="upper bond / lower bond", alpha=0.5)
        plt.plot(upper, "r--", alpha=0.5)
        
        if plot_anomalies:
            anomalies = np.array([np.NaN]*len(y_test))
            anomalies[y_test<lower] = y_test[y_test<lower]
            anomalies[y_test>upper] = y_test[y_test>upper]
            plt.plot(anomalies, "o", markersize=10, label = "Anomalies")
    
    error = mean_absolute_percentage_error(prediction, y_test)
    plt.title("Mean absolute percentage error {0:.2f}%".format(error))
    plt.legend(loc="best")
    plt.tight_layout()
    plt.grid(True);
    
def plotCoefficients(model,X_train):
    """
        Plots sorted coefficient values of the model
    """
    
    coefs = pd.DataFrame(model.coef_, X_train.columns)
    coefs.columns = ["coef"]
    coefs["abs"] = coefs.coef.apply(np.abs)
    coefs = coefs.sort_values(by="abs", ascending=False).drop(["abs"], axis=1)
    
    plt.figure(figsize=(15, 7))
    coefs.coef.plot(kind='bar')
    plt.grid(True, axis='y')
    plt.hlines(y=0, xmin=0, xmax=len(coefs), linestyles='dashed'); 
 
 
def timeSeriesAnalysis(SpatioTemporalData):
    spatioTempData=pd.read_csv(SpatioTemporalData)
    # print(spatioTempData.columns)
    '''
    Index(['Date', 'Cases - Total', 'Deaths - Total',
       'Cases - Age 0-17','Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 
       'Cases - Female','Cases - Male', 'Cases - Unknown Gender',
       'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx','Cases - Unknown Race/Ethnicity', 
       'Deaths - Age 0-17','Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49','Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79','Deaths - Age 80+', 'Deaths - Age Unknown', 
       'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 
       'Deaths - Latinx','Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx','Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity'],
       dtype='object')
    '''
    #01-plot data
    plt.figure(figsize=(15, 7))
    plt.plot(spatioTempData['Cases - Total'])
    plt.title('Cases - Total (daily data)')
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(15, 7))
    plt.plot(spatioTempData["Deaths - Total"])
    plt.title('Deaths - Total (daily data)')
    plt.grid(True)
    plt.show()
    
    
    dataDF=spatioTempData[['Date','Cases - Total',"Deaths - Total"]].rename(columns={'Cases - Total':"casesT","Deaths - Total":"deathsT"})
    dataDF.dropna(inplace=True)    
    dataDF_ts=dataDF.set_index('Date').sort_index()
    dataDF_ts.index=pd.to_datetime(dataDF_ts.index) #to DatatimeIndex format
    print("is null:",dataDF.isnull().sum())
    print(dataDF_ts[:10].index)
    
    timeSeries=dataDF_ts.casesT
    #A-Move, smoothe, evaluate
    #01-moving average
    def moving_average(series, n):
        '''
        Calculate average of last n observations
        '''
        return np.average(series[-n:])
    
    MA=moving_average(timeSeries, 7) 
    print("casesT moving_average:",MA)

    def plotMovingAverage(series, window, plot_intervals=False, scale=1.96, plot_anomalies=False):
    
        """
            series - dataframe with timeseries
            window - rolling window size 
            plot_intervals - show confidence intervals
            plot_anomalies - show anomalies 
        """
        rolling_mean = series.rolling(window=window).mean()
    
        plt.figure(figsize=(15,5))
        plt.title("Moving average\n window size = {}".format(window))
        plt.plot(rolling_mean, "g", label="Rolling mean trend")
    
        # Plot confidence intervals for smoothed values
        if plot_intervals:
            mae = mean_absolute_error(series[window:], rolling_mean[window:])
            deviation = np.std(series[window:] - rolling_mean[window:])
            lower_bond = rolling_mean - (mae + scale * deviation)
            upper_bond = rolling_mean + (mae + scale * deviation)
            plt.plot(upper_bond, "r--", label="Upper Bond / Lower Bond")
            plt.plot(lower_bond, "r--")
            
            # Having the intervals, find abnormal values
            if plot_anomalies:
                anomalies = pd.DataFrame(index=series.index, columns=series.to_frame().columns)
                anomalies[series<lower_bond] = series[series<lower_bond]
                anomalies[series>upper_bond] = series[series>upper_bond]
                plt.plot(anomalies, "ro", markersize=10)
            
        plt.plot(series[window:], label="Actual values")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.xticks(rotation='vertical')
    
    plotMovingAverage(timeSeries, 3)
    plotMovingAverage(timeSeries, 7)
    plotMovingAverage(timeSeries, 14)
    
    #plot confidence intervals  anomaly detection system
    plotMovingAverage(timeSeries, 4, plot_intervals=True)
    #test the values abnormal !the function is not perfect enough. it will not catch each period peaks as an anomaly
    ts_anomaly=timeSeries.copy()
    ts_anomaly.iloc[-20] = ts_anomaly.iloc[-20] * 0.2 # say we have 80% drop of ads 
    plotMovingAverage(ts_anomaly, 4, plot_intervals=True, plot_anomalies=True)

    ts_rolling=timeSeries.rolling(window=15)
    plt.figure()
    ts_rolling.mean().plot(title="ts_mean_rolling")


    #02-Weighted average    
    def weighted_average(series, weights):
        """
            Calculate weighter average on series
        """
        result = 0.0
        weights.reverse()
        for n in range(len(weights)):
            result += series.iloc[-n-1] * weights[n]
        return float(result)
  
    WA=weighted_average(timeSeries, [0.6, 0.3, 0.1])
    print("Weighted average:",WA)
    
    #B-Exponential smoothing
    #03-exponential smoothing
    def exponential_smoothing(series, alpha):
        """
            series - dataset with timestamps
            alpha - float [0.0, 1.0], smoothing parameter
        """
        result = [series[0]] # first value is same as series
        for n in range(1, len(series)):
            result.append(alpha * series[n] + (1 - alpha) * result[n-1])
        return result
    
    def plotExponentialSmoothing(series, alphas):
        """
            Plots exponential smoothing with different alphas
            
            series - dataset with timestamps
            alphas - list of floats, smoothing parameters
            
        """
        with plt.style.context('seaborn-white'):    
            plt.figure(figsize=(15, 7))
            for alpha in alphas:
                plt.plot(exponential_smoothing(series, alpha), label="Alpha {}".format(alpha))
            plt.plot(series.values, "c", label = "Actual")
            plt.legend(loc="best")
            plt.axis('tight')
            plt.title("Exponential Smoothing")
            plt.grid(True);
    
    plotExponentialSmoothing(timeSeries, [0.3, 0.05])

    #04-double exponential smoothing
    def double_exponential_smoothing(series, alpha, beta):
        """
            series - dataset with timeseries
            alpha - float [0.0, 1.0], smoothing parameter for level
            beta - float [0.0, 1.0], smoothing parameter for trend
        """
        # first value is same as series
        result = [series[0]]
        for n in range(1, len(series)+1):
            if n == 1:
                level, trend = series[0], series[1] - series[0]
            if n >= len(series): # forecasting
                value = result[-1]
            else:
                value = series[n]
            last_level, level = level, alpha*value + (1-alpha)*(level+trend)
            trend = beta*(level-last_level) + (1-beta)*trend
            result.append(level+trend)
        return result

    def plotDoubleExponentialSmoothing(series, alphas, betas):
        """
            Plots double exponential smoothing with different alphas and betas
            
            series - dataset with timestamps
            alphas - list of floats, smoothing parameters for level
            betas - list of floats, smoothing parameters for trend
        """
        
        with plt.style.context('seaborn-white'):    
            plt.figure(figsize=(20, 8))
            for alpha in alphas:
                for beta in betas:
                    plt.plot(double_exponential_smoothing(series, alpha, beta), label="Alpha {}, beta {}".format(alpha, beta))
            plt.plot(series.values, label = "Actual")
            plt.legend(loc="best")
            plt.axis('tight')
            plt.title("Double Exponential Smoothing")
            plt.grid(True)
            
    plotDoubleExponentialSmoothing(timeSeries, alphas=[0.9, 0.02], betas=[0.9, 0.02])
    
    #05-Triple exponential smoothing  -seasonality  / This means we should’t use the method if our time series do not have seasonality
    #skiped code ref:Open Machine Learning Course. Topic 9. Part 1. Time series analysis in Python  https://medium.com/open-machine-learning-course/open-machine-learning-course-topic-9-time-series-analysis-in-python-a270cb05e0b3
   
    #C-ARIMA 差分自回归移动平均模型 autoregression integrated moving average model;自回归移动平均模型(ARMA(p，q)) AR代表p阶自回归过程，MA代表q阶移动平均过程
    #06-Time series cross validation- skiped same as above
    #07-Getting rid of non-stationarity and building SARIMA -skiped same as above
    
    #D-Linear (and not quite) models on time series  /ARIMA
    #Feature exctraction
    #08-Lags of time series
    data=timeSeries.copy().to_frame()
    data.columns=["y"]
    # Adding the lag of the target variable from 6 steps back up to 24
    for i in range(3, 10):
        data["lag_{}".format(i)] = data.y.shift(i)
     
    data.plot(subplots=True,figsize=(18, 12))   
     
    y = data.dropna().y
    X = data.dropna().drop(['y'], axis=1)
    
    # reserve 30% of data for testing
    X_train, X_test, y_train, y_test = timeseries_train_test_split(X, y, test_size=0.3)
    
    # machine learning in two lines
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    
    plotModelResults(lr, X_train, X_test,y_train,y_test,plot_intervals=True)
    plotCoefficients(lr,X_train)    
     
    
    #ref:https://www.cnblogs.com/tianqizhi/p/9277376.html
    #09-diff
    ts_diff=timeSeries.diff(1) #DataFrame.diff(self, periods=1, axis=0) → 'DataFrame'
    ts_diff.plot(title="1-g diff")
    
    #10-ACF(autocorrelation funcion)自相关函数； PACF（partial autocorrelation function）偏自相关函数
    fig = plt.figure(figsize=(12,8))
    #acf
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(timeSeries, lags=20,ax=ax1)
    ax1.xaxis.set_ticks_position('bottom')
    fig.tight_layout();
    #pacf
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(timeSeries, lags=20, ax=ax2)
    ax2.xaxis.set_ticks_position('bottom')
    fig.tight_layout();
    #图中的阴影表示置信区间，可以看出不同阶数自相关性的变化情况，从而选出p值和q值
     
    #11-scatter plot
    lags=9
    ncols=3
    nrows=int(np.ceil(lags/ncols))
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(4*ncols, 4*nrows))
    for ax, lag in zip(axes.flat, np.arange(1,lags+1, 1)):
        lag_str = 't-{}'.format(lag)
        X = (pd.concat([timeSeries, timeSeries.shift(-lag)], axis=1,
                       keys=['y'] + [lag_str]).dropna())
     
        X.plot(ax=ax, kind='scatter', y='y', x=lag_str);
        corr = X.corr().as_matrix()[0][1]
        ax.set_ylabel('Original')
        ax.set_title('Lag: {} (corr={:.2f})'.format(lag_str, corr));
        ax.set_aspect('equal');
        # sns.despine();
        # print(X)
        break
    fig.tight_layout();

    #12-template
    def tsplot(y, lags=None, title='', figsize=(14, 8)):
        
        fig = plt.figure(figsize=figsize)
        layout = (2, 2)
        ts_ax   = plt.subplot2grid(layout, (0, 0))
        hist_ax = plt.subplot2grid(layout, (0, 1))
        acf_ax  = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
         
        y.plot(ax=ts_ax)
        ts_ax.set_title(title)
        y.plot(ax=hist_ax, kind='hist', bins=25)
        hist_ax.set_title('Histogram')
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
        [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
        sns.despine()
        plt.tight_layout()
        return ts_ax, acf_ax, pacf_ax    
    tsplot(timeSeries, title='daily cases of Covid-19', lags=36)
    
    #13-model estimation:ARIMA 差分自回归移动平均模型    
    ts_df= timeSeries
    n_sample = ts_df.shape[0]
    n_train=int(0.80*n_sample)+1
    n_forecast=n_sample-n_train
    ts_train = ts_df.iloc[:n_train]
    ts_test = ts_df.iloc[n_train:]
    print(ts_train.shape)
    print(ts_test.shape)
        
    # Fit the model
    arima200 = sm.tsa.SARIMAX(ts_train, order=(1,0,0))#order里边的三个参数p,d,q
    model_results = arima200.fit()#fit模型    

    #当多组值都不符合时，遍历多组值，得出最好的值
    p_min = 0
    d_min = 0
    q_min = 0
    p_max = 4
    d_max = 0
    q_max = 4
     
    # Initialize a DataFrame to store the results
    results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                               columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])
     
    for p,d,q in itertools.product(range(p_min,p_max+1),
                                   range(d_min,d_max+1),
                                   range(q_min,q_max+1)):
        if p==0 and d==0 and q==0:
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
            continue
         
        try:
            model = sm.tsa.SARIMAX(ts_train, order=(p, d, q),
                                   #enforce_stationarity=False,
                                   #enforce_invertibility=False,
                                  )
            results = model.fit()
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
        except:
            continue
    results_bic = results_bic[results_bic.columns].astype(float)        
            
    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.heatmap(results_bic,
                     mask=results_bic.isnull(),
                     ax=ax,
                     annot=True,
                     fmt='.2f',
                     );
    ax.set_title('BIC')        
                
    #模型评估标准：AIC/BIC两个指标，均值越低越好 AIC(akaike information criterion) BIC(bayesian information criterion)
    # Alternative model selection method, limited to only searching AR and MA parameters
    train_results = sm.tsa.arma_order_select_ic(ts_train, ic=['aic', 'bic'], trend='nc', max_ar=4, max_ma=4)
    print('AIC', train_results.aic_min_order)
    print('BIC', train_results.bic_min_order)   
    
    #14-模型残差检验
    #残差分析 正态分布 QQ图线性 /Q-Q图：越像直线，则是正态分布；越不是直线，离正态分布越远。
    model_results.plot_diagnostics(figsize=(16, 12));#statsmodels库    
    '''
    时间序列建模基本步骤：
    1-获取被观测系统时间序列数据；
    2-对数据绘图，观测是否为平稳时间序列；对于非平稳时间序列要先进行d阶差分运算，化为平稳时间序列；
    3-经过第二步处理，已经得到平稳时间序列。要对平稳时间序列分别求得其自相关系数ACF 和偏自相关系数PACF ，通过对自相关图和偏自相关图的分析，得到最佳的阶层 p 和阶数 q
    4-由以上得到的 ，得到ARIMA模型。然后开始对得到的模型进行模型检验
    '''
    
    # E-ARIMA_statsmodels.tsa.arima_model
    timeSeries_df=timeSeries.to_frame()
    timeSeries_df.plot(figsize=(12,8))
    plt.legend(bbox_to_anchor=(1.25, 0.5))
    plt.title("daily cases")
    sns.despine()
        
    timeSeries_diff = timeSeries_df.diff(1)
    timeSeries_diff = timeSeries_diff.dropna()
     
    plt.figure()
    plt.plot(timeSeries_diff)
    plt.title('一阶差分')
    plt.show()
    
    acf = plot_acf(timeSeries_diff, lags=20)
    plt.title("ACF")
    acf.show()
    
    pacf = plot_pacf(timeSeries_diff, lags=20)
    plt.title("PACF")
    pacf.show()    
        
    timeSeries_resample=timeSeries.resample("1D").mean()    
    sampleSplit=math.ceil(timeSeries_resample.shape[0]*0.7)
    ARIMA_model = ARIMA(timeSeries_resample[:sampleSplit], order=(1, 1, 1),freq='1D')    
    result = model.fit()
    pred = result.predict(start=pd.to_datetime('2020-04-05'), end=pd.to_datetime('2020-04-10'),dynamic=True, typ='levels')#预测，指定起始与终止时间。预测值起始时间必须在原始数据中，终止时间不需要
    print(pred)
    result.forecast(1)
    result.forecast(n_periods=10)
    print("^"*50)
    print(result.forecast(n_periods=10))
    
    pred = results.get_prediction(start=pd.to_datetime('2020-04-05'), end=pd.to_datetime('2020-04-20'), dynamic=False)
    pred_ci = pred.conf_int()
    plt.figure()
    ax=timeSeries_resample.plot(label='observed')    
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('daily cases')    
    plt.show()
    print(timeSeries_resample[:sampleSplit].index)
            
    #F-tfresh /over 1200 features  https://tsfresh.readthedocs.io/en/latest/ 
    #15-skiped apart from just gave one feature as an example
    '''
    tsfresh is a python package. It automatically calculates a large number of time series characteristics, the so called features. Further the package contains methods to evaluate the explaining power and importance of such characteristics for regression or classification tasks.
    '''
    from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
    from tsfresh import extract_features, extract_relevant_features, select_features
    from tsfresh.utilities.dataframe_functions import impute
    from tsfresh.feature_extraction import ComprehensiveFCParameters
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    import tsfresh
    # extraction_settings = ComprehensiveFCParameters()#提取特征
    # X = extract_features(timeSeries_resample.to_frame(),
    #                  column_id='id', column_sort='time',#以id为聚合，以time排序
    #                  default_fc_parameters=extraction_settings,
    #                  impute_function= impute)
    tsfresh_absSumChanges=tsfresh.feature_extraction.feature_calculators.absolute_sum_of_changes(timeSeries)
    print(tsfresh_absSumChanges)
    

if __name__=="__main__": 
    dataRoot=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data"
    dataFpDic={
            "Covid-19_dailyCases":os.path.join(dataRoot,r"COVID-19_Daily_Cases_and_Deaths.csv"),
         }

    '''E-Time Series Analysis'''
    #ref https://medium.com/open-machine-learning-course/open-machine-learning-course-topic-9-time-series-analysis-in-python-a270cb05e0b3  /translation: https://blog.csdn.net/jh1137921986/article/details/90257764
    # 18-ts feature, plot, stationarity,
    timeSeriesAnalysis(dataFpDic["Covid-19_dailyCases"])
    