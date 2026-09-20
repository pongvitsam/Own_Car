'use strict';

/**
 * Local-first merge helpers for GitHub Pages ↔ Google Sheets sync.
 * The browser app inlines the same formulas; npm tests use this module.
 */

function mergeRecordsById(localArr, remoteArr, preferLocal) {
  const map = new Map();
  const put = (item) => {
    if (!item || item.id == null) return;
    map.set(String(item.id), item);
  };
  if (preferLocal) {
    (remoteArr || []).forEach(put);
    (localArr || []).forEach(put);
  } else {
    (localArr || []).forEach(put);
    (remoteArr || []).forEach(put);
  }
  return Array.from(map.values());
}

function restoreSeedIfEmpty(current, seed) {
  if (!current || !seed) return current;
  const vehiclesEmpty = !Array.isArray(current.vehicles) || !current.vehicles.length;
  if (vehiclesEmpty) {
    current.vehicles = (seed.vehicles || []).slice();
    if (!Array.isArray(current.categories) || !current.categories.length) {
      current.categories = (seed.categories || []).slice();
    }
    if (!Array.isArray(current.maintenanceLogs) || !current.maintenanceLogs.length) {
      current.maintenanceLogs = (seed.maintenanceLogs || []).slice();
    }
    if (!Array.isArray(current.fuelLogs) || !current.fuelLogs.length) {
      current.fuelLogs = (seed.fuelLogs || []).slice();
    }
    if (!Array.isArray(current.alerts) || !current.alerts.length) {
      current.alerts = (seed.alerts || []).slice();
    }
  } else {
    if (!Array.isArray(current.categories)) current.categories = (seed.categories || []).slice();
    if (!Array.isArray(current.maintenanceLogs)) current.maintenanceLogs = [];
    if (!Array.isArray(current.fuelLogs)) current.fuelLogs = [];
    if (!Array.isArray(current.alerts)) current.alerts = [];
  }
  return current;
}

function shouldSkipRemoteApply(pendingMutations, retryQueueLength) {
  return (pendingMutations || 0) > 0 || (retryQueueLength || 0) > 0;
}

module.exports = {
  mergeRecordsById,
  restoreSeedIfEmpty,
  shouldSkipRemoteApply,
};
