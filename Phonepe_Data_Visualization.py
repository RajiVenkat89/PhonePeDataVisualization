import git
import os
import json
import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px

##Database connection 
client=mysql.connector.connect(host='localhost',user='root',password='root',database='phonepe')
cursor=client.cursor()

##Function to get the data cloned from Github and store it in local path. If data already available, it will skip the process
def data_collection():
    try: 
        repository_path="https://github.com/PhonePe/pulse.git"
        destination_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git"
        git.Repo.clone_from(repository_path,destination_path)
    except Exception as e:
        pass

##Function to get the State list from GeoMap
def geo_state_list():
        data=pd.read_json("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
        geo_state=[]
        for i in data['features']:
            state=i['properties']['ST_NM']
            geo_state.append(state)
        geo_state.sort(reverse=False)
        return geo_state

##Function to read the data from the folder for Aggregate- Transaction
def aggregate_transaction():
    agg_tns_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/aggregated/transaction/country/india/state/"
    agg_tns_st=os.listdir(agg_tns_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(agg_tns_st)):
        state_list[agg_tns_st[i]] = geo_state[i]
    ats={'state':[],'year':[],'quarter':[],'transaction_type':[],'transaction_count':[],'transaction_amount':[]}
    for s in agg_tns_st:        
        p_s=agg_tns_path+s+"/"
        agg_tns_yr=os.listdir(p_s)       
        for y in agg_tns_yr:            
            p_yr=p_s+y+"/"
            agg_tns_js=os.listdir(p_yr)            
            for j in agg_tns_js:                
                p_j=p_yr+j
                agg_tns_d=open(p_j,'r')
                agg_tns_dt=json.load(agg_tns_d)                
                try:
                    for i in agg_tns_dt['data']['transactionData']:
                        name=i['name']
                        count=i['paymentInstruments'][0]['count']
                        amount=i['paymentInstruments'][0]['amount']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        ats['state'].append(state)
                        ats['year'].append(y)
                        ats['quarter'].append(quarter)
                        ats['transaction_type'].append(name)
                        ats['transaction_count'].append(count)
                        ats['transaction_amount'].append(amount)
                except:
                    continue
    return ats

##Function to read the data from the folder for Aggregate- user

def aggregate_user():
    agg_usr_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/aggregated/user/country/india/state/"
    agg_usr_st=os.listdir(agg_usr_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(agg_usr_st)):
        state_list[agg_usr_st[i]] = geo_state[i]
    ausr={'state':[],'year':[],'quarter':[],'user_brand':[],'user_count':[],'user_percentage':[]}
    for s in agg_usr_st:        
        p_s=agg_usr_path+s+"/"
        agg_usr_yr=os.listdir(p_s)        
        for y in agg_usr_yr:
            p_yr=p_s+y+"/"
            agg_usr_js=os.listdir(p_yr)
            for j in agg_usr_js:
                p_j=p_yr+j
                agg_usr_d=open(p_j,'r')
                agg_usr_dt=json.load(agg_usr_d)
                try:
                    for i in agg_usr_dt['data']['usersByDevice']:
                        brand=i['brand']
                        count=i['count']
                        percentage=i['percentage']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        ausr['state'].append(state)
                        ausr['year'].append(y)
                        ausr['quarter'].append(quarter)
                        ausr['user_brand'].append(brand)
                        ausr['user_count'].append(count)
                        ausr['user_percentage'].append(percentage)
                except:
                    continue
    return ausr

##Function to read the data from the folder for Map- Transaction

def map_transaction():
    map_tns_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/map/transaction/hover/country/india/state/"
    map_tns_st=os.listdir(map_tns_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(map_tns_st)):
        state_list[map_tns_st[i]] = geo_state[i]
    mts={'state':[],'year':[],'quarter':[],'district':[],'transaction_count':[],'transaction_amount':[]}
    for s in map_tns_st:
        p_s=map_tns_path+s+"/"
        map_tns_yr=os.listdir(p_s)
        for y in map_tns_yr:
            p_yr=p_s+y+"/"
            map_tns_js=os.listdir(p_yr)
            for j in map_tns_js:
                p_j=p_yr+j
                map_tns_d=open(p_j,'r')
                map_tns_dt=json.load(map_tns_d)
                try:
                    for i in map_tns_dt['data']['hoverDataList']:
                        district=i['name'].split(' district')[0]
                        count=i['metric'][0]['count']
                        amount=i['metric'][0]['amount']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        mts['state'].append(state)
                        mts['year'].append(y)
                        mts['quarter'].append(quarter)
                        mts['district'].append(district)
                        mts['transaction_count'].append(count)
                        mts['transaction_amount'].append(amount)
                except:
                    continue
    return mts

##Function to read the data from the folder for Map- user

def map_user():
    map_usr_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/map/user/hover/country/india/state/"
    map_usr_st=os.listdir(map_usr_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(map_usr_st)):
        state_list[map_usr_st[i]] = geo_state[i]
    musr={'state':[],'year':[],'quarter':[],'district':[],'registered_users':[],'app_opens':[]}
    for s in map_usr_st:
        p_s=map_usr_path+s+"/"
        map_usr_yr=os.listdir(p_s)
        for y in map_usr_yr:
            p_yr=p_s+y+"/"
            map_usr_js=os.listdir(p_yr)
            for j in map_usr_js:
                p_j=p_yr+j
                map_usr_d=open(p_j,'r')
                map_usr_dt=json.load(map_usr_d)
                try:
                    for i_key,i_value in map_usr_dt['data']['hoverData'].items():
                        district=i_key.split(' district')[0]
                        reg_user=i_value['registeredUsers']
                        app_opens=i_value['appOpens']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"                        
                        state=state_list[s]
                        musr['state'].append(state)
                        musr['year'].append(y)
                        musr['quarter'].append(quarter)
                        musr['district'].append(district)
                        musr['registered_users'].append(reg_user)
                        musr['app_opens'].append(app_opens)
                except:
                    continue
    return musr

    ##Function to read the data from the folder for Transaction district

def top_transaction_district():
    top_tnsd_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/top/transaction/country/india/state/"
    top_tnsd_st=os.listdir(top_tnsd_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(top_tnsd_st)):
        state_list[top_tnsd_st[i]] = geo_state[i]
    ttsd={'state':[],'year':[],'quarter':[],'district':[],'transaction_count':[],'transaction_amount':[]}
    for s in top_tnsd_st:
        p_s=top_tnsd_path+s+"/"
        top_tnsd_yr=os.listdir(p_s)
        for y in top_tnsd_yr:
            p_yr=p_s+y+"/"
            top_tnsd_js=os.listdir(p_yr)
            for j in top_tnsd_js:
                p_j=p_yr+j
                top_tnsd_d=open(p_j,'r')
                top_tnsd_dt=json.load(top_tnsd_d)
                try:
                    for i in top_tnsd_dt['data']['districts']:
                        district=i['entityName']
                        count=i['metric']['count']
                        amount=i['metric']['amount']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]    
                        ttsd['state'].append(state)
                        ttsd['year'].append(y)
                        ttsd['quarter'].append(quarter)
                        ttsd['district'].append(district)
                        ttsd['transaction_count'].append(count)
                        ttsd['transaction_amount'].append(amount)
                except:
                    continue
    return ttsd

