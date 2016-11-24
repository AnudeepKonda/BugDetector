require 'rnn'
require 'nn'

-- Data pre processing goes here

	local n = 5--should be the vocabulary size, i.e 'no. of distinct tokens + 1'(to facilitate unknown tokens)

-- Language Model, Using vanilla RNN

local rho = 8
local hiddenSize = n
local nIndex = n
local Total_tokens -- Number of tokens in the current file should go here

-- Building recurrent neural network
local r = nn.Recurrent(
   hiddenSize, nn.Linear(hiddenSize, hiddenSize), 
   nn.Linear(hiddenSize, hiddenSize), nn.Sigmoid(), 
   rho
)

local rnn = nn.Sequential()
   :add(r)
   :add(nn.Linear(hiddenSize, nIndex))
   :add(nn.SoftMax())

rnn = nn.Recursor(rnn, rho)
print(rnn)


criterion = nn.MSECriterion()


inputs = torch.Tensor(rho, n)     --these should be set appropriately
targets = torch.Tensor(rho, n)
outputs = torch.Tensor(rho, n)

count = 0

while count < Total_tokens do
	rnn:zeroGradParameters() 
	rnn:forget() 
	for step = 1, rho do
		outputs[step] = rnn:forward(inputs[step])
		print(outputs[step]:size(), targets[step]:size())
		criterion:forward(outputs[step], targets[step])
	end
     
	gradOutputs, gradInputs = {}, {}
	for step=rho,1,-1 do -- reverse order of forward calls
		gradOutputs[step] = criterion:backward(outputs[step], targets[step])
 		gradInputs[step] = rnn:backward(inputs[step], gradOutputs[step])
	end
 
	rnn:updateParameters(0.1)

	count = count + rho
end
