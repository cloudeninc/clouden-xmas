'use strict'

const getVersion = require('./get-version')
const flashColor = require('./flash-color')

module.exports.getVersion = (event, context, callback) => {
  return Promise.resolve()
  .then(() => {
    return getVersion(event)
  })
  .then(sendSuccessProxyResponse.bind(null, callback), sendErrorProxyResponse.bind(null, callback))
}

module.exports.flashColor = (event, context, callback) => {
  return Promise.resolve()
  .then(() => {
    return flashColor(event)
  })
  .then(sendSuccessProxyResponse.bind(null, callback), sendErrorProxyResponse.bind(null, callback))
}

function sendSuccessProxyResponse(callback, response) {
  const responseBody = JSON.stringify(response)
  callback(null, {
    statusCode: 200,
    body: responseBody,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    }
  })
}

function sendErrorProxyResponse(callback, err) {
  let status = 500
  let message = err.message || JSON.stringify(err)
  const m = err.message && err.message.match(/^\[(\d+)\] *(.*)$/)
  if (m) {
    status = m[1]
    message = m[2]
  }
  callback(null, {
    statusCode: status,
    body: JSON.stringify({
      errorMessage: message,
    }),
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    }
  })
}
