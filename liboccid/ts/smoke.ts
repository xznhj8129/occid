import {
  createModel, dumps, parseModel, toData, fromData, isA,
  UID, DataRateSpec, Communication,
} from "./occid";

const uid: UID = createModel("UID", Uint8Array.from({ length: 16 }, (_, i) => i));
const rate: DataRateSpec = createModel("DataRateSpec", { nominal_bps: 9600 });
const semantic: Communication = rate;
const json = dumps(rate);
const parsed = parseModel(JSON.parse(json), "Communication");
if (!isA(parsed, "Communication")) throw new Error("bad ancestry");
console.log(uid.$model, semantic.$model, toData(parsed), fromData(JSON.parse(json)));
