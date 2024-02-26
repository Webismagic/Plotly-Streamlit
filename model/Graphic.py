import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from math import pi
from sqlalchemy import create_engine

class Graphics(object):
    
    _instance = None
    
    # Singleton Pattern
    def __new__(cls, year):
        if cls._instance is None:
            
            cls._instance = super(Graphics, cls).__new__(cls)
            cls._instance.df_years_data = pd.DataFrame()
            cls._instance.df_years_data_summary = pd.DataFrame()
            cls._instance._data_all = cls._instance._fetch_data_all(year)
            cls._instance._year = year
            '''
            for year in range (2013,2024) :
                if (year in [2020]):
                    continue
                    
                data_all = cls._instance._fetch_data_all(year) 
                
                #
                _data_all_years_2 = cls._instance._get_year_data(year, data_all)
                cls._instance.df_years_data = pd.concat([cls._instance.df_years_data, _data_all_years_2])
                
                # 
                _data_all_years = cls._instance._get_year_data_summary(year, data_all)
                cls._instance.df_years_data_summary = pd.concat([cls._instance.df_years_data_summary, _data_all_years])
               ''' 
            cls._instance.df_years_data = cls._instance._read_from_sqlite('df_years_data')
            cls._instance.df_years_data_summary = cls._instance._read_from_sqlite('df_years_data_summary')
            
        return cls._instance
    
#==================================================================
# 1 : Bar : distribution of species by month over one year
#------------------------------------------------------------------
    def get_graphic_type_1(self, year):

        data_final = self._get_year_data(year)
        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Month'] = df_without_boats.index.get_level_values('Date_sortie').month_name()
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')
        
        fig = px.bar(df_without_boats, x='Month', y='N', color='Species',title = f"Species distribution by month {year}", template='plotly_white',labels={"N": "# sightings"})
        
        return fig
    
#=====================================================================
# 2 : Line : distribution of year-round species by month over one year
#---------------------------------------------------------------------
    def get_graphic_type_2(self, year):

        species = ['Delphinus delphis','Grampus griseus','Physeter macrocephalus','Tursiops truncatus']
        data_final = self._get_year_data(year)

        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Month'] = df_without_boats.index.get_level_values('Date_sortie').month_name()
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')
            
        df_sessions = self._get_year_sessions(year)
        df_sessions['Month'] = df_sessions.index.get_level_values('Date_sortie').month_name()
             
        df_yearly = df_without_boats.query(f"Species in {species}")
        
        fig2 = px.line(df_yearly, x="Month", y="N", color="Species", title=f"Year-round Species {year}",template='plotly_white',labels={"N": "# sightings"})
        #fig2.update_layout(yaxis_range=[0,100])
        
        fig2.add_trace(go.Scatter(x=df_sessions['Month'],y=df_sessions['N'],mode="lines", line=go.scatter.Line(color="gray"),  name='Sessions', showlegend=True))
        
        return fig2
    
#===================================================================
# 3 : Line : distribution of seasonal species by month over one year
#-------------------------------------------------------------------
    def get_graphic_type_3(self, year):

        species =  ['Balaenoptera borealis','Globicephala macrorhynchus','Stenella coeruleoalba','Stenella frontalis']
        
        data_final = self._get_year_data(year)

        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Month'] = df_without_boats.index.get_level_values('Date_sortie').month_name()
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')

        df_sessions = self._get_year_sessions(year)
        df_sessions['Month'] = df_sessions.index.get_level_values('Date_sortie').month_name()
        
        df_season = df_without_boats.query(f"Species in {species}")

        fig3 = px.line(df_season, x="Month", y="N", color="Species", title=f"Seasonal species {year}", template='plotly_white',labels={"N": "# sightings"})
        
        fig3.add_trace(go.Scatter(x=df_sessions['Month'],y=df_sessions['N'],mode="lines", line=go.scatter.Line(color="gray"),  name='Sessions', showlegend=True))
        
        return fig3
    
