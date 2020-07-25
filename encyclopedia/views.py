from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django import forms


from . import util

import markdown2
import codecs
import sys
import random

# class NewPage(forms.Form):
#     title=forms.CharField(label="Title")



def index(request):
    if request.method=="POST":
        temp = request.POST.get('q','')
        searchResult = util.get_entry(temp)
    
        if searchResult==None:
            entries= util.list_entries()
            resultList=[en for en in entries if temp.lower() in en.lower()]
            # resultList=list(filter(lambda text : all([word in text for word in temp]),entries ))
            return render(request,"encyclopedia/searchResult.html",{
                "entries":resultList,
                "substring":temp
            })

        else:
            entry=mark_safe(markdown2.markdown(searchResult))
            return render(request, "encyclopedia/entry.html",{
                    "b":True,
                    "entry": entry,
                    "title": temp
                })
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })




def entry(request,entryTitle):
    temp = util.get_entry(entryTitle)
    
    if temp==None:
        return render(request, "encyclopedia/entry.html",{
        "b":False,
    })
    else:
        entry=mark_safe(markdown2.markdown(temp))
        return render(request, "encyclopedia/entry.html",{
                "b":True,
                "entry": entry,
                "title":entryTitle
            })



def add(request):

    if request.method=="POST":
        title = request.POST.get('title','')
        content = request.POST.get('content','')

        if title=='' or content=='':
            return render(request,"encyclopedia/add.html",{
                "noTitleroContent":True
            })

        entries= util.list_entries()
        # entries = [e.lower() for e in entries]
        if title in entries:
            return render(request,"encyclopedia/add.html",{
                "exists":True
            })
        else:
            util.save_entry(title,content)
            temp = mark_safe(markdown2.markdown(util.get_entry(title)))
            return render(request,"encyclopedia/entry.html",{
                "b":True,
                "entry": temp,
                "title":title
            })
        
    else:    
        return render(request,"encyclopedia/add.html")


def edit(request,title):
    if request.method=="POST":
        content = request.POST.get('content','')

        util.save_entry(title,content)
        temp = mark_safe(markdown2.markdown(util.get_entry(title)))

        return render(request,"encyclopedia/entry.html",{
            "b":True,
            "entry": temp,
            "title":title
        })

    else:
        temp = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "b":True,
            "entry":temp,
            "title":title
        })

def randomEntry(request):
    entries= util.list_entries()
    return redirect('entry',entryTitle=random.choice(entries))