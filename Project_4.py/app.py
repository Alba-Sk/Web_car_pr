# python environment- APP
import pandas as pd
import scipy.stats
import streamlit as st
import plotly.express as px
import altair
import datetime
from PIL import Image

#streamlit run app.py


# add the header
st.header('Buy and Sell car, discover the vehicle value!')
st.write('At our site, we are dedicated to helping you find and purchase your dream car. Leveraging the power of data science, we offer you valuable insights and a seamless experience to match you with the perfect vehicle. Explore our platform and discover how we can assist you in buying and selling cars with confidence and ease')

# get the data from CSV
vehicles = pd.read_csv('C:\\Users\\dejsi\\OneDrive\\Documents\\GitHub\\Project_4.py\\vehicles_us.csv', sep=',')
#data processing for missing values and convert from float to integer and string
vehicles_dt = vehicles.dropna()
vehicles_dt.reset_index(drop=True, inplace=True)
vehicles_dt['model_year'] = vehicles_dt['model_year'].astype(int).astype(str)
vehicles_dt['odometer'] = vehicles_dt['odometer'].astype(float).astype(int)
vehicles_dt['model'] = vehicles_dt['model'].str.title()

# create filter fir vehicles by fuel used
vehicles_fuel = vehicles_dt['fuel'].unique()

# return the value what it is selected on the WEB for the filter "vehicle fuel"
selected_fuel = st.selectbox('**Please select the vehicle fuel**', vehicles_fuel)

# creating the slider and adding on streamlit
year_min, year_max = int(vehicles_dt['model_year'].min()), int(vehicles_dt['model_year'].max())

year_slide= st.slider('**Please choose the year range**', min_value=year_min, max_value=year_max, value=(year_min, year_max))

#creating the year range
range_year = list(range(year_slide[0], year_slide[1] + 1))

vehicles_filtered = vehicles_dt[(vehicles_dt['fuel'] == selected_fuel) &
                                (vehicles_dt['model_year'].astype(int).isin(range_year))]



# streamlit the df
st.dataframe(vehicles_filtered, hide_index=True)


# Analyze for the prices and build hist
st.header('Analyzing the vehicle value')
st.write("""Let's analyze vehicle prices and determine which characteristics most influence the value. 
We will examine how different attributes, such as condition, fuel type, model, model year, and odometer, impact the price of vehicles. """)
list_price = ['condition', 'fuel', 'model', 'model_year','paint_color']

select_type = st.selectbox('**Vehicle price distribution for:**', list_price)

fig1 = px.histogram(vehicles_dt, x="price",color= select_type )
fig1.update_layout(title= "Vehicle value".format(select_type))

st.plotly_chart(fig1)

st.write('This scatter plot shows the relationship between vehicle price and selected characteristics, with colors indicating different vehicle age categories.')
def age_category(row):
    if row < 5:
        return '<5'
    elif row >= 5 and row <10:
        return '5-10'
    elif row >= 10 and row <15:
        return '10-15'
    else:
        return 'over 15'

#
vehicles_dt['model_year'] = vehicles_dt['model_year'].astype(int)
current_year = datetime.datetime.now().year
vehicles_dt['age'] = current_year - vehicles_dt['model_year']

vehicles_dt['age_category'] = vehicles_dt['age'].apply(age_category)

list_for_catter = ['model', 'odometer', 'condition', 'model_year', 'fuel']
chose_scatter = st.selectbox('**Price dependency for:**', list_for_catter)
sorted_categories = sorted(vehicles_dt[chose_scatter].unique())
fig2 = px.scatter(vehicles_dt, x="price", y=chose_scatter, color = "age_category", category_orders={chose_scatter: sorted_categories})
fig2.update_layout(title= "Price versus ".format(chose_scatter))

st.plotly_chart(fig2)


# Analize vehicles value prices by age
st.write('This scatter plot visualizes vehicle models based on selected characteristics, with color coding indicating different price categories. It helps in analyzing how vehicle price varies with attributes such as age, odometer reading, condition, and fuel type.')
def price_category(row):
    if row < 3000:
        return 'price less then $5000'
    elif row >= 5000 and row <20000:
        return 'price between $5000-$20000'
    elif row >= 20000 and row <70000:
        return 'price between $20000-$70000'
    elif row >= 70000 and row <150000:
        return 'price between $70000-$150000'
    else:
        return 'price over $150000'
    
vehicles_dt['price_category'] = vehicles_dt['price'].apply(price_category)

list_for_catg = ['age', 'odometer', 'condition', 'fuel']
chose_scat = st.selectbox('**Vehicle model dependency for:**', list_for_catg)
fig3 = px.scatter(vehicles_dt, y="model", x=chose_scat, color = "price_category")
fig3.update_layout(title= "Price versus ".format(chose_scat))

st.plotly_chart(fig3)



#Contact information 
st.write('**This Web is prepare by Alba, Data Scientist**')
upload_image = st.file_uploader('Upload your image (A1.jpg)', type=['jpg'])

if upload_image is not None:
    image = Image.open(upload_image)
    resize_image = image.resize((150, 150))
    st.write(resize_image.size)
    st.image(resize_image, caption='Upload your image',width=150)
    

st.write('**Ambasador at TripleTen**')
st.write("Contact: [LinkedIn](https://www.linkedin.com/in/albana-skeja-24as/)")