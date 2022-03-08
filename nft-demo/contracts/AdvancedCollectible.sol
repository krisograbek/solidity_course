// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    mapping(uint256 => Breed) public tokenIdToBreed;
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    // mapping for senders
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);

    // event

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        // assign the sender address to this request ID
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        // select a breed based on a random number
        Breed breed = Breed(randomNumber % 3);
        // assign a new token ID to a breed
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);

        // we can't use msg.sender for a sender, because VRFCoordinator
        // is calling this callback function
        // get sender
        address sender = requestIdToSender[requestId];
        // mint NFT with our sender and token ID
        _safeMint(sender, newTokenId);

        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        // built in function of ERC721
        // checks if the caller is an owner or approved
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721: caller is not owner nor approved"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}
