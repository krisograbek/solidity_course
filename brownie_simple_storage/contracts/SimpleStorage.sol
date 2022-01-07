// SPDX-Licence-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 favNumber = 10;

    // bool myBool = true;
    // string myStr = "string of text";
    // my account address in the metamask
    // address myAddr = 0x55595eD1bb53a2C54C4C6818773ace899A971959;

    function store(uint256 _favNumber) public returns (uint256) {
        favNumber = _favNumber;
        return favNumber;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    // create a structure
    struct Person {
        uint256 favNum;
        string name;
    }
    // array of structures
    Person[] public people;
    mapping(string => uint256) public nameToNum;

    function addPerson(string memory _name, uint256 _favNum) public {
        people.push(Person(_favNum, _name));
        nameToNum[_name] = _favNum;
    }
}
