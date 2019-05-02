import mpt

# Testcase in https://github.com/ethereum/wiki/wiki/Patricia-Tree#example-trie, Root Hash = 5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84
# Patricia trie =
#     [ <16>, [ <>, <>, <>, <>, [ <00 6f>, [ <>, <>, <>, <>, <>, <>, [ <17>, [ <>, <>, <>, <>, <>, <>, [ <35>, 'coin' ], <>, <>, <>, <>, <>, <>, <>, <>, <>, 'puppy' ] ],
#      <>, <>, <>, <>, <>, <>, <>, <>, <>, 'verb' ] ], <>, <>, <>, [ <20 6f 72 73 65>, 'stallion' ], <>, <>, <>, <>, <>, <>, <>, <> ]
#dict_ = {'646f' : b'verb', '646f67' : b'puppy', '646f6765' : b'coin', '686f727365' : b'stallion'}

# Testcase, Root Hash = a9116924943abeddebf1c0da975ebef7b2006ede340b0f9e18504b65b52948ed
dict_ = {'a711355' : b"45"}
# Testcase, Root Hash = 39067a59d2192dbde0af0968ba50ac88d02a41e3a9e06834e6f3490edec03cb5
#dict_ = {'a711355' : b"45", 'a7f9365' : b"2"}
# Testcase, Root Hash = 608b7c482ee39d36c1aadbbf38d8d4d7a557dbe5d0484c02a44a8bdb3f87f1e6
#dict_ = {'a711355' : b"45", 'a77d337' : b"1", 'a7f9365' : b"2"}
# Testcase: Root Hash = 5838ad5578f346f40d3e6b71f9a82ae6e5198dd39c52e18deec63734da512055
#dict_ = {'a711355' : b"45", 'a77d337' : b"1", 'a7f9365' : b"2", 'a77d397' : b"12"}
# Testcase, Root Hash = 0214f87faeb8417f4e5a73df8ee4aaaf904571fb9f859e2e8aa64f6f003ba3bf
#dict_ = {'a711355' : b"45", 'a711356' : b"46", 'a711357' : b"47", 'a77d337' : b"1", 'a7f9365' : b"2", 'a77d397' : b"12"}


############################################################################################################

# Released Testcase: Root Hash = 5838ad5578f346f40d3e6b71f9a82ae6e5198dd39c52e18deec63734da512055
#dict_ = {'a711355' : b"45", 'a77d337' : b"1", 'a7f9365' : b"2", 'a77d397' : b"12"}


############################################################################################################

# Homework Case [Real Ethereum Address]

# Original State: Root Hash = b3506d16d769a8aaf5e2fe2f4449a673b408472c04ba0e0837aba0bc9d5364cd
'''
dict_ = {
	'7c3002ad756d76a643cb09cd45409608abb642d9' : b'10',
	'7c303333756d555643cb09cd45409608abb642d9' : b'20',
	'7c303333756d777643cb09c999409608abb642d9' : b'30',
	'7c303333756d777643cb09caaa409608abb642d9' : b'40',
	'111102ad756d76a643cb09cd45409608abb642d9' : b'50'
}
'''

# New State (After Tx, no reward): Root Hash = eff402b46c2b81e230797cf224c5440aefde9335594271e19da8c75ecc476d08
'''
dict_ = {
	'7c3002ad756d76a643cb09cd45409608abb642d9' : b'8', # -2 (Update)
	'7c303333756d555643cb09cd45409608abb642d9' : b'20',
	'7c303333756d777643cb09c999409608abb642d9' : b'24', # -6 (Update)
	'7c303333756d777643cb09caaa409608abb642d9' : b'42', # +2 (Update)
	'111102ad756d76a643cb09cd45409608abb642d9' : b'50', 
	'11113333756d76a643cb09cd45409608abb642d9' : b'6' # +6 (New node)
}
'''

############################################################################################################

mpt.info(dict_)
