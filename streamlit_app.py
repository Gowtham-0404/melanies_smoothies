# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Own Smoothies:balloon:")
st.write(
  """Choose what fruits u want in the smoothie.
  """
)

name_on_the_order = st.text_input("Name on the Smoothie")
st.write("Name on the smoothie will be", name_on_the_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



options = st.multiselect(
    "CHOOSE ANY 5 fruits",
    my_dataframe,
    max_selections= 5
)
if options:
    ingredients_string=''
    for ingredients in options:
        ingredients_string+=ingredients+' '
    
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + name_on_the_order + """')"""
    st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered by'+name_on_the_order, icon="✅")




