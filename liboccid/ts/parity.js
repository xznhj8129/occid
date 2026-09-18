const fs = require('fs');
const occid = require('./dist-lib/occid.js');
const fixtures = JSON.parse(fs.readFileSync('fixtures.json', 'utf8'));
function canonical(value) {
  const sort = (x) => Array.isArray(x) ? x.map(sort) : x && typeof x === 'object'
    ? Object.fromEntries(Object.keys(x).sort().map(k => [k, sort(x[k])])) : x;
  return JSON.stringify(sort(value));
}
for (const [name, data] of Object.entries(fixtures)) {
  const restored = occid.fromData(data);
  const encoded = occid.toData(restored);
  if (canonical(encoded) !== canonical(data)) {
    console.error(name, JSON.stringify(data), JSON.stringify(encoded));
    throw new Error(`roundtrip mismatch: ${name}`);
  }
}
const state = occid.parseExactModel(fixtures.state, 'EntityState');
if (!occid.isA(state, 'State')) throw new Error('EntityState semantic ancestry failed');
if (state.received_ts !== null) throw new Error('optional default was not materialized');
if (canonical(occid.toData(state)) !== canonical(fixtures.state)) throw new Error('field presence was not preserved');
for (const bad of [
  {model:'Missing', value:{}},
  {enum:'AltitudeDatum', name:'MADE_UP'},
  {$bytes:'FF'},
  {$integer:'3.0'},
  {model:'UID', value:'00'},
]) {
  let failed = false;
  try { occid.fromData(bad); } catch (error) { if (error instanceof occid.CodecError) failed = true; else throw error; }
  if (!failed) throw new Error(`bad input accepted: ${JSON.stringify(bad)}`);
}
console.log('parity fixtures OK');
