import pandas as pd

df_data = pd.read_excel(io='pop202003.xls',sheet_name='市町村別人口')

#Check the number of rows and columns
print(df_data.shape)

#Extract only the number of columns
length = df_data.shape[1]

print(length)

#Change the name of columns to display　in a universal manner
#Instead of Japanese era name, use numbers
#Instead of Japanese, use English
df_data.columns = ['City_name', '2020-03-01_population', '2020-02-01_population',  '2020-02-01_number_of_increase/decrease','2020-02-01_rate_of_increase/decrease', '2019-02-01_population', '2019-02-01_number_of_increase/decrease', '2019-02-01_rate_of_increase/decrease']

print(df_data.columns)

#Delete the unfunctional rows
df_data = df_data.drop([0,1,2,3,4])

#Print the first 5 rows
print(df_data.head(5))

#Save the data as csv
df_data.to_csv(path_or_buf='pop202003_version1.csv',index=False)

#Read the data saved as csv
df_data = pd.read_csv('pop202003_version1.csv')

#Find the NaN in the '2020-03-01_population'
print(df_data['2020-03-01_population'].isnull())
#True is NaN

#Pull out the NaN in the '2020-03-01_population'
print(df_data[df_data['2020-03-01_population'].isnull()])

#Pull out only numbers that are not NaN 
df_data = df_data[~df_data['2020-03-01_population'].isnull()]

print(df_data.info())

#Save the updated data as new csv file
df_data.to_csv(path_or_buf='pop202003_version2.csv',index=False)

#Since the 'City name' has Japanese and English name, it is hard to see
df_data = pd.read_csv('pop202003_version2.csv')
print(df_data['City_name'])

#Separate it and make it into two columns
#Separate it by space
#But first need to delete the space that is not for separating Japanese and English
#aka the space between Chinese letters
def remove_hankaku(x):
    
    return str(x).replace(' ','')
print(df_data['City_name'].map(remove_hankaku))   

#Save the updated Data to new csv file
df_data.to_csv(path_or_buf='pop202003_version3.csv',index=False)

#Go back to the main purpose of separating and making it into two columns
#Since the English version starts with upper letter alphabet
#Separate by using the isupper function
df_data = pd.read_csv('pop202003_version3.csv')
def get_ja_name(x):
    ja_name = ''
    for num,i in enumerate(x):
        if(i.isupper()):
            ja_name = x[0:num]
            break;
    return ja_name

def get_en_name(x):
    en_name = ''
    for num,i in enumerate(x):
        if(i.isupper()):
            en_name = x[num:]
            break;
    return en_name

#Pull out the Japanese name
ja_name_list = df_data['City_name'].map(get_ja_name)

#Pull out the English name
en_name_list = df_data['City_name'].map(get_en_name)

#Push it into pandas
df_data['City_name'] = ja_name_list

df_data['市町村名_読み'] = en_name_list

#Save the updated Data to new csv file
df_data.to_csv(path_or_buf='pop202003_version4.csv',index=False)

df_data = pd.read_csv('pop202003_version4.csv')

#In order to facilitate future analysis and visualization
#Add the new column "Municipal_classification" for whether the relevant municipality is a city, town, or village

def chk_city_category(x):
    category = ''

    if('市' in x):
        category = 'City'
    elif('町' in x):
        category = 'Town'
    elif('村' in x):
        category = 'Village'
    elif('郡' in x):
        category = 'County'
    return category

#Create the new category row
df_data['Municipal_classification'] = df_data['City_name'].map(chk_city_category)

#Since the 1~2 and 14 rows contain aggregated results
#Delete them
df_data = df_data.drop(index=[0,1,13])

#Save the updated Data to new csv file
df_data.to_csv(path_or_buf='pop202003_version5.csv',index=False)

df_data = pd.read_csv('pop202003_version5.csv')

#Since population and increase/decrease never have decimal point
#Change the data type into integer

df_data = df_data.astype({'2020-03-01_population': int,'2020-02-01_population': int,'2020-02-01_number_of_increase/decrease': int,'2019-02-01_population': int,'2019-02-01_number_of_increase/decrease': int})

#Reorganize the data columns
df_data = df_data[['Municipal_classification','City_name','市町村名_読み', '2020-03-01_population', '2020-02-01_population', '2020-02-01_number_of_increase/decrease','2020-02-01_rate_of_increase/decrease', '2019-02-01_population', '2019-02-01_number_of_increase/decrease', '2019-02-01_rate_of_increase/decrease' ]]

print(df_data.columns)

#Save the updated Data to new csv file
df_data.to_csv(path_or_buf='pop202003_version6.csv',index=False)

#Visualize the Data
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use('ggplot')

df_data = pd.read_csv('pop202003_version6.csv')

#First, plot the number of data
sns.countplot(y=df_data['Municipal_classification'])
plt.show()

#Plot each city, town, and village population 
sns.stripplot(x="Municipal_classification", y="2020-03-01_population", data=df_data)
plt.show()
#It is clear that Village is the highest population, and City and Town are similar number
