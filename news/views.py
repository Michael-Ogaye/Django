from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import datetime as dt
from .models import Article
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  MoringaMerch
from .serializer import MerchSerializer
from rest_framework import status

# Create your views here.
def welcome(request):
    return render(request, 'all-news/welcome.html')







def convert_dates(dates):

    # Function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',"Sunday"]

    # Returning the actual day of the week
    day = days[day_number]
    return day

#..........
def news_of_day(request):
    date = dt.date.today()

    news = Article.todays_news()

    
            
    return render(request, 'all-news/today-news.html', {"date": date,"news":news})


def past_days_news(request,past_date):
        try:
        # Converts data from the string Url
         date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
        # Raise 404 error when ValueError is thrown
                raise Http404()
                assert False
                

        if date == dt.date.today():
          return redirect(news_of_day)
        news = Article.days_news(date)
        return render(request, 'all-news/past-news.html', {"date": date,"news":news})






def search_results(request):

            if 'article' in request.GET and request.GET["article"]:
                search_term = request.GET.get("article")
                searched_articles = Article.search_by_title(search_term)
                message = f"{search_term}"

                return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

            else:
                message = "You haven't searched for any term"


                return render(request, 'all-news/search.html',{"message":message})

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except :
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})




class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        form = MerchSerializer(data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)





    