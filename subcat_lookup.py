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
07 - Handles distances in LY and distances of letter 'D', in which an avm letter
     of 'D' is used in the avm_number.  Also adds all information to the object
     dictionary.  Also handels redshifts that begin with '-,'

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
10/23/12 (Bourque)
'''

import os
import sys
import hs2avm_number
from hs2avm_number import hs2avm_number
import hs2avm_word
from hs2avm_word import hs2avm_word

# -----------------------------------------------------------------------------

def assign_letter(subject_category, distance):
    '''
    Returns the letter A, B, C, D or E based on AVM top level taxonomy and
    the object's distance.
    '''

    # Set letter specifically for Magellanic Clouds
    if subject_category == 'Galaxy > Magellanic Clouds':
        return 'C.'
    if subject_category == 'Galaxy > Magellanic Cloud':
        return 'C.'

    # Set letter specifically for distance of 'D'
    if distance == 'D' or distance[0:2] == '-,':
        return 'D.'
        
    # Return no letter if no subject category is given
    if distance == '':
        return ''
        
    # Determine letter via distance    
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
    Returns an AVM subject category number and word for a Hubblesite subject 
    category
    '''

    number_dict = hs2avm_number()
    word_dict = hs2avm_word()
    avm_number = []
    avm_word = []

    try:
        # Build up AVM category
        for cat in category:
            if cat == 'Galaxy > Interacting':
                letter = assign_letter(cat, distance)
                subcat_num = letter + '5.1.7, ' + letter + '5.5.2'
                subcat_word = 'Galaxy.Interacting, Galaxy.Multiple'
                avm_word.append(subcat_word)
                avm_number.append(subcat_num)
                print '\tAVM subject category found for', cat, '\n'
            elif cat == 'Miscellaneous' or cat == 'unknown':
                avm_number, avm_word = [], []
            else:
                subcat_num = assign_letter(cat, distance) 
                subcat_num += number_dict[cat]
                avm_number.append(subcat_num)

                # Strip avm_number of letter, if it exists, for lookup
                if subcat_num[0].isalpha() == True:
                    subcat_num = subcat_num[2:]
                subcat_word = word_dict[subcat_num]
                avm_word.append(subcat_word)
                print '\tAVM subject category found for', cat, '\n'
    
        # Convert avm lists to strings
        avm_number = '; '.join(avm_number)
        avm_word = '; '.join(avm_word)

    except:
        print '***** No AVM category specified for', cat, '*****'
        print 'Please add appropriate entry to dictionaries'
        print 'Quitting process\n\n'
        sys.exit()
    
    return avm_number, avm_word
        
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

def prep_output(root, year, release, image, avm_number, avm_word, hs_category):
    '''
    Constructs a file with the year, release, image and subject category 
    information.  The file may contain duplicates.
    '''
    
    # Replace '&gt' in hs_category with '>'
    hs_category = hs_category.replace('&gt;','>')
        
    # Create ouput file if it doesn't already exist, write header
    if not os.path.exists(root + 'subcat_out.dat'):
        file = open(root + 'subcat_out.dat', 'w')
        file.write('year%release%image%avm number%avm word%Subject.Category'
                    + '\n')
        file.close()
    
    # Append file with new information
    file = open(root + 'subcat_out.dat', 'a')
    file.write(year + '%' + release + '%' + image + '%' +  \
               avm_number.replace(' ', '') + '%' + avm_word.replace(' ','') + 
               '%' + hs_category + '\n')
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

def update_obj_dict(root, year, release, image, object, distance, avm_number, 
                    avm_word, hs_subcat):
    '''
    Updates obj_dict.dat with object name and avm_category information.
    '''

    # Rebuild press release string
    pr = year + '-' + release + '-' + image

    pr_in_dict = [line.split('|')[0] for line in file(root + 'obj_dict.dat')]
    
    # Add entry to object dictionary if its not already in there
    if pr not in pr_in_dict:
        print '\tAdding', pr, 'to dictionary'
        dict = open(root + 'obj_dict.dat', 'a')
        dict.write(pr + '|' + object + '|' + distance + '|' + avm_number + \
                  '|' + avm_word + '|' + hs_subcat + '\n')
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
        avm_num, avm_word = avm_lookup(dist, new_hs_cat)
        update_obj_dict(root, yr, rel, im, obj, dist, avm_num, avm_word, 
                        old_hs_cat)

        prep_output(root, yr, rel, im, avm_num, avm_word, old_hs_cat)
    
    write_output(root)
            
    print '\nOutput file written to', root + 'subcat_out.dat\n'
   
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    subcat_lookup()