##Function to read the data from the folder for Transaction Pincode

def top_transaction_pincode():
    top_tnsp_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/top/transaction/country/india/state/"
    top_tnsp_st=os.listdir(top_tnsp_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(top_tnsp_st)):
        state_list[top_tnsp_st[i]] = geo_state[i]
    ttsp={'state':[],'year':[],'quarter':[],'pincode':[],'transaction_count':[],'transaction_amount':[]}
    for s in top_tnsp_st:
        p_s=top_tnsp_path+s+"/"
        top_tnsp_yr=os.listdir(p_s)
        for y in top_tnsp_yr:
            p_yr=p_s+y+"/"
            top_tnsp_js=os.listdir(p_yr)
            for j in top_tnsp_js:
                p_j=p_yr+j
                top_tnsp_d=open(p_j,'r')
                top_tnsp_dt=json.load(top_tnsp_d)
                try:
                    for i in top_tnsp_dt['data']['pincodes']:
                        pincode=i['entityName']
                        count=i['metric']['count']
                        amount=i['metric']['amount']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        ttsp['state'].append(state)
                        ttsp['year'].append(y)
                        ttsp['quarter'].append(quarter)
                        ttsp['pincode'].append(pincode)
                        ttsp['transaction_count'].append(count)
                        ttsp['transaction_amount'].append(amount)
                except:
                    continue
    return ttsp

##Function to read the data from the folder for top user district
def top_user_district():
    top_usrd_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/top/user/country/india/state/"
    top_usrd_st=os.listdir(top_usrd_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(top_usrd_st)):
        state_list[top_usrd_st[i]] = geo_state[i]
    tusrd={'state':[],'year':[],'quarter':[],'district':[],'registered_user':[]}
    for s in top_usrd_st:
        p_s=top_usrd_path+s+"/"
        top_usrd_yr=os.listdir(p_s)
        for y in top_usrd_yr:
            p_yr=p_s+y+"/"
            top_usrd_js=os.listdir(p_yr)
            for j in top_usrd_js:
                p_j=p_yr+j
                top_usrd_d=open(p_j,'r')
                top_usrd_dt=json.load(top_usrd_d)
                try:
                    for i in top_usrd_dt['data']['districts']:
                        district=i['name']
                        reg_user=i['registeredUsers']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        tusrd['state'].append(state) 
                        tusrd['year'].append(y)
                        tusrd['quarter'].append(quarter)
                        tusrd['district'].append(district)
                        tusrd['registered_user'].append(reg_user)
                except:
                    continue
    return tusrd

