// This is a script that ingests a bunch of coal mines into mongo

const fs = require('fs')

var glob = require('glob')
var path = require('path')

let filesArray = []

let dataPath = glob.sync('./data/**/*.*json').forEach((file) => {
    filesArray.push(path.resolve(file))
})

// console.log(filesArray)

// console.log(dataPath)

// Load json files and store each into a separate object.
// Push each object into an array

let jsonArray = []

const loadJson = (file) => {
    for (i in file) {
        // TODO: append a `properties` record with a start/end date to it
        jsonArray.push(i)
        // TODO: Call mongoimport on this array
    }
}

for (let i = 0; i < filesArray.length; i++) {
    loadJson(i)
}

console.log(jsonArray)