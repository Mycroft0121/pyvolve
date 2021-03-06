#! /usr/bin/env python

##############################################################################
##  pyvolve: Python platform for simulating evolutionary sequences.
##
##  Written by Stephanie J. Spielman (stephanie.spielman@gmail.com) 
##############################################################################




'''
    This module will generate the Markov chain's instantaneous rate matrix, Q.
'''



import numpy as np
from copy import deepcopy
from genetics import *
from state_freqs import *
ZERO      = 1e-8
MOLECULES = Genetics()


class MatrixBuilder(object):
    '''
        Parent class for model instantaneous matrix creation.
        
        Child class include the following:
            1. *aminoAcid_Matrix* 
                - Empirical amino acid models (currently, JTT, WAG, and LG and SCG05).
            2. *nucleotide_Matrix* 
                - Nucleotide models (GTR and nested)
            3. *mechCodon_Matrix*
                - So-called mechanistic codon models, which include GY-style and MG-style models (dN/dS models)
            4. *ECM_Matrix*
                - ECM (Kosiol2007) empirical codon model
            5. *mutSel_Matrix* 
                - Mutation-selection model (Halpern and Bruno 1998), extended for either codon or nucleotides
        
    '''
    
    def __init__(self, param_dict, scale_matrix = 'yang'):
        '''
            Construction requires a single positional argument, **param_dict**. This argument should be a dictionary containing parameters about the substitution process in order to construct the matrix.
            
            Optional keyword arguments:
                1. **scale_matrix** = <'yang', 'neutral', 'False/None'>. This argument determines how rate matrices should be scaled. By default, all matrices are scaled according to Ziheng Yang's approach, in which the mean substitution rate is equal to 1. However, for codon models (GY94, MG94), this scaling approach effectively causes sites under purifying selection to evolve at the same rate as sites under positive selection, which may not be desired. Thus, the 'neutral' scaling option will allow for codon matrices to be scaled such that the mean rate of *neutral* subsitution is 1. You may also opt out of scaling by providing either False or None to this argument, although this is not recommended. 
        '''
        
        self.params = param_dict
        self.scale_matrix = scale_matrix
        if type(self.scale_matrix) is str:
            self.scale_matrix = self.scale_matrix.lower()
        assert( self.scale_matrix == 'yang' or self.scale_matrix == 'neutral' or self.scale_matrix is False or self.scale_matrix is None ), "You have specified an incorrect matrix scaling scheme. Either 'Yang', 'neutral', or False/None are accepted (case-insensitive)."

        
         


    def _sanity_params(self):
        '''
            Sanity-check that all necessary parameters have been supplied to construct the matrix.
        '''
        print "Parent class method, not called."
        

    def _sanity_params_state_freqs(self):
        '''
            Sanity-check specifically state_freqs key/value in the params dictionary.
            If state_freqs not provided, then set to equal.
        '''
        
        if 'state_freqs' not in self.params:
            self.params['state_freqs'] = np.repeat(1./self._size, self._size)
        if len(self.params['state_freqs']) != self._size:
            raise AssertionError("state_freqs key in your params dict does not contain the correct number of values for your specified model.")



    def _sanity_params_mutation_rates(self, symmetric = True):
        '''
            Sanity-check specifically mu key/value in params dictionary.
            NOTE: mutation-selection models may take asymmetric mutation rates. However, this function assumes that rates are symmetric.
            Thus, if A->C is present but C->A is not, the latter will take on the A->C value.
            Any missing mutation rates are given a value of 1.
        '''
        
        if 'mu' in self.params:
            # Single float provided
            if type(self.params['mu']) is float:
                new_mu = {'AC':1.,  'CA':1.,  'AG':1.,  'GA':1.,  'AT':1.,  'TA':1.,  'CG':1.,  'GC':1.,  'CT':1.,  'TC':1.,  'GT':1.,  'TG':1.}
                for key in new_mu:
                    new_mu[key] *= self.params['mu']
                self.params['mu'] = new_mu
        
            # Dictionary of mu's provided. Make sure dictionary is full.
            elif type(self.params['mu']) is dict:
                for key in ['AC', 'AG', 'AT', 'CG', 'CT', 'GT']:
                    rev_key = str(key[1] + key[0])
                    
                    # Neither key pair. Add both
                    if key not in self.params['mu'] and rev_key not in self.params['mu']:
                        self.params['mu'][key] = 1.
                        self.params['mu'][rev_key] = 1.
                    
                    # If one key but not the other, fill in missing one symmetrically.
                    elif key not in self.params['mu'] and rev_key in self.params['mu']:
                        self.params['mu'][key] = self.params['mu'][rev_key]
                    
                    elif key in self.params['mu'] and rev_key not in self.params['mu']:
                        self.params['mu'][rev_key] = self.params['mu'][key]
            else:
                raise AssertionError("You must provide EITHER a single mutation or a dictionary of mutation rates for nucleotide pairs to the key 'mu' in the 'params' dictionary.")
        
        # Nothing specified, so simply use equal mutation rates to construct matrix
        else:
            self.params['mu'] = {'AC':1.,  'CA':1.,  'AG':1.,  'GA':1.,  'AT':1.,  'TA':1.,  'CG':1.,  'GC':1.,  'CT':1.,  'TC':1.,  'GT':1.,  'TG':1.}

        # Apply kappa as needed.        
        if 'kappa' in self.params:
            temp_mu = deepcopy( self.params['mu'] )
            self.params['mu'] = {'AC': temp_mu['AC'], 'AG': temp_mu['AG'] * float(self.params['kappa']), 'AT': temp_mu['AT'], 'CG': temp_mu['CG'], 'CT': temp_mu['CT']*float(self.params['kappa']), 'GT': temp_mu['GT'], 'CA': temp_mu['CA'], 'GA': temp_mu['GA'] * float(self.params['kappa']), 'TA': temp_mu['TA'], 'GC': temp_mu['GC'], 'TC': temp_mu['TC']*float(self.params['kappa']), 'TG': temp_mu['TG']}




    def _build_matrix( self, params ):
        ''' 
            Generate an instantaneous rate matrix.
        '''    
        matrix = np.zeros( [self._size, self._size] ) # For nucleotides, self._size = 4; amino acids, self._size = 20; codons, self._size = 61.
        for s in range(self._size):
            for t in range(self._size):
                # Non-diagonal
                rate = self._calc_instantaneous_prob( s, t, params )                
                matrix[s][t] = rate
                
            # Fill in the diagonal position so the row sums to 0, but ensure it doesn't became -0
            matrix[s][s]= -1. * np.sum( matrix[s] )
            if matrix[s][s] == -0.:
                matrix[s][s] = 0.
            #assert ( abs(np.sum(matrix[s])) < ZERO ), "Row in instantaneous matrix does not sum to 0."
        return matrix


    
    def _compute_yang_scaling_factor(self, matrix, params):
        '''
            Compute scaling factor. Note that we have arguments here since this function is used *both* with attributes and for temporary neutral matrix/params.
        '''
        scaling_factor = 0.
        for i in range(self._size):
            scaling_factor += ( matrix[i][i] * params['state_freqs'][i] )
        return scaling_factor
        
    
    def _compute_neutral_scaling_factor(self):
        '''
            Compute scaling factor you'd get if w=1, so mean neutral substitution rate is 1.
            Avoids confounding time issue with selection strength.
        '''
        neutral_params = self._create_neutral_params()
        neutral_matrix = self._build_matrix( neutral_params )
        scaling_factor = self._compute_yang_scaling_factor(neutral_matrix, neutral_params)
        return scaling_factor
        
 
    def __call__(self):
        ''' 
            Generate, scale, return instantaneous rate matrix.
        '''    
        
        # Construct matrix
        self.inst_matrix = self._build_matrix( self.params )
        
        # Scale matrix as needed.
        if self.scale_matrix:
            if self.scale_matrix == 'yang':
                scaling_factor = self._compute_yang_scaling_factor(self.inst_matrix, self.params)                
            elif self.scale_matrix == 'neutral':
                scaling_factor = self._compute_neutral_scaling_factor()
            else:
                raise AssertionError("You should never be getting here!! Please email stephanie.spielman@gmail.com and report error 'scaling arrival.'")
            self.inst_matrix /= -1.*scaling_factor
        return self.inst_matrix




    def _is_TI(self, source, target):
        ''' 
            Determine if a given nucleotide change is a transition or a tranversion.  Used in child classes nucleotide_Matrix, mechCodon_Matrix, ECM_Matrix, mutSel_Matrix .
            Returns True for transition, False for transversion.
            
            Arguments "source" and "target" are the actual nucleotides (not indices).
        '''
        
        ti_pyrim = source in MOLECULES.pyrims and target in MOLECULES.pyrims
        ti_purine = source in MOLECULES.purines and target in MOLECULES.purines    
        if ti_pyrim or ti_purine:
            return True
        else:
            return False
            
            
            
    def _is_syn(self, source, target):
        '''
            Determine if a given codon change is synonymous or nonsynonymous. Used in child classes mechCodon_Matrix, ECM_Matrix .
            Returns True for synonymous, False for nonsynonymous.
             
            Arguments arguments "source" and "target" are codon indices (0-60, alphabetical).
        '''
        
        source_codon = MOLECULES.codons[source]
        target_codon = MOLECULES.codons[target]
        if ( MOLECULES.codon_dict[source_codon] == MOLECULES.codon_dict[target_codon] ):
            return True
        else:
            return False           
    
    
    
    def _get_nucleotide_diff(self, source, target):
        ''' 
            Get the nucleotide difference(s) between two codons. Used in child classes ECM_Matrix, mechCodon_Matrix, mutSel_Matrix .
            Returns a string representing the nucleotide differences between source and target codon.
            For instance, if source is AAA and target is ATA, the string AT would be returned. If source is AAA and target is ACC, then ACAC would be returned.
            
            Input arguments source and target are codon indices (0-60, alphabetical).
        '''        
        
        source_codon = MOLECULES.codons[source]
        target_codon = MOLECULES.codons[target]
        return "".join( [source_codon[i]+target_codon[i] for i in range(len(source_codon)) if source_codon[i] != target_codon[i]] )
        
        
    
    def _calc_instantaneous_prob(self, source, target, params):
        ''' 
            Calculate a given element in the instantaneous rate matrix.
            Returns the substitution probability from source to target, for a given model.
            Arguments "source" and "target" are *indices* for the relevant aminos (0-19) /nucs (0-3) /codons (0-60). 
            PARENT CLASS FUNCTION. NOT IMPLEMENTED.

        '''
        return 0










