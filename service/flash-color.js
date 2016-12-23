'use strict'

const AWS = require('aws-sdk')
const promisify = require('es6-promisify')
const iot = new AWS.IotData({endpoint: process.env.IOT_ENDPOINT})
const iotPublish = promisify(iot.publish, iot)

const ALLOWED = {
  red: 'number',
  green: 'number',
  blue: 'number',
}
/**
 * Event looks like (flash count is 1..5)
 * {
 *   "red": 1,
 *   "green": 2
 *   "blue": 3
 * }
 */
module.exports = function(event) {
  const body = JSON.parse(event.body)
  const msg = {}
  Object.keys(body).map(key => {
    if (ALLOWED[key] && ALLOWED[key] === typeof body[key]) {
      msg[key] = body[key]
    }
  })
  if (Object.keys(msg).length <= 0) {
    return Promise.reject(new Error('[400] Bad Request'))
  }
  const payload = JSON.stringify(msg)
  return iotPublish({
    topic: process.env.MQTT_TOPIC,
    payload: payload,
  })
  .then(() => {
    return msg
  })
}
