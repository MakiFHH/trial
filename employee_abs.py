import xml.etree.ElementTree as Xet
import requests
import io
import base64
import pandas as pd

url = "https://fa-emmq-saasfaprod1.fa.ocs.oraclecloud.com/xmlpserver/services/PublicReportService?wsdl"
user='BITEAM'
pas='Fusion@123'
Headers = {'content-type': 'text/xml', 'SOAPACTION': ''}
SoapQueryRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService">
<soapenv:Header/>
<soapenv:Body> <pub:runReport> 
<pub:reportRequest>
    <pub:attributeFormat>xml</pub:attributeFormat>
    <pub:attributeLocale>en-US</pub:attributeLocale>
    <pub:reportAbsolutePath>/Custom/HCM/employee_abs_list.xdo</pub:reportAbsolutePath>
</pub:reportRequest>
<pub:userID>"""+user+"""</pub:userID>
<pub:password>"""+pas+"""</pub:password>
</pub:runReport> </soapenv:Body>
</soapenv:Envelope>"""
response = requests.post(url, data=SoapQueryRequest, headers=Headers)
st = (response.content)

outputXML = open("employee_abs_list.xml", "w")
str = st.decode('utf-8')

outputXML.write(str)
outputXML.close()

readXML = open("employee_abs_list.xml", "r")

for line in readXML.readlines():
    if 'reportBytes' in line:
        x = line.split('reportBytes')[1]
        x = x.replace('>', '')
        x = x.replace('</', '')

        finalOutput = base64.b64decode(x)
        finalOutput = finalOutput.decode('utf-8')

        outputNewXML = io.open("employee_abs_list_final.xml", "w", encoding="utf-8")
        outputNewXML.write(finalOutput)

        cols = ["COUNTRY",	"PERSON_NUMBER",	"FULL_NAME",	"PER_ABSENCE_ENTRY_ID",	"ABSENCE_TYPE_ID",	"ABSENCE_TYPE",	"START_DATE",	"END_DATE",	"DURATION",	"CREATION_DATE",	"ABSENCE_STATUS_CD",	"APPROVAL_STATUS_CD"]
        rows = []

        xmlparse = Xet.parse('employee_abs_list_final.xml')

        root = xmlparse.getroot()
        for i in root:
            COUNTRY = getattr(i.find("COUNTRY"), "text", None)
            PERSON_NUMBER = getattr(i.find("PERSON_NUMBER"), "text", None)
            FULL_NAME = getattr(i.find("FULL_NAME"), "text", None)
            PER_ABSENCE_ENTRY_ID = getattr(i.find("PER_ABSENCE_ENTRY_ID"), "text", None)
            ABSENCE_TYPE_ID = getattr(i.find("ABSENCE_TYPE_ID"), "text", None)
            ABSENCE_TYPE = getattr(i.find("ABSENCE_TYPE"), "text", None)
            START_DATE = getattr(i.find("START_DATE"), "text", None)
            END_DATE = getattr(i.find("END_DATE"), "text", None)
            DURATION = getattr(i.find("DURATION"), "text", None)
            CREATION_DATE = getattr(i.find("CREATION_DATE"), "text", None)
            ABSENCE_STATUS_CD = getattr(i.find("ABSENCE_STATUS_CD"), "text", None)
            APPROVAL_STATUS_CD = getattr(i.find("APPROVAL_STATUS_CD"), "text", None)

            rows.append({"COUNTRY": COUNTRY,
                        "PERSON_NUMBER": PERSON_NUMBER,
                        "FULL_NAME": FULL_NAME,
                        "PER_ABSENCE_ENTRY_ID": PER_ABSENCE_ENTRY_ID,
                        "ABSENCE_TYPE_ID": ABSENCE_TYPE_ID,
                        "ABSENCE_TYPE": ABSENCE_TYPE,
                        "START_DATE": START_DATE,
                        "END_DATE": END_DATE,
                        "DURATION": DURATION,
                        "CREATION_DATE": CREATION_DATE,
                        "ABSENCE_STATUS_CD": ABSENCE_STATUS_CD,
                        "APPROVAL_STATUS_CD": APPROVAL_STATUS_CD})

        df = pd.DataFrame(rows, columns=cols)

        # Writing dataframe to csv
        df.to_csv('employees_abs.csv',index = False,encoding='utf-8')