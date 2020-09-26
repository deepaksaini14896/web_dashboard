from django.shortcuts import render
import pandas as pd

# Create your views here.
def index(request):
	dataconfirm=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
	
	totalcases=dataconfirm[dataconfirm.columns[-1]].sum()
	lastupdate=dataconfirm.columns[-1]
	
	datadeath=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

	totaldeath=datadeath[datadeath.columns[-1]].sum()

	datarecover=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
	
	totalrecover=datarecover[datarecover.columns[-1]].sum()


	barplotdata=dataconfirm[['Country/Region',dataconfirm.columns[-1]]].groupby('Country/Region').sum()
	barplotdata=barplotdata.reset_index()
	barplotdata.columns=['Country/Region','Values']
	barplotdata=barplotdata.sort_values(by='Values',ascending=False)
	barcountry=barplotdata[['Country/Region','Values']].values.tolist()
	
	df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

	dataformap=[]
	tempo=[]
	for i,j in barcountry:
		try:
			tempdf3=df3[df3['name']==i].values.tolist()
			temp={}
			temp['code3']=df3[df3['name']==i].values.tolist()[0][0]
			temp['name']=df3[df3['name']==i].values.tolist()[0][1]
			temp['value']=j
			temp['code']=df3[df3['name']==i].values.tolist()[0][3]
			dataformap.append(temp)
		except:
			tempo.append(i)
			pass
	context={'totalcases':totalcases,
			 'lastupdate':lastupdate,
			 'totaldeath':totaldeath,
			 'totalrecover':totalrecover,
			 'barcountry':barcountry,
			 'maxrange':barcountry[0][1], #To check range for heat map
			 'dataformap':dataformap
			 }
	return render(request,'index.html',context)

def detail(request):
	countryname=request.POST['countryname']

	dataconfirm=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
	
	datarecover=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

	datadeath=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
	
	dates=list(dataconfirm.columns)
	dates=dates[4:]
	dates_len=len(dates)

	#data from total cases
	dates_data_cases=dataconfirm.loc[dataconfirm['Country/Region'] == countryname]
	dates_data_cases=list(dates_data_cases.iloc[0,4:])

	#data from total recoveres
	dates_data_recoveres=datarecover.loc[datarecover['Country/Region'] == countryname]
	dates_data_recoveres=list(dates_data_recoveres.iloc[0,4:])

	#data from total deaths
	dates_data_deaths=datadeath.loc[datadeath['Country/Region'] == countryname]
	dates_data_deaths=list(dates_data_deaths.iloc[0,4:])

	index=[]

	for i in range(0,dates_len,int(dates_len/10)):
		index.append(i)
	index[-1]=index[-1]+(dates_len-(int(dates_len/10)*10))-1

	labels=[]
	data_cases=[]
	data_recoveres=[]
	data_deaths=[]

	for i in index:
		labels.append(dates[i])
		data_cases.append(dates_data_cases[i])
		data_recoveres.append(dates_data_recoveres[i])
		data_deaths.append(dates_data_deaths[i])

	context={
		'countryname':countryname,
		'labels':labels,
		'data_cases':data_cases,
		'data_recoveres':data_recoveres,
		'data_deaths':data_deaths
	}

	return render(request,'countrydetails.html',context)