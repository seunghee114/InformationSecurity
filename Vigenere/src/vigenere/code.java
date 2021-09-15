package vigenere;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class code {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));

		// Array that stores input string.
		String[] plain = new String[5];
		for (int i = 0; i < 5; i++) {
			plain[i] = bf.readLine();
		}
		String key = bf.readLine();

		for (int i = 0; i < 5; i++) {
			System.out.println(vigenere(plain[i], key));
		}
	}

	/**
	 * consider only upper case.
	 * 
	 * @param plain : text to encrypt with vigenere cipher
	 * @param key   : encryption key
	 * @return text to Encrypted text
	 */
	public static String vigenere(String plain, String key) {
		int key_len = key.length();
		int len = plain.length();
		String cipher = "";
		for (int i = 0; i < len; i++) {
			int plainAt = plain.charAt(i) - 'A'; // plainAt : Alphabet index of the i-th character of the plain.
			int keyAt = -1;
			if (i < key_len) {
				keyAt = key.charAt(i) - 'A';
			} else { // if i is out of range of key_len
				keyAt = key.charAt(i % key_len) - 'A';
			}
			int n = keyAt + plainAt; // n : Alphabet index of encrypted character.
			if (n / 26 != 0) { // if n is out of the range of alphabet
				n %= 26;
			}
			cipher += (char) (n + 'A');
		}

		return cipher;
	}

}
