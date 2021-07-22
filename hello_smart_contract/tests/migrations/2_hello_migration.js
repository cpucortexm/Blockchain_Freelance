const Hello = artifacts.require("HelloWorld"); // require needs name of the smart contract

module.exports = function(deployer) {
  deployer.deploy(Hello);
};
