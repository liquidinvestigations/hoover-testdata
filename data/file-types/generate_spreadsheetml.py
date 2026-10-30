"""Write the synthetic SpreadsheetML 2003 samples into spreadsheetml/.

Run from this folder with Python 3. The output bytes are the same on each run.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spreadsheetml")

WORKBOOK = """<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
 <Worksheet ss:Name="Orders">
  <Table>
   <Row>
    <Cell><Data ss:Type="String">Order</Data></Cell>
    <Cell><Data ss:Type="String">Customer</Data></Cell>
    <Cell><Data ss:Type="String">Amount</Data></Cell>
    <Cell><Data ss:Type="String">Date</Data></Cell>
    <Cell><Data ss:Type="String">Paid</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="Number">1001</Data></Cell>
    <Cell><Data ss:Type="String">Example Trading Ltd</Data><Comment><Data>Invented name</Data></Comment></Cell>
    <Cell><Data ss:Type="Number">1250.5</Data></Cell>
    <Cell><Data ss:Type="DateTime">2024-03-01T00:00:00.000</Data></Cell>
    <Cell><Data ss:Type="Boolean">1</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="Number">1002</Data></Cell>
    <Cell ss:HRef="https://example.org/customer/2"><ss:Data ss:Type="String" xmlns="http://www.w3.org/TR/REC-html40"><B>Sample</B> Imports</ss:Data></Cell>
    <Cell ss:Index="4"><Data ss:Type="DateTime">2024-03-02T09:30:00.000</Data></Cell>
    <Cell><Data ss:Type="Boolean">0</Data></Cell>
   </Row>
   <Row ss:Index="6">
    <Cell ss:MergeAcross="1"><Data ss:Type="String">Total</Data></Cell>
    <Cell ss:Formula="=SUM(R[-4]C:R[-1]C)"><Data ss:Type="Number">1250.5</Data></Cell>
    <Cell><Data ss:Type="Error">#N/A</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
 <Worksheet ss:Name="Notes">
  <Table>
   <Row><Cell><Data ss:Type="String">Second sheet</Data></Cell></Row>
  </Table>
 </Worksheet>
</Workbook>
"""

ENTITY_EXPANSION = """<?xml version="1.0"?>
<!DOCTYPE Workbook [
 <!ENTITY a "aaaaaaaaaa">
 <!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">
]>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Worksheet ss:Name="Sheet1"><Table><Row><Cell><Data ss:Type="String">&b;</Data></Cell></Row></Table></Worksheet>
</Workbook>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, text in (("synthetic-workbook.xml", WORKBOOK),
                       ("synthetic-workbook-saved-as.xls", WORKBOOK),
                       ("doctype-entities.xml", ENTITY_EXPANSION)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\r\n") as f:
            f.write(text)


if __name__ == "__main__":
    main()
