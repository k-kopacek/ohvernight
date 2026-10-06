const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const path = require('node:path');

const TrailDiscovery = require('../../trail-discovery.js');
const DouglasDiscovery = require('../../explore/trail-seasons.js');
const trails = JSON.parse(fs.readFileSync(path.join(__dirname, '../../trails.geojson')));
const douglas = JSON.parse(fs.readFileSync(path.join(__dirname, '../../regions/douglas-co/research.json')));

test('Aspen and Douglas activity vocabularies stay in parity', () => {
  const activities = Object.keys(TrailDiscovery.activities).sort();
  assert.deepEqual(Object.keys(DouglasDiscovery.activities).sort(), activities);
  assert.deepEqual(Object.keys(trails.features[0].properties.activities).sort(), activities);
  assert.deepEqual(Object.keys(douglas.layers.trails.features[0].properties.activities).sort(), activities);
});

test('shared layer selection API keeps only displayWater after registry migration',()=>{
  assert.deepEqual(Object.keys(require('../../map-layers.js')),['displayWater']);
});
