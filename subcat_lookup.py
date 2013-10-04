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
04 - Refactored output to include a table of press release, subject name,
     distance (in parsec), Hubblesite Subject Category, AVM Letter and AVM 
     number.  Some minor adjustments made to avm_lookup function in order 
     to isolate letter. 

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
09/21/12 (Bourque)
'''

import os
import sys
import subcat_dictionary
from subcat_dictionary import *
import pyExcelerator
from pyExcelerator import *

# -----------------------------------------------------------------------------

def assign_letter(subject_category, distance):
    '''
    Returns the letter A, B, C, D or E based on AVM top level taxonomy and
    the object's distance.
    '''
    
    if subject_category == 'Galaxy > Magellanic Clouds':
        return 'C'
    if subject_category == 'Galaxy > Magellanic Cloud':
        return 'C'
    if distance == '' or distance == '0':
        return ''
    elif distance.isdigit() == True:
        if int(distance) < 1:
            return 'A'
        elif 1 < int(distance) < 40000:
            return 'B'
        elif 40000 < int(distance) < 100000000:
            return 'C'
        elif 100000000 <= int(distance):
            return 'D'
    else:
        return 'E'

# -----------------------------------------------------------------------------
    
def avm_lookup(distance, category):
    '''
    Returns an AVM subject category for a Hubblesite subject category
    '''

    dict = subcat_dictionary()
    try:
        # Build up AVM category
        for cat in category:
            if cat == 'Galaxy > Interacting':
                avm_letter = assign_letter(cat, distance)
                avm_subcat = '5.1.7, 5.5.2'
                print '\tAVM subject category found for', cat, '\n'
            else:
                avm_letter = assign_letter(cat, distance) 
                avm_subcat = dict[cat]
                print '\tAVM subject category found for', cat, '\n'
    
    except:
        print '***** No AVM category specified for', cat, '*****'
        print 'Please add appropriate entry to subcat_dictionary.py'
        print 'Quitting process\n\n'
        sys.exit()
    
    return avm_letter, avm_subcat
        
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

def prep_output(root, press_rel, object, hs_category, avm_letter, avm_subcat):
    '''
    Constructs a file with the year, release, image, object, HS category,
    avm letter and avm category information.
    '''
    
    # Convert hs_category from list to string
    hs_category = ', '.join(hs_category)
        
    # Create ouput file if it doesn't already exist, write header
    if not os.path.exists(root + 'subcat_out.dat'):
        file = open(root + 'subcat_out.dat', 'w')
        file.write('PR|Subj|HS SubCat|AVM letter|AVM SubCat' + '\n')
        file.close()
    
    # Append file with new information
    file = open(root + 'subcat_out.dat', 'a')
    file.write(press_rel + '|' +  object + '|' + hs_category + '|' + \
               avm_letter + '|' + avm_subcat + '\n')
    file.close()
        
# -----------------------------------------------------------------------------

def read_data_file(root):
    '''
    Reads in a file that contains information about release, image, object, 
    distance and hubblesite category
    '''
    
    (press_rel, hs_subcat, object, distance) = [], [], [], []
    
    # Construct lists for each variable
    print '\n*** Reading in data from subcat_in.dat ***\n'
    for line in file(root + 'subcat_in.dat'):
        line_elements = [x for x in line.split('%')]

        press_rel.append(line_elements[0])
        hs_subcat.append(line_elements[1])
        object.append(line_elements[2])
        distance.append(line_elements[3])

    return press_rel, hs_subcat, object, distance

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

def write_excel_output(root):
    '''
    Constructions the output file subcat_out.xls.
    '''

    (press_rel, object, hs_subcat, avm_letter, avm_subcat) = [], [], [], [], [],
   
    # Read in columns in subcat_out.dat
    for line in file(root + 'subcat_out.dat'):
        line_elements = [x for x in line.split('|')]

        press_rel.append(line_elements[0])
        object.append(line_elements[1])
        hs_subcat.append(line_elements[2])
        avm_letter.append(line_elements[3])
        avm_subcat.append(line_elements[4])

    # Create Excel workbook
    workbook = Workbook()
    docsheet = workbook.add_sheet('sheet1')

    # Row Counter
    row = 0

    # Set styles
    font = Font()
    font.bold = True
    fontstyle = XFStyle()
    fontstyle.font = font
    docsheet.row(0).set_style(fontstyle)

    # Write columns to excel file
    for pr, obj, hs_cat, letter, avm_cat in zip(press_rel, object, hs_subcat,
                                                avm_letter, avm_subcat):

        docsheet.write(row, 0, pr)
        docsheet.write(row, 1, obj)
        docsheet.write(row, 2, hs_cat)
        docsheet.write(row, 3, letter)
        docsheet.write(row, 4, avm_cat)
        row = row + 1

    # Save the workbook
    workbook.save(root + 'subcat_out.xls')
    
# -----------------------------------------------------------------------------

def write_text_output(root):
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
    press_rel, hs_subcat, object, distance = read_data_file(root)
    
    # Prep data for other functions
    new_hs_subcat = prep_hs_subcat(hs_subcat)
  
    # For each instance of data, find AVM category and write to output file.
    for rel, obj, dist, new_hs_cat in zip(press_rel, object, distance, 
                                          new_hs_subcat,):
        avm_letter, avm_subcat = avm_lookup(dist, new_hs_cat)
        prep_output(root, rel, obj, new_hs_cat, avm_letter, avm_subcat)
    
    write_text_output(root)
    write_excel_output(root)
            
    print '\nOutput file written to', root + 'subcat_out.dat\n'
   
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    subcat_lookup()