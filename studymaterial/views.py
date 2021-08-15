from django.shortcuts import render
from studymaterial.forms import DashboardFom
from youtubesearchpython import VideosSearch
import requests
import wikipedia

# Create your views here.
def youtube(request):
	if request.method =="POST":
		form=DashboardFom(request.POST)
		text=request.POST.get('text')
		vedio=VideosSearch(text,limit=12)
		result_list=[]
		for i in vedio.result()['result']:
			result_dict={
				'input':text,
				'title':i['title'],
				'duration':i['duration'],
				'thumbnail':i['thumbnails'][0]['url'],
				'channel':i['channel']['name'],
				'link':i['link'],
				'views':i['viewCount']['short'],
				'published':i['publishedTime']
			}
			desc=''
			if i['descriptionSnippet']:
				for j in i['descriptionSnippet']:
					desc +=j['text']
			result_dict['description']=desc
			result_list.append(result_dict)
			context={
				'form':form,
				'results':result_list
				}

		return render(request,'studymaterial/youtube.html',context)
	else:
		form=DashboardFom()
		context= {'form':form}
	return render(request,"studymaterial/youtube.html",context)
def books(request):
	if request.method =="POST":
		form=DashboardFom(request.POST)
		text=request.POST['text']
		url="https://www.googleapis.com/books/v1/volumes?q="+text
		r=requests.get(url)
		answer=r.json()
		result_list=[]
		for i in range(10):
			result_dict={
				'title':answer['items'][i]['volumeInfo']['title'],
				'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
				'description':answer['items'][i]['volumeInfo'].get('description'),
				'count':answer['items'][i]['volumeInfo'].get('pageCount'),
				'categories':answer['items'][i]['volumeInfo'].get('categories'),
				'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
				'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
				'preview':answer['items'][i]['volumeInfo'].get('previewLink')
			}
			result_list.append(result_dict)
			context={
				'form':form,
				'results':result_list
				}

		return render(request,'studymaterial/books.html',context)
	else:
		form=DashboardFom()
	context= {'form':form}
	return render(request,"studymaterial/books.html",context)

def dictionary(request):
	if request.method=="POST":
		form=DashboardFom(request.POST)
		text=request.POST['text']
		url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
		r=requests.get(url)
		answer=r.json()
		try:
			phonetics=answer[0]['phonetics'][0]['text']
			audio=answer[0]['phonetics'][0]['audio']
			definition=answer[0]['meanings'][0]['definitions'][0]['definition']
			example=answer[0]['meanings'][0]['definitions'][0]['example']
			synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
			context={
				'form':form,
				'input':text,
				'phonetics':phonetics,
				'audio':audio,
				'definition':definition,
				'example':example,
				'synonyms':synonyms
			}	
		except:
			context={
				'form':form,
				'input':''
				}
		return render(request,"studymaterial/dictionary.html",context)
	else:
		form=DashboardFom()
		context={'form':form}
	return render(request,"studymaterial/dictionary.html",context)

def wikipedias(request):
	if request.method =="POST":
		form=DashboardFom(request.POST)
		text=request.POST['text']
		search=wikipedia.page(text)
		context={
			'form':form,
			'title':search.title,
			'link':search.url,
			'details':search.summary
		}
		return render(request,"studymaterial/wikipedias.html",context)
	else:
		form=DashboardFom()
		context= {'form':form}
	return render(request,"studymaterial/wikipedias.html",context)

def joinmeeting(request):
	return render(request,"studymaterial/joinmeeting.html")

def googleform(request):
	return render(request,"studymaterial/googleform.html")
