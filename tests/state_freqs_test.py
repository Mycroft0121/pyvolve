#! /usr/bin/env python

##############################################################################
##  pyvolve: Python platform for simulating evolutionary sequences.
##
##  Written by Stephanie J. Spielman (stephanie.spielman@gmail.com) 
##############################################################################

''' Suite of unit tests for state_freqs module.'''

import unittest
from Bio import Seq
from Bio.Alphabet import generic_dna
from pyvolve import *
ZERO=1e-8
DECIMAL=8




class state_freqs_RandomFrequencies_Tests(unittest.TestCase):
    ''' Set of "unittests" for the EqualFrequencies subclass of StateFrequencies. Note that since random, cannot test exact values.'''
    
    def setUp(self):
        self.dec = 8
    
    ############################# by=codon tests ##################################
    def test_RandomFrequencies_calculate_freqs_bycodon_typecodon_restriction(self):
        correct_len = 61
        self.rFreqs = RandomFrequencies( by = 'codon', restrict = ['AGG', 'CCT', 'GCG', 'TGC'] )
        freqs = self.rFreqs(type = 'codon')
        sum = freqs[10] + freqs[23] + freqs[38] + freqs[54]
        np.testing.assert_almost_equal(sum, 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=codon, type=codon, with restriction.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=codon, type=codon.")
           
    def test_RandomFrequencies_calculate_freqs_bycodon_typecodon(self):
        correct_len = 61
        self.rFreqs = RandomFrequencies( by = 'codon' )
        freqs = self.rFreqs(type = 'codon')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=codon, type=codon.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=codon, type=codon.")
    
    def test_RandomFrequencies_calculate_freqs_bycodon_typeamino(self):
        correct_len = 20
        self.rFreqs = RandomFrequencies( by = 'codon' )
        freqs = self.rFreqs(type = 'amino')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=codon, type=amino.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=codon, type=codon.")

    def test_RandomFrequencies_calculate_freqs_bycodon_typenuc(self):
        correct_len = 4
        self.rFreqs = RandomFrequencies( by = 'codon' )
        freqs = self.rFreqs(type = 'nuc')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=codon, type=nuc.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=codon, type=codon.")
    

    ############################# by=amino tests ##################################
    def test_RandomFrequencies_calculate_freqs_byamino_typecodon(self):
        correct_len = 61
        self.rFreqs = RandomFrequencies( by = 'amino' )
        freqs = self.rFreqs(type = 'codon')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=amino, type=codon.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=amino, type=codon.")
    
    def test_RandomFrequencies_calculate_freqs_byamino_typeamino(self):
        correct_len = 20
        self.rFreqs = RandomFrequencies( by = 'amino' )
        freqs = self.rFreqs(type = 'amino')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=amino, type=amino.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=amino, type=amino.")

    def test_RandomFrequencies_calculate_freqs_byamino_typenuc(self):
        correct_len = 4
        self.rFreqs = RandomFrequencies( by = 'amino' )
        freqs = self.rFreqs(type = 'nuc')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=amino, type=nuc.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=amino, type=nuc.")

 

    ############################# by=nuc tests ##################################
    def test_RandomFrequencies_calculate_freqs_bynuc_typenuc(self):
        correct_len = 4
        self.rFreqs = RandomFrequencies( by = 'nuc'  )
        freqs = self.rFreqs(type = 'nuc')
        np.testing.assert_almost_equal(np.sum(freqs), 1., decimal = self.dec, err_msg = "RandomFrequencies do not sum to 1 for by=nuc, type=nuc.")
        self.assertEqual(len(freqs), correct_len, msg= "RandomFrequencies has incorrect size for by=nuc, type=nuc.")

 
 
 
 
 
 
 
 
 
 

class state_freqs_EqualFrequencies_Tests(unittest.TestCase):
    ''' Set of "unittests" for the EqualFrequencies subclass of StateFrequencies.'''
    
    def setUp(self):
        self.dec = 8 # For accuracy
    
    
    ############################# by=codon tests ##################################  
    def test_EqualFrequencies_calculate_freqs_bycodon_typecodon_restrict(self):
        correct = np.zeros(61)
        correct[10] = 0.25
        correct[23] = 0.25
        correct[38] = 0.25
        correct[54] = 0.25
        self.eqFreqs = EqualFrequencies( by = 'codon', restrict = ['AGG', 'CCT', 'GCG', 'TGC'])
        freqs = self.eqFreqs(type = 'codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=codon, type=codon with restriction.")
    
    def test_EqualFrequencies_calculate_freqs_bycodon_typecodon(self):
        correct = np.array(np.repeat(1./61., 61))
        self.eqFreqs = EqualFrequencies( by = 'codon' )
        freqs = self.eqFreqs(type = 'codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=codon, type=codon.")
    
    def test_EqualFrequencies_calculate_freqs_bycodon_typeamino(self):
        correct = np.array([0.0655737704918, 0.0327868852459, 0.0327868852459, 0.0327868852459, 0.0327868852459, 0.0655737704918, 0.0327868852459, 0.0491803278689, 0.0327868852459, 0.0983606557377, 0.016393442623, 0.0327868852459, 0.0655737704918, 0.0327868852459, 0.0983606557377, 0.0983606557377, 0.0655737704918, 0.0655737704918, 0.016393442623, 0.0327868852459])
        self.eqFreqs = EqualFrequencies( by = 'codon' )
        freqs = self.eqFreqs(type = 'amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=codon, type=amino.")
    
    def test_EqualFrequencies_calculate_freqs_bycodon_typenuc(self):
        correct = np.array([0.24043715846994534, 0.26229508196721313, 0.25136612021857924, 0.2459016393442623])
        self.eqFreqs = EqualFrequencies( by = 'codon' )
        freqs = self.eqFreqs(type = 'nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=codon, type=nuc.")

    ############################# by=amino tests ##################################
    def test_EqualFrequencies_calculate_freqs_byamino_typeamino_restrict(self):
        correct = [1./3., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1./3., 0., 1./3., 0., 0., 0., 0., 0., 0., 0.]
        self.eqFreqs = EqualFrequencies( by = 'amino', restrict = ['A', 'M', 'P'])
        freqs = self.eqFreqs(type = 'amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=amino, type=amino with restriction.")
    
    
    def test_EqualFrequencies_calculate_freqs_byamino_typecodon(self):
        correct = np.array([0.025, 0.025, 0.025, 0.025, 0.0125, 0.0125, 0.0125, 0.0125, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.01666667, 0.01666667, 0.05, 0.01666667, 0.025, 0.025, 0.025, 0.025, 0.0125, 0.0125, 0.0125, 0.0125, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.025, 0.025, 0.025, 0.025, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.025, 0.025, 0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.025, 0.05, 0.025, 0.00833333, 0.025, 0.00833333, 0.025])
        self.eqFreqs = EqualFrequencies( by = 'amino' )
        freqs = self.eqFreqs( type = 'codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=amino, type=codon.")
    
    def test_EqualFrequencies_calculate_freqs_byamino_typeamino(self):
        correct = np.array(np.repeat(1./20., 20))
        self.eqFreqs = EqualFrequencies( by = 'amino'  )
        freqs = self.eqFreqs(type = 'amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=amino, type=amino.")
    
    def test_EqualFrequencies_calculate_freqs_byamino_typenuc(self):
        correct = [ 0.27638889,  0.22083333,  0.24861111,  0.25416667]
        self.eqFreqs = EqualFrequencies( by = 'amino' )
        freqs = self.eqFreqs(type = 'nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=amino, type=nuc.")
    
    
    ############################# by=nuc tests ##################################
    def test_EqualFrequencies_calculate_freqs_bynuc_typenuc(self):
        correct = np.array(np.repeat(0.25, 4))
        self.eqFreqs = EqualFrequencies( by = 'nuc' )
        freqs = self.eqFreqs(type = 'nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "EqualFrequencies not calculated properly for by=nuc, type=nuc.")




class state_freqs_CustomFrequencies_Tests(unittest.TestCase):
    ''' Set of "unittests" for the CustomFrequencies subclass of StateFrequencies.'''
    
    def setUp(self):
        self.dec = 8 # For accuracy

  
    ############################## by = nuc #############################################
    def test_CustomFrequencies_calculate_freqs_bynuc_typenuc_singlenuc(self):
        correct = np.zeros(4)
        correct[1] = 1.0
        self.uFreqs = CustomFrequencies(by='nuc', freq_dict = {'C':1.0})
        freqs = self.uFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly by=nuc, type=nuc with single nucleotide freq specified.")
    
    def test_CustomFrequencies_calculate_freqs_bynuc_typenuc_multiplenuc(self):
        correct = np.zeros(4)
        correct[0] = 0.25
        correct[1] = 0.25
        correct[2] = 0.25
        correct[3] = 0.25
        self.uFreqs = CustomFrequencies(by='nuc', freq_dict = {'A':0.25, 'C':0.25, 'G':0.25, 'T':0.25})
        freqs = self.uFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly by=nuc, type=nuc with multiple nucleotide freqs specified.")
    
    ################################ by = codon ##########################################   
    def test_CustomFrequencies_calculate_freqs_bycodon_typecodon_singlecodon(self):
        correct = np.zeros(61)
        correct[1] = 1.0
        self.uFreqs = CustomFrequencies(by='codon', freq_dict = {'AAC':1.0})
        freqs = self.uFreqs( type='codon' )
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=codon, type=codon, single codon freq specified.")
    
    def test_CustomFrequencies_calculate_freqs_bycodon_typecodon_multiplecodons(self):
        correct = np.zeros(61)
        correct[1] = 0.5
        correct[2] = 0.5
        self.uFreqs = CustomFrequencies(by='codon', freq_dict = {'AAC':0.5, 'AAG':0.5})
        freqs = self.uFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=codon, type=codon, multiple codon freqs specified.")
    
    def test_CustomFrequencies_calculate_freqs_bycodon_typeamino(self):
        correct = np.zeros(20)
        correct[8] = 0.5
        correct[9] = 0.25
        correct[10] = 0.25
        self.uFreqs = CustomFrequencies(by = 'codon', freq_dict = {'AAA':0.5, 'ATG':0.25, 'CTT':0.25})
        freqs = self.uFreqs(type = 'amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=codon, type=amino, multiple codon freqs specified.")
       
       
       
    ################################ by = amino ##########################################
    def test_CustomFrequencies_calculate_freqs_byamino_typeamino_singleaa(self):
        correct = np.zeros(20)
        correct[1] = 1.0
        self.uFreqs = CustomFrequencies(by='amino', freq_dict = {'C':1.0})
        freqs = self.uFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=amino, type=amino with single aa specified.")
    
    def test_CustomFrequencies_calculate_freqs_byamino_typeamino_multipleaa(self):
        correct = np.zeros(20)
        correct[1] = 0.25
        correct[2] = 0.25
        correct[3] = 0.25
        correct[4] = 0.25
        self.uFreqs = CustomFrequencies(by='amino', freq_dict = {'C':0.25, 'D':0.25, 'E':0.25, 'F':0.25})
        freqs = self.uFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=amino, type=amino with multiple aas specified.")
    
    def test_CustomFrequencies_calculate_freqs_byamino_typecodon_multipleaa(self):
        correct = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.08333333, 0.08333333, 0.08333333, 0.08333333, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.125, 0.125, 0.125, 0.125, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.08333333, 0., 0.08333333, 0.]
        self.uFreqs = CustomFrequencies(by='amino', freq_dict = {'L':0.5, 'V':0.5})
        freqs = self.uFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "CustomFrequencies not calculated properly for by=amino, type=amino with multiple aas specified.")
    
    
  
class state_freqs_ReadFrequencies_Tests(unittest.TestCase):
    ''' Set of "unittests" for the ReadFrequencies subclass of StateFrequencies.'''
    
    def setUp(self):
        self.dec = 8 # For accuracy

    ################################# by = nuc ###########################################  
    def test_ReadFrequencies_calculate_freqs_bynuc_typenuc_nocol(self):
        correct = np.array([5./54., 12./54., 18./54., 19./54.])
        self.rFreqs = ReadFrequencies(by='nuc', file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=nuc, type=nuc, no columns.")

    def test_ReadFrequencies_calculate_freqs_bynuc_typenuc_col(self):
        correct = np.array([2./9., 7./9., 0, 0])
        self.rFreqs = ReadFrequencies(by='nuc', columns = [1,2,3], file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=nuc, type=nuc, with columns.")
    

    ################################## by = codon ########################################   
    def test_ReadFrequencies_calculate_freqs_bycodon_typecodon_nocol(self):
        correct = np.array([0, 0, 0, 0, 0, 1./18., 0, 0, 0, 0, 0, 0, 0, 0, 1./6., 0, 0, 0, 0, 0, 1./18., 1./18., 0, 0, 0, 0, 1./9., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1./6., 2./9., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1./6.])
        self.rFreqs = ReadFrequencies(by='codon', file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=codon, no columns.")


    def test_ReadFrequencies_calculate_freqs_bycodon_typecodon_col(self):
        correct = np.array([0, 0, 0, 0, 0, 1./9., 0, 0, 0, 0, 0, 0, 0, 0, 1./3., 0, 0, 0, 0, 0, 1./9., 1./9., 0, 0, 0, 0, 1./9., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2./9.])
        self.rFreqs = ReadFrequencies(by='codon', columns = [1,2,3], file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=codon, with columns.")

    def test_ReadFrequencies_calculate_freqs_bycodon_typeamino_nocol(self):
        correct = np.array([0, 0, 0, 0, 1./6., 0, 0, 0, 0, 0, 1./6., 0, 1./9., 0, 1./9., 0, 1./18., 7./18., 0, 0])
        self.rFreqs = ReadFrequencies(by='codon', file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=amino, no columns.")
  
    def test_ReadFrequencies_calculate_freqs_bycodon_typeamino_col(self):
        correct = np.array([0, 0, 0, 0, 2./9., 0, 0, 0, 0, 0, 1./3., 0, 2./9., 0, 1./9., 0, 1./9., 0, 0, 0])
        self.rFreqs = ReadFrequencies(by='codon', columns = [1,2,3], file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=amino, with columns.")
    
    def test_ReadFrequencies_calculate_freqs_bycodon_typenuc_nocol(self):
        correct = np.array([5./54., 12./54., 18./54., 19./54.])
        self.rFreqs = ReadFrequencies(by='codon', file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=nuc, no columns.")

    def test_ReadFrequencies_calculate_freqs_bycodon_typenuc_col(self):
        correct = np.array([5./27., 8./27., 5./27., 9./27.])
        self.rFreqs = ReadFrequencies(by='codon', columns = [1,2,3], file = 'tests/freqFiles/testFreq_codon_aln.fasta')
        freqs = self.rFreqs(type='nuc')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=codon, type=nuc, with columns.")


    ################################## by = amino ########################################   
    def test_ReadFrequencies_calculate_freqs_byamino_typeamino_nocol(self):
        correct = np.array([1./6., 1./6., 1./6., 1./6., 1./6., 1./6., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.rFreqs = ReadFrequencies(by='amino', file = 'tests/freqFiles/testFreq_amino_aln.fasta')
        freqs = self.rFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=amino, type=amino, no columns.")
    
    def test_ReadFrequencies_calculate_freqs_byamino_typeamino_col(self):
        correct = np.array([2./3., 0, 0, 1./3., 0., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.rFreqs = ReadFrequencies(by='amino', columns = [1,2,3], file = 'tests/freqFiles/testFreq_amino_aln.fasta')
        freqs = self.rFreqs(type='amino')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=amino, type=amino, with columns.")

    def test_ReadFrequencies_calculate_freqs_byamino_typecodon_nocol(self):
        correct = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.08333333, 0.08333333, 0.08333333, 0.08333333, 0.04166667, 0.04166667, 0.04166667, 0.04166667, 0.04166667, 0.04166667, 0.04166667, 0.04166667, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.08333333, 0, 0.08333333, 0, 0.08333333, 0, 0.08333333])
        self.rFreqs = ReadFrequencies(by='amino', file = 'tests/freqFiles/testFreq_amino_aln.fasta')
        freqs = self.rFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=amino, type=codon, no columns.")

    def test_ReadFrequencies_calculate_freqs_byamino_typecodon_col(self):
        correct = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1./6., 0,  1./6., 0,  1./6.,  1./6.,  1./6., 1./6., 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.rFreqs = ReadFrequencies(by='amino', columns = [1,2,3], file = 'tests/freqFiles/testFreq_amino_aln.fasta')
        freqs = self.rFreqs(type='codon')
        np.testing.assert_array_almost_equal(correct, freqs, decimal = self.dec, err_msg = "ReadFrequencies not calculated properly for by=amino, type=codon, with columns.")

    
def run_state_freqs_test():

    run_tests = unittest.TextTestRunner()
    
    print "Testing the RandomFrequencies subclass of StateFrequencies"
    test_suite_Rand = unittest.TestLoader().loadTestsFromTestCase(state_freqs_RandomFrequencies_Tests)
    run_tests.run(test_suite_Rand)

    print "Testing the EqualFrequencies subclass of StateFrequencies"
    test_suite_Equal = unittest.TestLoader().loadTestsFromTestCase(state_freqs_EqualFrequencies_Tests)
    run_tests.run(test_suite_Equal)

    print "Testing the CustomFrequencies subclass of StateFrequencies"
    test_suite_User = unittest.TestLoader().loadTestsFromTestCase(state_freqs_CustomFrequencies_Tests)
    run_tests.run(test_suite_User)

    print "Testing the ReadFrequencies subclass of StateFrequencies"
    test_suite_Read = unittest.TestLoader().loadTestsFromTestCase(state_freqs_ReadFrequencies_Tests)
    run_tests.run(test_suite_Read)

    
    
    
    
    
    
    
    