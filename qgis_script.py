import re

#OBS, de to nedenstående punkter er de eneste der skal tilpasses fra gang til gang
#resten af scriptet må ikke ændres. 
path: str = r"F:\GRF\Medarbejdere\philip\test\test3"+'\\' #stien til indput-filen // indsæt selv stien til filerne, imellem r" og "+ uden backslash til sidst
inputfilepoint ='resk_bogense19.geo'#inputfil til punktlaget // Skal udfyldes
inputfileline = ''#inputfil til linjelaget  // hvis der ikke er et seperat linje fil, kan dette felt lades stå tomt
inputdifffile = '' #inputfil til difference lag  // hvis der ikke er en seperat diff fil, kan dette felt stå tomt

#Lister der bruges i programmet
pointlist = [] #Liste over punkter // Oprettes i def point_edit ()
pointlist_1 = [] #itererede list over punkter // Oprettes i def point_edit ()
linelist = [] #liste over punkter til linjer // Oprettes i def line_edit ()
linelist_2 = [] #liste over punkter til linjer med koordinater // Oprettes i def line_edit ()
linelist_3 = [] #lister over linjestykker (kommaseperaret) // Oprettes i def line_edit ()
linelist_4 = [] #sorterede liste over linjestykker med ændret rækkefølge på information så dup_line_count virker  // Oprettes i def line_edit ()
linelist_5 = [] #liste over linjestykker med målingsantal // Oprettes i def line_edit ()
difflist = [] #liste med forskellige difference attributter til punkter // Oprettes i def diff_edit ()
difflist_2 = [] #editeret udgave af difflist // Oprettes i def diff_edit ()
difflist_3 = [] #opdateret udgave af difflist_2 med nye felter // Oprettes i def diff_edit ()
no_diff_point = [] #lister over punkter uden diff information // Oprettes i def diff_edit ()
no_diff_point_2 = [] #Samme som no_diff_point men kommaseperaret // Oprettes i def diff_edit ()
  
#funktion til at konvertere lister til strings
def convert_list_to_string(org_list, seperator=','): 
    return seperator.join(org_list)
        
#funktion til tekstediteringen af inputfilen (punkt-delen)
def point_edit ():
    with open(path+inputfilepoint,'r') as f: #inputfil
            val = 0 #val variablerne i dette script bruges til at opdele fil.
            for line in f: #Loop til tekst-editering af input-fil // Det meste af editeringen sker med regex.
                result = (line[:55]) #definere result // line:55 er valgt fordi de karakterer der kommer efter 55 i de originale filer omhandler tid/dato og er irrelevante.
                result = re.sub(r'(?m)\ # DK_.*\n?', '*', result)#fjerner gammel header
                result = re.sub('[mpr](\s+)',r'\1', result) #fjerner bogstaverne m r p
                result = re.sub(r'(\d) (\d)',r'\1\2',result) #fjerner mellemrum mellem tal
                result = re.sub(r'(\D) ',r'\1',result)#fjerner mellemrum efter bogstaver
                result = re.sub(r'(\d)\s+',r'\1,',result)#tal efterfulgt af mere en et mellemrum laves til tal+komma
                result = re.sub(r'(?m)^\*.*\n?', '', result)#fjern linjer der starter med *
                result = re.sub(r'^\s+', '', result) #Align tekst til venstreside
                if val == 0: #Hvis val er = 0 tilføjes Fastholdt punkt til linjen
                    result = re.sub(r"(.)$",r"\1Fastholdt punkt", result) #tilføjer Fastholdt punkt til sidste i hver linje indtil counter stiger er script slutter
                if '-1x' in line: #val stiger til en hvis en linjer der starter med -1x mødes
                    val = 1
                if val == 1: #Hvis val er = 0 tilføjes Beregnet punkt til linjen
                    result = re.sub(r"(.)$",r"\1Beregnet punkt", result) #tilføjer Beregnet punkt til sidste i hver linje indtil counter stiger er script slutter
                result = re.sub(r'(?m)^-.*\n?', '', result)#fjern linjer der starter med -

                #Laver løbenummre i hvert linje
                if result.startswith ('G'): #løbenumre der starter med g
                    lbnr=result.split(',')[0] #splitter linje ved første komma, så kun id er tilbage, som så skal udgøre løbenummer
                    point = lbnr+','+result #løbenummret skrives ind i linjen
                    pointlist.append (point) #linjen tilføjes punktlisten
                
                if result.startswith ('G') == False: #løbenumre der ikke starter med g
                    if result.startswith (' ') == False: #Hvis linjen ikke er tom køre loopet
                        lbnr=result.split(',')[0] #splitter linje ved første komma
                        if len(lbnr) != 0: #skipper empty lines
                            lbnr=lbnr.split('-')[2] #splitter linje efter det andet -
                            lbnr=lbnr.lstrip('0') #fjerner alle 0 indtil det første tal over 0. Ved at gøre dette + de to splits, ender man med at få et reelt løbenummer
                            point = lbnr+','+result #løbenummret skrives ind i linjen
                            pointlist.append(point) #linjen tilføjes punktlisten
                                           
                if "-1z" in line: #Hvis -1z er i linjen stopper denne del af scriptet
                    break    

            for i in range(len(pointlist)): #Der itereres i punktlisten
                 point_splitter=pointlist[i] #Ved at gøre dette opfattes listen som en string og ikke en liste og der kan derfor benyttes den indbygget split funktion
                 point_splitter=point_splitter.split(',')[0:5] #kommaseperarer listen og splitter ved hver 5 komma
                 pointlist_1.append(point_splitter) #resultatet indskrives i en liste


