#! /usr/bin/env python
'''
ABOUT:
This program intakes a file with image information and determines the AVM 
subject category for each press release.  Information with the new AVM subject 
categories from new executions of this script are written to an output file 
called 'obj_dict.dat'. This program is to be run from the command line.

subcat_lookup.py needs to be accompanied (in the same directory) by the files 
subcat_in.dat, hs2avm_number.dat, and avm_number2avm_word.dat.

subcat_in.dat should be a text file that contains the press release number, 
HubbleSite subject category, object, and distance for each press relelease to 
be processed, separated by '%', in that order.

hs2avm_number.dat should be a text file that contains the Hubblesite category
and the corresponding AVM subject category number, separated by a comma (',')

avm_number2avm_word.dat should be a text file that contains the AVM subject
category number and the corresponding AVM subject category word, separated
by a comma (',').

EXAMPLE:  From the command line:

            python subcat_lookup.py

AUTHOR:
Matthew Bourque
Space Telescope Science Institute
bourque@stsci.edu

LAST UPDATED:
02/19/13 (Bourque)
'''

import os
import sys
import subprocess
import numpy as np

class SubcatLookup():
    '''
    Parent class
    '''

    # -------------------------------------------------------------------------

    def __init__(self):
        '''
        Initialization function.
        '''

        # Set the data path
        self.root = os.getcwd() + '/'

        # Create obj_dict.dat, if it doesn't already exist
        if os.path.exists(self.root + 'obj_dict.dat') == False:
            subprocess.call(['touch', self.root + 'obj_dict.dat'])
            print '\n\tCreating obj_dict.dat file'

    # -------------------------------------------------------------------------

    def assign_letter(self, subject_category, distance):
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
        if distance == 'D' or distance[0:2] == '-;':
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

    # -------------------------------------------------------------------------
        
    def avm_lookup(self, distance, category):
        '''
        Returns an AVM subject category number and word for a Hubblesite 
        subject category.
        '''

        self.avm_number = []
        self.avm_word = []

        try:

            # Build up AVM category
            for cat in category:

                # Special case for Galaxy > Interacting
                if cat == 'Galaxy > Interacting':
                    letter = self.assign_letter(cat, distance)
                    subcat_num = letter + '5.1.7, ' + letter + '5.5.2'
                    subcat_word = 'Galaxy.Interacting, Galaxy.Multiple'
                    self.avm_word.append(subcat_word)
                    self.avm_number.append(subcat_num)
                    print '\tAVM subject category found for', cat, '\n'

                # Special case for Miscellaneous or unknown
                elif cat == 'Miscellaneous' or cat == 'unknown':
                    self.avm_number, self.avm_word = [], []

                # Normal cases
                else:
                    subcat_num = self.assign_letter(cat, distance) 
                    subcat_num += self.avm_number_dict[cat]
                    self.avm_number.append(subcat_num)

                    # Strip avm_number of letter, if it exists, for lookup
                    if subcat_num[0].isalpha() == True:
                        subcat_num = subcat_num[2:]
                    subcat_word = self.avm_word_dict[subcat_num]
                    self.avm_word.append(subcat_word)
                    print '\tAVM subject category found for', cat, '\n'
        
            # Convert avm lists to strings
            self.avm_number = '; '.join(self.avm_number)
            self.avm_word = '; '.join(self.avm_word)

        except Exception:
            print '***** No AVM category specified for', cat, '*****'
            print 'Please add appropriate entry to dictionaries'
            print 'Quitting process\n\n'
            sys.exit()
            
    # -------------------------------------------------------------------------

    def build_subcat_dict(self, datafile):
        '''
        Builds a dictionary relating the Hubblesite category to the AVM subject
        category number or AVM subject category word, depending on the 
        datafile.
        '''

        # Ensure that the data file exists
        assert os.path.isfile(datafile), datafile + ' does not exist.'

        # Read in data from file
        dict_key, dict_value = np.loadtxt(datafile, dtype = str, 
            delimiter = ',', unpack = True, usecols = [0,1])

        # Convert to lists
        dict_key = list(dict_key)
        dict_value = list(dict_value)

        # Ensure there is no missing data
        for key, value in zip(dict_key, dict_value):
            assert key != '' and value != '', 'Missing data in dictionary.'

        # Build dictionary key for each line in lists
        avm_dict = {}
        for key, value in zip(dict_key, dict_value):
            avm_dict[key] = value

        return avm_dict

    # -------------------------------------------------------------------------

    def prep_hs_subcat(self):
        '''
        Takes a string of comma separated hubblesite subject categories and
        returns a list of the different category types.  Also removes 'X.' and
        '&gt;' from STPR results.
        '''
        
        self.new_hs_subcat = []
        
        for item in self.hs_subcat:
            item = item.strip('X.')
            item = item.replace('&gt;','>')
            item = item.split(', ')
            self.new_hs_subcat.append(item)

    # -------------------------------------------------------------------------

    def prep_image_info(self):
        '''
        Takes an STPR release info data string and splits it up into year, 
        release number and image letter.
        '''
        
        (self.year, self.release, self.image) = [], [], []
        
        for item in self.image_info:
            info_elements = [x for x in item.split('-')]
            self.year.append(info_elements[0])
            self.release.append(info_elements[1])
            self.image.append(info_elements[2])
        
    # -------------------------------------------------------------------------

    def prep_output(self, year, release, image):
        '''
        Constructs a file with the year, release, image and subject category 
        information.  The file may contain duplicates.
        '''
            
        # Create ouput file if it doesn't already exist, write header
        if not os.path.exists(self.root + 'subcat_out.dat'):
            with open(self.root + 'subcat_out.dat', 'w') as outfile:
                outfile.write('year%release%image%avm number%avm word' + '\n')

        # Rebuild press release string
        pr = year + '-' + release + '-' + image
        
        # Append file with new information
        with open(self.root + 'subcat_out.dat', 'a') as outfile:
            outfile.write(pr + '%' + self.avm_number + '%' + 'X.' + 
                          self.avm_word + '\n')
            
    # -------------------------------------------------------------------------

    def read_data_file(self):
        '''
        Reads in a file that contains information about release, image, object,
        distance and hubblesite category.
        '''
        
        (self.image_info, self.hs_subcat, self.object, self.distance) = \
            [], [], [], []
        
        # Construct lists for each variable
        print '\n*** Reading in data from subcat_in.dat ***\n'
        with open(self.root + 'subcat_in.dat', 'r') as datafile:
            for line in datafile:
		print line
                line_elements = [x for x in line.split('%')]

                self.image_info.append(line_elements[0])
                self.hs_subcat.append(line_elements[1])
                self.object.append(line_elements[2])
                self.distance.append(line_elements[3])

    # -------------------------------------------------------------------------

    def update_obj_dict(self, year, release, image, object, distance):
        '''
        Updates obj_dict.dat with object name and avm_category information.
        '''

        # Rebuild press release string
        pr = year + '-' + release + '-' + image

        # Replace distance of 'D' or '' with '-'
        if distance == '' or distance == 'D':
            distance = '-'

        distance = distance.replace('D', '-')

        pr_in_dict = [line.split('|')[0] for line in file(self.root + 
                      'obj_dict.dat')]

        # Remove duplicate avm_word and avm_number
        self.avm_word = self.avm_word.split('; ')
        self.avm_word = set(self.avm_word)
        self.avm_word = ', '.join(self.avm_word)
        self.avm_number = self.avm_number.split('; ')
        self.avm_number = set(self.avm_number)
        self.avm_number = ', '.join(self.avm_number)
        
        # Add entry to object dictionary if its not already in there
        if pr not in pr_in_dict:
            print '\tAdding', pr, 'to dictionary'
            with open(self.root + 'obj_dict.dat', 'a') as objdict:
                objdict.write(pr + '|' + object + '|' + distance + '|' + 
                    self.avm_number + '; ' + 'X.' + self.avm_word + '\n')
        else:
            pass
        
    # -------------------------------------------------------------------------

    def write_output(self):
        '''
        Constructs the output file subcat_out.dat with year, release, iamge and
        subject category information and ensures that there are no duplicate
        entries.
        '''
        
        # Use temp file to append only unique information
        unique_release = set()
        outfile = open(self.root + 'subcat_out_tmp.dat', 'a')
        for line in open(self.root + 'subcat_out.dat', 'r'):
            if line not in unique_release:
                outfile.write(line)
                unique_release.add(line)
        outfile.close()
        
        # Replace output file with temporary output file
        os.remove(self.root + 'subcat_out.dat')
        os.rename(self.root + 'subcat_out_tmp.dat', self.root + 
            'subcat_out.dat')
        
        
    # -------------------------------------------------------------------------
    #       Main Controller
    # -------------------------------------------------------------------------

    def subcat_lookup(self):
        '''
        The main controller.
        '''

        # Read in data and subject category dictionary
        self.read_data_file()

        # Build subject catagory dictionary
        self.avm_number_dict = self.build_subcat_dict(self.root + 
            'hs2avm_number.dat')
        self.avm_word_dict = self.build_subcat_dict(self.root + 
            'avm_number2avm_word.dat')
        
        # Prep data for other functions
        self.prep_image_info()
        self.prep_hs_subcat()
        
        # For each instance of data, find AVM category and write to output 
        # file.
        for yr, rel, im, obj, dist, new_hs_cat in zip(self.year, \
        self.release, self.image, self.object, self.distance, \
        self.new_hs_subcat):
            self.avm_lookup(dist, new_hs_cat)
            self.update_obj_dict(yr, rel, im, obj, dist)
            self.prep_output(yr, rel, im)
        
        self.write_output()
                
        print '\nOutput file written to', self.root + 'subcat_out.dat\n'
   
# -----------------------------------------------------------------------------
# For command line execution.
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    s = SubcatLookup()
    s.subcat_lookup()
