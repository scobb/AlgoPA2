'''
Created on Sep 27, 2014

@author: scobb
'''
import os, sys
import subprocess

def rename(dir, files, results_dir, tag):
    out_tag = 'test_out'
    for file in files:
        if 'out' in file:
            new_filename = tag + file.replace('file','').replace('out', out_tag)
        else:
            new_filename = tag + file.replace('file', '')
        subprocess.call(['cp', os.path.join(dir, file),
                        os.path.join(results_dir, new_filename)])


def check(dir, correct_dir):
    outputs = []
    correct_outputs = []
    for f in os.listdir(dir):
        if 'out' in f:
            outputs.append(os.path.join(dir, f))
    for f in os.listdir(correct_dir):
        if 'out' in f:
            correct_outputs.append(os.path.join(correct_dir, f))
    outputs.sort()
    correct_outputs.sort()
    for i in range(len(outputs)):
        process = subprocess.Popen(['diff', outputs[i], correct_outputs[i]], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if out:
            print ('Failed diff:\nours: %s\ntheirs: %s\ndiff: \n' %(outputs[i],
                                                                      correct_outputs[i]) + out.decode('utf-8'))
                                                                      
            #return
    print( "Check returned successful.")

if __name__ == '__main__':
    script_dir = os.getcwd()
    test_dir = os.path.join(script_dir, 'test')
    sample_test_dir = os.path.join(script_dir, 'sample_tests')
    
    for in_file in os.listdir(sample_test_dir):
        if 'in' in in_file:
            out_file = open(os.path.join(test_dir, in_file.replace('in','out')), 'a+')
            out_file.flush()
            print ('out_file %s' % str(out_file))
            process = subprocess.Popen(['./RUN.py', os.path.join(test_dir, in_file)], stdout=subprocess.STDOUT)
            out_file.close()
            
    #check(test_dir, sample_test_dir)
            
    
    
        
    
    