#funktion til teksteditering af inputfilen (linje-delen)
def line_edit():
    #loop til at diffinere hvilken input fil der skal benyttes
    if inputfileline!='':
        flex_input=inputfileline
    if inputfileline=='':
        flex_input=inputfilepoint

    with open(path+flex_input,'r') as f: #input-fil
            val= 0 #val variablerne i dette script bruges til at opdele fil.
            for line in f: 
                if "#DK_ni" in line: #skipper del af fil som ikke skal bruges og val sættes til 1
                    val = 1 
            
                #teksteditering af input-fil
                if val == 1:
                    result = re.sub(r'(?m)\;.*\n?',r'', line) #fjern linjer med ; (herunder journalnummeret)
                    result = re.sub(r'(\d) (\d)',r'\1\2',result) #fjerner mellemrum mellem tal
                    result = re.sub(r'(\D) ',r'\1',result)#fjerner mellemrum efter bogstaver
                    result = re.sub(r'^\s+',r'', result) #Align tekst til venstreside
                    result = re.sub(r'\s+',r',', result) #Erstatter mere end et mellemrum/tab med komma
                    result = re.sub(r',.*?\*',r'', result) #Sletter alt fra første komma og til slutningen af linjen så kun punktnummer er tilbage
                    result = re.sub(r',',r'', result) #fjerner alle komma'er
                    result = re.sub(r'(?m)\#.*\n?',r'', result) #fjerner linjer med #
                    result = re.sub(r'-1a',r'', result)#fjern linjer med -1a
                    linelist.append (result) #resultater skrives i liste
           
            #fjerner tomme entries i listen
            while("" in linelist) : 
                linelist.remove("") 
            
            #Bruger funktionen convert_list_to_string // laver linelist til en string
            #Splitter herefter den nye string på komma og ligger den i en ny liste.
            linelist_str = convert_list_to_string(linelist)
            linelist_split=linelist_str.split(',')  

            #kombinere linje punkter i linelist med punkt kordinater fra pointlist
            for i in range(len(linelist_split)):
                for j in range(len(pointlist_1)):
                    if linelist_split[i]==pointlist_1[j][1]:
                        linelist_2.append(linelist_split[i]+','+pointlist_1[j][2]+','+pointlist_1[j][3]) 
                        
            #linjerne består før denne kommando af punkt+koordinater, denne kommando sammensætter linjer 2 og 2 så der er 2xpunkter 4xkoordinater på hver linje
            points_to_lines=[",".join(linelist_2[i:i+2]) for i in range(0, len(linelist_2), 2)]
            
            
            for i in range(len(points_to_lines)): #Der itereres i linjelisten
                var=points_to_lines[i] #Ved at gøre dette opfattes listen som en string og ikke en liste og der kan derfor benyttes den indbygget split funktion
                var=var.split(",") #linjerne komma seperares 
                linelist_3.append(var) #linjerne skrives i liste

            #Denne del kræver en større forklaring. Hvert linjestykke har to punkter og linjen mellem disse to punkter kan være målt flere gange i marken.
            #Så det vil sige at en linje består af punkt 1, x-koord 1, y-koord 1, punkt 2, x-koord 2 og y-koord 2, men når linjen er målt flere gange kan rækkefølge være 
            #omvendt så det er punkt 2, x-koord 2, y-koord 2, punkt 1, x-koord 1 og y-koord 1 i stedet. Det er den samme linje der står flere gange i listen men i omvendt rækkefølge
            #Derfor rykkes der i næste kommando om på rækkefølgen så linjer der er ens, ser ens ud i listen, så der kan fjernes duplicates og der kan tælles antal målinger.
            #Der sorteres i hver entry i linjelisten, så hver entry  
            for i in range(len(linelist_3)):
                if linelist_3[i][0] < linelist_3[i][3]: #Punkt nummeret er definerende for at finde ens linjer så det størst nummer vil stå først
                    linelist_4.append(linelist_3[i][0]+','+linelist_3[i][3]+','+linelist_3[i][1]+','+linelist_3[i][2]+','+linelist_3[i][4]+','+linelist_3[i][5])
                
                if linelist_3[i][0] > linelist_3[i][3]: #Punkt nummeret er definerende for at finde ens linjer så det størst nummer vil stå først
                    linelist_4.append(linelist_3[i][3]+','+linelist_3[i][0]+','+linelist_3[i][4]+','+linelist_3[i][5]+','+linelist_3[i][1]+','+linelist_3[i][2])

            
            #Fjerner linjestykker der er ens og tæller antal gange strækningen er målt       
            dup_line_count = {i:linelist_4.count(i) for i in linelist_4}
            for i in dup_line_count:
                var1=i, dup_line_count[i] #count funktionen der bruges laver en dictonary, key+value skrives i en variable
                line_with_count=var1[0]+','+str(var1[1]) #variablen laves om til en string
                line_with_count_split=line_with_count.split(',')[0:7] #stringen laves til en kommaseperaret liste
                linelist_5.append(line_with_count_split) #listen gemmes 


