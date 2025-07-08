from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList,OneLineIconListItem,IconLeftWidget
from kivymd.uix.datatables import MDDataTable
import os
from time import strftime
import datetime
#Window.size = [360,610]

from kivy.metrics import dp
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas


#main
class Cotise(MDApp):
    Screen_Manager = ObjectProperty(None)
    def build(self):
        self.theme_cls.theme_style = "Dark"
        main = Builder.load_file("main2.kv")
        #main.ids.cr.current = "Page1"
        return main

    def on_start(self):
        if not os.path.exists(os.getcwd() + "/" + "Base_de_donne" ):
            os.mkdir(os.getcwd() + "/" + "Base_de_donne" )
    def do(self,instance):
        Name = self.root.ids.Ident.text
        Pass = self.root.ids.Pass.text
        if "" in [Name,Pass]:
            toast("Tous les champs sont Oblig. !")
        else:
            if (Name,Pass) in [("Deg","Deg"),("Zelipro","Dieuestgrand")]:
            #if Name in ["Zelipro","Deg"] and Pass in ["Deg","Dieuestgr@nd"]:
                self.show_info(title = "Message",text = "Bienvenue M.Elisée",fonct = self.Next)
            else:
                toast("Vous n'est pas le Bienvenue !")
    
    def show_info(self,title,text,fonct = None):
        self.MD = MDDialog(
            title = title,
            text = text,
            buttons = [
                MDFlatButton(
                    text = "Ok",
                    on_release=lambda x : self.Ok(x,fonct)
                )
            ]
        )
        self.MD.open()
    
    def Ok(self,instance,fonct):
        self.MD.dismiss()
        if fonct:
            fonct()
    
    def Next(self):
        Pge = self.root.ids.cr.current
        self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])+1)}"
    
    def Back(self,instance):
        self.Back_s()
    
    def Back_s(self):
        Pge = self.root.ids.cr.current
        if Pge[-1] == "1":
            self.stop()
        else:
            self.root.ids.cr.current = f"{Pge[:-1]}{str(int(Pge[-1])-1)}"
    
    def New_Cot(self,instance):
        Cont = MDBoxLayout(orientation =  'vertical',size_hint =(0.3,0.3))
        self.input = MDTextField (hint_text = "Motif",helper_text = "Exple : Marriage de Zeli",helper_text_mode = "on_focus",halign = "center")
        But =MDFlatButton(text = "[b]Valider[/b]",on_release= self.Valider2,pos_hint= {'center_x': 0.5,'center_y': 0.4})
        Cont.add_widget(self.input)
        Cont.add_widget(But)
        
        
        self.pop = Popup(
            title = "Information",
            content = Cont,
            size_hint = (0.8,0.3)
        )
        
        self.pop.open()
    
    def Valider2(self,instance):
         text = self.input.text

         if text == "":
             toast("Ce champs est Obligatoire !")
         else:
            self.Lieu = os.getcwd() + "/" + "Base_de_donne" 
            fil = os.path.exists(self.Lieu + "/" + text)
            if fil:
                toast("Ce motif exist déjà !")
            else:
                os.mkdir(self.Lieu + "/" + text)
                toast(f"{text} est enregistré avec succes !")
                self.pop.dismiss()
                #self.Back_s()
                
    def Ok2(self,instance):
        self.pop.dismiss()
    
    def FICHIER_DOC(self,rep):
        return [fic for fic in os.listdir(rep) if os.path.isdir(os.path.join(rep,fic))]
    
    def Cotiser(self,instance):
        self.root.ids.cr.current = "Page3"
        self.place = os.getcwd() + "/Base_de_donne"
        Pge = self.root.ids.List
        for elmt in self.FICHIER_DOC(self.place):
            Lis = OneLineIconListItem(
                text = elmt,
                on_release= lambda x : self.appui(x),
            )
            Icon = IconLeftWidget(icon = "folder")
            Lis.add_widget(Icon)
            Pge.add_widget(Lis)
    
    def appui(self,instance):
        self.Lieu2 = self.place + "/" + instance.text
        self.Instance = instance.text
        self.root.ids.cr.current = "Page4"
        self.Page4()
    
    def Page4(self):
        self.place = self.Lieu2 + "/Les_Cotisations"
        Pge = self.root.ids.List2
        for elmt in ["Ajouter","Voir la liste","Total","Version Pdf"]:
            Lis = OneLineIconListItem(
                text = elmt,
                on_release=lambda x :self.appui2(x)
            )
            Icon = IconLeftWidget(icon = "list-box")
            Lis.add_widget(Icon)
            Pge.add_widget(Lis)
    
    def appui2(self,instance):
        dic = {"Ajouter" : self.add,"Voir la liste" : self.list,"Total": self.total,"Version Pdf" : self.pdf}
        do = dic.get(instance.text)
        do()
        
    def list(self):
        fil = os.path.exists(self.place)
        if fil:
            try:
                self.root.ids.cr.current = "Page5"
                self.root.ids.TopBar.title = self.Instance
                Pge = self.root.ids.Data   
                
                row_data2 = []
                with open(self.place+"/Liste","r") as file:
                    tous = file.read()
                
                tous = tous.split('\n')
                i = 1
                Tous = []
                for emt in tous:
                    if len(emt)>6:
                        emt = emt.split("!!!")
                        Tous = [str(i)] + emt
                        i += 1
                        row_data2.append(tuple(Tous))
               
               
                Data = MDDataTable(
                pos_hint = {"center_x":0.5,"center_y":0.5},
                use_pagination = True,
                size_hint=(0.9,0.5),
                column_data =  [
                    ("ID",dp(12)),("Date",dp(25)),("Name",dp(35)),("Prix",dp(25))
                    ],
                row_data = row_data2)
                Pge.add_widget(Data)
            except:
              toast("Fichier vide ! 1")
        else:
            toast("Fichier vide ! 2")
    def add(self):
        Cont = MDBoxLayout(orientation = 'vertical',spacing = 5)
        self.Name = MDTextField(hint_text = "Name",helper_text = "Maybe first name + second name",helper_text_mode = "on_focus",halign = "center")
        self.prix = MDTextField(input_filter = "int",hint_text = "Prix",helper_text = "300 , 500 ,....",helper_text_mode = "on_focus",halign = "center")
        self.But = MDFlatButton(text = "[b]Valider[/b]",on_release=self.Valider3,pos_hint = {"center_x":.5})
        
        Cont.add_widget(self.Name)
        Cont.add_widget(self.prix)
        Cont.add_widget(self.But)
        
        self.pop2 = Popup(
            title = "Information",
            content = Cont,
            size_hint = (0.9,0.4)
        )
        self.pop2.open()
    
    def Valider3(self,instance):
        if "" in [self.Name.text ,self.prix.text]:
            toast("Tous les champs sont obligatoire !")
        elif self.exist(self.Name.text):
            toast("Ce nom existe  déjà")
        else:
            self.pop2.dismiss()
            self.oui()
            toast("Ajout effectué !!!")
        
    def contenu(self):
            retur = []
            with open(self.place + "/Liste","r") as file:
                tous = file.read()
            tous = tous.split("\n")
            Date = ""
            Som = 0
            for elmt in tous:
                if len(elmt)>6:
                    elmt = elmt.split("!!!")
                    if Date != elmt[0]:
                        Date = elmt[0]
                        retur.append(Date)
                    retur.append(f"{elmt[1]} : {elmt[2]}")
                    Som += int(elmt[2])
            retur.append(f"Total = {Som}")
            return retur
        
    def PDF(self, rep, Messagess): #Ici
        file = canvas.Canvas(f"{rep}/Liste.pdf", pagesize=letter)
        file.setTitle("Liste PDF")
        
        # Configuration initiale
        line = 750  # Position verticale initiale
        page_number = 1
        
        def draw_header():
            """Dessine l'en-tête sur chaque page"""
            nonlocal file, line
            header = f"REPPORT DE COTISATION POUR {self.Instance}"
            file.setFont("Helvetica-Bold", 18)
            file.drawString(150, line, f"{header}")
            file.setLineWidth(1.5)
            file.line(150, line - 3, 200 + file.stringWidth(f"{header}", "Helvetica-Bold", 17), line - 3)
            file.setFont("Helvetica", 16)
            line -= 40
        
        # Dessiner l'en-tête de la première page
        draw_header()
        
        for elmt in Messagess:
            # Vérifier si on a besoin d'une nouvelle page
            if line < 50:  # Marge basse
                file.showPage()
                page_number += 1
                line = 750
                draw_header()
            
            # Dessiner l'élément avec son formatage approprié
            if "Total" in elmt or len(elmt.split("/")) == 3:
                file.drawString(250, line, elmt)
                #file.line(250, line - 2, 250 + file.stringWidth(elmt, "Helvetica", 12), line - 2)
            else:
                file.drawString(200, line, elmt)
                #file.line(200, line - 2, 200 + file.stringWidth(elmt, "Helvetica", 12), line - 2)
            
            line -= 25  # Espacement entre les lignes
        
        # Pied de page sur la dernière page
        file.setFont("Helvetica", 10)
        file.drawString(500, 30, f"Fin du document - {datetime.datetime.now().strftime('%d/%m/%Y')}")
        
        file.save()
        
    def oui(self,Exist = False):#Finalement le Exist du paramettre n'a serivie a rien
        self.place2 = self.place
        Exist = os.path.exists(self.place2)
        
            
        def not_existe():
            with open(self.place2+'/Liste',"a") as file:
                file.write("\n"+strftime("%D")+"!!!"+self.Name.text + "!!!"+self.prix.text)
                
        if not Exist:
            os.mkdir(self.place2)
            not_existe()
        else:
            Vue = False
            tous = ""
            with open(self.place2+'/Liste',"r") as file:
                tous = file.read()
            tous = tous.split("\n")
            tous2  = []
            for elmt in tous:
                elmt2 = ""
                if len(elmt) > 6:
                    elmt = elmt.split("!!!")
                    if elmt[1] == self.Name.text:
                        elmt2  = f"{strftime("%D")}" + "!!!"+elmt[1] + "!!!" +str(int(elmt[2])+int(self.prix.text))
                        Vue = True
                    else:
                        elmt2 = "!!!".join(elmt)
                tous2.append(elmt2)
            #Reinitialiser le fichier
            if Vue:
                with open(self.place2+'/Liste',"w") as file:
                    file.write("\n".join(tous2))
            else:
                not_existe()
                
            toast("Modification éffectué !")
        self.PDF(self.place,self.contenu())
        
        for elmt in [self.Name ,self.prix]:
            elmt.text = "" 
            
    
    def exist(self,name):
            fil = os.path.exists(self.place)
            if not fil:
                return False
            else:
                tous = ""
                try:
                    with open(self.place2+'/Liste',"r") as file:
                        tous = file.read()
                    tous = tous.split("\n")
                    for elmt in tous:
                        if len(elmt) > 6:
                            elmt = elmt.split("!!!")
                            if elmt[1] == name:
                                return True
                    return False
                except:
                    return False
    
        
    def Change(self,instance):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def Option_List(self,instance):
        dic = {"Leave":self.stopp , "Help":self.help , "About as":self.info}
        dic.get(instance.text)()
    
    def info(self):
        self.show_info(title = "info" , text = "Name : Fint it \nAuthor : Elisée ATIKPO")
    def help(self):
        self.show_info(title = "Help" ,text="Here is for a cotisation so , follow the instrction.\nThanks")
    def stopp(self):
        self.show_info(title = "Info",text = "Bye !!!",fonct=self.stop)
            
    def total(self): #Pge 7
        fil = os.path.exists(self.place)
        print(self.place)
        if fil:
            try:
                self.show_info(title = "Total",text = f"Le total des prix est {self.Somme_prix()} FCFA.")
            except:
                toast("Vous n'avez rien ajouté ! 1")
        else:
             toast("Vous n'avez rien ajouté ! 2")
    
    def Somme_prix(self):
        with open(self.place + "/Liste","r") as file:
            tous = file.read()
        tous = tous.split("\n")
        Som = 0
        for emt in tous:
            if emt!="":
                emt = emt.split("!!!")
                Som += int(emt[-1])
        return Som
    
    def pdf(self): #Pge 8
        fil = os.path.exists(self.place)
        if fil:
            try:
                self.root.ids.cr.current = "Page6"
            except:
                toast("Vous n'avez rien ajouté !")
        else:
             toast("Vous n'avez rien ajouté !")
    
    def this(self,instance):
        selct = self.root.ids.selct.selection
        print(selct)
        try:
            file_select = selct[0]
            print(file_select)
            self.PDF(file_select,self.contenu())
            toast(f"Fichier enregisté à\n {file_select}")
        except:
            toast("Impossible !")
Cotise().run()