import os;

from itertools import groupby
from decimal import *;


class Assignment2:
	""" Class to crack the messege of One-Time Pad Algoritm"""
	messages = [
		"BB3A65F6F0034FA957F6A767699CE7FABA855AFB4F2B520AEAD612944A801E",
		"BA7F24F2A35357A05CB8A16762C5A6AAAC924AE6447F0608A3D11388569A1E",
		"A67261BBB30651BA5CF6BA297ED0E7B4E9894AA95E300247F0C0028F409A1E",
		"A57261F5F0004BA74CF4AA2979D9A6B7AC854DA95E305203EC8515954C9D0F",
		"BB3A70F3B91D48E84DF0AB702ECFEEB5BC8C5DA94C301E0BECD241954C831E",
		"A6726DE8F01A50E849EDBC6C7C9CF2B2A88E19FD423E0647ECCB04DD4C9D1E",
		"BC7570BBBF1D46E85AF9AA6C7A9CEFA9E9825CFD5E3A0047F7CD009305A71E"
		]

	firstCharacter = 32;
	notFill = "#"


	validSpaceText = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.;:?!";
		
	def __init__ (self):
		#Change Messages from HEX String to Ordinal Integers
		self.messAsLists = [ [ord(x) for x in m.decode("hex")] for m in self.messages ]


		self.validSpaceTextList = [ord(x) for x in self.validSpaceText]
		self.validSpaceTextList.sort();

		self.validKeys = {}
		for m in self.validSpaceTextList:
			self.validKeys[m ^ self.firstCharacter] = m;

		
	def crackMessages(self):
		mlen = len (self.messAsLists[0]);
		self.results = [ [ [] for i in range(0, mlen)] for j in range (0, len(self.messAsLists))];

		for i in range (0, len (self.messAsLists)):
			for j in range (i + 1, len (self.messAsLists)):
				self.makeXor (i, j);

		
		self.reduceCombination();
	

	def makeXor (self, index1, index2):
		m1 = self.messAsLists[index1];
		m2 = self.messAsLists[index2];

		mlen = len (m1);
		for i in range (0, mlen):
			xor = m1[i] ^ m2[i];


			if xor > 32:
				#Only if is a Letter & Space we try to crack it
				if xor in self.validKeys:

					# Check if is m1[i] with letter
					c = self.validKeys[xor];

					# Both messages are posible to have this letter
					self.results[index1][i].extend (chr(c))
					self.results[index2][i].extend (chr(c))


	def cleanFilled (self):
		for m in self.results:
			for i in range (0, len(m)):
				if (len (m[i]) >= 2):
					m[i].remove(self.notFill)
					m[i] = list(set(m[i]))


	def reduceCombination(self):
		print "Before Reducing Combinations ...."
		self.printPartialResult()

		mlen = len(self.results[0]);
		for j in range (0, mlen):
			toRemove = [];
			for indexMessage in range (0, len(self.results)):
				mess = self.results[indexMessage];
				slen = len (set (mess[j]));
				
				# There is only one character that fullfill this position so we remove from the other messages this letter
				if (slen == 1):
					letter = mess[j][0];
					if (len(mess[j]) == 1):
						toRemove.extend(letter)
					else:
						toRemove.extend(mess[j][1:])
					del mess[j][1:]

					
			self.removeLetters (toRemove, j);
					#mess[j] = [letter];
		print "After Reducing Combinations ...."
		self.printPartialResult()


	def removeLetters (self, toRemove, position):
		for i in range (0, len(self.results)):
			comp = self.results[i][position];

			if (len (comp) > 1):
				for letter in toRemove:
					if (letter in comp):
						comp.remove(letter);

				if (len(comp) == 0):
					comp.extend(" ");

			else:
				if (len(comp) == 0):
					comp.extend(self.notFill);


	def printPartialResult (self):
		print " Printing Messages : "
		index = 0;
		for m in self.results:
			print index, m
			index += 1;
			#print "".join(m);
			
	def printFinalResult (self):
		print " Printing FINAL Messages : "
		
		for m in self.results:
			s = "";

			for c in m:
				s += "".join(c);

			print s

if ("__main__" == __name__):
	otp = Assignment2 ();
	otp.crackMessages();
	otp.printFinalResult();
	
	