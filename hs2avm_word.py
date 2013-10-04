#! /usr/bin/env python
'''
ABOUT:
This program defines a dictionary that is used as a conversion between
Hubblesite subject category and AVM subject category word.

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
01/25/13 (Bourque)
'''

def hs2avm_word():
    '''
    The Hubblesite to AVM subject category word dictionary
    '''
    
    dict = {}

    dict['1'] = 'Planet'
    dict['1.1.1'] = 'Planet.Terrestrial'
    dict['1.1.2'] = 'Planet.Gas Giant'
    dict['1.2.2'] = 'Planet.Atmosphere'
    dict['1.4'] = 'Planet.Satellite'
    dict['1.5'] = 'Planet.Ring'

    dict['2.1'] = 'Interplanetary Body.Dwarf Planet'
    dict['2.2'] = 'Interplanetary Body.Comet'
    dict['2.3'] = 'Interplanetary Body.Asteroid'

    dict['3'] = 'Star'
    dict['3.1.7'] = 'Star.White Dwarf'
    dict['3.1.8'] = 'Star.Blue Supergiant'
    dict['3.1.9'] = 'Star.Neutron Star'
    dict['3.1.9.1'] = 'Star.Neutron Star.Pulsar'
    dict['3.1.10'] = 'Star.Black Hole'
    dict['3.2.1'] = 'Star.Variable'
    dict['3.2.1.5'] = 'Star.Variable.Nova'
    dict['3.2.3'] = 'Star.Brown Dwarf'
    dict['3.6.3'] = 'Star.Multiple'
    dict['3.6.4.1'] = 'Star.Cluster.Open'
    dict['3.6.4.2'] = 'Star.Cluster.Globular'
    dict['3.7.1'] = 'Star.Planetary System'
    dict['3.7.2.1'] = 'Star.Disk.Protoplanetary'

    dict['4.1.3'] = 'Nebula.Planetary'
    dict['4.1.4'] = 'Nebula.Supernova Remnant'
    dict['4.1.5'] = 'Nebula.Jet'
    dict['4.1.6'] = 'Nebula.Bow Shock'
    dict['4.1.7'] = 'Nebula.Intergalactic Medium'
    dict['4.2.1'] = 'Nebula.Emission'
    dict['4.2.3'] = 'Nebula.Dark'
    
    dict['5'] = 'Galaxy'
    dict['5.1.1'] = 'Galaxy.Spiral'
    dict['5.1.4'] = 'Galaxy.Elliptical'
    dict['5.1.6'] = 'Galaxy.Irregular'
    dict['5.1.7'] = 'Galaxy.Interacting'
    dict['5.1.8'] = 'Galaxy.Gravitationally Lensed'
    dict['5.2.2'] = 'Galaxy.Dwarf'
    dict['5.3.2'] = 'Galaxy.AGN'
    dict['5.4.1'] = 'Galaxy.Bulge'
    dict['5.4.3'] = 'Galaxy.Disk'
    dict['5.5.3'] = 'Galaxy.Cluster'

    dict['6.1.1'] = 'Cosmology.Deep Field Survey'
    dict['6.1.2'] = 'Cosmology.Large-Scale Structure'
    dict['6.2.2'] = 'Cosmology.Gamma Ray Burst'
    dict['6.2.3'] = 'Cosmology.Dark Matter'
    dict['6.2.4'] = 'Cosmology.Dark Energy/Acceleration'
    dict['6.2.5'] = 'Cosmology.Universe Age/Size'

    dict['7.1'] = 'The Sky.Night Sky'
    dict['7.1.1'] = 'The Sky.Constellation'
    
    return dict