#===========================================================
# 4 : Line : distribution of boats by month over one year
#-----------------------------------------------------------
    def get_graphic_type_4(self, year):
        
        data_final = self._get_year_data(year)
        df_only_boats = data_final[data_final.index.get_level_values('Species') == 'bateau']
        df_only_boats['Month'] = df_only_boats.index.get_level_values('Date_sortie').month_name()
        df_only_boats['Year'] = df_only_boats.index.get_level_values('Date_sortie').year
           
        df_sum_year = df_only_boats.groupby(['Year'])['N'].sum().reset_index()
        boat_sum = df_sum_year['N'][0]

        fig4 = px.line(df_only_boats, x="Month", y="N", title=f"Number of boats {year} : {boat_sum} boats", template='plotly_white',labels={"N": "# boats"})
        #fig4.update_yaxes(range=[0,70])

        return fig4
    
#=====================================================================
# 5 : Line : distribution of sessions(half-days) by month over one year
#---------------------------------------------------------------------
    def get_graphic_type_5(self, year):

        df_only_sessions = self._get_year_sessions(year)

        df_only_sessions['Month'] = df_only_sessions.index.get_level_values('Date_sortie').month_name()

        session_sum = df_only_sessions['N'].sum()
        
        fig = px.line(df_only_sessions, x="Month", y="N", title=f"Number of sessions {year} : {session_sum} sessions", template='plotly_white',labels={"N": "# sessions"})
        #fig4.update_yaxes(range=[0,70])

        return fig

    
#=====================================================================
# 6 : Donut : distribution of sightings by month over one year
#---------------------------------------------------------------------
    def get_graphic_type_6(self, year):

        data_final = self._get_year_data(year)
        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Month'] = df_without_boats.index.get_level_values('Date_sortie').month_name()
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')
        
        fig = px.pie(df_without_boats, values='N', names='Month', title=f'Sighting distribution by Month {year}')
        fig.update_traces(hole=.3)

        return fig

#=====================================================================
# 7 : Donut : distribution of sightings by species over one year
#---------------------------------------------------------------------
    def get_graphic_type_7(self, year):

        data_final = self._get_year_data(year)
        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')
        
        fig2 = px.pie(df_without_boats, values='N', names='Species', title=f'Sighting distribution by Species {year}')

        # Use `hole` to create a donut-like pie chart
        fig2.update_traces(hole=.3)

        return fig2
    
#=====================================================================
# 8 : Line : distribution of species sightings over years
#--------------------------------------------------------------------- 

    def get_graphic_type_8(self):
        
        df_years_data_final = self.df_years_data_summary
        df_without_boats = df_years_data_final.query('Species!="bateau"')
        df_with_boats = df_years_data_final.query('Species=="bateau"')
        
        fig_years = px.line(df_without_boats, x="Year", y="N_x", color="Species", title="Species by Year",template='plotly_white',labels={"N_x": "# sightings"})
        fig_years.update_layout(xaxis_range=[2013,2023])#, yaxis_range=[0,100])
        
        fig_years.add_trace(go.Scatter(x=df_with_boats['Year'],y=df_with_boats['N_y'],mode="lines", line=go.scatter.Line(color="gray"),  name='Sessions', showlegend=True))

        return fig_years

#=====================================================================
# 9 : Line : distribution of boats over years
#---------------------------------------------------------------------
    def get_graphic_type_9(self):

        df_years_data_final = self.df_years_data_summary
        df_only_boats = df_years_data_final.query('Species=="bateau"')

        fig_years_boats = px.line(df_only_boats, x="Year", y="N_x", title="Boats by Year",template='plotly_white',labels={"N_x": "# boats"})
        fig_years_boats.update_layout(xaxis_range=[2013,2023])#, yaxis_range=[0,100])

        return fig_years_boats

