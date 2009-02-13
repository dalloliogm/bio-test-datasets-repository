#!/usr/bin/env python
# Copyright 2009 Giovanni Marco Dall'Olio - dalloliogm@gmail.com
#
# This is a template for (bio)python unittests.
# 
# There are many comments which explain how a basic unit test should be written, 
# and how it works.
# 
#
# Usage:
#
# You can run the tests in this file by executing it directly with the python interpreted:
#
# $: python biotest_template.py
# ....
#
# However, it is recommended to use nose [1] to run it.
# Download and install nose on your computer, and then run:
# $: nosetests biotest_template.py
# ...
# to execute all the tests automatically.
# It is recommended to read nose's documentation to understand everything about its' plugins 
# and usage.
# 
# [1] http://code.google.com/p/python-nose/
#

"""
Short Description of the test package

Long description of the test package (facultative)
"""
import logging
import unittest
import pdb
    

# basic tutorial
#   Every class represents a test case.
#   For example, let's say we want to prove that the function SeqIO can read correctly fasta and genbank files.
#   We will write at least two test case, each one testing a specific format example.
#
# glossary:
# - fixtures: instructions that are needed to prepare the environment where tests will be execute; for example, 
#             importing specific libraries, opening files, etc..
#             See http://docs.python.org/library/unittest.html .

class SimpleFastaCase(unittest.TestCase):
    """Short description of the test case (e.g. "Test SeqIO behaviour on a simple dna sequence")

    Long description of the test case (facultative).
    """
    # - CONFIGURATION SECTION -
    #   put here any variable that are specific to this test case.
    # For example, the sequences to test, the name of the files to open, etc..

    sequence = '''\
>simplefastaseq
acgcgatgtttagctgactgagcggcgcccgtaagcannctacatctgactgacgtacgtaggtac
ctaggtctagggaggtcagcnntactatctttcacggctactatcgaggagaaactcgtaggagga
'''
    format = 'fasta'

    known_values = {'id': 'simplefastaseq', 
                        'description': 'simplefastaseq',
                        'sequence': 'acgcgatgtttagctgactgagcggcgcccgtaagcannctacatctgactgacgtacgtaggtacctaggtctagggaggtcagcnntactatctttcacggctactatcgaggagaaactcgtaggagga'}

    _test_is_set = False

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *BEFORE* executing *ALL* tests
        #   described below.
        #
        # Usually people use this function to open input files, create sqlite databases, configure 
        # the logging module, etc..
        # 
        # note: don't be scared by the @classmethod thing. But notice that we are using 'cls'
        # instead of 'self'
        
        logging.basicConfig(level = logging.DEBUG)
        from StringIO import StringIO
        from Bio import SeqIO

        cls.seqfilehandler = StringIO(cls.sequence)
        cls.sequences = SeqIO.parse(cls.seqfilehandler, cls.format)
        cls.seqrecord = cls.sequences.next()

        cls._test_is_set = True

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *AFTER* executing all tests.
        # if you don't need this method, you can remove it.
        pass
    
    def setUp(self):
        # - PER-TEST FIXTURES -
        #   put here any instruction you want to be run *BEFORE* *EVERY* test is executed.

        # the following is an hack to have global fixtures in case you don't want to use nose:
        if self._test_is_set is False:
            self.setUpClass()

    def tearDown(self):
        # - PER-TEST FIXTURES -
        #   put here any instructions you want to be run *AFTER* *EVERY* test is executed.

        # you may want to put a debugger breakpoint here before the other instructions.
#        pdb.set_trace()
        pass

    # Tests definitions:
    #   any method of this class having the word 'test_' in its name will be considered a test.
    def test_knownValues(self):
        """Compare the results from SeqIO.parse against some known values"""
        # all the outputs from print statements will be shown only if the test fails
        print self.seqrecord
        print self.seqrecord.seq.tostring(), self.known_values['sequence']
        self.assertEqual(self.seqrecord.seq.tostring(), self.known_values['sequence'])
        self.assertEqual(self.seqrecord.id, self.known_values['id'])

    def test_stopIteration(self):
        """Check that SeqIO returns an IterationError if there are no sequences left in the file."""
        
        self.assertRaises(StopIteration, self.sequences.next)


# as we were saying TabFormatSequence derives from SimpleSeqCase so it inherits all its methods and tests.
class TabFormatSequence(SimpleFastaCase):
    """Test SeqIO's behaviour on a tab-format sequence"""
    sequence = """
seq1    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
"""
    format = 'tab'
    known_values = {'id': 'seq1',
                        'description': 'seq1',
                        'sequence': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}
    _test_is_set = False

    # you don't need to re-define setUp and setUpClass methods here, because they are inherited from SimpleSeqCase
    # all the tests methods are also inherited, but maybe you want to define some more
    def test_SomethingSpecialThatShouldHappenWithBlankSequences(self):
        pass


# if you don't want to use nose, this is an hack to do it without having to change the current template
if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(SimpleFastaCase, TabFormatSequence)
