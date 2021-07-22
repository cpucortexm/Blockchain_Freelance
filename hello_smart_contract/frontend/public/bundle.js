var contractABI = [
    {
      "inputs": [],
      "name": "hello",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "pure",
      "type": "function",
      "constant": true
    }
  ];

  var contractAddress = '0xcFb962032Ba7A16eb7e5e1059BB3531E7d38CcfE'; // pointer to the deployed contract

  var web3 = new Web3('http://localhost:9545')

  var helloworld = new web3.eth.Contract(contractABI, contractAddress)   // contract instance of hello world
  
  
document.addEventListener('DOMContentLoaded', () =>{
  helloworld.methods.hello().call()     // gets the data from smart contract function
  .then(result =>{
      document.getElementById('hello').innerHTML = result;  // gets data from 
  })
});