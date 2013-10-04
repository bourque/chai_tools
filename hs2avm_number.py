#! /usr/bin/env python
'''
ABOUT:
This program defines a dictionary that is used as a conversion between
Hubblesite subject category and AVM subject category number

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
01/25/13 (Bourque)
'''

def hs2avm_number():
    '''
    The Hubblesite to AVM subject category number dictionary
    '''
    
    dict = {}
    
    dict['Cosmology > Distant Galaxies'] = '6.1.1'
    dict['Cosmology > Intergalactic Gas'] = '4.1.7'
    dict['Cosmology > Universe: Age/Size'] = '6.2.5'
    
    dict['Exotic > Black Hole'] = '3.1.10'
    dict['Exotic > Dark Energy'] = '6.2.4'
    dict['Exotic > Dark Matter'] = '6.2.3'
    dict['Exotic > Gamma Ray Burst'] = '6.2.2'
    dict['Exotic > Gravitational Lens'] = '5.1.8'
    dict['Exotic > Distant Galaxies'] = '5'
    dict['Exotic > Gravitational Lens Galaxy > Cluster'] = '5.1.8'
    
    dict['Galaxy > Cluster'] = '5.5.3'
    dict['Galaxy > Dwarf'] = '5.2.2'
    dict['Galaxy > Elliptical'] = '5.1.4'
#    dict['Galaxy > Interacting'] = '5.1.7'
    dict['Galaxy > Irregular'] = '5.1.6'
    dict['Galaxy > Magellanic Clouds'] = '5.1.6'
    dict['Galaxy > Magellanic Cloud'] = '5.1.6'
    dict['Galaxy > Milky Way Center'] = '5.4.1'
    dict['Galaxy > Quasar/Active Nucleus'] = '5.3.2'
    dict['Galaxy > Quasar/Active Nucleus Galaxy > Spiral'] = '5.3.2'
    dict['Galaxy > Spiral'] = '5.1.1'
    
    dict['Nebula > Dark'] = '4.2.3'
    dict['Nebula > Dark Nebula > Emission'] = '4.2.1'
    dict['Nebula > Emission'] = '4.2.1'
    dict['Nebula > Planetary'] = '4.1.3'
    dict['Nebula > Reflection'] = '4.2.3'
    dict['Nebula > Supernova Remnant'] = '4.1.4'
    dict['Nebula > Emission Star Cluster > Globular Star Cluster > Open'] = '3.6.4.1'
    
    dict['Solar System > Venus'] = '1.1.1'
    dict['Solar System > Mars'] = '1.1.1'
    dict['Solar System > Jupiter'] = '1.1.2'
    dict['Solar System > Saturn'] = '1.1.2'
    dict['Solar System > Uranus'] = '1.1.2'
    dict['Solar System > Neptune'] = '1.1.2'
    dict['Solar System > Pluto'] = '2.1'
    dict['Solar System > Planetary Moon'] = '1.4'
    dict['Solar System > Planetary Ring'] = '1.5'
    dict['Solar System > Weather/Atmosphere'] = '1.2.2'
    dict['Solar System > Asteroid'] = '2.3'
    dict['Solar System > Comet'] = '2.2'
    dict['Solar System > Kuiper Belt Object'] = '2.3'
    dict['Solar System > Minor Body'] = '2.3'
    
    dict['Star > Bow Shock'] = '4.1.6'
    dict['Star > Brown Dwarf'] = '3.2.3'
    dict['Star > Constellation'] = '7.1.1'
    dict['Star > Massive Star'] = '3'
    dict['Star > Multiple Star Systems'] = '3.6.3'
    dict['Star > Neutron Star'] = '3.1.9'
    dict['Star > Nova'] = '3.2.1.5'
    dict['Star > Protostellar Jet'] = '4.1.5'
    dict['Star > Protoplanetary Disk'] = '3.7.2.1'
    dict['Star > Pulsar'] = '3.1.9.1'
    dict['Star > Star Field'] = '7.1'
    dict['Star > Extrasolar Planets'] = '3.7.1'
    dict['Star > Supernova'] = '3.1.8'
    dict['Star > Variable Star'] = '3.2.1'
    dict['Star > White Dwarf'] = '3.1.7'
    
    dict['Star Cluster > Globular'] = '3.6.4.2'
    dict['Star Cluster > Open'] = '3.6.4.1'
    
    dict['Survey > Galactic Center Survey > '] = '5'
    dict['Survey > GOODS'] = '6.1.1'
    dict['Survey > Hubble Deep Field'] = '6.1.1'
    dict['Survey > Hubble Ultra Deep Field'] = '6.1.1'
    dict['Survey > Medium Deep Survey'] = '6.1.1'
    dict['Survey > COSMOS'] = '6.1.2'
    dict['Survey > CLASH'] = '5.1.8'
    dict['Survey > CANDELS'] = '6.1.1'
    dict['Survey > PHAT'] = '5.4.3'
    dict['Survey > BoRG'] = '5'
    
    dict['unknown'] = ''
    
    return dict