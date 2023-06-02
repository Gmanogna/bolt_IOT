import json,time,conf,requests                                                         
from boltiot import Bolt,Sms                                            
def getdetails():      
    url="https://api.openweathermap.org/data/2.5/air_pollution/history?lat=28.7041&lon=77.1025&start=1606223>    
    response=requests.request('GET',url)                                                                 
    response=json.loads(response.text)                                                              
    AQI=response["list"][-1]['main']['aqi']                                           
    co=response['list'][-1]['components']['co']                                   
    no=response['list'][-1]['components']['no']                              
    no2=response['list'][-1]['components']['no2']                         
    o3=response['list'][-1]['components']['o3']                   
    so2=response['list'][-1]['components']['so2']               
    pm2_5=response['list'][-1]['components']['pm2_5']          
    pm10=response['list'][-1]['components']['pm10']         
    nh3=response['list'][-1]['components']['nh3']        
    return [AQI,co,no,no2,o3,so2,pm2_5,pm10,nh3]      
  
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)                    
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)      
get=getdetails()                                                 
try:                                                  
    print("AQI INDEX of the place is",get[0])      
    print("CO of the place in ug/m3--",get[1])  
    print("NO of the place in ug/m3--",get[2])   
    print("NO2 of the place in ug/m3--",get[3])
    print("O3 of the place in ug/m3--",get[4])  
    print("SO2 of the place in ug/m3--",get[5]) 
    print("PM2_5 of the place in ug/m3--",get[6])  
    print("PM10 of the place in ug/m3--",get[7])   
    print("NH3 of the place in ug/m3 --",get[8])   
    if get[0]==1:                 
        print("Air Quality : GOOD") 
    elif get[0]==2:  
        print("Air Quality : FAIR")  
    elif get[0]==3:       
        print("Air Quality : MODERATE")        
        print("sending sms")          
        response=sms.send_sms("AQI is "+str(get[0])+" --UNHEALTHY FOR SENSITIVE GROUPS")      
        print("status of sms",response.status)                                      
    elif get[0]==4:                     
        print("Air Quality : POOR")       
        print("sending sms")              
        response=sms.send_sms("AQI is "+str(get[0])+" --UNHEALTHY")       
        print("status of sms",response.status)                              
    elif get[0]==5:                                                     
        print("Air Quality : HAZARDOUS")       
        print("sending sms")                   
        response=sms.send_sms("AQI is "+str(get[0])+" --VERY UNHEALTHY")   
        print("status of sms",response.status)                             
except Exception as e:                                     
    print("error,",e)
if get[0]>=4:    
    try:      
        response=mybolt.digitalWrite('0',"HIGH")      
        print(response)                            
        print("buzzer ON")                         
        time.sleep(5)                              
        response=mybolt.digitalWrite('0','LOW')   
        print(response)      
        print("buzzer OFF")                       
except Exception as e:    
    print("error details:",e)