class aminoAcid_Matrix(MatrixBuilder):
    ''' 
        Child class of MatrixBuilder. This class implements functions relevant to constructing amino acid model instantaneous matrices.
        Note that all empirical amino acid replacement matrices are in the file empirical_matrices.py.
    '''        
    
    def __init__(self, *args, **kwargs):
        super(aminoAcid_Matrix, self).__init__(*args, **kwargs)
        self._size = 20
        self._code = MOLECULES.amino_acids
        self._sanity_params()
        self._init_empirical_matrix()

       
    
    def _sanity_params(self):
        '''
            Sanity-check that all necessary parameters have been supplied to construct the matrix.
            Required aminoAcid_Matrix params keys:
                1. state_freqs
                2. aa_model (but this is checked earlier here)
        '''
        self._sanity_params_state_freqs()
        assert( 'aa_model' in self.params ), "You must specify an amino acid model (key 'aa_model') in the params dictionary."  
        
       
        
    def _init_empirical_matrix(self):
        '''
            Function to load the appropriate replacement matrix from empirical_matrices.py 
        '''
        import empirical_matrices as em
        aa_model = self.params['aa_model'].lower() # I have everything coded in lower case
        try:
            self.emp_matrix = eval("em."+aa_model+"_matrix")
        except:
            raise AssertionError("\n\nCouldn't figure out your empirical matrix specification. Note that we currently only support the JTT, WAG, or LG empirical amino acid models.")
            
            
            
            
    def _calc_instantaneous_prob( self, source, target, params ):
        ''' 
            Returns the substitution probability (s_ij * p_j, where s_ij is replacement matrix entry and p_j is target amino frequency) from source to target for amino acid empirical models.
            Arguments "source" and "target" are indices for the relevant aminos (0-19).
            
            * Third argument not used here! *
        '''
        return self.emp_matrix[source][target] * self.params['state_freqs'][target]        


    def _compute_neutral_scaling_factor(self):
        ''' No selection component to aminoAcid empirical matrices. '''
        return -1.




