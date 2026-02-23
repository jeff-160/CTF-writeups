import os
import subprocess

images = [f'fam_members/{i}' for i in os.listdir("fam_members")]

with open("family_business.txt", "r") as f:
    pwds = [p.strip() for p in f.read().split("\n") if p.strip()]

for image in images:
    print(f"Processing: {os.path.basename(image)}")
    found = False
    
    for pwd in pwds:
        try:
            result = subprocess.run(['steghide', 'extract', '-sf', image, '-p', pwd, '-f'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Image: {os.path.basename(image)} | Password: {pwd}")
                found = True
        except Exception as e:
            print(f"Error with {pwd}: {e}")
    
    if not found:
        print(f"No password found for {os.path.basename(image)}")