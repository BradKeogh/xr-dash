# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import panel as pn
pn.extension()
import hvplot.pandas
import datetime

# %% [markdown]
# # 1 load data

# %%
path = './data/XR_IMPACT_DASHBOARD_BRADFORMAT.xlsx'

def load_data_excel(path):
    "Load data from each sheet in excel file"
    net_zero = pd.read_excel(path, sheet_name = 'net_zero')
    la_dec = pd.read_excel(path, sheet_name = 'la_declarations')
    social = pd.read_excel(path, sheet_name = 'social_media_stats')
    books = pd.read_excel(path, sheet_name = 'book_sales')
    data_web = pd.read_excel(path, sheet_name = 'web_stats')
    return(net_zero, la_dec, social, books, data_web) # should call all these data_ in future!

data_net_zero, data_la_dec, data_social, data_books, data_web = load_data_excel(path)
# long term we should move to csvs i think.

# %% [markdown]
# # 2 create pane to assemble
# %% [markdown]
# ## WEB visit panes

# %%
data_web.head()


# %%
web_plot_usersPERday = data_web.hvplot(x='date',y ='all_web_users')
web_plot_usersPERday


# %%
web_number_maxUSERSperDay = data_web.all_web_users.max()
web_number_maxUSERSperDay

# %% [markdown]
# ## Books panes
# 
# Assuming this is a cumulative figures?

# %%
data_books.tail()


# %%
# can possibly get rid of this, just get it in format i want
data_books['month'] = data_books.as_at_date.apply(lambda x: x.month)

data_books['year'] = data_books.as_at_date.apply(lambda x: x.year)

books_monthly = data_books.groupby(['year','month']).max().reindex()


# %%
books_plot_booksPermonth = books_monthly.hvplot(x='as_at_date',y ='total_sales')
books_plot_booksPermonth


# %%


# %% [markdown]
# ## social media panes 

# %%
data_social.head()


# %%
def make_social_media_plot(social_media_platform_name, dropdown_list):
    """
    Get plot and dropdown for social media.
    social_media_platform_name, str, name of platform
    dropdown_list, list of str, names of options to filter by in dropdown
    """
    data_oneplatform = data_social[data_social.domain == social_media_platform_name]
    
    dropdown_selector_widget = pn.widgets.Select(options=dropdown_list) # make column selecter dropdown

    @pn.depends(dropdown_selector_widget.param.value) # make linked plot
    def social_fb_plot(value):
        app = data_oneplatform.hvplot(x='date',y = value)
        return(app)

    social_media_plot = pn.Column(social_fb_plot, dropdown_selector_widget)
    social_media_plot

    return(social_media_plot)

# can change dropdown list in below if want different columns
socialmedia_plot_byday_facebook = pn.Row(make_social_media_plot('Facebook', dropdown_list = ['follows','likes']), name = 'Facebook')
socialmedia_plot_byday_twitter = pn.Row(make_social_media_plot('Twitter', dropdown_list = ['follows','likes']), name = 'Twitter')

socialmedia_plot_byday_alltabs = pn.Tabs(socialmedia_plot_byday_facebook, socialmedia_plot_byday_twitter)
socialmedia_plot_byday_alltabs

# %% [markdown]
# ## la_declaration panes

# %%
data_la_dec.tail()


# %%
data_la_dec['declaration_date_month'] = data_la_dec.declaration_date + pd.offsets.MonthBegin(-1)
# la_dec['declaration_date_month'].apply(lambda x : x.date())


# %%
la_dec_onlydec = data_la_dec[data_la_dec.is_declared == 'YES']

# %% [markdown]
# Calc number declared each month

# %%
la_dec_month = la_dec_onlydec.groupby('declaration_date_month').count()['is_declared'] #.plot(kind='bar')#.reindex()
la_dec_month = pd.DataFrame(la_dec_month).rename(columns={'is_declared':'declared'})
# la_dec_month


# %%
### make new index
start = la_dec_month.index[0]
end = la_dec_month.index[-1]
end
new_index = pd.date_range(start=start, end=end, freq=pd.offsets.MonthBegin(1))
# new_index