class nucleotide_Matrix(MatrixBuilder):
    ''' 
        Child class of MatrixBuilder. This class implements functions relevant to constructing nucleotide model instantaneous matrices.
        All models computed here are essentially nested versions of GTR.
    '''        
    
    def __init__(self, *args, **kwargs):
        super(nucleotide_Matrix, self).__init__(*args, **kwargs)
        self._size = 4
        self._code = MOLECULES.nucleotides
        self._sanity_params()



    def _sanity_params(self):
        '''
            Sanity-check that all necessary parameters have been supplied to construct the matrix.
            Required nucleotide_Matrix params keys:
                1. state_freqs
                2. mu
        '''
        self._sanity_params_state_freqs()
        self._sanity_params_mutation_rates()
      


    def _calc_instantaneous_prob(self, source, target, params):
        ''' 
            Returns the substitution probability (\mu_ij * p_j, where \mu_ij are nucleotide mutation rates and p_j is target nucleotide frequency) from source to target for nucleotide models.
            Arguments "source" and "target" are indices for the relevant nucleotide (0-3).
            
            * Third argument not used here! *
        '''
        source_nuc = self._code[source]
        target_nuc = self._code[target]
        if source_nuc == target_nuc:
            return 0.
        else:
            return self.params['state_freqs'][target] * self.params['mu']["".join(sorted(source_nuc + target_nuc))]


    def _compute_neutral_scaling_factor(self):
        ''' No selection component to nucleotide matrices. '''
        return -1.






