import pymysql
import xlwt
import subprocess
def getConn(database='test'):
    args = dict(
        host='localhost',
        user='root',
        passwd='123',
        db=database,
        charset='utf8'
    )
    conn = pymysql.connect(**args)
    return conn

def mysql2excel(database='test',table='user',savePath='.',excelResult = ''):
    conn = getConn(database)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    data_list = cursor.fetchall()
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("sheet1")
    row_number = len(data_list)
    column_number = len(cursor.description)
    for i in range(column_number):
        sheet.write(0,i,cursor.description[i][0])
    for i in range(row_number):
        for j in range(column_number):
            sheet.write(i+1,j,data_list[i][j])
    excelName = savePath+"mysql_{}_{}.xls".format(database,table)
    if excelResult != '':
        excelName = excelResult
    excel.save(excelName)
    return excelName

if __name__ == "__main__":
    excelName = mysql2excel("test","user","/home/pi/Documents/")
    cmd = "libreoffice --pt {}".format("/home/pi/Documents/"+excelName)
    subprocess.call(cmd,shell=True)