# Import python packages
import streamlit as st
import os
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")
  
name=st.text_input("Name on Order")
st.write("Name on your smoothie order will be",name)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose upto 5 ingredients',my_dataframe,max_selections=5)
if ingredients_list:
    ing_str=''
    for fruit in ingredients_list:
        ing_str+=fruit+' '
        st.subheader(fruit+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)  
        df=st.dataframe(data=smoothifruit_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
                    values ('""" +name+"""','"""+ ing_str + """')"""
    #st.write(my_insert_stmt)
    submit=st.button('Submit Order')
    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name, icon="✅")
