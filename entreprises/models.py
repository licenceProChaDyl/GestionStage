from django.db import models
from django.forms import ModelForm
import re


RE_CEDEX = re.compile(r'(.*)\b\s*cedex.*$',re.IGNORECASE|re.MULTILINE)
def addslashes(s):
    return re.sub("(\\\\|'|\")", lambda o: "\\"+o.group(1),s)

class Entreprise(models.Model,):
    nom        = models.CharField(max_length=100)
    adresse    = models.CharField(max_length=250)
    codePostal = models.CharField(max_length= 10)
    ville      = models.CharField(max_length= 50)
    pays       = models.CharField(max_length= 30)
    telephone  = models.CharField(max_length= 20)
    latitude   = models.FloatField()
    longitude  = models.FloatField()

    def __str__(self):
        return self.nom

    @property
    def latlng(self):
        return [self.latitude,self.longitude]

    @latlng.setter
    def latlng(self, x):
        self.latitude, self.longitude = x

    @property
    def ville_propre(self):
        v = self.ville
        m = RE_CEDEX.match(v)
        if m:
            v = m.group(1)
        return v
    @property
    def nom_propre(self):
        n =  self.nom
        return addslashes(n)

    
    @property
    def adresse_propre(self):
        a=self.adresse
        m =  RE_BP.match(a)
        if m:
            a= m.group(1)
        return addslashes(a)

class Contact(models.Model):
    entreprise = models.ForeignKey(Entreprise, related_name="contacts")
    nom        = models.CharField(max_length=30)
    libelle    = models.CharField(max_length=30)
    email      = models.EmailField(null=True, blank=True)
    telephone  = models.CharField(max_length=20)

    def __str__(self):
        return self.nom

class Pays(models.Model):
    code = models.PositiveSmallIntegerField(unique=True)
    alpha2 = models.CharField(max_length=2,unique=True)
    alpha3 = models.CharField(max_length=3,unique=True)
    nom_en_gb = models.CharField(max_length=45)
    nom_fr_fr = models.CharField(max_length=45)

    def __str__(self):
        return self.nom_fr_fr


class VillesDeFrance(models.Model):
    id                           = models.AutoField(primary_key=True, db_column="ville_id")
    departement                  = models.CharField(max_length=3,     db_column="ville_departement")
    slug                         = models.CharField(max_length=255,   db_column="ville_slug")
    nom                          = models.CharField(max_length=45,    db_column="ville_nom")
    nom_reel                     = models.CharField(max_length=45,    db_column="ville_nom_reel")
    nom_soundex                  = models.CharField(max_length=45,    db_column="ville_nom_soundex")
    nom_metaphone                = models.CharField(max_length=45,    db_column="ville_nom_metaphone")
    code_postal                  = models.CharField(max_length=255,   db_column="ville_code_postal")
    commune                      = models.CharField(max_length=3,     db_column="ville_commune")
    code_commune                 = models.CharField(max_length=5,     db_column="ville_code_commune")
    arrondissement               = models.PositiveSmallIntegerField(  db_column="ville_arrondissement")
    canton                       = models.CharField(max_length=4,     db_column="ville_canton")
    amdi                         = models.PositiveSmallIntegerField(  db_column="ville_amdi")
    population_2010              = models.PositiveIntegerField(       db_column="ville_population_2010")
    population_1999              = models.PositiveIntegerField(       db_column="ville_population_1999")
    population_2012              = models.PositiveIntegerField(       db_column="ville_population_2012")
    densite_2010                 = models.IntegerField(               db_column="ville_densite_2010")
    surface                      = models.PositiveIntegerField(       db_column="ville_surface")
    longitude_deg                = models.FloatField(                 db_column="ville_longitude_deg")
    latitude_deg                 = models.FloatField(                 db_column="ville_latitude_deg")
    longitude_grd                = models.CharField(max_length=9,     db_column="ville_longitude_grd")
    latitude_grd                 = models.CharField(max_length=8,     db_column="ville_latitude_grd")
    longitude_dms                = models.CharField(max_length=9,     db_column="ville_longitude_dms")
    latitude_dms                 = models.CharField(max_length=8,     db_column="ville_latitude_dms")
    zmin                         = models.IntegerField(               db_column="ville_zmin")
    zmax                         = models.IntegerField(               db_column="ville_zmax")
    population_2010_order_france = models.IntegerField(               db_column="ville_population_2010_order_france")
    densite_2010_order_france    = models.IntegerField(               db_column="ville_densite_2010_order_france")
    surface_order_france         = models.IntegerField(               db_column="ville_surface_order_france")

    class Meta:
        db_table = "villes_france"

    def __str__(self):
        return self.nom_reel
        
class AjoutForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AjoutForm, self).__init__(*args, **kwargs)
		self.fields['nom'].label = "Nom "
		self.fields['adresse'].label = "Adresse"
		self.fields['codePostal'].label = "Code postal"
		self.fields['ville'].label = "Ville"
		self.fields['pays'].label = "Pays"
		self.fields['telephone'].label = "Telephone"
		self.fields['latitude'].label = "Latitude"
		self.fields['longitude'].label = "Longitude"

		#il est possible de metre que un seul champ en utilisant le model entreprise, il suffit de ne le préciser ni dans le init ni le meta
	class Meta:
		model = Entreprise
		fields = ('nom', 'adresse', 'codePostal','ville','pays' ,'telephone' ,'latitude' ,'longitude' )      
		
class ModifForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ModifForm, self).__init__(*args, **kwargs)
		self.fields['nom'].label = "Nom"
		self.fields['adresse'].label = "Adresse"
		self.fields['codePostal'].label = "Code postal"
		self.fields['ville'].label = "Ville"
		self.fields['pays'].label = "Pays"
		self.fields['telephone'].label = "Telephone"
		self.fields['latitude'].label = "Latitude"
		self.fields['longitude'].label = "Longitude"
		
		#il est possible de metre que un seul champ en utilisant le model entreprise, il suffit de ne le préciser ni dans le init ni le meta
	class Meta:
		model = Entreprise
		fields = ('nom', 'adresse', 'codePostal','ville','pays' ,'telephone' ,'latitude' ,'longitude' )    		
        
class EntrepriseAjoutForm(ModelForm):
    class Meta:
        model = Entreprise