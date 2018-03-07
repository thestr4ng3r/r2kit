'''
Author: Matt Brooks, @cmatthewbrooks

DESCRIPTION:

The sessionstarter.py script is helpful when starting a new
r2 session against a suspected malware target. It will handle
auto-analysis as well as naming specific types of functions.

ARGS:

Use the optional -i flag to point to a directory of sig hash files
generated by sigs.py

NOTES:

- When using zsigs from a signature file, only the "bytes" sigs
  are considered. The "refs" and "graphs" sigs are too loose for
  my taste and in the instances where they match correctly, a
  "bytes" signature exists for the same function. If you determine
  a case where the "refs" or "graphs" signatures were useful without
  an existing "bytes" signature, please file a Github issue.

TODO:


'''

import os,sys
import argparse
import json

import r2pipe 
import r2utils as R2utils

class SessionStarter:

    def __init__(self, input_obj = None):
        
        self.r2utils = R2utils.r2utils()
        self.r2 = self.r2utils.get_analyzed_r2pipe_from_input(input_obj)
        
        self.sigs_location = None
        self.sigs_location_type = None

    def set_sigs_location(self, infile):

        if os.path.isdir(infile):

            self.sigs_location = infile
            self.sigs_location_type = 'directory'

        elif os.path.isfile(infile):
            
            self.sigs_location = infile
            self.sigs_location_type = 'file'

    def rename_library_code(self):
        
        if not self.sigs_location:
            return None

    def rename_common_funcs(self):

        funcj_list = self.r2utils.get_funcj_list(self.r2)

        for funcj in funcj_list:

            if (self.r2utils.check_is_import_jmp_func(funcj) 
                and funcj['name'].startswith('fcn.')):

                self.r2.cmd('s ' + str(funcj['addr']))
                self.r2.cmd('afn jmp_' + 
                    self.r2utils.get_import_from_import_jmp_func(funcj)
                )

            elif (self.r2utils.check_is_wrapper_func(funcj) 
                and funcj['name'].startswith('fcn.')):

                self.r2.cmd('s ' + str(funcj['addr']))
                self.r2.cmd('afn wrapper_' + 
                    self.r2utils.get_call_from_wrapper(funcj).replace(' ','_')
                )

            elif (self.r2utils.check_is_global_assignment_func(funcj) 
                and funcj['name'].startswith('fcn.')):

                self.r2.cmd('s ' + str(funcj['addr']))
                self.r2.cmd(
                    'afn globalassign_' + funcj['name'].replace('.','')
                )

if __name__ == '__main__':

    ss = SessionStarter()
    ss.rename_library_code()
    ss.rename_common_funcs()
