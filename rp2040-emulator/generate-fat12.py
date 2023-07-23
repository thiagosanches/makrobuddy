from littlefs import LittleFS
files = ['code.py']
output_image = 'fat12.img'  # symlinked/copied to rp2040js root directory
lfs = LittleFS(block_size=4096, block_count=352, prog_size=256)
for filename in files:
    with open(filename, 'rb') as src_file, lfs.open(filename, 'w') as lfs_file:
        lfs_file.write(src_file.read().decode('utf-8'))
with open(output_image, 'wb') as fh:
    fh.write(lfs.context.buffer)