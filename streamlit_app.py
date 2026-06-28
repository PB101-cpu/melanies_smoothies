# Import python packages
import streamlit as st

##from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"🥤 Customize Your Smoothie ! :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))



name_on_order = st.text_input("The Name On Smoothie :")
st.write("The Name On Your Smoothie Will Be: ", name_on_order)


ingredients_list = st.multiselect(
    'Choose Upto 5 ingredients :',
    my_dataframe,
    max_selections=6
)
ingredients_string = ''
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
   # ingredients_string = ''

for fruit_chosen in ingredients_list:
    ingredients_string +=fruit_chosen + ' '


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
time_to_insert=st.button('Submit Order')
#st.write(my_insert_stmt)

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
sf_df = st.DataFrame(data=smoothiefroot_response.json(),use_container_width=true)
