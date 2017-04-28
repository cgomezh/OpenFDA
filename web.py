#Practica7
#Copyright <2017> <CLAUDIA GOMEZ>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this
#software and associated documentation files (the "Software"), to deal in the Software
#without restriction, including without limitation the rights to use, copy, modify, merge,
#publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to
#whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or
#substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import http.server
import http.client
import json
import socketserver

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"

    def get_main_page(self):
        html="""
        <html>
            <head>
                <title>OpenFDA  Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <input type="submit" value="Medicinal Product">
                    <input type="text"  name="limit"></input>
                    </input>
                </form>
                <form method="get" action="searchDrug">
                    <input type="text"  name="drug"></input>
                    <input type="submit" value="Drud Search in OpenFDA">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type="submit" value="Companies">
                    <input type="text"  name="limit"></input>
                    </input>
                </form>
                <form method="get" action="searchCompany">
                    <input type="text"  name="company"></input>
                    <input type="submit" value="Company Search in OpenFDA">
                    </input>
                </form>
                <form method="get" action="patientsex">
                    <input type="submit" value="patiensex">
                    <input type="text"  name="limit"></input>
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def limit(self):
        url=self.path
        url1=url.split("=")
        limit=url1[1]
        if limit=='':
            limit=10
        return limit

    def read_data(self):
        limit=self.limit()
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)  #se pone self porque la constante OPENFDA_API_URL esta definida dentro de la clase
        conn.request("GET",self.OPENFDA_API_EVENT +"?limit="+str(limit))
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        #200 OK
        data1 = r1.read()          # This will return entire content.
        data=data1.decode("utf8")  #Para decodifiar y que quede en string y poder leerlo en la terminal
        return data

    def get_event(self):
        data=self.read_data()
        event=json.loads(data)
        results=event["results"]
        return results
#LISTA DE MEDICAMENTOS
    def get_med_list(self, results):
        lista=[]
        for event in results:
            patient=event["patient"]
            drug=patient["drug"]
            medicinal_product=drug[0]["medicinalproduct"]
            lista+=[medicinal_product]
        return lista

    def get_medicinal_product(self,lista):
        s=''
        for med in lista:
            s+="<li>"+med+"</li>"     # li para añadir un trozo
        html2="""
        <html>
            <head>
                <title>Medicinal Product</title>
            </head>
            <body>
                <h1>Medicinal Product</h1>
                <ul>
                    %s
                </ul>
            </body>
        </html>""" %(s)
        return html2
#LISTA DE COMPAÑIAS
    def get_company_list(self, results):
        listac=[]
        for event in results:
            listac.append(event["companynumb"])
        return listac

    def get_companies(self,listac):
        s=''
        for med in listac:
            s+="<li>"+med+"</li>"     # li para añadir un trozo
        html3="""
        <html>
            <head>
                <title>Companies</title>
            </head>
            <body>
                <h1>Companies</h1>
                <ul>
                    %s
                </ul>
            </body>
        </html>""" %(s)
        return html3

    def get_companies_from_events (self, data):
        data=self.search_drug()
        events=data
        event=json.loads(events)
        results=event["results"]
        companies=[]
        for event in results:
            companies.append(event["companynumb"])
        return companies


    def get_companies_names(self, companies):
        s=''
        for drug in companies:
            s+="<li>"+drug+"</li>"
        html4="""
        <html>
            <head>
                <title> companies </title>
            </head>
            <body>
                <h1>Companies names</h1>
                <ul>
                    %s
                </ul>
            </body>
        </html3>""" %(s)
        return html4

    def search_drug(self):
        url=self.path
        url1=url.split("=")
        drug=url1[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_EVENT +"?limit=10"+'&search=patient.drug.medicinalproduct:'+drug)
        r1 = conn.getresponse()
        data1 = r1.read()
        data=data1.decode("utf8")
        return data

#BUSCAR MEDICAMENTO A PARTIR DE COMPAÑIA
    def search_company(self):
        url=self.path
        url1=url.split("=")
        company=url1[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_EVENT +"?limit=10"+'&search=patient.drug.medicinalproduct:'+company)
        r1 = conn.getresponse()
        data1=r1.read()
        datac=data1.decode("utf8")
        return datac

    def get_drug_from_events(self,datac):
        datac=self.search_company()
        events=datac
        event=json.loads(events)
        results=event["results"]
        drugs=[]
        for event in results:
            patient=event["patient"]
            drug=patient["drug"]
            medicinal_product=drug[0]["medicinalproduct"]
            drugs.append(medicinal_product)
        return drugs

    def get_drug_names(self,drugs):
        s=''
        for drug in drugs:
            s+="<li>"+drug+"</li>"
        html5="""
        <html>
            <head>
                <title> drugs </title>
            </head>
            <body>
                <h1>Drugs names</h1>
                <ul>
                    %s
                </ul>
            </body>
        </html5>""" %(s)
        return html5

#SEXO DEL PACIENTE
    def patientsex(self,results):
        patient_list=[]
        for event in results:
            patient=event["patient"]
            patient_sex=patient["patientsex"]
            patient_list+=patient_sex
        return patient_list

    def get_patient_sex(self, patient_list):
        s=''
        for sex in patient_list:
            s+="<li>"+sex+"</li>"
        html6="""
        <html>
            <head>
                <title>Patient Sex</title>
            </head>
            <body>
                <h1>Patient Sex</h1>
                <ul>
                    %s
                </ul>
            </body>
        </html>"""%(s)

        return html6

    def do_GET(self):
        main_page=False
        is_drug=False
        is_companies=False
        is_search_companies=False
        is_search_drugs=False
        is_patient_sex=False
        if self.path=="/":
            main_page=True
        elif "/listDrugs?" in self.path:
            is_drug=True
        elif "/listCompanies?" in self.path:
            is_companies=True
        elif "/searchDrug" in self.path:
            is_search_companies=True
        elif "/searchCompany" in self.path:
            is_search_drugs=True
        elif "/patientsex?" in self.path:
            is_patient_sex=True
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        #event=json.loads(data)

        if main_page:
            html=self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_drug:
            limit=self.limit()
            results=self.get_event()
            lista=self.get_med_list(results)
            html2=self.get_medicinal_product(lista)
            self.wfile.write(bytes(html2, "utf8"))
        elif is_search_companies:
            data=self.search_drug()
            companies=self.get_companies_from_events(data)
            html4=self.get_companies_names(companies)
            self.wfile.write(bytes(html4, "utf8"))
        elif is_companies:
            limit=self.limit()
            results=self.get_event()
            listac=self.get_company_list(results)
            html3=self.get_companies(listac)
            self.wfile.write(bytes(html3, "utf8"))
        elif is_search_drugs:
            datac=self.search_company()
            drugs=self.get_drug_from_events(datac)
            html5=self.get_drug_names(drugs)
            self.wfile.write(bytes(html5, "utf8"))
        elif is_patient_sex:
            results=self.get_event()
            patient_list=self.patientsex(results)
            html6=self.get_patient_sex(patient_list)
            self.wfile.write(bytes(html6, "utf8"))
