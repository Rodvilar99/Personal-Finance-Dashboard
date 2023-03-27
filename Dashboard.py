#!/usr/bin/env python
# coding: utf-8

# In[1]:


# data analysis
import pandas as pd
import numpy as np
# Dashboard
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')


# In[2]:


#import CSV
df = pd.read_csv('Fargo.csv')


# In[3]:


# check if csv imported correct
df.head() 


# In[4]:


df['category'] = 'not assigned'
df.head()


# In[5]:


#categories
    # Groceries
    # Shopping
    # Food
    # Rent
    # Utilities
    # Subscriptions
    # Misc
    # Transport
    # Education
    # Fees

# Misc

df['category'] = np.where(df['Description'].str.contains(
    'CMSVEND|USTREASTAXP|PredictionStrike|TERABYTE|CONNECTED REALIT|FLIFF|CRISTOBAL|GRACELAND UNIVERSI|FEE|CHCSI|STATE|DETROIT'),'Misc', df['category'])

# Transport

df['category'] = np.where(df['Description'].str.contains(
    'JEFFERSON|UBER|KUM&GO|CASEYS|CHOCODELICE|DELTA'),'Transport', df['category'])

# Subscriptions

df['category'] = np.where(df['Description'].str.contains(
    'ADOBE|APPLE.COM|Amazon Prime|LinkedIn|Disney Plus|FANATIZ|REZI|NBA|CHEGG|SLINGTV|PARAMNT|FuboTV'),'Subscriptions', df['category'])
# Shopping

df['category'] = np.where(df['Description'].str.contains(
    'Amazon.com|Mktp|H&M|DOLLAR|KOHLS|Temu.com|Kindle|LEGO|NINTENDO|Forever|AMOCO|KINDLE|SOCCER'),'Shopping', df['category'])

# Education

df['category'] = np.where(df['Description'].str.contains(
    'SIX|COURSRA'),'Education', df['category'])


# Utlities

df['category'] = np.where(df['Description'].str.contains(
    'LAMONIMUNIC|US MOBILE|MARIA GOM| PSN*LAMONI'),'utilities', df['category'])

# Rent

df['category'] = np.where(df['Description'].str.contains(
    'RECURRING GRACELAND UNIVERSI'),'Rent', df['category'])

# Food

df['category'] = np.where(df['Description'].str.contains(
    'PIZZA|Subway|LINDEN|CAMPBELL|POUTINE|DUKE|STARBUCKS'),'Food', df['category'])

# Groceries

df['category'] = np.where(df['Description'].str.contains(
    'Wal-Mart|HY-VEE'),'Groceries', df['category'])


# In[6]:


# set date as datetime format
df['Date'] = pd.to_datetime(df['Date'])


# In[7]:


# extract month and date
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year


# In[8]:


pd.options.display.max_rows = 999
df.head(200)


# In[9]:


# get the last month and year
last_year = df['Year'].max()
last_month = df[df['Year'] == last_year]['Month'].max()



# filter last month
last_month_expenses = df[(df['Month'] == last_month) & (df['Year'] == last_year)]
# exclude not assigned
last_month_expenses = last_month_expenses[last_month_expenses["category"].str.contains("not assigned") == False] 
last_month_expenses


# In[10]:


last_month_expenses = last_month_expenses.groupby('category')['Transaction'].sum().reset_index()

last_month_expenses['Transaction']=last_month_expenses['Transaction'].astype('str')
last_month_expenses['Transaction']=last_month_expenses['Transaction'].str.replace('-','')
last_month_expenses['Transaction']=last_month_expenses['Transaction'].astype('float')
# sort values
last_month_expenses = last_month_expenses.sort_values(by='Transaction', ascending=False)
# round values
last_month_expenses['Transaction'] = last_month_expenses['Transaction'].round().astype(int)

last_month_expenses


# In[11]:


last_month_expenses_tot = last_month_expenses['Transaction'].sum()
last_month_expenses_tot


# In[12]:


def calculate_difference (event):
    income = float(income_widget.value)
    recurring_expenses = float(recurring_expenses_widget.value)
    monthly_expenses = float(monthly_expenses_widget.value)
    difference = income - recurring_expenses - monthly_expenses
    difference_widget.value = str(difference)


# In[13]:


income_widget = pn.widgets.TextInput(name="income", value="0")
recurring_expenses_widget = pn.widgets.TextInput(name="Recurring Expenses", value="0")
monthly_expenses_widget = pn.widgets.TextInput(name="Non-Recurring Expenses", value=str(last_month_expenses_tot))
difference_widget = pn.widgets.TextInput(name="Last Month's saving", value="0")


# In[14]:


income_widget.param.watch(calculate_difference, "value")
recurring_expenses_widget.param.watch(calculate_difference, "value")
monthly_expenses_widget.param.watch(calculate_difference, "value")