#funktion til teksteditering af differencefiler 
def diff_edit():
    with open(path+inputdifffile,'r',encoding="latin-1") as f: #input-fil // skal encodes ellers vil qgis ikke sammenarbejde
            val = 0 #val variablerne i dette script bruges til at opdele fil.
            for line in f: #Loop til tekst-editering af difference fil
                if "DK_h" in line: #skipper del af fil som ikke skal bruges og val sættes til 1
                    val = 1  
                
                #teksteditering af difference fil
                if val == 1:
                    result = re.sub(r'^\s+', '', line) #Align tekst til venstreside
                    result = re.sub(r'(?m)\DK_.*\n?', '',result)#fjerner label i toppen
                    result = re.sub(r'(?m)Label.*\n?', '', result)#fjerner label i bunden
                    result = re.sub(r'(\d) (\d)',r'\1-\2',result) #fjerner mellemrum mellem tal
                    result = re.sub(r'(\D) ',r'\1',result) #fjerner mellemrum efter bogstaver
                    result = re.sub(r'\D\D ',r' ',result) #fjerner ord på to bogstaver som er efterfuglt af mellemrum
                    result = re.sub(r' \D',r' ',result) #fjerner bogstaver der står alene
                    result = re.sub(r'(\d)\s+(\d)',r'\1,\2',result)# laver mellemrum om til kommaer
                    result = re.sub(r'^\s+',r'',result)#fjern mellemrum i starten af en linje
                    result = re.sub(r'\s+',r'', result) #fjerner linjeskift
                    difflist.append(result) #gemmer resultat i en liste
                    
                if "Label" in line:
                    break
                
            #fjerner tomme entries i listen  
            while("" in difflist) : 
                difflist.remove("") 
            
            #Difference filen har information om hvert punkt fordelt over tre linjer, her sammensættes de til en linje per punkt
            merge_difffile_lines=[",".join(difflist[i:i+3]) for i in range(0, len(difflist), 3)]
            
            #
            for i in range(len(merge_difffile_lines)): #Der itereres i difflisten
                var=merge_difffile_lines[i] #Ved at gøre dette opfattes listen som en string og ikke en liste og der kan derfor benyttes den indbygget split funktion
                var=var.split(",") #kommaseperarer listen
                difflist_2.append(var) #linjerne skrives i liste
                
            #fjerner tomme entries i listen                
            while("" in difflist_2): 
                difflist_2.remove("") 

            #editere punkt information og tilføjer et nyt felt
            for i in range (len(difflist_2)):
                time1= re.sub(r'\.',':',difflist_2[i][3]) #feltet vedr. tid formateres fra . til : som seperator
                time2= re.sub(r'\.',':',difflist_2[i][7]) #feltet vedr. tid formateres fra . til : som seperator                
                diff='%.3f'%(float(difflist_2[i][8])*1000)+' mm' #kotedifference udregens og formaters 
                #de nye felter skrives sammen med de gamle
                combine=(difflist_2[i][0]+','+difflist_2[i][1]+','+difflist_2[i][2]+','+time1+','+difflist_2[i][4]+','+difflist_2[i][5]+','+difflist_2[i][6]+','+time2+','+diff) 
                combine=combine.split(',')[0:9] #kommaseperarer vores nye string
                difflist_3.append(combine) #skriver resultatet ind i en liste

            #Finder punkter som ikke har nogle information fra difference filen, dette gøres ved at lægge de to lister samme og tælle duplicates, hvis et punkt ikke har nogle
            #duplicate har den ingen info
            for i in range(len(difflist_3)):
                no_diff_point.append(difflist_3[i][0])
            for i in range(len(pointlist_1)):
                no_diff_point.append(pointlist_1[i][1])

            #Fjerner alle duplicate punkter, åltså punkter med et count over 1 
            no_diff_counter = {i:no_diff_point.count(i) for i in no_diff_point}
            for i in no_diff_counter:
                var1=i, no_diff_counter[i] #count funktionen der bruges laver en dictonary, key+value skrives i en variable
                if var1[1]==1: #Hvis count for et punkter er = 1 skrives det i en liste.
                    no_diff_point_2.append(var1[0])


