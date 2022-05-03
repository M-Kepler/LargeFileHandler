# generate test file input.txt


content='{"id": "c9b72270-b548-47f5-af9d-6372846bd758", "symbol": "166842.XSHE", "price": 66.51, "quantity": 295, "type": "feature", "datetime": "2011-07-16 00:42:32481"}' > input.txt
echo $content > input.txt

# it will generate 1 * 2^30 lines

# _1GB = 1073741824 bytes
# lines = _1GB / sizeof($content) # 6669203.875776397 lines
# 2^22 = 4194304  lines -----> 644 MB
# 2^23 = 8388608  lines -----> 1.2578125 GB
# 2^24 = -----> 2.515625 GB
# 2^25 = -----> 5.03125 GB
# 2^26 = -----> 10.0625 GB
# 2^27 = -----> 20.125 GB
# 2^28 = -----> 40.25 GB
# 2^29 = -----> 80.5 GB
# 2^30 = -----> 161.0 GB

# for i in {1..22}; do cat input.txt input.txt > input2.txt && mv input2.txt input.txt; done
for i in {1..20}; do cat input.txt input.txt > input2.txt && mv input2.txt input.txt; done

wc input.txt
