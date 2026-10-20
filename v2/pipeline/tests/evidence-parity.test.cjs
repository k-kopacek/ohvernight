const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const path = require('node:path');

const Trust = require('../../trust.js');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/freshness-vectors.json'), 'utf8'));

for (const vector of fixture) {
  test(`freshness parity: ${vector.name}`, () => {
    assert.equal(Trust.freshness(vector.record, Date.parse(vector.now)), vector.expected);
  });
}
