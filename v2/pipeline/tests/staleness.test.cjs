const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const path = require('node:path');

const TripRules = require('../../trip-rules.js');
const Trust = require('../../trust.js');
const RootTripRules = require('../../../trip-rules.js');
const V2 = path.resolve(__dirname, '../..');
const load = relative => JSON.parse(fs.readFileSync(path.join(V2, relative), 'utf8'));
const golden = load('pipeline/tests/fixtures/trip-evaluation-golden.json');
const registry = load('pipeline/config/rules-registry.json');
const v2Places = [...load('overnight-options.json').places, ...load('ridb-options.json').places];
const rootPlaces = load('../overnight-options.json').places;
const trips = golden.trips;
const vehicles = golden.vehicles;
const suffix = ' The source review is out of date; recheck the linked sources before travel.';

function v2Evaluate(place, trip, today, now) {
  return TripRules.evaluate(Trust.applyRules(place, registry, Date.parse(`${now}T00:00:00Z`)), trip, today);
}

function rootEvaluate(place, trip, today) {
  return RootTripRules.evaluate(place, trip, today);
}

function assertGolden(rows, places, evaluate) {
  let index = 0;
  for (const place of places) {
    for (const vehicle of vehicles) {
      for (const tripBase of trips) {
        const result = evaluate(place, {...tripBase, vehicle}, golden.today, golden.now.slice(0, 10));
        const expected = rows[index++];
        assert.deepEqual({status: result.status, label: result.label, tripNote: result.tripNote,
          sourceStale: result.sourceStale ?? false}, expected);
      }
    }
  }
  assert.equal(index, rows.length);
}

test('T10: v2 fresh evaluations match the base golden matrix', () => {
  assertGolden(golden.v2.flatMap(place => place.results), v2Places,
    (place, trip, today, now) => v2Evaluate(place, trip, today, now));
});

test('T11: stale v2 restrictions remain restrictive and gain the review suffix', () => {
  const cases = [
    {place: {id: 'limit', kind: 'dispersed', checked_on: '2026-09-24', stay_limit_days: 5},
      trip: {arrive: '2026-07-10', depart: '2026-07-18', vehicle: 'high_clearance'}},
    {place: {id: 'tent', kind: 'dispersed', checked_on: '2026-09-24', tent_only: true},
      trip: {arrive: '2026-07-10', depart: '2026-07-12', vehicle: 'passenger_car'}},
    {place: {id: 'car', kind: 'dispersed', checked_on: '2026-09-24', requires_high_clearance: true},
      trip: {arrive: '2026-07-10', depart: '2026-07-12', vehicle: 'passenger_car'}},
    {place: {id: 'rv', kind: 'dispersed', checked_on: '2026-09-24', requires_high_clearance: true},
      trip: {arrive: '2026-07-10', depart: '2026-07-12', vehicle: 'motorhome'}},
    {place: {id: 'season', kind: 'dispersed', checked_on: '2026-09-24', access: {designations: {
      passenger_car: {designation: 'open', dates_open: '05/01-09/30'}}}},
      trip: {arrive: '2027-01-15', depart: '2027-01-17', vehicle: 'passenger_car'}},
  ];
  for (const {place, trip} of cases) {
    const fresh = v2Evaluate(place, trip, '2026-09-26', '2026-09-26');
    for (const staleToday of ['2026-10-25', '2026-09-26']) {
      const stalePlace = staleToday === '2026-09-26' ? {...place, checked_on: undefined} : place;
      const stale = v2Evaluate(stalePlace, trip, staleToday, `${staleToday}T00:00:00Z`.slice(0, 10));
      assert.equal(stale.status, fresh.status);
      assert.equal(stale.label, fresh.label);
      assert.equal(stale.tripNote, fresh.tripNote + suffix);
      assert.equal(stale.sourceStale, true);
    }
    const future = v2Evaluate({...place, checked_on: '2026-10-26'}, trip, '2026-09-26', '2026-09-26');
    assert.equal(future.status, fresh.status);
    assert.equal(future.label, fresh.label);
    assert.equal(future.tripNote, fresh.tripNote + suffix);
    assert.equal(future.sourceStale, true);
  }
});

test('T12: stale supportive v2 outcomes become unknown', () => {
  const cases = [
    {kind: 'lodging'},
    {kind: 'dispersed'},
    {kind: 'dispersed', access: {designations: {passenger_car: {
      designation: 'open', dates_open: '05/01-09/30'}}}},
  ];
  for (const place of cases) {
    const result = v2Evaluate({...place, checked_on: '2026-09-24'},
      {arrive: '2026-07-10', depart: '2026-07-12', vehicle: 'passenger_car'},
      '2026-10-25', '2026-10-25');
    assert.equal(result.status, 'review');
    assert.equal(result.label, 'Source review is stale');
    assert.doesNotMatch(result.tripNote, /Within the mapped/);
    assert.equal(result.sourceStale, true);
  }
});

