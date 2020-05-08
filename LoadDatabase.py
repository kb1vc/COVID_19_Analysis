# Find the "latest" JHU/CSSE database load it, and return the
# dataframe (with less-than-useful columns optionally removed)

# this is the base directory for the data files.  It assumes
# that the CSSE database has been imported as a submodule.

#
# We may have to look back a few days.  If so, we'll warn
# the user that the database is a little old, and they might
# want to update their submodule.
#
import datetime as dtim
import os.path
import pandas as pd

def findDate(days_ago):
    """Find a date in mm-dd-yyyy format for this day minus days_ago"""
    target_day = dtim.datetime.now() - dtim.timedelta(days = days_ago)
    mmddyyyy = "%02d-%02d-%4d" % (target_day.month, target_day.day, target_day.year)
    return mmddyyyy


def findFile(filename_template, days_ago):
    """Look for a file in the CSSE database for the date 'today - days_ago'"""
    fname = filename_template % findDate(days_ago)
    # does the file exist?
    if os.path.exists(fname) & os.path.isfile(fname):
        return fname
    else:
        return None

    
def searchForFile(filename_template):
    """deeper and deeper we travel into the onion.  Look back 30 days
    until we either find a file, or come up dry.  Either way, if we have
    to look back more than one day, suggest a git submodule update"""

    found_on_first_try = True
    ret = None
    for i in range(30):
        j = i + 1
        fn = findFile(filename_template, j)
        if fn == None:
            found_on_first_try = False
        else:
            ret = fn
            break

    if not found_on_first_try:
        if ret == None:
            print("Looked back 30 days and couldn't find a file")
            warn = "must"
        else:
            print("Had to look back more than one day")
            warn = "may want to"

        print("You %s do a \"submodule update\" at the base of your git-tree to get a copy of more recent CSSE database files." % warn)

    return ret


def loadDatabase(report_selector, remove_cols = {"FIPS", "Country_Region", "Last_Update", "Lat", "Long_", "UID", "ISO3"}):
    """ Find a good database file, and read it, returning a dataframe"""
    # build the report filename
    report_name = None
    sel = report_selector.upper()
    if sel == "US":
        report_name = "daily_reports_us"
    elif sel == "WORLD":
        report_name = "daily_reports"
    else:
        print("Report selector must be either \"US\" or \"WORLD\"")
        return None
    
    base_dir = "./COVID-19/csse_covid_19_data/csse_covid_19_%s" % report_name

    if not (os.path.exists(base_dir) and os.path.isdir(base_dir)):
        print("Could not find a database directory.  Did you load the CSSE COVID-19 submodule?")
        return None
    
    
    base_fname = base_dir + "/%s.csv"
          
    db_fname = searchForFile(base_fname)

    if db_fname == None:
        return None
    
    print("Report file %s" % db_fname)
    rep = pd.read_csv(db_fname)
    # drop a few of the less useful columns
    orig_cols = set(list(rep))
    # make sure we don't try to remove a column that doesn't exist
    actual_remove_cols = list(orig_cols.intersection(remove_cols))
    return rep.drop(columns = actual_remove_cols)