class mechCodon_Matrix(MatrixBuilder):    
    ''' 
        Child class of MatrixBuilder. This class implements functions relevant to "mechanistic" (dN/dS) codon models.
        Models include both GY-style or MG-style varieties, although users should *always specify codon frequencies* to class instance!
        Both dS and dN variation are allowed, as are GTR mutational parameters (not strictly HKY85).
    
    '''        


 
    def __init__(self, params, type = "GY94", scale_matrix = "yang"):
        self.model_type = type
        assert(self.model_type == 'GY94' or self.model_type == 'MG94'), "\n\nFor mechanistic codon models, you must specify a model_type as GY94 (uses target *codon* frequencies) or MG94 (uses target *nucleotide* frequencies.) I RECOMMEND MG94!!"
        super(mechCodon_Matrix, self).__init__(params, scale_matrix)
        self._size = 61
        self._code = MOLECULES.codons    
        self._sanity_params()
        if self.model_type == "MG94":
            self._nuc_freqs = CustomFrequencies(by = 'codon', freq_dict = dict(zip(self._code, self.params['state_freqs'])))(type = 'nuc')


    
    def _sanity_params(self):
        '''
            Sanity-check that all necessary parameters have been supplied to construct the matrix.
            Required codon_Matrix params keys:
                1. state_freqs
                2. mu
                3. beta, alpha
            Additionally, grabs nucleotide frequencies if needed for MG94 simulation.
        '''
        self._sanity_params_state_freqs()
        self._sanity_params_mutation_rates()
        if 'omega' in self.params:
            self.params['beta'] = self.params['omega']
        if 'beta' not in self.params:
            raise AssertionError("You must provide a dN value (using either the key 'beta' or 'omega') in params dictionary to run this model!")
        if 'alpha' not in self.params:
            self.params['alpha'] = 1.
        



    def _calc_prob(self, target_codon, target_nuc, nuc_pair, factor):
        ''' 
            Calculate instantaneous probability of (non)synonymous change for mechanistic codon models.
            Argument *factor* is either dN or dS.
            
            NOTE: can leave self.params here as state_freqs still won't change for neutral scaling factor.
        '''
        prob =  self.params['mu'][nuc_pair] * factor 
        if self.model_type == 'GY94':
            prob *= self.params['state_freqs'][target_codon]
        else:
            prob *= self._nuc_freqs[ MOLECULES.nucleotides.index(target_nuc) ]        
        return prob
    


    def _calc_instantaneous_prob(self, source, target, params):
        ''' 
            Returns the substitution probability from source to target for mechanistic codon models.
            Arguments "source" and "target" are indices for the relevant codons (0-60).
        
            Third argument can be specified as non-self when we are computing neutral scaling factor.
        ''' 
        nuc_diff = self._get_nucleotide_diff(source, target)
        if len(nuc_diff) != 2:
            return 0.
        else:
            nuc_pair = "".join(sorted(nuc_diff[0] + nuc_diff[1]))
            if self._is_syn(source, target):
                return self._calc_prob(target, nuc_diff[1], nuc_pair, params['alpha'])
            else:
                return self._calc_prob(target, nuc_diff[1], nuc_pair, params['beta'])




    def _create_neutral_params(self):
        '''
            Return self.params except with alpha, beta equal to 1.
        '''
        return {'state_freqs': self.params['state_freqs'], 'mu': self.params['mu'], 'beta':1., 'alpha':1.}








