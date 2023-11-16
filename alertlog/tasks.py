
import datetime
import requests
from django.db.models import Q
import mysql.connector
from datetime import date, datetime, timedelta
from multiprocessing import Pool
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from .models import *
from django.contrib.auth.models import User

channel_layer = get_channel_layer()

@shared_task
def get_joke():
    connection_db2 = mysql.connector.connect(
        host="192.168.9.25",
        user="alert",
        password="P@ssword1234560",
        database="Alertsystem"
    )
    cursor_db2 = connection_db2.cursor()
    cursor_db2.execute("SELECT * FROM alertlog_roles")
    db2_data = cursor_db2.fetchall()


    for row in db2_data:
        process_row(row)
   

    # Bağlantıyı kapatma
    cursor_db2.close()
    connection_db2.close()

def delete_logs(logs_id,cursor_db1,connection_db1):
    delete_query = "DELETE FROM table_kiber WHERE id  = %s"
    print("delete  gecdi" )
    for log in logs_id:
        cursor_db1.execute(delete_query, log)
        print("delete ID :", log)
        connection_db1.commit()

def process_row(row):
    # db1 bağlantısı
    connection_db1 = mysql.connector.connect(
        host="192.168.0.254",
        user="kiber",
        password="kibeR@2023@Kiber",
        database="logsdb"
    )
    cursor_db1 = connection_db1.cursor()
    cursor_db1_1 = connection_db1.cursor()

    connection_db2 = mysql.connector.connect(
        host="192.168.9.25",
        user="alert",
        password="P@ssword1234560",
        database="Alertsystem"
    )
    cursor_db2 = connection_db2.cursor()

    print("my row  ", row)
    role_name = row[1]
  
    description = row[2]
    severity_in = row[3]
    application_role = row[4]
    index_number = row[5]
    split_character = row[6]
    start_message = row[7]
    severity_out = row[8]
    own_text = row[9]

    delete_log = "SELECT id FROM table_kiber LIMIT 10"
    cursor_db1_1.execute(delete_log)
    logs_id = cursor_db1_1.fetchall()
    #print(type(logs_id), "id  =", logs_id)

    if start_message:
        #print("ookokk")
        cursor_db1.execute("SELECT id, hostname, severity, facility, application, message, timestamp FROM table_kiber WHERE severity = %s  AND application = %s AND  message LIKE %s AND message LIKE %s LIMIT 10", (severity_in, application_role, (description+"%"), ("" + start_message + "%")))
        filtered_data = cursor_db1.fetchall()
        print(" filterdata : ", filtered_data)

    else:
        cursor_db1.execute("SELECT id, hostname, severity, facility, application, message, timestamp FROM table_kiber WHERE severity = %s  AND application = %s AND  message LIKE  %s LIMIT 10", (severity_in, application_role, description+"%"))
        filtered_data = cursor_db1.fetchall()
        print(" filterdata2 : ", filtered_data)

    # Verileri db2.filterlog tablosuna yazma
    for filtered_row in filtered_data[:10]:
        id, hostname, severity, facility, application, message, timestamp = filtered_row
        my_message = " "
        if index_number:
            my_message = message.split(split_character)
            my_message = my_message[int(index_number)]
            #print("test ip  ", my_message)
        else:
            my_message = message

        text_message = my_message + "   " + own_text
      
        
        postdata(hostname, severity_out, facility, application, message, timestamp, role_name, text_message)

        print("yazgy gosuldy")
        connection_db2.commit()

    #pool = Pool(daemon=False)
   # pool.apply_async(
        delete_logs(logs_id,cursor_db1,connection_db1)
 
    cursor_db1.close()
    connection_db1.close()
    cursor_db2.close()
    connection_db2.close()
    print ("islem dyndy")
    
    
    
def postdata(hostname,severity,facility,application,message,timestamp,role, text_message):
    print("postdata, gecdi")
    usersss=[1,2]
    try:
    
        url = "http://192.168.9.129:8088/logs"
        
        data = {
        "hostname": hostname,
        "severity": severity,
        "facility": facility,
        "application": application,
        "message": message,
        "timestamp": timestamp.isoformat(),
        "role": role,
        "is_know": False,
        "text_message":text_message,
        "users":usersss
        }
        
        users = User.objects.filter(id__in=usersss).values('username')
       
        for user in users:

            user_data = {'type': 'chat_message', 'message': data, 'username': user['username'], 'room': user['username']}

            async_to_sync(channel_layer.group_send)('chat_'+user['username'], user_data) 
        # for user in users:
        #     async_to_sync(channel_layer.group_send)('chat_'+user,{'type':'chat_message','message':data,'username':'user','room':user})    
        
        # async_to_sync(channel_layer.group_send)('chat_admin',{'type':'chat_message','message':data,'username':'user','room':'admin'})
        # async_to_sync(channel_layer.group_send)('chat_test',{'type':'chat_message','message':data,'username':'user','room':'test'})

        print("benim data jsonlarym, ", data)
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("POST isteği başarılı!")
        else:
            print("POST isteği başarısız. Hata kodu:", response.status_code)
    except KeyError:
        print(KeyError)

@shared_task
def countdata():        
        today = datetime.now().date()
        today1 = date.today()
        last_month = today - timedelta(days=30)         
        today1 = date.today()
        start_of_week = today1 - timedelta(days=today1.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        
        
        alldatamonth = Filterlog.objects.all().filter(Q(timestamp__gte=last_month) & Q(timestamp__date__lte=today1) & Q(is_know =False))
        allcountmonth = alldatamonth.count()
        warning_month = alldatamonth.filter(severity__icontains='warning').count()
        info_month = alldatamonth.filter(severity__icontains='info').count()
        error_month = alldatamonth.filter(severity__icontains='ERR').count()
        
        response_month= {
        'total_month' : allcountmonth,
        'warning_month': warning_month,
        'info_month': info_month,
        'error_month': error_month,           
        }
         
            
  
        print("week gecdi")
        alldata_week = Filterlog.objects.filter(Q(timestamp__date__range=(start_of_week, end_of_week)) & Q(is_know =False))
        #alldata = Filterlog.objects.all().filter(Q(timestamp__gte=last_week) & Q(timestamp__lte=today))
        allcount_week = alldata_week.count()
        warning_week = alldata_week.filter(severity__icontains='warning').count()
        info_week = alldata_week.filter(severity__icontains='info').count()
        error_week = alldata_week.filter(severity__icontains='ERR').count()
        
        response_week = {
        'total_week' : allcount_week,
        'warning_week': warning_week,
        'info_week': info_week,
        'error_week': error_week,           
        }
        
        
    
   
        
        alldata_day = Filterlog.objects.filter(timestamp__range=(start_of_day, end_of_day),is_know =False)
        #alldata = Filterlog.objects.all().filter(Q(timestamp__date=today))
        allcount_day = alldata_day.count()
        warning_day = alldata_day.filter(severity__icontains='warning').count()
        info_day = alldata_day.filter(severity__icontains='info').count()
        error_day = alldata_day.filter(severity__icontains='ERR').count()
        print(alldata_day)
        
        response_day = {
        'total_day' : allcount_day,
        'warning_day': warning_day,
        'info_day': info_day,
        'error_day': error_day,           
        }
        

        
        async_to_sync(channel_layer.group_send)('countdata',{'type':'send_data','text':[response_day,response_week,response_month]})
        
        
      
        