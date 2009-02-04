#!/usr/bin/env python
# python script by ...
"""
Short Description of the test package

Long description of the test package (facultative)

Example:
SeqIO test cases

This module contains many test cases to check SeqIO's behaviour.
"""
import logging
import unittest


# In principle, every test case should be described by a different unittest.TestCase subclass.
# You can write a basic test case with all the test methods that you want to run on it, 
# and then define the other test cases by subclassing it.

# For example, in this file we are testing SeqIO's behaviour on two kinds of fasta files: a
# simple sequence, and a blank sequence.
# We have defined the test case for the simple sequence first, and then we have used inheritance
# (note that the BlankSeqCase class, below, derives from SimpleSeqCase) to define the second.



class SimpleSeqCase(unittest.TestCase):
	"""Short description of the test case (e.g. "Test SeqIO behaviour on a simple dna sequence")

	Long description of the test case (facultative).
	"""
	# put here any variable that you want to share within all the tests, but changes between test cases
	# For example, notice that we re-define these values in BlankSeqCase.
	seqcontent = '>seq1\nactgactgacgtacgtaggtac\n'
	known_values = {'id': 'seq1', 
						'description': 'seq1',
						'sequence': 'actgactgacgtacgtaggtac'}
	
	@classmethod
	def setUpClass(cls):
		# put here any instructions you want to execute only *once* before executing *all* tests 
		# described in this test case.
		# Usually here people open input files, create databases, etc..
		# note: this method will only work if you use nose (>0.10) to execute your tests. 
		# Otherwise, you will have to do some tricks or move these instructions under the setUp
		# function below.
		# note2: don't be scared by the @classmethod thing. But notice that we are using 'class'
		# instead of 'self'

		from StringIO import StringIO
		from Bio import SeqIO

		cls.seqfilehandler = StringIO(cls.seqcontent)
		cls.sequences = SeqIO.parse(cls.seqfilehandler, 'fasta')
		cls.seqrecord = cls.sequences.next()

	@classmethod
	def tearDownClass(cls):
		# put here any method you want to execute only *once* after *all* tests are executed.
		# if you don't need this method, you can remove it.
		pass
	
	def setUp(self):
		# put here any instructions you want to be run before *every* test is executed.
		#TODO: come with something to put here...
		pass

	def tearDown(self):
		# put here any instructions you want to be run after *every* test is executed.
		pass


	# Any method of this class with its name starting with 'test_' will be considered a test.
	def test_knownValues(self):
		"""
		Compare the results from SeqIO.parse against some known values
		"""
		# all the outputs from print statements will be shown only if the test fails
		print self.seqrecord
		print self.seqrecord.seq.tostring(), self.known_values['sequence']
		self.assertEqual(self.seqrecord.seq.tostring(), self.known_values['sequence'])
		self.assertEqual(self.seqrecord.id, self.known_values['id'])

	def test_stopIteration(self):
		"""
		Check that SeqIO returns an IterationError if there are no sequences left in the file.
		"""
		
		self.assertRaises(StopIteration, self.sequences.next)


# as we were saying before, BlankSeqCase derives from SimpleSeqCase so it inherits all its methods.
class BlankSeqCase(SimpleSeqCase):
	"""Test SeqIO's behaviour on a blank sequence"""
	seqcontent = ">seq1\n\n"
	known_values = {'id': 'seq1',
						'description': 'seq1',
						'sequence': ''}

	# you don't need to re-define setUp and setUpClass methods here, because they are inherited from SimpleSeqCase
	# all the tests methods are also inherited, but maybe you want to define some more
	def test_SomethingSpecialThatShouldHappenWithBlankSequences(self):
		pass