##Function to read the data from the folder for top user pincode

def top_user_pincode():
    top_usrp_path="C:/Users/Dharmarajan/Documents/Guvi/Project/Project 2/Phonepe_git/data/top/user/country/india/state/"
    top_usrp_st=os.listdir(top_usrp_path)
    geo_state=geo_state_list()
    state_list={}
    for i in range(0, len(top_usrp_st)):
        state_list[top_usrp_st[i]] = geo_state[i]
    tusrp={'state':[],'year':[],'quarter':[],'pincode':[],'registered_user':[]}
    for s in top_usrp_st:
        p_s=top_usrp_path+s+"/"
        top_usrp_yr=os.listdir(p_s)
        for y in top_usrp_yr:
            p_yr=p_s+y+"/"
            top_usrp_js=os.listdir(p_yr)
            for j in top_usrp_js:
                p_j=p_yr+j
                top_usrp_d=open(p_j,'r')
                top_usrp_dt=json.load(top_usrp_d)
                try:
                    for i in top_usrp_dt['data']['pincodes']:
                        pincode=i['name']
                        reg_user=i['registeredUsers']
                        q=int(j.strip('.json'))
                        if (q==1):
                            quarter="Quarter 1"
                        elif (q==2):
                            quarter="Quarter 2"
                        elif (q==3):
                            quarter="Quarter 3"
                        else:
                            quarter="Quarter 4"
                        state=state_list[s]
                        tusrp['state'].append(state)
                        tusrp['year'].append(y)
                        tusrp['quarter'].append(quarter)
                        tusrp['pincode'].append(pincode)
                        tusrp['registered_user'].append(reg_user)      
                except:
                    continue
    return tusrp

#Function to insert data into table aggregate_transaction

