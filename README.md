# SpaceMissionsDashboard
An interactive dashboard to visualize and analyze historical space mission data from 1957 to 2022.

## Tech Stack
Python + Streamlit  
I picked this tech stack because both Python and Streamlit are simple to use and therefore fast  
to prototype with. Python also has great libraries for csv file parsing.    

## Running the App  
To run the app, make sure you have streamlit, pandas, pytest, and plotly installed.    
You can run it with the command "python -m streamlit run app.py"  

## Design Choices  
The app includes a main table that supports standard ordering methods alongside    
some more advanced filters such as Date Range, Company, Mission Status, Location,      
and Rocket. These filters can be used in combination with each other to deliver    
more precise results.  

The app also includes average missions per year, which allows the user to adjust  
the year range and view the corresponding results.  

The app also shows a missions per year graph that shows the number of missions  
each year for every year in the dataset. I included this because it is interesting  
to see how missions decreased after the space race.   

I also included charts for the top companies by mission count and mission status counts    
(ie. how many failures were there overall) as well as the most used rocket.  
At the bottom of the page, there are also some basic statistics like total missions  
and total success rate.      

## Note on Testing  
The test examples in the instruction document did not seem to match with the data in the csv file    
(in csv file NASA has 203 missions, but the instruction doc example says 394)       
