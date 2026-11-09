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
  let max = 0;
  main.concat(fuel).forEach((n) => { if (n > max) max = n; });
  return max;
}

function canComputeFuelSegment(distance, liters) {
  return Number(distance) > 0 && Number(liters) > 0;
}

// Odometer must stay between neighbouring entries by date.
function odometerBoundsForDate(vehicleId, excludeFuelId, date, maintenanceLogs, fuelLogs) {
  let min = 0;
  let max = null;
  const consider = (l) => {
    if (!l || l.vehicleId !== vehicleId) return;
    const odo = Number(l.odo) || 0;
    const d = String(l.date || '');
    if (!date || !d || d <= date) {
      if (odo > min) min = odo;
    } else if (max == null || odo < max) {
      max = odo;
    }
  };
  (maintenanceLogs || []).forEach(consider);
  (fuelLogs || []).forEach((l) => { if (l && l.id !== excludeFuelId) consider(l); });
  return { min, max };
}

module.exports = {
  odometerBoundsForDate,
  ensureStateShape,
  parseRequiredNumber,
  nextEntityId,
  latestOdometerSafe,
  canComputeFuelSegment,
};
