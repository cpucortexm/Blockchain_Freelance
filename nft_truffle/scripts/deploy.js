
const hre = require("truffle");

async function main() {

   var DigitalArt = artifacts.require("./DigitalArt.sol");

   const token1 = await DigitalArt.new("DigitalArtToken", "DT");
   const token2 = await DigitalArt.new("DigitalArtToken", "DT");
   return [token1, token2];

}