# %%
la_dec_month = la_dec_month.reindex(new_index)
la_dec_month.fillna(0, inplace=True)
la_dec_month['declared'] = la_dec_month.cumsum()
total_LAs = data_la_dec.shape[0]# get undeclared numbers column (calc from total found in data)
la_dec_month['undeclared'] = total_LAs - la_dec_month['declared']
# la_dec_month.head()


# %%
la_dec_plot_declaredBYmonth = la_dec_month.hvplot.bar(x='index', y=['declared','undeclared'],stacked=True, rot=30, ylabel='Local Authorities')
la_dec_plot_declaredBYmonth

# %% [markdown]
# ###### local auhtority map pane

# %%
la_dec_map = pn.pane.HTML("""
Interactive map of local authorites? Areas will be shaded based on if they have declared or not.""",
                      width=600, height=300, background=(20, 170,55))
la_dec_map


# %%
start = pd.datetime(2018,1,1)
end = pd.datetime.today()
widget_date_slider = pn.widgets.DateSlider(end=end, start=start, value=end)
widget_date_slider

# %% [markdown]
# date = widget_date_slider.value
# datetime_value = datetime.datetime(date.year, date.month, date.day)
# 
# LAs_declared_at_date = la_dec_month[la_dec_month.index <= datetime_value][-1:].declared.values[0] # get previous value from table
# %% [markdown]
# LAs_declared_at_date = la_dec_month[la_dec_month.index <= pd.datetime(2019,1,1)][-1:].declared.values[0] # get previous value from table
# %% [markdown]
# LAs_declared_at_date

# %%
@pn.depends(widget_date_slider.param.value) # make linked plot
def la_get_number_declared(value):
    # get number of LAs declared at date.
    date = widget_date_slider.value
    datetime_value = datetime.datetime(date.year, date.month, date.day)
    LAs_declared_at_date = la_dec_month[la_dec_month.index <= datetime_value][-1:].declared.values[0] # get previous df value from table
    # make string to return
    string_declaration = "LAs DECLARED AT DATE: {0}".format(int(LAs_declared_at_date))
    return(string_declaration)


LAmap_slider_description = pn.Column(
    "Move the slide to see which LAs have declared at a specific date. The map also updates with the slider.",
    widget_date_slider,
    la_get_number_declared,
)

LAmap_slider_description

# %% [markdown]
# ###### LA histogram for dates decalred pane

# %%
LA_net_zero_hist = data_la_dec.target_net_zero_year.hvplot.hist(ylabel="number of LA's")
LA_net_zero_hist

# %% [markdown]
# ### net zero panes

# %%
data_net_zero


# %%
parties_list = list(data_net_zero.org_name.values)
parties_string = ' '.join([str(item) for item in parties_list ])


# %%
parties_declared_net_zero_list = pn.pane.HTML(parties_string, width=600, height=300, background=(20, 170,55))
parties_declared_net_zero_list


# %%
net_zero_plot = data_net_zero.hvplot.barh(x='org_name', y='target_net_zero_year', ylim=[2020,2055])
net_zero_plot


# %%


# %% [markdown]
# # Summary panes

# %%
total_books = int(data_books.total_sales.max())
total_LAs_declared = int(la_dec_month.declared.max())
total_political_org_declared = data_net_zero[data_net_zero.is_political_org == 'YES'].shape[0]

str_max_webusers = "#### " + str(data_web.all_web_users.max())
SUMMARY_MAX_WEBPERDAY = pn.Column(
    pn.panel("### MAX WEBSITE USERS IN ONE DAY"),
    pn.panel(str_max_webusers),
)


str_nos_dec = str(total_LAs_declared) + '/' + str(total_LAs)
str_nos_dec = '#### ' + str_nos_dec

SUMMARY_LAs_DECLARED = pn.Column(
    pn.panel("### LA'S DECLARED CLIM EMERG"),
    pn.panel(str_nos_dec),
)

str_total_books = "#### " + str(total_books)
SUMMARY_BOOKS_SOLD = pn.Column(
    pn.panel("### TOTAL BOOKS SOLD"),
    pn.panel(str_total_books),
)

