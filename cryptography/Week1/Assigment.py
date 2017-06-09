import os;

from itertools import groupby
from decimal import *;


class VigenereCraker:
	""" Class to crack the messege of Vigenere algoritm"""
	message = """F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"""
	validSpaceText = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.;:?!";

	maxKeyLenght = 13;
	minKeyLenght = 2;
		
	def __init__ (self):
		self.messAsList = [ord(x) for x in self.message.decode("hex")]


		self.validSpaceTextList = [ord(x) for x in self.validSpaceText]
		self.validSpaceTextList.sort();



	def findKeyLenght(self):
		qi_max = -1.0;
		qi_key = -1;
		for i in range(self.minKeyLenght, self.maxKeyLenght + 1):
			qi = self.calculateQi(i);
			print "Pi for key[%d] id (val=%f)" % (i, qi)
			if (qi_max < qi):
				qi_max = qi;
				qi_key = i;
				
		print "key Lenght Selected is (key=%d with qi=%f)" % (qi_key, qi_max)
		return qi_key;

	def my_range(self, start, end, step):
		while start <= end:
			yield start
			start += step

	def calculateQiv0(self, lenght):
		total = 0;
		for i in self.my_range (0, len(self.messAsList), lenght):
			substr = self.messAsList[i:i+lenght];
			frecuency = [len(list(group)) for key, group in groupby(substr)]
			#print substr, frecuency
			pi = sum([p * p for p in frecuency]);
			total += pi;

		return total;


	def splitMessage(self, keysize):
		keygroups =[ [] for i in range (0, keysize)]
		messLenght = len(self.messAsList);

		for i in range(0, messLenght):
			keygroups[i%keysize].append (self.messAsList[i]);

		return keygroups



	def calculateQi(self, keysize):
		keygroups = self.splitMessage(keysize)
		qi = 0;
		members = len(keygroups)

		for tuple in keygroups:

			frecuency = [len(list(group)) for key, group in groupby(tuple)]
			
			pi = sum([p * p for p in frecuency]);
			pi = Decimal(pi) / (len(tuple) * len(tuple));
			qi += pi;

		return qi / (members * members);


	def findAllKeys (self, keysize):
		keygroups = self.splitMessage(keysize);

		keysAvailable = [ [] for i in range (0, keysize)]

		for keypos in range (0, keysize):

			for charCode in range(0,257):
				valid = True;

				for word in keygroups[keypos]:
					#word = int (group, 16);
					xor = word ^ charCode
					#print chr(charCode), group, word, charCode, xor
					if (not (xor in self.validSpaceTextList)):
						valid = False;
						break;

				if (valid):
					#print "Key found ", chr(charCode), charCode, keypos 
					keysAvailable[keypos].append (charCode);

		return keysAvailable;
		

	def decode (self, keys, keysize):
		possibleKeys = [];
		self.mixUpKeys (possibleKeys, list(), keys);

		for key in possibleKeys:
			messageDecode = "";
			print "trying to decode with key ", key, "".join([chr(x) for x in key])

			for i in range (0, len (self.messAsList)):
				enc = self.messAsList[i];

				dec = enc ^ key[i % keysize];
				messageDecode += chr(dec);

			print "Message Decoded [[%s\n]]" % messageDecode



	def mixUpKeys (self, total, actual, keysLeft):
		if (not keysLeft):
			total.append(actual);
			#print "Find New Possible Key", actual
			return;

		for key in keysLeft[0]:
			newActual = list(actual);
			newActual.append(key);
			self.mixUpKeys(total, newActual, keysLeft[1:]);



	def crack (self):
		keylen = self.findKeyLenght();
		if (keylen < 0):
			print ("Key Lenght could not be found");
			return;

		keys = self.findAllKeys (keylen);

		print "Keys found ", keys

		message = self.decode (keys, keylen);



if ("__main__" == __name__):
	vc = VigenereCraker ();
	vc.crack();
	
	