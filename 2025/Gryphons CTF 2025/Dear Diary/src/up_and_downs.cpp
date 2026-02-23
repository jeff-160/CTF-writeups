#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>

using namespace std;

class CustomEncryption {
private:
    int rails;
    vector<int> modValues;
    
    string preprocessText(const string& text) {
        string processed = "";
        for (char c : text) {
            if (c != ' ') {
                processed += toupper(c);
            }
        }
        return processed;
    }
    
    string removeSpecialCharacters(const string& text) {
        string cleaned = "";
        for (char c : text) {
            if (isalnum(c)) {  // Keep only alphanumeric characters
                cleaned += c;
            }
        }
        return cleaned;
    }
    
    string railFenceEncrypt(const string& text, int numRails) {
        if (numRails <= 1) return text;
        
        vector<string> rails(numRails);
        int rail = 0;
        bool directionDown = true;
        
        for (char c : text) {
            rails[rail] += c;
            
            if (rail == 0) {
                directionDown = true;
            } else if (rail == numRails - 1) {
                directionDown = false;
            }
            
            rail += directionDown ? 1 : -1;
        }
        
        string encrypted = "";
        for (const string& r : rails) {
            encrypted += r;
        }
        
        return encrypted;
    }
    
    void generateModValues() {
        modValues.clear();
        for (int i = 0; i < 5; i++) {
            modValues.push_back(10 + i*7) ; //Fixed mod 
        }
    }
    
    string applyModTransformations(const string& text) {
        string result = text;
        
        for (int iteration = 0; iteration < 5; iteration++) {
            string transformed = "";
            int modVal = modValues[iteration];
            
            for (size_t i = 0; i < result.length(); i++) {
                char c = result[i];
                
                if (isalpha(c)) {
                    int offset = (c - 'A' + modVal + i) % 26;
                    transformed += char('A' + offset);
                } else {
                    transformed += c;
                }
            }
            
            result = transformed;
        }
        
        return result;
    }
    
    string addSpacing(const string& text) {
        string spaced = "";
        for (size_t i = 0; i < text.length(); i++) {
            spaced += text[i];
            if ((i + 1) % 5 == 0 && i != text.length() - 1) {
                spaced += " ";
            }
        }
        return spaced;
    }
    
public:
    CustomEncryption(int numRails = 3, int seed = 12345) : rails(numRails) {
        srand(seed);
        generateModValues();
    }
    
    string encrypt(const string& plaintext) {
        string processed = preprocessText(plaintext);
        string cleaned = removeSpecialCharacters(processed);  // Remove special characters
        string railEncrypted = railFenceEncrypt(cleaned, rails);
        string modEncrypted = applyModTransformations(railEncrypted);
        string final = addSpacing(modEncrypted);
        return final;
    }
};

int main() {
    string plaintext = "GCTF25{REDACTED}"; 
    int rails = 3;
    int seed = 12345;
    
    CustomEncryption encryptor(rails, seed);
    string encrypted = encryptor.encrypt(plaintext);
    
    cout << encrypted << endl;
    
    return 0;
}