str_total_political_org_declared = "#### " + str(total_political_org_declared)

SUMMARY_POL_PARTIES_DECLARED = pn.Column(
    pn.panel("### POLITICAL ORG'S DECLARED CLIM EMERG"),
    pn.panel(str_total_political_org_declared),
)


# %%
SUMMARY_PANES = pn.Column(
    pn.Row(SUMMARY_MAX_WEBPERDAY , SUMMARY_BOOKS_SOLD),
    pn.Row(SUMMARY_POL_PARTIES_DECLARED, SUMMARY_LAs_DECLARED),
)
# SUMMARY_PANES

# %% [markdown]
# # 3 create tabs
# %% [markdown]
# ### Header- title with logo

# %%
logo = pn.panel('./images/XR-logo-RGB-Black-Linear.png', height=100)
logo

header_text  = """
# IMPACT DASHBOARD
"""
header_prose = pn.panel(header_text, height=130)
header_prose


# %%
header_row = pn.Row( header_prose,pn.layout.HSpacer(), logo,width_policy='fixed', width=900) # 
header_row

# %% [markdown]
# key_figures = pn.Column(
#     pn.Row('# ENGAGEMENT'),
#     pn.Row(KF_numbers),
# )

# %%


# %% [markdown]
# #### create each page (each called body_*****)

# %%
body_summary = pn.Column(
    pn.Row('# XR SUMMARY'),
    SUMMARY_PANES,
    name = 'SUMMARY',
)
# body_summary


# %%
body_engagement = pn.Column(
    header_row,
    
    pn.Row('### Website visits'),
    pn.Row(web_plot_usersPERday, "Text description here"),
    pn.Row('### Social Media'),
    pn.Row(socialmedia_plot_byday_alltabs, "Text description here"), # Twitter over time plot
    pn.Row('### Books sold'),
    pn.Row(books_plot_booksPermonth, "Text description here"), # books sold over time plot
    pn.Row('### Donations'),
    pn.Row("**donations plot here**" , "Donations text description here"),
    # NOTE: consider putting above titles on their own row and the plot and description in its own row. Will space better.
    # next plots here
    
    name = 'ENGAGEMENT'
    
)

# body_engagement


# %%
body_telltruth = pn.Column(
    header_row,
    pn.Row('# TELL THE TRUTH'),
    
    pn.Row('### POLITICAL ORGANISATIONS DECLARED'),
    pn.Row(parties_declared_net_zero_list, """This could include another vis once we have more organisations declared. Perhaps a vertical bar chart of number of organisations who have declared. Each bar being 
           'political orgs', 'museams', etc. I have not idea how XR would keep track of these? Do they plan to collect a list? """),
    pn.Row('### LOCAL AUTHORITIES DECLARED'),
    pn.Row(la_dec_plot_declaredBYmonth, " We need the complete list of LAs as its currnetly incomplete. (job for Brian)"),
    pn.Row(la_dec_map, LAmap_slider_description),
    name = 'TELL THE TRUTH',
)

# body_telltruth


# %%
body_actnow = pn.Column(
    header_row,
    pn.Row('#ACT NOW'),
    pn.Row('### POLITICAL NET ZERO TARGETS'),
    pn.Row(net_zero_plot, """ Decription here """),
    pn.Row('### LA NET ZERO TARGETS'),
    pn.Row(LA_net_zero_hist, "Desription of histogram of LA dates."),
    
    # plots here pn.Row(pn.Column('### Local Authorities declared', la_dec_plot), " \n \n \n Text description here"),
    name = 'ACT NOW',
)

body_beyondpolitics = pn.Column(
    header_row,
    pn.Row('# BEYOND POLITICS'),
    # plots here     pn.Row(pn.Column('### Local Authorities declared', la_dec_plot), " \n \n \n Text description here"),
    name = 'BEYOND POLITICS',
)


# %%
dashboard = pn.Tabs(body_summary, body_telltruth, body_actnow, body_beyondpolitics, body_engagement)
# dashboard


# %%



# %%
dashboard.servable(); # needed for using: panel serve , from command line or on heroku


# %%
# dashboard.show() # only need this to serve when running a jupyter notebook


# %%



