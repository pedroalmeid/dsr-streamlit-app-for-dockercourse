import streamlit as st
import pandas as pd
import numpy as np

from plots import create_scatter_plot, create_country_plot, create_comparison_plots, create_comparison_plots_past
from data import get_data
from models import get_life_prediction

def main():
    st.set_page_config(layout="wide")

    st.markdown("# 🌍 Global Life Quality and Economic Analysis 📊 - Edited by Pedro")

    st.markdown("""
    This app allows you to explore the relationships between poverty, 
    life expectancy, and GDP across different countries and years. 
    Use the sidebars to select options and interact with the data.
    """)

    # Get the merged dataframes
    merged_df = get_data()

    merged_df = merged_df.dropna(subset=['country', 'GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'Life Expectancy (IHME)', 'year'], axis=0)
    
    # Sidebar
    #continents = st.sidebar.multiselect("Select Continents", 
    #                                    merged_df['Continent'].unique().tolist(),
    #                                    default=merged_df['Continent'].unique().tolist())


    # Tabs
    tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

    with tab1:
        st.header("Global Overview")

        # Key statistics
        

        # Scatter plot
        year = st.slider("Select Year for Visualization", min_value=1990, max_value=2016, value=2016)

        #latest_year = filtered_df['year'].max()
        frozen_df = merged_df[merged_df['year']==year]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Global Average Life Expectancy", f"{frozen_df['Life Expectancy (IHME)'].mean():.1f} years")
        with col2:
            st.metric("Global Median GDP per capita", f"${frozen_df['GDP per capita'].median():,.0f}")
        with col3:
            st.metric("Global Poverty Average", f"{frozen_df['headcount_ratio_upper_mid_income_povline'].mean():,.0f}%")
        with col4:
            st.metric("Number of Countries", f"{frozen_df['country'].nunique()}")

        fig = create_scatter_plot(merged_df, year)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"Correlation coefficients in {year}")
        # Correlation analysis
        

        cols1, cols2, cols3 = st.columns(3)
        correlation_1 = frozen_df['Life Expectancy (IHME)'].corr(frozen_df['GDP per capita'])
        correlation_2 = frozen_df['Life Expectancy (IHME)'].corr(frozen_df['headcount_ratio_upper_mid_income_povline'])
        correlation_3 = frozen_df['GDP per capita'].corr(frozen_df['headcount_ratio_upper_mid_income_povline'])
        
  
        with cols1:
            st.metric("Life Expectancy & GDP per capita in", f"{correlation_1:.2f}")
        with cols2:
            st.metric("Life Expectancy & Poverty percentage", f"{correlation_2:.2f}")
        with cols3:
            st.metric("GDP per capita & Poverty percentage", f"{correlation_3:.2f}")

        st.markdown("""
        ### Key Insights
        - There's a strong positive correlation between GDP per capita and life expectancy.
        - There's a even stronger inverse correlation between poverty and life expectancy.
        - The size of the bubbles indicate how much poorer the poor countries are, to the extent that the richest countries are almost not seen.
        - The changes in the correlation between GDP per capita and poverty rates across time indicate fluctuations in the distribution of wealth.
        """)


        get_life_prediction(merged_df)

    with tab2:
        st.header("Country Deep Dive")
        
         # Country selection
        countries = sorted(merged_df['country'].unique())
        country = st.selectbox('Select a Country', countries)

        # Country plot
        country_data = merged_df[merged_df['country'] == country].copy()

        fig = create_country_plot(country_data, country)
        st.plotly_chart(fig, use_container_width=True)

        # Latest statistics for selected country
        latest_country_year = country_data['year'].max()
        latest_country_data = country_data[country_data['year']==latest_country_year].iloc[0]

        st.write(f"### Latest Statistics for {country} ({latest_country_year})")
        st.write(f"Life Expectancy: {latest_country_data['Life Expectancy (IHME)']:.2f} years")
        st.write(f"GDP per capita: ${latest_country_data['GDP per capita']:,.2f}")
        #st.write(f"Human Development Index: {latest_country_data['Human Development Index']:.3f}")

        # Latest statistics for selected country and selected year

        # Year selection
        st.write("\n")
        st.write("\n")
        selected_year = st.slider(f"## Select the year to dispay statistics for", 
                                  min_value=int(country_data['year'].min()), 
                                  max_value=int(country_data['year'].max()), 
                                  value=int(country_data['year'].max()))


        selected_country_data = country_data[country_data['year']==selected_year]
        
        if not selected_country_data.empty:
            selected_country_data = selected_country_data.iloc[0]
            st.write(f"### Statistics for {country} in Year {selected_year}")
            st.write(f"Life Expectancy: {selected_country_data['Life Expectancy (IHME)']:.2f} years")
            st.write(f"GDP per capita: ${selected_country_data['GDP per capita']:,.2f}")

            #st.write(f"### {country} in the World Distribution in {selected_year}",)
            comparison_fig = create_comparison_plots(merged_df, country_data, country, selected_year)
            st.plotly_chart(comparison_fig, use_container_width=True)
        else:
            st.write(f"### No data available for {country} in year {selected_year}")

        

    with tab3:
        st.header("Data Explorer")

        st.subheader("Global data for selected time range")

        year_range = st.slider("Select Year Range", 
                                   min_value=int(merged_df['year'].min()), 
                                   max_value=int(merged_df['year'].max()), 
                                   value=(int(merged_df['year'].min()), int(merged_df['year'].max())))

        # Filter data based on selections
        filtered_df = merged_df[(merged_df['year'].between(year_range[0], year_range[1]))]

        # Data table
        st.write(filtered_df)


        # Download option
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='global_development_data.csv',
            mime='text/csv',
        )

        st.subheader(f"Local data for {country} for all available years.")
        st.write(country_data)

        # Download option
        csv =country_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{country}_development_data.csv',
            mime='text/csv',
        )


if __name__ == "__main__":
    main()