#============================================================================
# 10 : Line : distribution of sighings/sessions and sighings/boats over years
#----------------------------------------------------------------------------    
    def get_graphic_type_10(self):

        df_years_data_final = self.df_years_data_summary
        df_without_boats = df_years_data_final.query('Species!="bateau"')
        df_without_boats = df_without_boats[['Year','Species', 'N_x', 'N_y']]
        
        df_only_boats = df_years_data_final.query('Species=="bateau"')
        df_only_boats = df_only_boats[['Year', 'N_x']]
        
        df_years_data_final = df_without_boats.merge(df_only_boats, on=['Year'])
        df_years_data_final =df_years_data_final.rename(columns={'N_x_x':'N', 'N_y':'Sessions','N_x_y':'Boats'})
        
        df_years_data_final['percent_boats'] = round(df_years_data_final['N'] / df_years_data_final['Boats'] *100)
        df_years_data_final['percent_sessions'] = round(df_years_data_final['N'] / df_years_data_final['Sessions'] *100)
        
        #fig_years = px.line(df_years_data_final, x="Year", y="percent_boats", color="Species", title="Species by Year",template='plotly_white',labels={"percent_boats": "% sightings/boats"})
        #fig_years.update_layout(xaxis_range=[2013,2023])#, yaxis_range=[0,100])
        #fig_years.show()
        
        fig_years2 = px.line(df_years_data_final, x="Year", y="percent_sessions", color="Species", title="Percentage of sessions with species presence",template='plotly_white',labels={"percent_sessions": "% of sessions"})
        fig_years2.update_layout(xaxis_range=[2013,2023])#, yaxis_range=[0,100])
        fig_years2.show()
        
        fig_years3 = px.line(df_years_data_final, x="Year", y="Sessions", title="Sessions (half-days) by Year",template='plotly_white',labels={"Sessions": "# sessions"})
        fig_years3.update_layout(xaxis_range=[2013,2023])#, yaxis_range=[0,100])

        return fig_years3
    
#=========================================================
# 11 : Line : distribution of boats by month over years
#---------------------------------------------------------     
    def get_graphic_type_11(self):

        df_years_data = self.df_years_data.reset_index()
        df_years_data_boats = df_years_data.query("Species == 'bateau' and N>0")
        
        df_years_data_boats['Month'] = df_years_data_boats['Date_sortie'].dt.month_name()
        df_years_data_boats['Year'] = df_years_data_boats['Date_sortie'].dt.year
        df_years_data_boats['n_month'] = df_years_data_boats['Date_sortie'].dt.month
        
        df_years_data_boats = df_years_data_boats.groupby(['n_month', 'Month', 'Year'])['N'].sum().reset_index()

        fig_boats_years = px.line(df_years_data_boats, x="Month", y="N", color="Year", title="Boats by month",template='plotly_white',labels={"N": "# boats"})

        return fig_boats_years
   
#================================================================
# 12b : polar : distribution of sightings by species over one year
#---------------------------------------------------------------- 
#https://plotly.com/python/polar-chart/

    def get_graphic_type_12(self, year):
        
        data_final = self._get_year_data(year)
        df_without_boats = data_final[data_final.index.get_level_values('Species') != 'bateau']
        df_without_boats['Month'] = df_without_boats.index.get_level_values('Date_sortie').month_name()
        df_without_boats['Species'] = df_without_boats.index.get_level_values('Species')
        
        df_sessions = self._get_year_sessions(year)
        df_sessions['Month'] = df_sessions.index.get_level_values('Date_sortie').month_name()
        df_sessions['Species'] = 'Sessions'
        
        df_polar = pd.concat([df_without_boats, df_sessions])
           
        fig_polar = px.line_polar(df_polar, r="N", theta="Month", color="Species", line_close=True, color_discrete_sequence=px.colors.sequential.Plasma_r,title = f"Species distribution by month {year}")
        
        return fig_polar
        
