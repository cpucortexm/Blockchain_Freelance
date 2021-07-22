const Hello = artifacts.require('HelloWorld');    // require always uses name of the smart contract

contract('HelloWorld', () => {
  it('should return Hello World', async () => {
    const helloWorld = await Hello.deployed();
    const result = await helloWorld.hello();
    assert(result === 'Hello World');
  });
});
