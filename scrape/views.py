from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Review, Tour
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import time
import csv
import datetime
import pandas as pd
import urllib.parse


@login_required
def home(request):
    params = {'url': '', 'stars': [], 'form': None, 'reviews': []}
    if request.method == 'POST':
        form = RequestForm(request.POST)
        params['url'] = request.POST['url']
        params['stars'] = request.POST.getlist('stars')
        params['form'] = form
        if form.is_valid():
            context = survey(params)
            return render(request, 'scrape/result.html', context)
    else:
        params['form'] = RequestForm()
    return render(request, 'scrape/home.html', params)


@login_required
def about(request):
    return render(request, 'scrape/about.html', {'title': 'test'})


def survey(params):
    tour = Tour()
    tour.url = params['url']
    url = params['url']
    if not url.endswith('/'):
        url += '/'
    url += 'reviews/page:{}/?'
    for star in params['stars']:
        url += 'rate={}&'.format(star)
    url += 'gwith=2&gwith=3&gwith=4&gwith=5&gwith=6&lang=2'
    i = 1
    titles = []
    authors = []
    post_dates = []
    contents = []
    rates = []
    with_whoms = []
    dates = []
    while True:
        time.sleep(1)
        bs = BS(urlopen(url.format(i)), 'html.parser')
        if i == 1:
            tour_name = bs.find('h2',{'id':'activityname'}).get_text()
            tour.title = tour_name
            tour.save()
        reviews = bs.findAll('div', {'class': 'review'})
        for review in reviews:
            title = review.find('h2').get_text().replace(' ', '').replace('\r', '\n')
            try:
                post_date = datetime.datetime.strptime(review.find('a').next_sibling.replace(', ', ''),
                                                       '%Y/%m/%d').date()
                author = review.find('a').get_text()
            except:
                post_date = datetime.datetime.strptime(review.find('h2').next_sibling.split(', ')[1], '%Y/%m/%d').date()
                author = review.find('h2').next_sibling.split(', ')[0].replace('\n投稿者: ', '')
            content = review.find('p', {'class': 'usercomment'}).get_text().replace('\r', '\n')
            ths = [item.get_text() for item in review.find('table', {'class': 'review_summary_table'}).findAll('th')]
            tds = [item.get_text() if not item.get_text() == '' else item.find('div')['class'][1].replace('icon_',
                                                                                                          '').replace(
                '_stars', '') for item in review.find('table', {'class': 'review_summary_table'}).findAll('td')]
            try:
                rate = int(tds[ths.index('評価:')])
            except:
                rate = 0
            try:
                with_whom = tds[ths.index('利用形態:')]
            except:
                with_whom = '記載なし'
            try:
                date = datetime.datetime.strptime(tds[ths.index('参加日:')], '%Y/%m/%d').date()
            except:
                date = '記載なし'
            titles.append(title)
            authors.append(author)
            post_dates.append(post_date)
            contents.append(content)
            rates.append(rate)
            with_whoms.append(with_whom)
            dates.append(date)
        nav = bs.find('div', {'class': 'page_navi'})
        try:
            if '次へ' in nav.get_text():
                i += 1
            else:
                break
        except:
            break
    for i in range(len(titles)):
        review = Review()
        review.tour = tour
        review.title = titles[i]
        review.author = authors[i]
        review.date_posted = post_dates[i]
        review.content = contents[i]
        review.star = rates[i]
        review.type = with_whoms[i]
        if dates[i] != '記載なし':
            review.tour_date = dates[i]
        review.save()
    df = pd.DataFrame({'title': titles,
                       'author': authors,
                       'date_posted': post_dates,
                       'content': contents,
                       'star': rates,
                       'with_whom': with_whoms,
                       'tour_date': dates})
    reviews = tour.review_set.all()
    context = {'reviews': reviews, 'tour': tour}
    return context


def download(request, survey_id):
    tour = get_object_or_404(Tour, pk=survey_id)
    reviews = tour.review_set.all()
    response = HttpResponse(content_type='text/csv')
    filename = '{}.csv'.format(tour.title)
    quoted_filename = urllib.parse.quote(filename)
    response['Content-Disposition'] = "attachment;  filename='{}'; filename*=UTF-8''{}".format(quoted_filename, quoted_filename)
    writer = csv.writer(response)
    header = ['タイトル', '投稿者', '投稿日', '投稿内容', '評価', '利用形態', '参加日']
    writer.writerow(header)
    for review in reviews:
        writer.writerow([
            review.title,
            review.author,
            review.date_posted,
            review.content,
            review.star,
            review.type,
            review.tour_date
        ])
    return response