#Definere style til punkter i qgis, rækkefølgene af alle qgis dele er vigtigt så der må ikke rykkes rundt på dette ellers vil det ikke virke. 
def qgis_symbology():
    #Find aktivt lag
    layer = iface.activeLayer()
    #Definer hvor script skal finde symboler
    shape = QgsSimpleMarkerSymbolLayerBase
    #Laver dictionary, som tilknytter farve, signaturlabel, og symbol til attributterne i type kolonne 
    type_class = {
        'Beregnet punkt': (QColor("#0000b6"), 'Beregnet punkt', shape.Circle),
        'Fastholdt punkt': (QColor("#8e0000"), 'Fastholdt punkt', shape.Triangle),
    }
    #Laver liste til at gemme værdier tilknyttet i loopet
    categories = []
    #Itererer over vores dictionary, og gemmer værdier til hver entry i vores liste
    for classes, (colour, label, shape) in type_class.items():
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        #Tilknytter en shape til listen
        symbol.symbolLayer(0).setShape(shape)
        
        #Tilknytter farve og størrelse til listen
        symbol.setColor(QColor(colour))
        symbol.setSize(1.5)
        
        #Gemmer værdier i listen
        category = QgsRendererCategory(classes, symbol, label, shape)
        categories.append(category)
        
        #aktivere labels
        layer_settings  = QgsPalLayerSettings()
        
        #tilføjer symbology til labels
        text_format = QgsTextFormat()
        text_format.setFont(QFont("Arial", 8))
        text_format.setSize(8)
        text_format.setColor(QColor("#0000b6"))
    
        #giver labels buffer
        buffer_settings = QgsTextBufferSettings()
        buffer_settings.setEnabled(True)
        buffer_settings.setSize(0.8)
        buffer_settings.setColor(QColor("white"))
        text_format.setBuffer(buffer_settings)
        
        #Sammenknytter lag og symbologi og definerer field name der skal laves labels for
        layer_settings.setFormat(text_format)
        layer_settings.fieldName = "Fikspunkt" #field name for labels
        
        #Vælger placeringstype for label: 6=Cartographic, 0=Around point, 1=Offset from point
        layer_settings.placement = 1
        #De efterfølgende tre linjere kode skal kun bruges hvis man vælger offset from point
        #Vælger placering af label fra 0-8, hvor 0 er øverste venstre hjørne, og 8 er det nederste venstre hjørne, der er tre placeringer per linje.
        layer_settings.quadOffset = 3
        #Offset X og Y
        layer_settings.xOffset = -2.5
        layer_settings.yOffset = 0
     
       
    # Field name // feltnavn i vores punktfil, som der skal symboliseres
    expression = 'type'
    #Kombinere vores attributtabel og liste, så laget kan vises i qgis
    renderer = QgsCategorizedSymbolRenderer(expression, categories)
    layer.setRenderer(renderer)
    
    #Loader labels ind i QGIS
    layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(layer_settings)
    
    #Opdatere vores lag, så nye styles bliver brugt
    layer.triggerRepaint()

