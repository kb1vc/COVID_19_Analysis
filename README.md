# COVID_19_Analysis
Example Jupyter Notebook (s) to analyze the JHU COVID-19 databases.

This isn't exactly big data, but it uses some tools that have proved 
useful in many big data experiments.

The Jupyter notebook here reads a "current" version of the JHU CSSE COVID-19
database and does some example slice-and-dice on the data.  It is moderately
simple to extend the analysis or take it in a completely new direction. 

The notebook is intended as an example a starting point.  It is *not* a 
pandas tutorial.  For something like that see [here](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html)

To try out the file, you'll need to have installed jupyter notebook.  Then do this 

```
jupyter notebook DailyExp.ipynb
```

When the jupyter web page pops up in a nearby browser, you should see a 
menubar.  Select Kernel->Restart & Run All

This will read in a recent copy of the JHU COVID-19 database for cases reported in the US. 