def agg_trans_insert(agg_trns):
    agg_trns_df=pd.DataFrame(agg_trns) 
    ats_cquery="""create table if not exists aggregate_transaction(state varchar(100),year int,quarter varchar(50),transaction_type varchar(100),
                transaction_count int,transaction_amount double)"""
    cursor.execute(ats_cquery)
    client.commit()
    ats_tquery="delete from aggregate_transaction"
    cursor.execute(ats_tquery)
    try:
        ats_iquery="""insert into aggregate_transaction (state,year,quarter,transaction_type,transaction_count,transaction_amount) 
                    values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(ats_iquery,agg_trns_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table aggregate_user

def agg_usr_insert(agg_usr):
    agg_usr_df=pd.DataFrame(agg_usr)
    ausr_cquery="""create table if not exists aggregate_user(state varchar(100),year int,quarter varchar(50),user_brand varchar(100),
                user_count int,user_percentage double)"""
    cursor.execute(ausr_cquery)
    client.commit()
    ausr_tquery="delete from aggregate_user"
    cursor.execute(ausr_tquery)
    try:
        ausr_iquery="""insert into aggregate_user (state,year,quarter,user_brand,user_count,user_percentage) 
                    values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(ausr_iquery,agg_usr_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table map_transaction
def map_trns_insert(map_trns):
    map_trns_df=pd.DataFrame(map_trns)
    mts_cquery="""create table if not exists map_transaction(state varchar(100),year int,quarter varchar(50),district varchar(100),
                transaction_count int,transaction_amount double)"""
    cursor.execute(mts_cquery)
    mts_tquery="delete from map_transaction"
    cursor.execute(mts_tquery)
    try:
        mts_iquery="""insert into map_transaction (state,year,quarter,district,transaction_count,transaction_amount)
                     values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(mts_iquery,map_trns_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table map_user
def map_usr_insert(map_usr):
    map_usr_df=pd.DataFrame(map_usr)
    musr_cquery="""create table if not exists map_user (state varchar(100),year int,quarter varchar(50),district varchar(100),
                registered_users int,app_opens int)"""
    cursor.execute(musr_cquery)
    musr_tquery="delete from map_user"
    cursor.execute(musr_tquery)
    try:
        musr_iquery="""insert into map_user (state,year,quarter,district,registered_users,app_opens) 
                    values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(musr_iquery,map_usr_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table top_transaction_district

def top_trnsd_insert(top_trnsd):
    top_trnsd_df=pd.DataFrame(top_trnsd)
    ttsd_cquery="""create table  if not exists top_transaction_district(state varchar(100),year int,quarter varchar(50),district varchar(100),
                transaction_count int,transaction_amount double)"""
    cursor.execute(ttsd_cquery)
    ttsd_tquery="delete from top_transaction_district"
    cursor.execute(ttsd_tquery)
    try:
        ttsd_iquery="""insert into top_transaction_district (state,year,quarter,district,transaction_count,transaction_amount) 
                    values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(ttsd_iquery,top_trnsd_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table top_transaction_pincode

def top_trnsp_insert(top_trnsp):
    top_trnsp_df=pd.DataFrame(top_trnsp)
    ttsp_cquery="""create table  if not exists top_transaction_pincode(state varchar(100),year int,quarter varchar(50),pincode int,
                transaction_count int,transaction_amount double)"""
    cursor.execute(ttsp_cquery)
    ttsp_tquery="delete from top_transaction_pincode"
    cursor.execute(ttsp_tquery)
    try:
        ttsp_iquery="""insert into top_transaction_pincode (state,year,quarter,pincode,transaction_count,transaction_amount)
                    values(%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(ttsp_iquery,top_trnsp_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table top_user_district

def top_usrd_insert(top_usrd):
    top_usrd_df=pd.DataFrame(top_usrd) 
    tusrd_cquery="""create table  if not exists top_user_district (state varchar(100),year int,quarter varchar(50),district varchar(100),
                registered_users int)"""
    cursor.execute(tusrd_cquery)
    tusrd_tquery="truncate top_user_district"
    cursor.execute(tusrd_tquery)
    try:
        tusrd_iquery="""insert into top_user_district (state,year,quarter,district,registered_users) values(%s,%s,%s,%s,%s)"""
        cursor.executemany(tusrd_iquery,top_usrd_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function to insert data into table top_user_pincode
def top_usrp_insert(top_usrp):
    top_usrp_df=pd.DataFrame(top_usrp)
    tusrp_cquery="""create table  if not exists top_user_pincode(state varchar(100),year int,quarter varchar(50),pincode int,
                registered_users int)"""
    cursor.execute(tusrp_cquery)
    tusrp_tquery="truncate top_user_pincode"
    cursor.execute(tusrp_tquery)
    try:
        tusrp_iquery="""insert into top_user_pincode (state,year,quarter,pincode,registered_users) values(%s,%s,%s,%s,%s)"""
        cursor.executemany(tusrp_iquery,top_usrp_df.values.tolist())
        client.commit()
    except Exception as e:
        st.write(e)

#Function used to get the data and insert into the corrresponding tables.
def data_insertion():
    agg_trns=aggregate_transaction()
    agg_trans_insert(agg_trns)
    agg_usr=aggregate_user()
    agg_usr_insert(agg_usr)
    map_trns=map_transaction()
    map_trns_insert(map_trns)
    map_usr=map_user()
    map_usr_insert(map_usr)
    top_trnsd=top_transaction_district()
    top_trnsd_insert(top_trnsd)
    top_trnsp=top_transaction_pincode()
    top_trnsp_insert(top_trnsp)
    top_usrd=top_user_district()
    top_usrd_insert(top_usrd)
    top_usrp=top_user_pincode()
    top_usrp_insert(top_usrp)

#Function to plot the India map based on the coordinates given
def geomap(data,locations,color,title):
    fig = px.choropleth(
    data,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations=locations,
    color=color,
    color_continuous_scale='Reds',
    title=title)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(geo_bgcolor='Black',showlegend=False)
    #st.plotly_chart(fig)
    st.plotly_chart(fig,use_container_width=False)

#Function to plot barchart  based on the coordinates given
def barchart(data,x,y,title):
    fig=px.bar(data,x=x,y=y,title=title)
    st.plotly_chart(fig,use_container_width=True)

#Function to plot the barchart based on the coordinates given
def barchart_colour(data,x,y,colour,title):
    fig=px.bar(data,x=x,y=y,color=colour,title=title)
    st.plotly_chart(fig,use_container_width=False)

#Function to plot the PieChart based on the coordinates given
def piechart(data,names,values,title):
    fig=px.pie(data,names=names,values=values,title=title)  
    st.plotly_chart(fig,use_container_width=True)

 ##This is the main program which will get the inputs from the end user in the streamlit screen and performt the below operations
 # 1. Cloning of the data from the github
 # 2. Data insertion into the tables in the data base 
 # 3. User will have option to visualize the data using 2 tabs . One is Transaction and user 
 # 4. If Transaction tab is selected the user will have option to view the data in geo map for the transaction count/Amount
 #    and the top 10 transaction districts and pincodes in bar/pie chart based on 3 options State,Quarter and year 
 # 5. If User tab is selected the user will have option to view the data in geo map for the User count
 #    and the Registered user top 10 districts and pincodes based on 3 options State,Quarter and year             
st.set_page_config(layout="wide")
st.header(':blue[PHONEPE DATA VISUALIZATION]')
Menu = st.selectbox(
   "**:green[PLEASE SELECT THE MENU FROM BELOW]**",
   ("Please select an option","Data Collection","Data Insertion into Database", "Data Visualization","Data Insights")
   )

if (Menu=="Data Collection"):
    st.write("*This Section is to get the Data related to PhonePe from Github and Clone it in Local system*")
    collect=st.button("Clone Data from Github")
    if (collect==True):
        data_collection()
        st.write("Data Collection completed Successfully")
    collect=False

elif (Menu=="Data Insertion into Database"):
    st.write("*This section is to process and insert the data from the specified paths in Local system to Database Tables*")
    insert=st.button("Insert Data into DB")
    if(insert==True):
        try:  
            data_insertion()
            st.write("Data Insertion completed")
        except Exception as e:
            st.write(e)
    insert=False

elif (Menu=="Data Visualization"):
    st.write("*This Section helps to represent the Data related to Transactions and User using Maps/ Charts*")
    colA,colB,colC=st.columns(3)
    state_query='select distinct state from aggregate_transaction order by state'
    cursor.execute(state_query)
    state=cursor.fetchall()
    state_list=[i[0] for i in state]
    state_menu=['All State']
    state_menu.extend(state_list)
    State_St_Menu=colA.selectbox("State:",state_menu,key='state select')
    year_query='select distinct year from aggregate_transaction order by year'
    cursor.execute(year_query)        
    year=cursor.fetchall()
    year_list=[i[0] for i in year]
    year_menu=['All Year']
    year_menu.extend(year_list)
    Year_St_Menu = colB.selectbox("Year:",year_menu,key='year select')
    qr_query='select distinct quarter from aggregate_transaction order by quarter'
    cursor.execute(qr_query)
    quarter=cursor.fetchall()
    qr_list=[i[0] for i in quarter]
    qr_menu=['All Quarter']
    qr_menu.extend(qr_list)
    Qr_St_Menu = colC.selectbox("Quarter:",qr_menu,key='quarter select')
    Transaction,Users=st.tabs(["Transaction","Users"])
    with Transaction:
        type=st.radio(":red[Type]",["Transaction Count","Transaction Amount"],horizontal=True,key='type')
        top=st.radio(":red[Top 10]",["District","Pincode"],horizontal=True,key='top',index=None)
        show=st.button("Get Data Analysis",key='T')
        if(type=='Transaction Count' and show==True):
            col1,col2=st.columns(2)
            if(top==None):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    with col1:
                        cursor.execute("select state,sum(transaction_count) from aggregate_transaction group by state order by state")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Count','Transaction Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction group by state,transaction_type order by state,transaction_type")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Count','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(transaction_count) from aggregate_transaction where year=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Count','Transaction Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where year=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Count','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(transaction_count) from aggregate_transaction where quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0): 
                            df=pd.DataFrame(output,columns=['State','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Count','Transaction Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Count','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(transaction_count) from aggregate_transaction where year=%s and quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Count','Transaction Count')
                        else:
                            st.write("Data Not Available")    
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where year=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Count','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(transaction_count) from map_transaction where state=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Count','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where state=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Count',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(transaction_count) from map_transaction where state=%s and year=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Count','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where state=%s and year=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Count',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(transaction_count) from map_transaction where state=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Count','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where state=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Count',"Overall:Transaction Type")
                    show=False
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(transaction_count) from map_transaction where state=%s and year=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        barchart(df,'District','Transaction Count','Overall- Bar chart Representation')
                    with col2:
                        cursor.execute("select state,transaction_type,sum(transaction_count) from aggregate_transaction where state=%s and year=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Count'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Count',"Overall:Transaction Type")
                    show=False
            elif(top=='District'):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):            
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district group by district order by transaction_count desc limit 10")
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where year=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                            
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where quarter=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where year=%s and quarter=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where state=%s and quarter=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where state=%s and year=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False               
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select district,sum(transaction_count) as transaction_count from top_transaction_district where state=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(transaction_count)  as transaction_count from top_transaction_district where state=%s and year=%s and quarter=%s group by district order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Count','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Count','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False             
            elif(top=='Pincode'):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):            
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode group by pincode order by transaction_count desc limit 10")
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where year=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where quarter=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where year=%s and quarter=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where state=%s and quarter=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where state=%s and year=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count) as transaction_count from top_transaction_pincode where state=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(transaction_count)  as transaction_count from top_transaction_pincode where state=%s and year=%s and quarter=%s group by pincode order by transaction_count desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Count'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Count','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
        elif(type=='Transaction Amount' and show==True):
            col1,col2=st.columns(2)
            if(top==None):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    with col1:
                        cursor.execute("select state,round(sum(transaction_amount),2) from aggregate_transaction group by state order by state")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Amount','Transaction Amount')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction group by state,transaction_type order by state,transaction_type")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Amount','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    with col1:
                        cursor.execute("select state,round(sum(transaction_amount),2) from aggregate_transaction where year=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Amount','Transaction Amount')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where year=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Amount','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,round(sum(transaction_amount),2) from aggregate_transaction where quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0): 
                            df=pd.DataFrame(output,columns=['State','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Amount','Transaction Amount')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Amount','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,round(sum(transaction_amount),2) from aggregate_transaction where year=%s and quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','Transaction Amount','Transaction Amount')
                        else:
                            st.write("Data Not Available")    
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where year=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'State','Transaction Amount','Transaction Type',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,round(sum(transaction_amount),2) from map_transaction where state=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Amount','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where state=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Amount',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    with col1:
                        cursor.execute("select district,round(sum(transaction_amount),2) from map_transaction where state=%s and year=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Amount','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where state=%s and year=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Amount',"Overall:Transaction Type")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    with col1:
                        cursor.execute("select district,round(sum(transaction_amount),2) from map_transaction where state=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'District','Transaction Amount','Overall- Bar chart Representation')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where state=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Amount',"Overall:Transaction Type")
                    show=False
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,round(sum(transaction_amount),2) from map_transaction where state=%s and year=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        barchart(df,'District','Transaction Amount','Overall- Bar chart Representation')
                    with col2:
                        cursor.execute("select state,transaction_type,round(sum(transaction_amount),2) from aggregate_transaction where state=%s and year=%s and quarter=%s group by state,transaction_type order by state,transaction_type",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','Transaction Type','Transaction Amount'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart(df,'Transaction Type','Transaction Amount',"Overall:Transaction Type")
                    show=False
            elif(top=='District'):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):            
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district group by district order by transaction_amount desc limit 10")
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where year=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where quarter=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where year=%s and quarter=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where state=%s and quarter=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where state=%s and year=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False               
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2) as transaction_amount from top_transaction_district where state=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,round(sum(transaction_amount),2)  as transaction_amount from top_transaction_district where state=%s and year=%s and quarter=%s group by district order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Transaction Amount','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Transaction Amount','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
            elif(top=='Pincode'):
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):            
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode group by pincode order by transaction_amount desc limit 10")
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where year=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where quarter=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where year=%s and quarter=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where state=%s and quarter=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where state=%s and year=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2) as transaction_amount from top_transaction_pincode where state=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False                    
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,round(sum(transaction_amount),2)  as transaction_amount from top_transaction_pincode where state=%s and year=%s and quarter=%s group by pincode order by transaction_amount desc limit 10",values)
                    output=cursor.fetchall()
                    if(len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Transaction Amount'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Transaction Amount','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")         
                    show=False
    with Users:
        top=st.radio(":red[Top 10]",["District","Pincode"],horizontal=True,key='user',index=None)
        show=st.button("Get Data Analysis",key="A")
        if(top==None):
            if (show==True):
                col1,col2=st.columns(2)
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    with col1:
                        cursor.execute("select state,sum(user_count) from aggregate_user group by state order by state")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','User Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','User Count','User Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select user_brand,sum(user_count),round(sum(user_percentage),2) from aggregate_user group by user_brand order by user_brand")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['User Brand','User Count','User Percentage'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'User Brand','User Count','User Percentage','UserBrand/Percentage')			
                        show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(user_count) from aggregate_user where year=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','User Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','User Count','User Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select user_brand,sum(user_count),round(sum(user_percentage),2) from aggregate_user where year=%s group by user_brand order by user_brand",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['User Brand','User Count','User Percentage'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'User Brand','User Count','User Percentage','UserBrand/Percentage')
                        show=False
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(user_count) from aggregate_user where quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','User Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','User Count','User Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select user_brand,sum(user_count),round(sum(user_percentage),2) from aggregate_user where quarter=%s group by user_brand order by user_brand",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['User Brand','User Count','User Percentage'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'User Brand','User Count','User Percentage','UserBrand/Percentage')
                        show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select state,sum(user_count) from aggregate_user where year=%s and quarter=%s group by state order by state",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['State','User Count'])
                            df.index.name="S.No"
                            df.index+=1
                            geomap(df,'State','User Count','User Count')
                        else:
                            st.write("Data Not Available")
                    with col2:
                        cursor.execute("select user_brand,sum(user_count),round(sum(user_percentage),2) from aggregate_user where year=%s and quarter=%s group by user_brand order by user_brand",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['User Brand','User Count','User Percentage'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'User Brand','User Count','User Percentage','UserBrand/Percentage')
                        show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(registered_users),sum(app_opens) from map_user where state=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Registered Users','App Opens'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'District','Registered Users','App Opens','Overall Registered Users')  
                        else:
                            st.write("Data Not Available")
                        show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(registered_users),sum(app_opens) from map_user where state=%s and year=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Registered Users','App Opens'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'District','Registered Users','App Opens','Overall Registered Users')
                        else:
                            st.write("Data Not Available")
                        show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(registered_users),sum(app_opens) from map_user where state=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Registered Users','App Opens'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'District','Registered Users','App Opens','Overall Registered Users')
                        else:
                            st.write("Data Not Available")
                        show=False
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    with col1:
                        cursor.execute("select district,sum(registered_users),sum(app_opens) from map_user where state=%s and year=%s and quarter=%s group by district order by district",values)
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Registered Users','App Opens'])
                            df.index.name="S.No"
                            df.index+=1
                            barchart_colour(df,'District','Registered Users','App Opens','Overall Registered Users')  
                        else:
                            st.write("Data Not Available")                    			
                        show=False
        elif(top=='District'):
            if (show==True):
                col1,col2=st.columns(2)
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                        cursor.execute("select district,sum(registered_users) as registered_users from top_user_district group by district order by registered_users desc limit 10")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['District','Registered User'])
                            df.index.name="S.No"
                            df.index+=1
                            with col1:
                                barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                            with col2:
                                piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                        else:
                            st.write("Data Not Available")
                        show=False 
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where year=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False 
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where quarter=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False 
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where year=%s and quarter=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False 
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where state=%s and quarter=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False 
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where state=%s and year=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select district,sum(registered_users) as registered_users from top_user_district where state=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select district,sum(registered_users)  as registered_users from top_user_district where state=%s and year=%s and quarter=%s group by district order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['District','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        with col1:
                            barchart(df,'District','Registered User','Top 10 District- Bar chart Representation')
                        with col2:
                            piechart(df,'District','Registered User','Top 10 District- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
        elif(top=='Pincode'):
            if (show==True):
                col1,col2=st.columns(2)
                if(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                        cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode group by pincode order by registered_users desc limit 10")
                        output=cursor.fetchall()
                        if (len(output)>0):
                            df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                            df.index.name="S.No"
                            df.index+=1
                            piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                        else:
                            st.write("Data Not Available")
                        show=False 
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[Year_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where year=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False  
                elif(State_St_Menu=='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Qr_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where quarter=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                elif(State_St_Menu=='All State' and Year_St_Menu!='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where year=%s and quarter=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu!='All Quarter'):
                    values=[State_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where state=%s and quarter=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu!='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu,Year_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where state=%s and year=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                elif(State_St_Menu!='All State' and Year_St_Menu=='All Year' and Qr_St_Menu=='All Quarter'):
                    values=[State_St_Menu]
                    cursor.execute("select pincode,sum(registered_users) as registered_users from top_user_pincode where state=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
                else:
                    values=[State_St_Menu,Year_St_Menu,Qr_St_Menu]
                    cursor.execute("select pincode,sum(registered_users)  as registered_users from top_user_pincode where state=%s and year=%s and quarter=%s group by pincode order by registered_users desc limit 10",values)
                    output=cursor.fetchall()
                    if (len(output)>0):
                        df=pd.DataFrame(output,columns=['Pincode','Registered User'])
                        df.index.name="S.No"
                        df.index+=1
                        piechart(df,'Pincode','Registered User','Top 10 Pincode- Pie chart Representation')
                    else:
                        st.write("Data Not Available")
                    show=False
    ##Option to get few insights based on various tables and conditions. Given the options as Selectbox and based on selection,
    ##the Output will be displayes
elif (Menu=="Data Insights"):
    st.write("*This Section helps to get some Insights based on Analysis of various Data*")
    Insight_1="Insight 1: The Year with highest no of Registered users recorded across India"
    Insight_2="Insight 2: A district which loves the phonepe app the most"
    Insight_3="Insight 3: The States which has least used the App"
    Insight_4="Insight 4: Transaction Type with highest Transaction Amount in the year 2023"
    Insight_5="Insight 5: The Quarter which tops Registered Users across all the years"
    Insight_6="Insight 6: State which has recorded highest AppOpens in Quarter3"
    Insight_7="Insight 7: Highest used User Brand in State Tamil Nadu"
    Insight_8="Insight 8: District with highest Transaction value across India"
    Insight_9="Insight 9: Pincode with least number of Users across India"
    Insight_10="Insight 10: State with Least User Percentage"
    option = st.selectbox(
       ":green[Choose to get more Insights..]",
        (Insight_1,Insight_2, Insight_3,Insight_4,Insight_5,Insight_6,Insight_7,Insight_8,Insight_9,Insight_10),
        index=None,
        placeholder="--Select--",
        )
    if(option==Insight_1):
        cursor.execute("select year,sum(registered_users) as Regd_Users from map_user group by year order by Regd_Users desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['Year','Registered_Users'])
        year=df.Year[0]
        regusers=df.Registered_Users[0]
        st.write(f'Based on the Data Analysis, the Year - **{year}** has the highest number of Registered users recorded across India with Registered Users Count as **{regusers}**.')
    elif(option==Insight_2):
        cursor.execute("select district,sum(registered_users) as count from map_user group by district order by count desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['District','Registered_Users'])
        district=df.District[0]
        regusers=df.Registered_Users[0]
        st.write(f'The District : **{district.upper()}** loves the Phonepe App most as it has the highest number of Registered Users: **{regusers}**.')
    elif(option==Insight_3):
        cursor.execute("select state,sum(transaction_count) as count from aggregate_transaction group by state order by count limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['State','Transaction_Count'])
        state=df.State[0]
        trncount=df.Transaction_Count[0]
        st.write(f'The State : **{state.upper()}** does not have much awareness about the Phonepe App as the number of Transactions is least in the state with the Transaction count recorded as: **{trncount}**.')
    elif(option==Insight_4):
        cursor.execute("select transaction_type,sum(transaction_count) as count from aggregate_transaction where year=2023 group by transaction_type order by count desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['Transaction_Type','Transaction_Count'])
        trntype=df.Transaction_Type[0]
        trncount=df.Transaction_Count[0]
        st.write(f'The PhonePe App is mostly used for the Transaction Type : **{trntype.upper()}** as the Transaction count peaks to - **{trncount}**.')
    elif(option==Insight_5):
        cursor.execute("select quarter,sum(registered_users) as Regd_Users from map_user group by quarter order by Regd_Users desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['Quarter','Registered_Users'])
        quarter=df.Quarter[0]
        regusers=df.Registered_Users[0]
        st.write(f'The Quarter : **{quarter.upper()}** tops as Number of Registered Users hikes across all the years in that Quarter with the count of - **{regusers}**.')
    elif(option==Insight_6):
        cursor.execute("select state,sum(app_opens) as app_opens from map_user where quarter ='Quarter 3' group by state order by app_opens desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['State','App_Opens'])
        state=df.State[0]
        appopens=df.App_Opens[0]
        st.write(f'The State : **{state.upper()}** records the highest number of AppOpens in the QUARTER 3, with the number reaching upto - **{appopens}**.')
    elif(option==Insight_7):
        cursor.execute("select user_brand,sum(user_count) as count from aggregate_user where state='Tamil Nadu' group by user_brand order by count desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['User_Brand','User_Count'])
        userbrand=df.User_Brand[0]
        usercount=df.User_Count[0]
        st.write(f'In the State : TamilNadu, User Brand - **{userbrand.upper()}** is being the widely used by Phone Pe App Users as it has the highest number of Users- **{usercount}**.')
    elif(option==Insight_8):
        cursor.execute("select district,round(sum(transaction_amount),2) as amount from top_transaction_district group by district order by amount desc limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['District','Transaction_Amount'])
        district=df.District[0]
        trnamt=df.Transaction_Amount[0]
        st.write(f'The Highest Transaction value - **{trnamt}** is recorded in the District-  **{district.upper()}** across India.')
    elif(option==Insight_9):
        cursor.execute("select pincode,sum(registered_users) as users from top_user_pincode group by pincode order by users limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['Pincode','Registered_Users'])
        pincode=df.Pincode[0]
        regusers=df.Registered_Users[0]
        st.write(f'The least number of Users - **{regusers}** accessing the App across India is from the Pincode - **{pincode}**')
    elif(option==Insight_10):
        cursor.execute("select state,round(sum(user_percentage),2) as percent from aggregate_user group by state order by percent limit 1")
        output=cursor.fetchall()
        df=pd.DataFrame(output,columns=['State','User_Percent'])
        state=df.State[0]
        userpercent=df.User_Percent[0]
        st.write(f'The state : **{state.upper()}** has the least user percentage for accessing the App across India with the % as - **{userpercent}**')
    else:
        st.write("*Select an Option*")
else:
    st.write("*Select an option from the Menu*")