class mutSel_Matrix(MatrixBuilder):    
    ''' 
        Child class of MatrixBuilder. This class implements functions relevant to constructing mutation-selection balance model instantaneous matrices, according to the HalpernBruno 1998 model.
        Here, this model is extended such that it can be used for either nucleotide or codon. This class will automatically detect which one you want based on your state frequencies.

    '''
    
    def __init__(self, *args, **kwargs):
        super(mutSel_Matrix, self).__init__(*args, **kwargs)
        self._sanity_params()      


    def _sanity_params(self):
        '''
            Sanity-check that all necessary parameters have been supplied to construct the matrix.
            Required codon_Matrix params keys:
                1. state_freqs
                2. mu
        '''
        if self.params['state_freqs'].shape == (61,):
            self._model_class = 'codon'
            self._size = 61
            self._code = MOLECULES.codons
        elif self.params['state_freqs'].shape == (4,):
            self._model_class = 'nuc'
            self._size = 4
            self._code = MOLECULES.nucleotides
        else:
            raise AssertionError("\n\nMutSel models need either codon or nucleotide frequencies.")
        self._sanity_params_state_freqs()
        self._sanity_params_mutation_rates()
        
        
                   

    def _calc_instantaneous_prob(self, source, target, params):
        ''' 
            Calculate the substitution probability from source to target for mutation-selection-balance models.
            Arguments "source" and "target" are indices for the relevant codons (0-60) or nucleotide (0-3).
        
            Third argument can be specified as non-self when we are computing neutral scaling factor.

        '''        
        
        nuc_diff = self._get_nucleotide_diff(source, target)
        if len(nuc_diff) != 2:
            return 0.
        else:
            pi_i  = params['state_freqs'][source]           # source frequency
            pi_j  = params['state_freqs'][target]           # target frequency 
            mu_ij = params["mu"][nuc_diff]                  # source -> target mutation rate
            mu_ji = params["mu"][nuc_diff[1] + nuc_diff[0]] # target -> source mutation rate

            if pi_i <= ZERO or pi_j <= ZERO: 
                inst_prob = 0.
            elif abs(pi_i - pi_j) <= ZERO:
                inst_prob = mu_ij
            else:
                pi_mu = (pi_j*mu_ji)/(pi_i*mu_ij)
                inst_prob =  np.log(pi_mu)/(1. - 1./pi_mu) * mu_ij
            return inst_prob
            
            
    def _create_neutral_params(self):
        '''
            Return self.params except without selection (equal state_freqs!).
        '''
        return {'state_freqs': np.repeat(1./self._size, self._size), 'mu': self.params['mu']}
           
            
            
  
  
  








