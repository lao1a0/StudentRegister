import pymysql
import xlwt
import subprocess
import datetime
import time

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
    cursor.execute("select * from {} where 体温 between 35 and 37.2".format(table))
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
    now_time =  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    excelName = savePath+"table_{}_{}.xls".format(table,now_time)
    #print(">>"+excelName)
    if excelResult != '':
        excelName = excelResult
    excel.save(excelName)
    return excelName
def Mix():
    excelName = mysql2excel("test","user","/home/pi/Documents/")
    #print(excelName)
    time.sleep(0.3)
    cmd = "libreoffice {}".format(excelName)
    subprocess.call(cmd,shell=True)
if __name__ == "__main__":
    Mix()
