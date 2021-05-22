from astroquery.vizier import Vizier
import pandas as pds

v = Vizier(columns=['_RAJ2000', '_DEJ2000'])
result = v.query_region("HD 226868", radius="1s")
print(result[150].to_pandas().keys())