class ECM_Matrix(MatrixBuilder):
    ''' 
        Child class of MatrixBuilder. This class implements functions relevant to constructing a matrix specifically for the ECM (described in Kosiol2007) model.
        We support both restricted (instantaneous single changes only) and unrestricted (instantaneous single, double, or triple) versions of this model (see paper for details).
        
        !!! NOTE: The ECM model supports omega (dN/dS) and kappa (TI/TV) ratios in their calculations, and therefore I have included these parameters here. HOWEVER, I do NOT recommend their use.
    
    ''' 
    
    def __init__(self, params, type = 'restricted', scale_matrix = 'yang'):
        if type.lower() == 'restricted' or type.lower() == 'rest':
            self.restricted = True
        elif type.lower() == 'unrestricted' or type.lower() == 'unrest':
            self.restricted = False
        else:
            raise AssertionError("For an ECM model, you must specify whether you want restricted (single nuc instantaneous changes only) or unrestricted (1-3 instantaneous nuc changes) Second argument to Model initialization should be 'rest', 'restricted', 'unrest', 'unrestricted' (case insensitive).")
        
        super(ECM_Matrix, self).__init__(params, scale_matrix)
        self._size = 61
        self._code = MOLECULES.codons
        self._sanity_params()
        self._init_empirical_matrix()
    
      
      
    def _sanity_params(self):
        '''
            Sanity checks for parameters dictionary.
        '''
        self._sanity_params_state_freqs()
            
        if 'omega' in self.params:
            self.params['beta'] = self.params['omega']
        if 'beta' not in self.params:
            self.params['beta'] = 1.
        if 'alpha' not in self.params:
            self.params['alpha'] = 1.
        if 'k_ti' not in self.params:
            self.params['k_ti'] = 1.
        if 'k_tv' not in self.params:
            self.params['k_tv'] = 1.
    
    
    
    def _init_empirical_matrix(self):
        '''
            Function to load the appropriate replacement matrix from empirical_matrices.py 
        '''
        import empirical_matrices as em
        if self.restricted:
            self.emp_matrix = em.ecmrest_matrix
        else:
            self.emp_matrix = em.ecmunrest_matrix
        


    def _set_kappa_param(self, nuc_diff):
        ''' 
            Calculations for the "kappa" parameter(s) for the ECM model. See the 2007 paper for details.
        '''
        num_ti = 0
        num_tv = 0
        for i in range(0, len(nuc_diff), 2):
            source_nuc = nuc_diff[i]
            target_nuc = nuc_diff[i+1]
            if self._is_TI(source_nuc, target_nuc):
                num_ti += 1
            else:
                num_tv += 1
        return self.params['k_ti']**num_ti * self.params['k_tv']**num_tv




    def _calc_instantaneous_prob(self, source, target, params):
        ''' 
            Returns the substitution probability from source to target for ECM models.
            Arguments "source" and "target" are indices for the relevant codons (0-60).
            
            Third argument can be specified as non-self when we are computing neutral scaling factor.
        '''  
        
        nuc_diff = self._get_nucleotide_diff(source, target)
        if len(nuc_diff) == 0  or (self.restricted and len(nuc_diff) != 2):
            return 0.
        else:
            kappa_param = self._set_kappa_param(nuc_diff)
            if self._is_syn(source, target):
                return self.emp_matrix[source][target] * params['state_freqs'][target] * params['alpha'] * kappa_param
            else:
                return self.emp_matrix[source][target] * params['state_freqs'][target] * params['beta'] * kappa_param



    def _create_neutral_params(self):
        '''
            Return self.params except with alpha, beta equal to 1.
        '''
        return {'state_freqs': self.params['state_freqs'], 'k_ti': self.params['k_ti'], 'k_tv': self.params['k_tv'], 'alpha':1., 'beta':1.}

          
            
