import pandas as pds
import requests 
from io import StringIO

def get_sky_patch(ra, dec, obj_class = None): 
    
    '''
        ra -> right ascension in a tuple of degrees, lower and upper bound.
        dec -> declination in a tuple of degrees, lower and upper bound.
        obj_class -> the type of celestial object to select.  Choices are STAR, QSO, GALAXY. * means all.
    '''
    
    # Separate the tuples into their lower and upper bounds.
    ra_lower, ra_upper = ra
    dec_lower, dec_upper = dec

    # We make the query so that it can select from the SDSS data server.
    '''  
        SELECT -> this chooses which values to e taken from the table.
        FROM -> this is where we select which table to query.
        JOIN -> we combine two or more tables into one on a specific column.
        WHERE -> we restrict the data based on Boolean conditions.
    '''

    # Defining the query based on whether a class has been selected or not.
    if obj_class is not None: 
        query = f'''SELECT
                        p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, p.cx, p.cy, p.cz,
                        s.class, s.z as redshift
                    FROM PhotoObj AS p
                    JOIN SpecObj AS s ON s.bestobjid = p.objid
                    WHERE
                        s.class = "{obj_class}" and 
                        p.ra between {ra_lower} and {ra_upper} and
                        p.dec between {dec_lower} and {dec_upper}
                '''

    else:
        query = f'''SELECT
                        p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, p.cx, p.cy, p.cz,
                        s.class, s.z as redshift
                    FROM PhotoObj AS p
                    JOIN SpecObj AS s ON s.bestobjid = p.objid
                    WHERE
                        p.ra between {ra_lower} and {ra_upper} and
                        p.dec between {dec_lower} and {dec_upper}
                '''

    
    # This is where the data is located.  
    url = f'http://skyserver.sdss.org/dr14/SkyServerWS/SearchTools/SqlSearch?cmd={query}&format=csv'
    
    # Making a request to get the data.
    request = requests.get(url)
    
    # We see if there is a successful request.
    if request.status_code == 200:
        
        # This creates a csv file from the request.
        csv = StringIO(request.text)
        
        # Making into a dataframe, since operations on that are easier.
        df = pds.read_csv(csv, skiprows = 1)
        
        return df

    else:
        # If not, we alert the user.
        print('Poor request!')

        return None