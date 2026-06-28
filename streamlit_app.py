# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col , when_matched
# Write directly to the app
st.title(f"🥤 Pending Smoothie Orders ! :cup_with_straw:")
st.write('Orders That Needs To Be filled')


##option = st.selectbox(
 ##   "What Is Your Favorite Fruit ?",
 ##   ("Banana", "Strawberries", "Peaches"),
##)

##st.write("Your Favorite Fruit Is :", option)
cnx=st.connection("snowflake")
session=cnx.session()
##session = get_active_session()
##order_filled = 1
my_dataframe = session.table("SMOOTHIES.public.ORDERS") \
    .filter((col("ORDER_FILLED") ==0) & col("NAME_ON_ORDER").is_not_null()) \
    
editable_df = st.data_editor(my_dataframe)


#my_insert_stmt = f"""insert into smoothies.public.orders(ORDER_FILLED)
                #    values ({order_filled})"""

submitted= st.button('Submit')
if submitted:

    try:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])

        st.success("Order(s) Updated!", icon="👍")
    except:
        st.write('Something went wrong.')
            
else:
    st.success('There are no pending orders right now.', icon="👍")
