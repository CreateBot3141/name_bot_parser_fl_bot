def get_message (user_id,namebot,text1,text2,href,name,categoriya,name_find):
    import iz_telegram
    import datetime
    url = 'https://www.fl.ru'
    message_out,menu = iz_telegram.get_message (user_id,'Информационное сообщение',namebot)
    message_out = message_out.replace('%%href%%',url+str(href))
    message_out = message_out.replace('%%text1%%',str(text1))
    message_out = message_out.replace('%%name%%',str(name))
    message_out = message_out.replace('%%text2%%',str(text2))
    message_out = message_out.replace('%%categoriya%%',str(categoriya))
    message_out = message_out.replace('%%time%%',str(datetime.datetime.now()))
    message_out = message_out.replace('%%name_find%%',str(name_find))
    markup = ''
    return message_out,markup


def find_name_in_message (text1,text2,href,name,categoriya,name_find):
    name_find = name_find.replace('_',' ')
    message_out = ''
    markup      = ''
    label       = 'не найдено'
    if name.upper().find  (name_find.upper()) != -1:
        label = 'Найдено'
    if text1.upper().find (name_find.upper()) != -1:
        label = 'Найдено'
    if text2.upper().find (name_find.upper()) != -1:
        label = 'Найдено'
    return label

def get_list_find_name_in_message (namebot,user_id,text1,text2,href,name,categoriya):
    import iz_func
    db,cursor = iz_func.connect ()
    list_key = ''
    label    = '' 
    nomer = 0
    sql = "select id,name from parser_fl_bot_task where status <> 'delete' and user_id = '"+str(user_id)+"' and name <> '';"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:         
        id,name_find = rec.values ()
        name_find = name_find.replace('_',' ')
        #word = message_in.replace('list_message_','')
        answer = find_name_in_message (text1,text2,href,name,categoriya,name_find)
        if answer == 'Найдено':
            nomer = nomer + 1
            label = 'Найдено'
            if nomer > 1:
                list_key = list_key +','+ name_find
            else:    
                list_key = list_key + name_find
    return list_key,label


def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import time
    import iz_func
    import iz_telegram
    db,cursor = iz_func.connect ()
    label = ''

    if message_in.find ('/list_') != -1:      
        word = message_in.replace('/list_','')   
        sql = "select id,name from parser_fl_bot_task where user_id = '"+str(user_id)+"' and status <> 'delete' and name <> '';"
        cursor.execute(sql)
        data = cursor.fetchall()
        st = ''
        nomer = 0
        for rec in data: 
            nomer = nomer + 1
            id,name = rec.values ()
            name = name.replace('_',' ')
            if nomer > 1:
                st = st + ' or '
            st = st + "(name like '%"+str(name)+"%' or text_full like '%"+str(name)+"%' or text_smail like '%"+str(name)+"%')"
        if st != '':
            sql = "select id,name,text_full,text_smail,href,categoriya from parser_fl_bot_history where "+str(st)+" limit "+str(word)+";"
        else:    
            sql = "select id,name,text_full,text_smail,href,categoriya from parser_fl_bot_history where 1=1 limit "+str(word)+";"
     
        cursor.execute(sql)
        data_answer = cursor.fetchall()
        for rec_answer in data_answer: 
            id,name,text_full,text_smail,href,categoriya = rec_answer.values ()
            name_find  = 'нет данных'
            name_find,label = get_list_find_name_in_message (namebot,user_id,text_full,text_smail,href,name,categoriya)
            message_out,markup = get_message (user_id,namebot,iz_func.change_back (text_smail),iz_func.change_back (text_full),href,iz_func.change_back (name),categoriya,name_find) 
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        label = 'no send'


    if message_in == '/cancel':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Отмена ввода слова','S',0)
        label = 'no send'
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        label = 'no send'

    if message_in.find ('/start') != -1:
        iz_func.save_variable (user_id,"status","",namebot)
        iz_telegram.language (namebot,user_id)
        status = ''
        label = 'no send'

    if message_in.find ('Отмена') != -1:
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'ОтменаЗапуск','S',0)
        label = 'no send'

    if message_in == 'Добавить':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Кнопка Добавить','S',0)
        label = 'no send'
        iz_func.save_variable (user_id,"status","Ввод нового слова",namebot)

    if message_in == 'История':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Кнопка История','S',0)
        label = 'no send'

    if message_in == 'Список поиска' or message_in == '/find':        
        #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Кнопка Список поиска','S',0)
        message_out,menu = iz_telegram.get_message (user_id,'Кнопка Список поиска',namebot)
        sql = "select id,name from parser_fl_bot_task where user_id = '"+str(user_id)+"' and status <> 'delete';"
        cursor.execute(sql)
        data = cursor.fetchall()
        snrong = ''
        nomer = 0
        for rec in data: 
            nomer = nomer + 1
            id,name = rec.values ()
            snrong = snrong + '<code>'+str(nomer) +') '+ name +'</code>      (/delete_'+str(id)+')\n'
        message_out = message_out.replace('%%snrong%%',str(snrong))
        markup = '' 
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        label = 'no send'

    if message_in.find ('/delete_') != -1:
        word  = message_in.replace('/delete_','')
        sql = "select id,name from parser_fl_bot_task where id = '"+str(word)+"';"
        cursor.execute(sql)
        data = cursor.fetchall()
        name = ''
        for rec in data: 
            id,name = rec.values ()
        #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Корректировка значени','S',0)
        message_out,menu = iz_telegram.get_message (user_id,'Корректировка значени',namebot)
        message_out      = message_out.replace('%%СловоПоиска%%',str(name))
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        sql = "UPDATE parser_fl_bot_task SET status = 'delete' WHERE `id` = '"+str(word)+"' and user_id = '"+str(user_id)+"'"
        cursor.execute(sql)
        db.commit() 
        label = 'no send'       

    if message_in.find ('Контакты') != -1:
        label = 'no send'  
        message_out,markup = iz_telegram.get_kontakt (user_id,namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)

    if status == '' and label == '':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'В моем арсенале нет такой команды','S',0)

    if status == 'Ввод нового слова':
        if label != 'no send':
            iz_func.save_variable (user_id,"status","",namebot)
            #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Новое слово записано','S',0)
            message_out,menu = iz_telegram.get_message (user_id,'Новое слово записано',namebot)
            message_out      = message_out.replace('%%СловоПоиска%%',str(message_in))
            markup = ''
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
            label = 'no send'
            sql = "INSERT INTO parser_fl_bot_task (`name`,`namebot`,`status`,`user_id`) VALUES ('{}','{}','{}','{}')".format (message_in,namebot,'',user_id)
            cursor.execute(sql)
        else:    
            iz_func.save_variable (user_id,"status","",namebot)
        db.commit()




