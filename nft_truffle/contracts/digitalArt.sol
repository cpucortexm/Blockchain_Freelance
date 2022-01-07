//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.7;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract DigitalArt is ERC721 {
    string private _name;
    string private _symbol;
    Art[] public arts;
    uint256 private pendingArtCount;
    mapping (uint256 => address) private _tokenOwner;
    mapping (address => uint256) private _ownedTokensCount;
    mapping (uint256 => address) private _tokenApprovals;
    mapping (address => mapping (address => bool)) private _operatorApprovals;
    mapping(uint256 => ArtTxn[]) private artTxns;
    uint256 public index;
    struct Art {
        uint256 id;
        string title;
        string description;
        uint256 price;
        string date;
        string authorName;
        address payable author;
        address payable owner;
        uint status;
        string image;
    }
    struct ArtTxn {
       uint256 id; 
       uint256 price;
       address seller;
       address buyer;
       uint txnDate;
       uint status;
    }

   event LogArtSold(uint _tokenId, string _title, string _authorName, uint256 _price, address _author,  address _current_owner, address _buyer);
   event LogArtTokenCreate(uint _tokenId, string _title, string _category, string _authorName, uint256 _price, address _author,  address _current_owner);
   event LogArtResell(uint _tokenId, uint _status, uint256 _price); 
   constructor (string memory name, string memory symbol) ERC721(name, symbol){}

    function createTokenAndSellArt(string memory _title, string memory _description, 
                                   string memory _date, string memory _authorName,  uint256 _price, string memory _image) public {
        require(bytes(_title).length > 0, 'The title cannot be empty');
        require(bytes(_date).length > 0, 'The Date cannot be empty');
        require(bytes(_description).length > 0, 'The description cannot be empty');
        require(_price > 0, 'The price cannot be empty');
        require(bytes(_image).length > 0, 'The image cannot be empty');
        Art memory _art = Art({
            id: index,
            title: _title,
            description: _description,
            price: _price,
            date: _date,
            authorName: _authorName,
            author: payable(msg.sender),
            owner: payable(msg.sender),
            status: 1,
            image: _image
        });
        arts.push(_art);   // push to the array
        uint256 tokenId = arts.length -1 ;   // array length -1 to get the token ID
        _safeMint(msg.sender, tokenId); 
        emit LogArtTokenCreate(tokenId,_title,  _date, _authorName,_price, msg.sender, msg.sender);
        index++;
        pendingArtCount++;
    }

    function buyArt(uint256 _tokenId) payable public {
        (uint256 _id, string memory _title, ,uint256 _price, uint _status,,string memory _authorName, address _author,address payable _current_owner, ) =  findArt(_tokenId);
        require(_current_owner != address(0));
        require(msg.sender != address(0));
        require(msg.sender != _current_owner);
        require(msg.value >= _price);
        require(arts[_tokenId].owner != address(0));

        //transfer ownership of art
        _transfer(_current_owner, msg.sender, _tokenId);
        //return extra payment
        if(msg.value > _price) payable(msg.sender).transfer(msg.value - _price);
        //make a payment
        _current_owner.transfer(_price);
        arts[_tokenId].owner = payable(msg.sender);
        arts[_tokenId].status = 0;
        ArtTxn memory _artTxn = ArtTxn({
            id: _id,
            price: _price,
            seller: _current_owner,
            buyer: msg.sender,
            txnDate: block.timestamp,
            status: _status
        });
        artTxns[_id].push(_artTxn);
        pendingArtCount--;
        
        emit LogArtSold(_tokenId,_title,  _authorName,_price, _author,_current_owner,msg.sender);
    }
    function resellArt(uint256 _tokenId, uint256 _price) payable public {
          require(msg.sender != address(0));
          require(isOwnerOf(_tokenId,msg.sender));
          arts[_tokenId].status = 1;
          arts[_tokenId].price = _price;
           pendingArtCount++;
          emit LogArtResell(_tokenId, 1, _price);   
    }
    function findArt(uint256 _tokenId) public view   returns (
        uint256, string memory, string memory, uint256, uint status,  string memory, string memory, address, address payable, string memory) {
            Art memory art = arts[_tokenId];
            return (art.id, art.title, art.description,
                 art.price,   art.status, art.date, art.authorName, art.author, art.owner,art.image);
    }
  
    function findAllArt() public view  returns (uint256[] memory, address[] memory, address[] memory,  uint[] memory) {
         uint256 arrLength = arts.length;
         uint256[] memory ids = new uint256[](arrLength);
         address[] memory authors = new address[](arrLength); 
         address[] memory owners= new address[](arrLength); 
         uint[] memory status = new uint[](arrLength);
         for (uint i = 0; i < arrLength; ++i) {
            Art memory art = arts[i];
            ids[i] = art.id;
            authors[i] = art.author;
            owners[i] = art.owner;
            status[i] = art.status;
         }
        return (ids,authors, owners, status);
    }
     function findAllPendingArt() public view  returns (uint256[] memory, address[] memory, address[] memory,  uint[] memory) {
        if (pendingArtCount == 0) {
           return (new uint256[](0),new address[](0), new address[](0), new uint[](0));  
        } else {
             uint256 arrLength = arts.length;
             uint256[] memory ids = new uint256[](pendingArtCount);
             address[] memory authors = new address[](pendingArtCount); 
             address[] memory owners= new address[](pendingArtCount); 
             uint[] memory status = new uint[](pendingArtCount);
             uint256 idx = 0;
             for (uint i = 0; i < arrLength; ++i) {
                Art memory art = arts[i];
                if(art.status==1) {
                    ids[idx] = art.id;
                    authors[idx] = art.author;
                    owners[idx] = art.owner;
                    status[idx] = art.status; 
                    idx++;
                }
             }
            return (ids,authors, owners, status);  
        }

    }   
    function findMyArts()  public view returns (uint256[] memory _myArts) {
        require(msg.sender != address(0));
        uint256 numOftokens = balanceOf(msg.sender);
        if (numOftokens == 0) {
            return new uint256[](0);
        } else {
            uint256[] memory myArts = new uint256[](numOftokens);
            uint256 idx = 0;
            uint256 arrLength = arts.length;
            for (uint256 i = 0; i < arrLength; i++) {
                if (ownerOf(i) == msg.sender) {
                    myArts[idx] = i;
                    idx++;
                }
            }
            return myArts;
        }
    }

    function getArtAllTxn(uint256 _tokenId) public view  returns (uint256[] memory _id, uint256[] memory _price,address[] memory seller,address[] memory buyer, uint[] memory _txnDate ){
        ArtTxn[] memory artTxnList = artTxns[_tokenId];
        uint256 arrLength = artTxnList.length;
        uint256[] memory ids = new uint256[](arrLength);
        uint256[] memory prices = new uint256[](arrLength);
        address[] memory sellers = new address[](arrLength);
        address[] memory buyers = new address[](arrLength);
        uint[] memory txnDates = new uint[](arrLength);
        for (uint i = 0; i < artTxnList.length; ++i) {
           ArtTxn memory artTxn = artTxnList[i];
           ids[i] = artTxn.id;
           prices[i] = artTxn.price; 
           sellers[i] =artTxn.seller; 
           buyers[i] =artTxn.buyer; 
           txnDates[i] =artTxn.txnDate; 
        }
         return (ids,prices,sellers,buyers, txnDates);
    }


    function isOwnerOf(uint256 tokenId, address account) public view returns (bool) {
        address owner = _tokenOwner[tokenId];
        require(owner != address(0));
        return owner == account;
    }


    function get_symbol() external view returns (string memory)
    {
        return symbol();
    }

    function get_name() external view returns (string memory)
    {
        return name();
    }


}