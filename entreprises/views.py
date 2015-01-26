from django.shortcuts import render
from django.shortcuts import render_to_response
from django.forms import ModelForm
from django import forms
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import HttpResponse

from django.http import Http404
from pygeocoder import Geocoder
import os

from entreprises.models import Entreprise
from entreprises.models import AjoutForm
from entreprises.models import ModifForm
from entreprises.models import EntrepriseAjoutForm

def accueil(request):
    entreprise_list=Entreprise.objects.all().order_by('nom')
    paginator = Paginator(entreprise_list, 15)
    
    page = request.GET.get('page')
    try:
        entreprises = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entreprises = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entreprises = paginator.page(paginator.num_pages)

    return render_to_response('entreprises/index.html',{'entreprises':entreprises})


def detailEntreprise(request, entreprise_id=None):
	if (id==None):
		return HttpResponseRedirect('/entreprises')
	else:
		detailEntreprise = Entreprise.objects.get(pk=entreprise_id)
		return render(request, "entreprises/detailsEntreprises.html", {'detailEntreprise': detailEntreprise})
	
def ajouterEntreprise(request):
    entrepriseform=EntrepriseAjoutForm() 
    con={'entrepriseform': entrepriseform}
    con.update(csrf(request))
    if len(request.POST)>0:
        entrepriseform=EntrepriseAjoutForm(request.POST) #si on est en post== reponse au form
        con={'entrepriseform': entrepriseform}
        if entrepriseform.is_valid():
            entreprise=entrepriseform.save(commit=False)
            con.update(csrf(request))
            entreprise.save()
            ok="La nouvelle entreprise a bien ete enregistree."
            return render(request, "entreprises/success.html", {
            "message":ok,                                                                                                                        
            })
            #return render_to_response('entreprises/success.html')
        else:
            ko="Votre saisie comporte des erreurs. Tous les champs sont obligatoires."
            return render(request, "entreprises/erreur.html", {
            "message":ko,                                                                                                                       
            })
            #return render_to_response('entreprises/erreur.html')
    else:
        #on est pas en post donc pr�sentation pour la premire fois du form
        return render_to_response('entreprises/ajouterEntreprise.html', con, context_instance=RequestContext(request))
    
def delete(request, entreprise_id=None):
    if (entreprise_id==None):
         return HttpResponseRedirect('/entreprises')
    else:            
        entreprise = Entreprise.objects.get(pk=entreprise_id)
        ok="L'entreprise a bien été supprimée."
        entreprise.delete()
        return render(request, "entreprises/success.html", {
        "message":ok,
        })
            #return render_to_response('entreprises/success.html')
            
def modifierEntreprise(request, entreprise_id=None):
    detailEntreprise = Entreprise.objects.get(pk=entreprise_id) 
    form = ModifForm(instance = detailEntreprise)
    con ={'form': form}
    con.update(csrf(request))
    if len(request.POST) > 0:
        form =ModifForm( request.POST , instance = detailEntreprise )
        if form.is_valid():
            modification=form.save(commit=False)
            con.update(csrf(request))
            modification.save()
            ok="Les données de l'entreprise ont bien été mise à jour."
            return render(request, "entreprises/success.html", {
            "message":ok,                                                                                                                        
            })
            #return HttpResponseRedirect("/entreprises") #Nous renvoie la si le formulaire est juste    
        else:
            return render(request, "entreprises/modifierEntreprise.html", {'detailEntreprise': detailEntreprise})
    else:
        return render(request, "entreprises/modifierEntreprise.html", {'detailEntreprise': detailEntreprise})

def geoloc(request, entreprise_id=None):
    geocoder=Geocoder()
    try:
        proxy=os.environ['http_proxy']
        geocoder.set_proxy(proxy)
    except KeyError:
        pass
    entreprise = Entreprise.objects.get(pk=entreprise_id)
    adresseComplete = entreprise.adresse_propre+","+entreprise.ville_propre

    try:
        if geocoder.geocode(adresseComplete).valid_address :
            resultat = geocoder.geocode(adresseComplete)
            entreprise.latitude=resultat[0].coordinates[0]
            entreprise.longitude=resultat[0].coordinates[1]
            message = "adresse : "+str(resultat[0].coordinates)
            entreprise.save()
        else:
            message = "adresse non valide"
    except Exception as inst:
        message=inst.args
        
    return render(request, "templates/maps.html")
