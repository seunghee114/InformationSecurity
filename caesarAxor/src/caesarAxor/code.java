package caesarAxor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class code {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		// Arrays that stores input string.
		String[] caesar_text = new String[3];
		String[] xor_text = new String[3];

		for (int i = 0; i < 3; i++) {
			caesar_text[i] = br.readLine();
		}
		for (int i = 0; i < 3; i++) {
			xor_text[i] = br.readLine();
		}
		int key = Integer.parseInt(br.readLine());

		for (int i = 0; i < 3; i++) {
			System.out.println(caesar(caesar_text[i], key));
		}
		for (int i = 0; i < 3; i++) {
			System.out.println(xor(xor_text[i], key));
		}

	}

	/**
	 * 
	 * @param plain : text to encrypt with caesar cipher
	 * @param key   : encryption key
	 * @return text to Encrypted text
	 */
	public static String caesar(String plain, int key) {
		int len = plain.length();
		String cipher = "";
		for (int i = 0; i < len; i++) {
			int temp = plain.charAt(i);
			if (65 <= temp && temp <= 90) { // upper case
				int n = temp - 'A' + key;
				if (n / 26 != 0) { // if n is out of range
					n %= 26;
				}
				cipher += (char) (n + 'A');
			}
			if (97 <= temp && temp <= 122) { // lower case
				int n = temp - 'a' + key;
				if (n / 26 != 0) { // if n is out of range
					n %= 26;
				}
				cipher += (char) (n + 'a');
			}
		}
		return cipher;
	}

	/**
	 * 
	 * @param plain : text to encrypt with xor cipher
	 * @param key   : encryption key
	 * @return text to Encrypted text
	 */
	public static String xor(String plain, int key) {
		int len = plain.length();
		String cipher = "";
		for (int i = 0; i < len; i++) {
			int temp = plain.charAt(i);
			cipher += (char) (temp ^ key); // ^ -> xor operator
		}
		return cipher;
	}

}
