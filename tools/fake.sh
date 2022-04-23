# generate test file input.txt

echo '{"id": "c9b72270-b548-47f5-af9d-6372846bd758", "symbol": "166842.XSHE", "price": 66.51, "quantity": 295, "type": "feature", "datetime": "2011-07-16 00:42:32481"}' > input.txt

# it will generate 1 * 2^30 lines
# for i in {1..30}; do cat input.txt input.txt > input2.txt && mv input2.txt input.txt; done

for i in {1..15}; do cat input.txt input.txt > input2.txt && mv input2.txt input.txt; done

wc input.txt