test('T13: stale v2 shipped exclusions remain excluded', () => {
  for (const place of v2Places) {
    for (const vehicle of vehicles) {
      for (const tripBase of trips) {
        const trip = {...tripBase, vehicle};
        const fresh = v2Evaluate(place, trip, golden.today, golden.now.slice(0, 10));
        if (fresh.status !== 'excluded') continue;
        const stale = v2Evaluate(place, trip, '2027-06-01', '2027-06-01');
        assert.equal(stale.status, 'excluded', `${place.id}/${vehicle}/${trip.arrive}`);
      }
    }
  }
});

test('T14: stale and unconfirmed rules merge restrictions most restrictively', () => {
  const staleRule = {place_ids: ['rule-place'], stay_limit_days: 5,
    requires_high_clearance: true, last_confirmed_at: '2026-01-01T00:00:00Z',
    max_age_hours: 24, source_url: 'https://example.org/rule'};
  const place = {id: 'rule-place', stay_limit_days: 3, requires_high_clearance: false};
  const result = Trust.applyRules(place, {rules: [staleRule]}, Date.parse('2026-09-26T00:00:00Z'));
  assert.equal(result.stay_limit_days, 3);
  assert.equal(result.requires_high_clearance, true);
  assert.ok(result.ruleReview);

  const noPlaceLimit = Trust.applyRules({id: 'rule-place'}, {rules: [staleRule]},
    Date.parse('2026-09-26T00:00:00Z'));
  assert.equal(noPlaceLimit.stay_limit_days, 5);
  assert.equal(noPlaceLimit.requires_high_clearance, true);
  assert.equal(Trust.applyRules({id: 'rule-place', stay_limit_days: 3},
    {rules: [{...staleRule, stay_limit_days: 5, requires_high_clearance: false}]},
    Date.parse('2026-09-26T00:00:00Z')).stay_limit_days, 3);
});

test('T15: root fresh evaluations match the base golden matrix', () => {
  assertGolden(golden.root.flatMap(place => place.results), rootPlaces,
    (place, trip, today) => rootEvaluate(place, trip, today));
});

test('T15: stale root restrictions survive without adding stay-limit logic', () => {
  const cases = [
    {tent_only: true, kind: 'dispersed'},
    {requires_high_clearance: true, kind: 'dispersed'},
    {requires_high_clearance: true, kind: 'dispersed', vehicle: 'motorhome'},
    {kind: 'dispersed', access: {designations: {passenger_car: {
      designation: 'open', dates_open: '05/01-09/30'}}}},
  ];
  for (const base of cases) {
    const vehicle = base.vehicle || 'passenger_car';
    const trip = {arrive: '2027-01-15', depart: '2027-01-17', vehicle};
    const place = {...base, checked_on: '2026-09-24'};
    const fresh = rootEvaluate(place, trip, '2026-09-26');
    const stale = rootEvaluate(place, trip, '2026-10-25');
    assert.equal(stale.status, fresh.status);
    assert.equal(stale.label, fresh.label);
    assert.equal(stale.tripNote, fresh.tripNote + suffix);
    assert.equal(stale.sourceStale, true);
  }
});

test('T15: stale root supportive outcomes become unknown', () => {
  for (const place of [{kind: 'lodging'}, {kind: 'dispersed'}]) {
    const result = rootEvaluate({...place, checked_on: '2026-09-24'},
      {arrive: '2026-07-10', depart: '2026-07-12', vehicle: 'passenger_car'}, '2026-10-25');
    assert.equal(result.status, 'review');
    assert.equal(result.label, 'Source review is stale');
    assert.doesNotMatch(result.tripNote, /Within the mapped/);
    assert.equal(result.sourceStale, true);
  }
});

test('T15: stale root shipped exclusions remain excluded', () => {
  for (const place of rootPlaces) {
    for (const vehicle of vehicles) {
      for (const tripBase of trips) {
        const trip = {...tripBase, vehicle};
        const fresh = rootEvaluate(place, trip, golden.today);
        if (fresh.status !== 'excluded') continue;
        const stale = rootEvaluate(place, trip, '2027-06-01');
        assert.equal(stale.status, 'excluded', `${place.id}/${vehicle}/${trip.arrive}`);
      }
    }
  }
});