#Laver en rule-based style til qgis, dette laves som en funktion der kan kaldes senere når reglerne skal defineres.
#Counter inkluderes så "no filter" kan fjeres fra lag.
def rule_based_style(layer, symbol, renderer, label, expression, color):
    root_rule = renderer.rootRule() #starter regel
    rule = root_rule.children()[0].clone() #kloner først regel når funktion køres, denne regel laves om til den nye regel
    rule.setLabel(label) #definere regelens label
    rule.setFilterExpression(expression) #definere reglen
    rule.symbol().setColor(QColor(color)) #definere farven for hver regel
    rule.symbol().setWidth(0.3) #predefinere størrelsen på symbol kan kun ændres her og ikke defineres ved at køre funktion
    root_rule.appendChild(rule) #tilføjer regel
    layer.setRenderer(renderer) #opretter lag
    rule_based_style.counter += 1 #tæller hvor mange gange funktionen har kørt
    var=rule_based_style.counter #gemmer count i en variable
    if var == 3: #når count rammer tre er den sidste regle tilføjter og den tomme regle fjenres fra laget
        root_rule.removeChildAt(0) #fjerner tom regel
    layer.triggerRepaint() #opdatere lagets style
    iface.layerTreeView().refreshLayerSymbology(layer.id()) #opdatere signaturforklaringen
rule_based_style.counter = 0 #counter starter fra 0

#tegner linjestykkerne i qgis
def qgis_line ():
    #definerer lag til linjer
    zlayer = QgsVectorLayer('LineString?crs=epsg:25832', 'observationslinje' , 'memory')
    prov = zlayer.dataProvider() #definere variable til obervaring af lag infromation
    #opretter fields til attribute tabellen
    prov.addAttributes([QgsField("Punkt-1", QVariant.String),
                      QgsField("Punkt-2",  QVariant.String),
                      QgsField("Antal Målinger", QVariant.String)])
    zlayer.updateFields() 

    #looper igennem liste med punkt koordinater
    for i in range(len(linelist_5)):
        val1 = linelist_5[i][2]
        val2 = linelist_5[i][3]
        val3 = linelist_5[i][4]
        val4 = linelist_5[i][5]
        
        #koordinater fodres til punkter
        point1 = QgsPoint(float(val2),float(val1))
        point2 = QgsPoint(float(val4),float(val3))
    
        #Tegner linjer mellem punkter
        feat = QgsFeature() #definere variable til at gemme features i
        feat.setGeometry(QgsGeometry.fromPolyline([point1, point2]))
        feat.setAttributes([linelist_5[i][0],linelist_5[i][1],linelist_5[i][6]]) #giver information til fields ud fra data i linelist_5
        prov.addFeatures([feat]) #tilføjer punkter til variable
        zlayer.updateExtents() #opdater map extent
        QgsProject.instance().addMapLayers([zlayer]) #tilføjer lag/data til canvas 
        
        layer = iface.activeLayer() #finde linjelaget 
        symbol = QgsSymbol.defaultSymbol(layer.geometryType()) #gemmer geometry type i variable
        renderer = QgsRuleBasedRenderer(symbol) #opdatere symbology for lag så det bruge vores rulebasedrender funktion
    
    #køre funktionen rule_based_style og tilføjer tre regler, med label,ekspression og symbology
    rule_based_style(layer, symbol, renderer, '1 Måling', '"Antal Målinger"=1', 'orange')
    rule_based_style(layer, symbol, renderer, '2 Målinger', '"Antal Målinger"=2', 'blue')
    rule_based_style(layer, symbol, renderer, '4+ Målinger', '"Antal Målinger"=4 or "Antal Målinger">4', 'red')

#tegner punkter i qgis
def qgis_point ():
    #definerer lag til linjer
    layer =  QgsVectorLayer('Point?crs=epsg:25832', 'Point' , "memory")
    pr = layer.dataProvider() #definere variable til obervaring af lag infromation
    #opretter fields til attribute tabellen
    pr.addAttributes([QgsField("lbnr", QVariant.String),
                  QgsField("fikspunkt",  QVariant.String),
                  QgsField("type", QVariant.String)])
    layer.updateFields() 
    
    pt = QgsFeature() #definere variable til at gemme features i

    #looper igennem liste med punkt koordinater
    for i in range(len(pointlist_1)):
        val2 = pointlist_1[i][2] #x-koordinat
        val1 = pointlist_1[i][3] #y-koordinat
        point1 = QgsPointXY(float(val1),float(val2))  #gemmer punkter i variable
        pt.setGeometry(QgsGeometry.fromPointXY(point1)) #definere features til vores variable som punkter
        pt.setAttributes([pointlist_1[i][0],pointlist_1[i][1],pointlist_1[i][4]]) #giver punkterne attributer
        pr.addFeatures([pt]) #tilføjer punkter+attributer til ny feature variable
        layer.updateExtents() #opdatere map extent
        QgsProject.instance().addMapLayers([layer]) #tilføjer lag til canvas
    
    qgis_symbology() #kører symbology funktionen og giver laget en symbology og labels


