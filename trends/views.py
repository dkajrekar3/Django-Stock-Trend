from django.shortcuts import render
import yfinance
from datetime import datetime, timedelta
from django.http import HttpResponse
import plotly.express as px

# Create your views here.
def home(request):
    if request.method =='POST':
        symbol=request.POST.get('symbol')
        
        monthend=datetime.now()
        monthstart=monthend-timedelta(days=30)

        #collecting data from Yahoo Finance API

        data = yfinance.download(symbol, start = monthstart,end = monthend)

        if data.empty:
            return HttpResponse('Enter Valid Name')

        #Preparing Data

        monthdata={
            'open':list(data.Open),
            'close':list(data.Close),
            'high':list(data.High),
            'low':list(data.Low),
            'date':list(data.index.strftime('%y-%m-%d'))
        }

        #preparing Charts

        hlfig=px.line(
            x=monthdata['date'],
            y=[monthdata['high'],monthdata['low']],
            title= symbol + ' Monthly Chart(High/low Prize)',
            labels={'x':'Date','y':'prize'},
        )
        hlchart=hlfig.to_html()

        ocfig=px.line(
            x=monthdata['date'],
            y=[monthdata['open'],monthdata['close']],
            title= symbol + ' Monthly Chart(Open/close Prize)',
            labels={'x':'Date','y':'prize'},
        )
        occhart=ocfig.to_html()
    
        #sending data to templates
        context={
            'symbol':symbol,
            'hlchart':hlchart,
            'occhart':occhart
        }

        return render(request,'trends/result.html',context)
    return render(request,'trends/home.html')