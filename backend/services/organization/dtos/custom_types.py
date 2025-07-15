import re

from pydantic import constr

OrganizationName = constr(min_length=3, max_length=20, strip_whitespace=True) # Max and min length can be tweaked as per requirements