pn.Row(income_widget, recurring_expenses_widget, monthly_expenses_widget, difference_widget).show()


# In[15]:


last_month_expenses_chart = last_month_expenses.hvplot.bar(
    x='category',
    y='Transaction',
    height=250,
    width=850,
    title="Last Month Expenses",
    ylim=(0,500))
last_month_expenses_chart


# In[16]:


#date to datetime format
df['Date'] = pd.to_datetime(df['Date'])
# get the month and year from the date column
df['Month-Year'] = df['Date'].dt.to_period('M')
monthly_expenses_trend_by_category = df.groupby(['Month-Year', 'category']) ['Transaction'].sum().reset_index()


# In[17]:


# create monthly expensess trend bar chart
monthly_expenses_trend_by_category['Transaction']=monthly_expenses_trend_by_category['Transaction'].astype('str')
monthly_expenses_trend_by_category['Transaction']=monthly_expenses_trend_by_category['Transaction'].str.replace('-','')
monthly_expenses_trend_by_category['Transaction']=monthly_expenses_trend_by_category['Transaction'].astype('float')
monthly_expenses_trend_by_category = monthly_expenses_trend_by_category[monthly_expenses_trend_by_category['category'].str.contains('not assigned') == False]

monthly_expenses_trend_by_category


# In[18]:


monthly_expenses_trend_by_category = monthly_expenses_trend_by_category.sort_values(by='Transaction', ascending=False)
monthly_expenses_trend_by_category['Transaction'] = monthly_expenses_trend_by_category['Transaction'].round().astype(int)
monthly_expenses_trend_by_category["Month-Year"] = monthly_expenses_trend_by_category['Month-Year'].astype(str)
monthly_expenses_trend_by_category = monthly_expenses_trend_by_category.rename(columns={'Transaction': 'Amount'})

monthly_expenses_trend_by_category


# In[19]:


# Define the categories
categories = [
    'all',
    'Groceries',
    'Food',
    'Rent',
    'Shopping',
    'Utilities',
    'Subscriptions',
    'Misc',
    'Transport',
    'Education',
    'Fees'
]

# Create the widget
select_category1 = pn.widgets.Select(name='Select Category', options=categories)

# Display the widget
select_category1


# In[20]:


# prepare plot
def plot_expenses(category):
    if category == 'all':
        plot_df = monthly_expenses_trend_by_category.groupby('Month-Year').sum()
    else:
        plot_df = monthly_expenses_trend_by_category[monthly_expenses_trend_by_category['category'] == category].groupby('Month-Year').sum()
    plot = plot_df.hvplot.bar(x='Month-Year', y='Amount')
    return plot

#callback function
@pn.depends(select_category1.param.value)
def update_plot(category):
    plot = plot_expenses(category)
    return plot

# layout
monthly_expenses_trend_by_category_chart = pn.Row(select_category1, update_plot)
monthly_expenses_trend_by_category_chart[1].width = 600

monthly_expenses_trend_by_category_chart


# In[21]:


#summary
df = df[['Date', 'category', 'Description', 'Transaction']]
df['Transaction']=df['Transaction'].astype('str')
df['Transaction']=df['Transaction'].str.replace('-','')
df['Transaction']=df['Transaction'].astype('float')

df = df[df['category'].str.contains('not assigned') == False]
df['Transaction'] = df['Transaction'].round().astype(int) 
df


# In[22]:


# def to set dataframe based on category
def filter_df(category):
    if category == 'all':
        return df
    return df[df['category'] == category]
# datagrame widget with category
summary_table = pn.widgets.DataFrame(filter_df('all'), height = 300,width=400)

#callback category update
def update_summary_table(event):
    summary_table.value = filter_df(event.new)

# add the callback to the widget
select_category1.param.watch(update_summary_table, 'value')

summary_table


# In[23]:


# final dashboard
template = pn.template.FastListTemplate(
    title="Personal Finances Summary",
    sidebar=[
        pn.pane.Markdown("## *Be careful with the expenses!!*"),
        pn.pane.PNG('png-transparent-united-states-dollar-money-united-states-one-hundred-dollar-bill-money-saving-bank-cash.png', sizing_mode='scale_both'),
        pn.pane.Markdown(""),
        select_category1
    ],
    main=[
        pn.Row(income_widget, recurring_expenses_widget, monthly_expenses_widget, difference_widget, width=950, height=100),
        pn.Row(last_month_expenses_chart, height=240, width=50),
        pn.GridBox(
            monthly_expenses_trend_by_category_chart[1],
            summary_table,
            ncols=2,
            width=500,
            align='start',
            sizing_mode='stretch_width'
        )
    ]
)

template.show()


# In[ ]:




