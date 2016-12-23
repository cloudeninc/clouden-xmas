'use strict'

const fs = require('fs')
const path = require('path')

const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json')))

module.exports = function(event) {
  return {
    service: pkg.name,
    version: pkg.version,
  }
}