#=====================================================================
# 13: Bar : distribution of boats per day over one year
#---------------------------------------------------------------------
    def get_graphic_type_13(self, year):
        
        data_final = self._get_year_data(year, full=1)
        df_only_boats = data_final.xs('bateau',level='Species')

        fig = px.bar(df_only_boats, x=df_only_boats.index,y='N', title=f"Number of boats per day {year} ", template='plotly_white',labels={"Date_sortie":"Date","N": "# boats"}, color=df_only_boats.index.month_name())

        return fig


#================================================================
#  internal functions
#---------------------------------------------------------------- 
    
    # get data to build dataframe for graphics over one year
    def _get_year_data(self, year, data=None, full=0):
        
        if (data is None):
            if (self._year != year):
                data_all =self._fetch_data_all(year)
                self._year = year
                self._data_all = data_all
            else:
                data_all = self._data_all
        else:
            data_all = data
        
        data_all = data_all.groupby(['Species'])
        
        if (full == 0):
            data_all = data_all.resample('M').sum()
        else:
            data_all = data_all.resample('D').sum()
            
        data_all = data_all.sort_index(level=['Date_sortie', 'Species'])

        return data_all
     
    
    # get data to build dataframe for sessions graphic over one year (with multi-index)
    def _get_year_sessions(self, year):

        if (self._year != year):
            data_all =self._fetch_data_all(year)
            self._year = year 
            self._data_all = data_all
        else:
            data_all = self._data_all
            
        #filter on boats, remove if all species needed
        data_all = data_all.query('Species=="bateau"')

        # transform N to 0 and 1
        data_all['N'] = data_all['N'].apply(lambda x: 1 if x > 0 else x)
        
        # sum on Month of date multi-index
        data_all = data_all.groupby(['Species', pd.Grouper(level='Date_sortie', freq='M')])['N'].sum()
       
        data_sessions = pd.DataFrame(data_all)

        return data_sessions


    #get year data to build over years graphic
    def _get_year_data_summary(self, year, data):

        data_all = data.reset_index()
        data_all['Year'] = data_all['Date_sortie'].dt.year

        data_all_boats = data_all.query("Species == 'bateau' and N>0")
        data_all_boats = data_all_boats.groupby(['Year'], as_index=False)['N'].count()
              
        data_all = data_all.query("N>0")
        data_all = data_all.groupby(['Year','Species'])['N'].sum().reset_index()
        
        df_year_obs_by_sessions = data_all.merge(data_all_boats, on='Year')
        df_year_obs_by_sessions['percent'] = round(df_year_obs_by_sessions['N_x'] / df_year_obs_by_sessions['N_y'] *100)
        
        return df_year_obs_by_sessions

   
    #read csv data files to create global dataframe (long)
    def _fetch_data_all(self, year):
        
        print("read data",year)
        data_all = pd.DataFrame()

        for i in range(4,11):
            #file_name = f"/home/webismagic/mysite/data/azores/data_{year}/Azores-{i}-{year}.csv"
            file_name = f"data_{year}/Azores-{i}-{year}.csv"
            df_temp = pd.read_csv(file_name,sep=',')
            df_temp_long = pd.melt(df_temp, id_vars =['espece','periode'], value_vars = df_temp.iloc[:,2:33],var_name='Date_sortie',value_name='N')
            data_all = pd.concat([data_all, df_temp_long])

        data_all.index = pd.to_datetime(data_all['Date_sortie'], dayfirst=True)
        del data_all['Date_sortie']
        data_all = data_all.rename(columns={'espece': 'Species'})
        return data_all
    
    def _save_to_sqlite (self, df1,df2):
        # Définir le moteur SQLite
        engine = create_engine('sqlite:///azores-data-full.db')
        df1 = df1.reset_index()
        
        # Sauvegarder le DataFrame dans SQLite
        df1.to_sql('df_years_data', engine, index=False)
        df2.to_sql('df_years_data_summary', engine, index=False)
        
    def _read_from_sqlite(self, table):
        
        # Définir le moteur SQLite
        engine = create_engine('sqlite:///azores-data.db')

        # Lire la table dans un DataFrame
        return pd.read_sql_table(table, engine)
  
