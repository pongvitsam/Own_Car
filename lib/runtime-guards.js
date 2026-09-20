'use strict';

function ensureStateShape(state) {
  const next = state && typeof state === 'object' ? state : {};
  if (!Array.isArray(next.vehicles)) next.vehicles = [];
  if (!Array.isArray(next.categories)) next.categories = [];
  if (!Array.isArray(next.maintenanceLogs)) next.maintenanceLogs = [];
  if (!Array.isArray(next.fuelLogs)) next.fuelLogs = [];
  if (!Array.isArray(next.alerts)) next.alerts = [];
  if (!Array.isArray(next.lineLogs)) next.lineLogs = [];
  return next;
}

function parseRequiredNumber(raw, label, opts) {
  opts = opts || {};
  const n = opts.integer ? parseInt(raw, 10) : parseFloat(raw);
  if (!Number.isFinite(n)) return { ok: false, error: 'กรุณากรอก' + label + 'ให้ถูกต้อง' };
  if (opts.min != null && n < opts.min) {
    return { ok: false, error: label + 'ต้องไม่น้อยกว่า ' + opts.min };
  }
  if (opts.gt != null && !(n > opts.gt)) {
    return { ok: false, error: 'กรุณากรอก' + label };
  }
  return { ok: true, value: n };
}

function nextEntityId(prefix, items) {
  const used = Object.create(null);
  (items || []).forEach((item) => {
    if (item && item.id) used[String(item.id)] = true;
  });
  let n = 1;
  let id;
  do {
    id = prefix + String(n).padStart(3, '0');
    n += 1;
  } while (used[id]);
  return id;
}

function latestOdometerSafe(vehicleId, maintenanceLogs, fuelLogs) {
  const main = (maintenanceLogs || []).filter((l) => l && l.vehicleId === vehicleId).map((l) => Number(l.odo) || 0);
  const fuel = (fuelLogs || []).filter((l) => l && l.vehicleId === vehicleId).map((l) => Number(l.odo) || 0);
  return Math.max(0, ...main, ...fuel);
}

function canComputeFuelSegment(distance, liters) {
  return Number(distance) > 0 && Number(liters) > 0;
}

module.exports = {
  ensureStateShape,
  parseRequiredNumber,
  nextEntityId,
  latestOdometerSafe,
  canComputeFuelSegment,
};
