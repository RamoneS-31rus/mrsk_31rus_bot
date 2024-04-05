import datetime, requests

from api import url_planned, url_emergency, url_unplanned

def set_format(data):
    if data and isinstance(data, list):
        if 'ScheduledTimeRemoval' not in data[0]:            
            data = [{'name': x['DisconnectionObject'].replace('Белгород г;', '').replace('\n\n', '\n').strip(),
                     'time_down': datetime.datetime.strptime(x['DisconnectionDateTime'].replace('T', ' '),
                                                             '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y %H:%M"),
                     'time_up': datetime.datetime.strptime(x['EnergyOnPlanningDateTime'].replace('T', ' '),
                                                           '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y %H:%M")} for x in data]              
        else:            
            data = [{'name': x['StreetHome'],
                     'time_up': datetime.datetime.strptime(x['ScheduledTimeRemoval'].replace('T', ' '),
                                                           '%Y-%m-%d %H:%M:%S').strftime("%d.%m.%Y %H:%M")} for x in data]
    return data


def get_data_category(data):
    text = ""
    data = set_format(data)         
    
    if isinstance(data, list) and 'time_down' in data[0]:
        for i in data:           
            name = i['name']
            time_down = i['time_down']
            time_up = i['time_up']
            text = text + f"{name}\nОтключение с {time_down} по {time_up}\n {'- '*30}\n"
    elif isinstance(data, list) and 'time_down' not in data[0]:
        for i in data:
            name = i['name']
            time_up = i['time_up']
            text = text + f"{name}\n<b>Отключение до {time_up}</b>\n {'- '*30}\n"
    return text


def get_data_search(data, street):
    text = ""
    data = set_format(data)        
    
    if isinstance(data, list) and 'time_down' in data[0]:
        for i in data:
            if street in i['name']:
                name = i['name']
                time_down = i['time_down']
                time_up = i['time_up']
                text = text + f"{name}\n<b>Отключение с {time_down} по {time_up}</b>\n {'- '*30}\n"  
    elif isinstance(data, list) and 'time_down' not in data[0]:
        for i in data:
            if street in i['name']:
                name = i['name']
                time_up = i['time_up']
                text = text + f"{name}\n<b>Отключение до {time_up}</b>\n {'- '*30}\n"    
    return text


def get_data_planned():
    response = requests.get(url_planned)     
    data = get_data_category(response.json())    
    return data
    

def get_data_emergency():
    response = requests.get(url_emergency)    
    data = get_data_category(response.json())    
    return data


def get_data_unplanned():
    response = requests.get(url_unplanned)    
    data = get_data_category(response.json())    
    return data


def get_data_search_planned(street):     
    response = requests.get(url_planned)
    data = get_data_search(response.json(), street)        
    return data    


def get_data_search_emergency(street):      
    response = requests.get(url_emergency)
    data = get_data_search(response.json(), street)    
    return data


def get_data_search_unplanned(street):      
    response = requests.get(url_unplanned)
    data = get_data_search(response.json(), street)    
    return data
