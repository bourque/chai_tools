#! /usr/bin/env python
'''
ABOUT:
This program intakes a row of image information and looks up the AVM subject
category in a pre-made dictionary.  If a corresponding entry does not exist
in the dictionary, it is added.  Ultimately, the AVM subject category is
returned. Information with the new AVM subject category is written to an
output file.  This program is to be run from the command line.  It is 
essential to have obj_dict.dat, subcat_in.dat and subcat_lookup.py files in the
current working directory.

VERSION:
02 - input should contain id, object name, hs subject category and distance
     (%-separated).  The distance is optional.

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
08/30/12 (Bourque)
'''

import os
import sys
import subcat_dictionary
from subcat_dictionary import *

# -----------------------------------------------------------------------------

def assign_letter(distance):
    '''
    Returns the letter A, B, C, D or E based on AVM top level taxonomy and
    the object's distance.
    '''
    
    if distance == '':
        return ''
    elif distance.isdigit() == True:
        if int(distance) < 1:
            return 'A.'
        elif 1 < int(distance) < 40000:
            return 'B.'
        elif 40000 < int(distance) < 100000000:
            return 'C.'
        elif 100000000 <= int(distance):
            return 'D.'
    else:
        return 'E.'

# -----------------------------------------------------------------------------
    
def avm_lookup(distance, category):
    '''
    Returns an AVM subject category for a Hubblesite subject category
    '''

    dict = subcat_dictionary()
    avm_category = []
    
    try:
        # Build up AVM category
        for cat in category:
            subcat = assign_letter(distance)
            subcat += dict[cat]
            avm_category.append(subcat)
            print '\tAVM subject category found for', cat, '\n'
    
        # Convert avm_category list to string
        avm_category = '; '.join(avm_category)
    
    except:
        print '***** No AVM category specified for', cat, '*****'
        print 'Please add appropriate entry to subcat_dictionary.py'
        print 'Quitting process\n\n'
        sys.exit()
    
    return avm_category
        
# -----------------------------------------------------------------------------

def prep_hs_subcat(hs_subcat):
    '''
    Takes a string of comma separated hubblesite subject categories and
    returns a list of the different category types.  Also removes 'X.' and
    '&gt;' from STPR results
    '''
    
    preped_hs_subcat = []
    
    for item in hs_subcat:
        item = item.strip('X.')
        item = item.replace('&gt;','>')
        item = item.split(', ')
        preped_hs_subcat.append(item)
    
    return preped_hs_subcat

# -----------------------------------------------------------------------------

def prep_image_info(image_info):
    '''
    Takes an STPR release info data string and splits it up into year, 
    release number and image letter
    '''
    
    (year, release, image) = [], [], []
    
    for item in image_info:
        info_elements = [x for x in item.split('-')]
        year.append(info_elements[0])
        release.append(info_elements[1])
        image.append(info_elements[2])
  
    return year, release, image
    
# -----------------------------------------------------------------------------

def prep_output(root, year, release, image, avm_category, hs_category):
    '''
    Constructs a file with the year, release, image and subject category 
    information.  The file may contain duplicates.
    '''
    
    # Replace '&gt' in hs_category with '>'
    hs_category = hs_category.replace('&gt;','>')
        
    # Create ouput file if it doesn't already exist, write header
    if not os.path.exists(root + 'subcat_out.dat'):
        file = open(root + 'subcat_out.dat', 'w')
        file.write('year%release%image%Subject.Category' + '\n')
        file.close()
    
    # Append file with new information
    file = open(root + 'subcat_out.dat', 'a')
    file.write(year + '%' + release + '%' + image + '%' +  \
               avm_category.replace(' ', '') + '; ' + hs_category + '\n')
    file.close()
        
# -----------------------------------------------------------------------------

def read_data_file(root):
    '''
    Reads in a file that contains information about release, image, object, 
    distance and hubblesite category
    '''
    
    (image_info, hs_subcat, object, distance) = [], [], [], []
    
    # Construct lists for each variable
    print '\n*** Reading in data from subcat_in.dat ***\n'
    for line in file(root + 'subcat_in.dat'):
        line_elements = [x for x in line.split('%')]

        image_info.append(line_elements[0])
        hs_subcat.append(line_elements[1])
        object.append(line_elements[2])
        distance.append(line_elements[3])

    return image_info, hs_subcat, object, distance

# -----------------------------------------------------------------------------

def update_obj_dict(root, object, avm_category):
    '''
    Updates obj_dict.dat with object name and avm_category information.
    '''
    
    obj_list = object.split(';')
    avm_list = avm_category.split(';')

    obj_in_dict = [line.split('|')[0] for line in file(root + 'obj_dict.dat')]
    
    for obj, avm in zip(obj_list, avm_list):
    
        # Add entry to object dictionary if its not already in there
        if obj not in obj_in_dict:
            print '\tAdding', obj, 'to dictionary'
            dict = open(root + 'obj_dict.dat', 'a')
            dict.write(obj + '|' + avm + '\n')
            dict.close()
        else:
            pass
    
# -----------------------------------------------------------------------------

def write_output(root):
    '''
    Constructs the output file subcat_out.dat with year, release, iamge and
    subject category information and ensures that there are no duplicate
    entries.
    '''
    
    # Use temp file to append only unique information
    unique_release = set()
    outfile = open(root + 'subcat_out_tmp.dat', 'a')
    for line in open(root + 'subcat_out.dat', 'r'):
        if line not in unique_release:
            outfile.write(line)
            unique_release.add(line)
    outfile.close()
    
    # Replace output file with temporary output file
    os.remove(root + 'subcat_out.dat')
    os.rename(root + 'subcat_out_tmp.dat', root + 'subcat_out.dat')
    
    
# -----------------------------------------------------------------------------
#       Main Controller
# -----------------------------------------------------------------------------

def subcat_lookup():
    '''
    The main controller.
    '''
    
    # Set the data path
    root = os.getcwd() + '/'

    # Read in data
    image_info, hs_subcat, object, distance = read_data_file(root)
    
    # Prep data for other functions
    year, release, image = prep_image_info(image_info)
    new_hs_subcat = prep_hs_subcat(hs_subcat)
    
    # For each instance of data, find AVM category and write to output file.
    for yr, rel, im, obj, dist, new_hs_cat, old_hs_cat in zip(year, release, 
                                                              image, object, 
                                                              distance, 
                                                              new_hs_subcat,
                                                              hs_subcat):
        avm = avm_lookup(dist, new_hs_cat)
        update_obj_dict(root, obj, avm)
        prep_output(root, yr, rel, im, avm, old_hs_cat)
    
    write_output(root)
            
    print '\nOutput file written to', root + 'subcat_out.dat\n'
   
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    subcat_lookup()