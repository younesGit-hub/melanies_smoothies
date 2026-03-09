import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")  # doit correspondre au nom du secret
session = cnx.session()

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom  Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write ('The name on your Smoothie will be' + name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list: 
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

#New section
import requests

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# exemple pour vérifier la réponse
if smoothiefroot_response.status_code == 200:
    st.write(smoothiefroot_response.json())
else:
    st.error(f"Erreur API: {smoothiefroot_response.status_code}")