def qgis_diff ():
    #definerer lag med differencer
    layer =  QgsVectorLayer('Point?crs=epsg:25832', 'Diff' , "memory")
    pr = layer.dataProvider() #definere variable til obervaring af lag infromation
    #opretter fields til attribute tabellen
    pr.addAttributes([QgsField("LBNR", QVariant.String),
                  QgsField("Fikspunkt",  QVariant.String),
                  QgsField("Type", QVariant.String),
                  QgsField("Måleår",  QVariant.String),
                  QgsField("Difference",  QVariant.String),
                  QgsField("Ny Kote",  QVariant.String),
                  QgsField("Ny Dato",  QVariant.String),
                  QgsField("Ny Tid",  QVariant.String),
                  QgsField("Gl. Kote",  QVariant.String),
                  QgsField("Gl. Dato",  QVariant.String),
                  QgsField("Gl. Tid",  QVariant.String)])
    layer.updateFields() 
    
    #definere variable til at gemme features i
    pt = QgsFeature()

    #looper igennem liste med punkt koordinater
    for i in range(len(pointlist_1)):
        val2 = pointlist_1[i][2] #x-koordinat
        val1 = pointlist_1[i][3] #y-koordinat
        point1 = QgsPointXY(float(val1),float(val2))  #gemmer punkter i variable
        pt.setGeometry(QgsGeometry.fromPointXY(point1)) #definere features til vores variable som punkter
        #looper igennem difflist_3 og tilføjer information fra denne liste til punkter
        for j in range(len(difflist_3)):
            for k in range(len(temp2)): #der er to statements her et er for punkter med information og det andet er for punkter uden.
                if difflist_3[j][0]==pointlist_1[i][1]:
                    pt.setAttributes([pointlist_1[i][0],difflist_3[j][0],pointlist_1[i][4],difflist_3[j][5],difflist_3[j][8],difflist_3[j][1],difflist_3[j][2],difflist_3[j][3],difflist_3[j][4],difflist_3[j][6],difflist_3[j][7]])
                elif pointlist_1[i][1]==temp2[k]:
                    pt.setAttributes([pointlist_1[i][0],pointlist_1[i][1],pointlist_1[i][4],'NULL','NULL','NULL','NULL','NULL','NULL','NULL','NULL'])
                            
        pr.addFeatures([pt]) #tilføjer punkter+attributer til ny feature variable
        layer.updateExtents() #opdatere map extent
        QgsProject.instance().addMapLayers([layer]) #tilføjer lag til canvas


#Her defineres hvilket del af programmet der skal køre og i hvilken rækkefølge.
#Desunden opsættes eventuelle afhængigheder for hver del, hvis der er noget der skal være opfyldt for delen køre.
#Der gives en fejl tilbage til brugen hvis inputfilpoint ikke er udfyldt, det er det eneste krav til at scriptet kan køre.
if inputfilepoint != '': #kører hvis felet er udfyldt i starten af scriptet
    point_edit()
    
if inputfilepoint == '': #giver en fejlmeddelse hvis feltet ikke er udfyldt
    print ('Error: Inputfil mangler')
    
if inputfilepoint != '': #køre linje delen af scriptet hvis bare inputfilepoint er udfyldt
    line_edit()
    
if inputdifffile !='': #køre kun hvis inputdifffil er udfyldt
    diff_edit()

if inputfilepoint != '': #køre linje delen af scriptet hvis bare inputfilepoint er udfyldt (virker kun i qgis, denne del skal udkommenteres hvis det køres i editor)
    qgis_line()
    
if inputfilepoint != '': #køre punkt delen af scriptet hvis bare inputfilepoint er udfyldt (virker kun i qgis, denne del skal udkommenteres hvis det køres i editor)
    qgis_point ()

if inputdifffile !='': #køre diff delen af scriptet hvis inputdifffil er udfyldt (virker kun i qgis, denne del skal udkommenteres hvis det køres i editor)
    qgis_diff()
  

