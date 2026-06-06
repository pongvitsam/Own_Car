'use strict';

/**
 * Pure car-care logic mirrored from gas/Fuel.gs, gas/Alerts.gs, gas/Odometer.gs, gas/Scripts.html.
 * npm test source of truth; GAS duplicates these formulas (Apps Script has no require).
 */

const THAI_MONTHS_SHORT = [
  'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
  'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.',
];

const MS_PER_DAY = 1000 * 60 * 60 * 24;

function getLatestOdometer(vehicleId, maintenanceLogs, fuelLogs) {
  const main = (maintenanceLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .map((l) => l.odo);
  const fuel = (fuelLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .map((l) => l.odo);
  const all = main.concat(fuel).concat([0]);
  return Math.max(...all);
}

function getLatestOdometerAtDate(vehicleId, dateStr, maintenanceLogs) {
  const logsBeforeDate = (maintenanceLogs || [])
    .filter((l) => l.vehicleId === vehicleId && l.date <= dateStr)
    .sort((a, b) => b.odo - a.odo);
  return logsBeforeDate.length > 0 ? logsBeforeDate[0].odo : 0;
}

function validateFuelOdometer(newOdo, lastOdo) {
  if (newOdo < lastOdo) {
    return { valid: false, error: 'ระยะไมล์ปัจจุบันน้อยกว่าระยะล่าสุดของรถ!' };
  }
  return { valid: true };
}

function validateOdometerOnly(newOdo, lastOdo) {
  if (newOdo < lastOdo) {
    return { valid: false, error: 'กิโลเมตรปัจจุบันน้อยกว่าครั้งล่าสุด!' };
  }
  return { valid: true };
}

function getFirstOdometer(vehicleId, maintenanceLogs) {
  const logs = (maintenanceLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .sort((a, b) => a.odo - b.odo);

  if (logs.length === 0) return 0;

  const validFirstOdoLogs = logs.filter((l) => l.odo > 0);
  return validFirstOdoLogs.length > 0 ? validFirstOdoLogs[0].odo : 0;
}

function computeMaintenanceCostPerKm(vehicleId, maintenanceLogs, latestOdo) {
  const logs = (maintenanceLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .sort((a, b) => a.odo - b.odo);

  const firstOdo = getFirstOdometer(vehicleId, maintenanceLogs);
  const totalDistance = latestOdo - firstOdo;
  const totalCost = logs
    .filter((l) => l.type === 'Maintenance')
    .reduce((sum, l) => sum + l.cost, 0);

  if (totalDistance > 0 && totalCost > 0) {
    return totalCost / totalDistance;
  }
  return 0;
}

/** Simple health percent from odo range (Scripts.html formula). */
function calculateHealthPercentFromRange(latestOdo, baseKm, targetKm) {
  const range = targetKm - baseKm;
  const runSinceLastAlertSet = latestOdo - baseKm;

  if (range <= 0) {
    return 100;
  }

  return Math.max(0, Math.min(100, 100 - (runSinceLastAlertSet / range) * 100));
}

function calculateHealthPercent({ vehicleId, latestOdo, alert, maintenanceLogs }) {
  if (!alert || alert.status !== 'Active') {
    return { percent: 100, tier: 'none' };
  }

  const firstOdo = getFirstOdometer(vehicleId, maintenanceLogs);
  const totalTargetKm = alert.targetKm;
  const baseKm = alert.lastUpdated
    ? getLatestOdometerAtDate(vehicleId, alert.lastUpdated, maintenanceLogs)
    : firstOdo;

  const safetyPct = calculateHealthPercentFromRange(latestOdo, baseKm, totalTargetKm);

  return { percent: safetyPct, tier: getHealthBarTier(safetyPct) };
}

function getHealthBarTier(safetyPct) {
  if (safetyPct < 20) return 'critical';
  if (safetyPct < 50) return 'warning';
  return 'healthy';
}

/** Fuelio full-tank segments (Scripts.html renderFuelLogs: consecutive full tanks only). */
function computeFuelLogMetrics(vehicleId, fuelLogs) {
  const logs = (fuelLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  let totalCostSum = 0;
  let totalLitersSum = 0;
  let efficiencySum = 0;
  let efficiencyCount = 0;

  const enriched = logs.map((log) => ({ ...log }));

  for (let i = 0; i < enriched.length; i++) {
    const current = enriched[i];
    totalCostSum += current.totalCost;
    totalLitersSum += current.liters;

    if (i > 0 && current.fullTank && enriched[i - 1].fullTank) {
      const distance = current.odo - enriched[i - 1].odo;
      if (distance > 0) {
        current.calculatedEfficiency = distance / current.liters;
        current.costPerKm = current.totalCost / distance;
        efficiencySum += current.calculatedEfficiency;
        efficiencyCount++;
      }
    }
  }

  let avgEfficiency = null;
  let avgCostPerKm = null;

  if (efficiencyCount > 0) {
    avgEfficiency = efficiencySum / efficiencyCount;

    const totalCalculatedCost = enriched.slice(1).reduce(
      (sum, l) => sum + (l.costPerKm ? l.totalCost : 0),
      0
    );
    const totalCalculatedDistance = enriched.slice(1).reduce(
      (sum, l, idx) => sum + (l.costPerKm ? l.odo - enriched[idx].odo : 0),
      0
    );
    avgCostPerKm =
      totalCalculatedDistance > 0 ? totalCalculatedCost / totalCalculatedDistance : null;
  }

  const lastPricePerLiter = logs.length > 0 ? logs[logs.length - 1].pricePerLiter : null;

  return {
    logs: enriched,
    totalCostSum,
    totalLitersSum,
    avgEfficiency,
    avgCostPerKm,
    lastPricePerLiter,
    efficiencyCount,
  };
}

function calculateFuelEfficiency(fuelLogs, vehicleId) {
  const metrics = computeFuelLogMetrics(vehicleId, fuelLogs);
  return {
    fills: metrics.logs.map((l) => ({
      logId: l.id,
      date: l.date,
      odo: l.odo,
      liters: l.liters,
      fullTank: l.fullTank,
      kmPerLiter: l.calculatedEfficiency ?? null,
      costPerKm: l.costPerKm ?? null,
      distance:
        l.calculatedEfficiency != null && metrics.logs.indexOf(l) > 0
          ? l.odo - metrics.logs[metrics.logs.indexOf(l) - 1].odo
          : null,
    })),
    averageKmPerLiter: metrics.avgEfficiency,
    averageCostPerKm: metrics.avgCostPerKm,
    efficiencyCount: metrics.efficiencyCount,
  };
}

function calculateCostPerKm(maintenanceLogs, vehicleId, fuelLogs) {
  const latestOdo = getLatestOdometer(vehicleId, maintenanceLogs, fuelLogs || []);
  return computeMaintenanceCostPerKm(vehicleId, maintenanceLogs, latestOdo);
}

function getEfficiencyTier(efficiency) {
  if (efficiency > 15) return 'good';
  if (efficiency > 11) return 'medium';
  return 'poor';
}

function resolveAlertServiceLabel(alert, categories, maintenanceLogs) {
  if (!alert) {
    return 'บำรุงรักษาตามกำหนด';
  }
  if (alert.serviceLabel) {
    return alert.serviceLabel;
  }
  if (alert.categoryId) {
    const cat = (categories || []).find((c) => c.id === alert.categoryId);
    if (cat) {
      return cat.name;
    }
  }
  const logs = (maintenanceLogs || []).filter(
    (l) =>
      l.vehicleId === alert.vehicleId &&
      l.date === alert.lastUpdated &&
      (l.alertKm > 0 || l.alertMonth > 0)
  );
  if (logs.length > 0) {
    const cat = (categories || []).find((c) => c.id === logs[0].category);
    if (cat) {
      return cat.name;
    }
  }
  return 'บำรุงรักษาตามกำหนด';
}

function buildAlertReason(isKmReached, isTimeReached, currentOdo, targetDate) {
  if (isKmReached && isTimeReached) {
    return 'ครบกำหนดทั้งระยะทางและเวลา';
  }
  if (isKmReached) {
    return `ระยะไมล์สะสมถึงกำหนด (${currentOdo.toLocaleString()} กม.)`;
  }
  return `ถึงกำหนดครบเวลาบำรุงรักษาแล้ว (${targetDate})`;
}

function evaluateAlert(alert, vehicle, currentOdo, today) {
  if (alert.status !== 'Active' || !vehicle) {
    return null;
  }

  const targetDate = new Date(alert.targetDate);
  const isKmReached = currentOdo >= alert.targetKm;
  const isTimeReached = today >= targetDate;

  if (!isKmReached && !isTimeReached) {
    return null;
  }

  const reason = buildAlertReason(isKmReached, isTimeReached, currentOdo, alert.targetDate);
  const message = `🚗 ${vehicle.name}: ${reason}`;

  return {
    alertId: alert.alertId,
    vehicleId: alert.vehicleId,
    reason,
    message,
    isKmReached,
    isTimeReached,
  };
}

function checkAlerts(alerts, vehicles, getCurrentOdo, today) {
  const triggered = [];
  const messages = [];

  for (const alert of alerts) {
    const vehicle = vehicles.find((v) => v.id === alert.vehicleId);
    const currentOdo = getCurrentOdo(alert.vehicleId);
    const result = evaluateAlert(alert, vehicle, currentOdo, today);
    if (result) {
      triggered.push(result);
      messages.push(result.message);
    }
  }

  return {
    notificationTriggered: triggered.length > 0,
    triggered,
    messages,
  };
}

function checkAlertStatus(currentOdo, targetKm, targetDate, now) {
  const nowDate = now instanceof Date ? now : new Date(now);
  const target = targetDate instanceof Date ? targetDate : new Date(targetDate);

  const kmRemaining = targetKm - currentOdo;
  const daysRemaining = Math.ceil((target.getTime() - nowDate.getTime()) / MS_PER_DAY);

  const urgent = kmRemaining <= 1000 || daysRemaining <= 15;
  const kmReached = currentOdo >= targetKm;
  const timeReached = nowDate >= target;

  return {
    urgent,
    kmRemaining,
    daysRemaining,
    kmReached,
    timeReached,
    shouldNotify: kmReached || timeReached,
  };
}

function buildLineAlertMessage(vehicle, reason, nowStr) {
  return (
    '\n🔧 MyHome CarCare แจ้งเตือนบำรุงรักษา\n' +
    `รถ: ${vehicle.name} (${vehicle.license})\n` +
    `สาเหตุ: ${reason}\n` +
    `วันที่: ${nowStr}\n` +
    'กรุณาตรวจสอบและนัดหมายซ่อมบำรุง'
  );
}

function getVehicleStatusLevel(alert, latestOdo, today) {
  if (!alert || alert.status !== 'Active') {
    return 'none';
  }

  const status = checkAlertStatus(latestOdo, alert.targetKm, alert.targetDate, today);
  return status.urgent ? 'urgent' : 'normal';
}

function formatThaiDate(dateStr) {
  const date = dateStr instanceof Date ? dateStr : new Date(dateStr);
  if (isNaN(date.getTime())) {
    return '-';
  }
  return `${date.getDate()} ${THAI_MONTHS_SHORT[date.getMonth()]} ${date.getFullYear() + 543}`;
}

function parseIsoDate(dateStr) {
  const parts = String(dateStr).split('-');
  if (parts.length !== 3) {
    return new Date(dateStr);
  }
  return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
}

/** Parse ISO date year without timezone drift (YYYY-MM-DD). */
function daysUntilDate(dateStr, now) {
  if (!dateStr) return null;
  const parts = String(dateStr).split('-');
  if (parts.length !== 3) return null;
  const target = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  const today = now instanceof Date ? new Date(now) : new Date(now);
  today.setHours(0, 0, 0, 0);
  return Math.ceil((target.getTime() - today.getTime()) / MS_PER_DAY);
}

function isExpiryUrgent(dateStr, withinDays, now) {
  const days = daysUntilDate(dateStr, now);
  if (days === null) return false;
  const threshold = withinDays != null ? withinDays : 30;
  return days <= threshold;
}

function getVehicleExpiryWarnings(vehicle, now, withinDays) {
  const threshold = withinDays != null ? withinDays : 30;
  const warnings = [];
  if (vehicle.prbExpiryDate && isExpiryUrgent(vehicle.prbExpiryDate, threshold, now)) {
    warnings.push({ type: 'prb', date: vehicle.prbExpiryDate, days: daysUntilDate(vehicle.prbExpiryDate, now) });
  }
  if (vehicle.insuranceExpiryDate && isExpiryUrgent(vehicle.insuranceExpiryDate, threshold, now)) {
    warnings.push({ type: 'insurance', date: vehicle.insuranceExpiryDate, days: daysUntilDate(vehicle.insuranceExpiryDate, now) });
  }
  return warnings;
}

function getLogYear(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') return null;
  const match = dateStr.match(/^(\d{4})/);
  return match ? parseInt(match[1], 10) : null;
}

function getMaintenanceYearsForVehicle(maintenanceLogs, vehicleId) {
  const yearCounts = {};
  (maintenanceLogs || []).forEach((l) => {
    if (l.type !== 'Maintenance' || l.vehicleId !== vehicleId) return;
    const year = getLogYear(l.date);
    if (year == null) return;
    yearCounts[year] = (yearCounts[year] || 0) + 1;
  });
  const years = Object.keys(yearCounts)
    .map(Number)
    .sort((a, b) => b - a);
  return { years, yearCounts };
}

function pickDefaultReportYear(years, yearCounts, currentYear, previousValue) {
  if (!years.length) return currentYear;
  const prev = previousValue != null ? parseInt(previousValue, 10) : NaN;
  if (!Number.isNaN(prev) && years.includes(prev)) return prev;
  if (yearCounts[currentYear]) return currentYear;
  return years.reduce(
    (best, y) => ((yearCounts[y] || 0) > (yearCounts[best] || 0) ? y : best),
    years[0]
  );
}

function computeAnnualReportStats(maintenanceLogs, vehicleId, year) {
  const targetYear = Number(year);
  const yearLogs = (maintenanceLogs || []).filter((l) => {
    if (l.type !== 'Maintenance' || l.vehicleId !== vehicleId) return false;
    return getLogYear(l.date) === targetYear;
  });
  const total = yearLogs.reduce((sum, l) => sum + (l.cost || 0), 0);
  return { yearLogs, total, count: yearLogs.length };
}

module.exports = {
  THAI_MONTHS_SHORT,
  getLatestOdometer,
  getLatestOdometerAtDate,
  validateFuelOdometer,
  validateOdometerOnly,
  getFirstOdometer,
  computeMaintenanceCostPerKm,
  calculateHealthPercent,
  calculateHealthPercentFromRange,
  getHealthBarTier,
  computeFuelLogMetrics,
  calculateFuelEfficiency,
  calculateCostPerKm,
  getEfficiencyTier,
  resolveAlertServiceLabel,
  buildAlertReason,
  evaluateAlert,
  checkAlerts,
  checkAlertStatus,
  buildLineAlertMessage,
  getVehicleStatusLevel,
  formatThaiDate,
  parseIsoDate,
  getLogYear,
  getMaintenanceYearsForVehicle,
  pickDefaultReportYear,
  computeAnnualReportStats,
  daysUntilDate,
  isExpiryUrgent,
  getVehicleExpiryWarnings,
};
