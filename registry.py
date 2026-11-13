# Elenco dei paesi: per aggiungerne uno, aggiungi una riga qui e (se vuoi dati automatici)
# crea collectors/<codice minuscolo>.py con una funzione collect().
# region: europe | asia | americas | oceania | africa
COUNTRIES = [
 # code, slug, region, nome IT, nome EN, ente fonte, url fonte
 ("AT","austria","europe","Austria","Austria","Statistik Austria","https://www.statistik.at/statistiken/tourismus-und-verkehr/fahrzeuge/kfz-neuzulassungen"),
 ("BE","belgium","europe","Belgio","Belgium","SPF Mobilité","https://mobilit.belgium.be/fr/documents/open-data/transport-routier/immatriculations-des-vehicules"),
 ("FR","france","europe","Francia","France","SDES","https://www.statistiques.developpement-durable.gouv.fr/immatriculation-des-vehicules-routiers?rubrique=58"),
 ("DE","germany","europe","Germania","Germany","KBA","https://www.kba.de/DE/Statistik/Produktkatalog/produkte/Fahrzeuge/fz8/fz8_gentab.html"),
 ("IT","italy","europe","Italia","Italy","UNRAE","https://unrae.it/dati-statistici/immatricolazioni"),
 ("LU","luxembourg","europe","Lussemburgo","Luxembourg","STATEC","https://lustat.statec.lu/"),
 ("NL","netherlands","europe","Paesi Bassi","Netherlands","RDW","https://opendata.rdw.nl/"),
 ("NO","norway","europe","Norvegia","Norway","OFV","https://ofv.no/"),
 ("PT","portugal","europe","Portogallo","Portugal","ACAP","https://www.acap.pt/pt/estatisticas"),
 ("ES","spain","europe","Spagna","Spain","DGT","https://www.dgt.es/"),
 ("SE","sweden","europe","Svezia","Sweden","SCB","https://www.scb.se/"),
 ("CH","switzerland","europe","Svizzera","Switzerland","Ufficio federale di statistica","https://www.bfs.admin.ch/"),
 ("JP","japan","asia","Giappone","Japan","JADA","https://www.jada.or.jp/pages/342/"),
 ("KR","southkorea","asia","Corea del Sud","South Korea","MOTIR","https://www.motir.go.kr/"),
 ("SG","singapore","asia","Singapore","Singapore","LTA","https://www.lta.gov.sg/"),
 ("TH","thailand","asia","Thailandia","Thailand","Thailand Automotive Institute","https://data.thaiauto.or.th/"),
 ("CN","china","asia","Cina","China","CPCA","http://www.cpcaauto.com/"),
 ("IN","india","asia","India","India","VAHAN (MoRTH)","https://vahan.parivahan.gov.in/vahan4dashboard/"),
 ("NZ","newzealand","oceania","Nuova Zelanda","New Zealand","Ministry of Transport","https://www.transport.govt.nz/statistics-and-insights/fleet-statistics/"),
 ("US","usa","americas","Stati Uniti","United States","Cox Automotive / Argonne (stime)","https://www.anl.gov/esia/light-duty-electric-drive-vehicles-monthly-sales-updates"),
]
REGIONS = {"europe":("Europa","Europe"),"asia":("Asia Pacifica","Asia Pacific"),
           "americas":("Americhe","Americas"),"oceania":("Oceania","Oceania"),"africa":("Africa","Africa")}
