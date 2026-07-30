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

/** Sentinel used when alert is time-only (no meaningful km target). */
const DISTANCE_ALERT_SENTINEL_KM = 90000000;

function isDistanceBasedAlert(alertOrTargetKm) {
  const target =
    alertOrTargetKm && typeof alertOrTargetKm === 'object'
      ? Number(alertOrTargetKm.targetKm)
      : Number(alertOrTargetKm);
  return Number.isFinite(target) && target > 0 && target < DISTANCE_ALERT_SENTINEL_KM;
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

/**
 * Remaining % and countdown km for distance-based maintenance.
 * Returns null when the alert/log is not distance-based.
 */
function getDistanceAlertCountdown({ latestOdo, baseKm, targetKm, alertKm }) {
  const target = Number(targetKm);
  if (!isDistanceBasedAlert(target)) return null;

  const odo = Number(latestOdo) || 0;
  let base = Number(baseKm);
  if (!Number.isFinite(base)) {
    const offset = Number(alertKm);
    base = Number.isFinite(offset) && offset > 0 ? target - offset : odo;
  }

  const remainingKm = target - odo;
  const percentRemaining = calculateHealthPercentFromRange(odo, base, target);

  return {
    remainingKm,
    absoluteRemainingKm: Math.max(0, remainingKm),
    overdueKm: remainingKm < 0 ? Math.abs(remainingKm) : 0,
    overdue: remainingKm <= 0,
    percentRemaining,
    targetKm: target,
    baseKm: base,
    tier: getHealthBarTier(percentRemaining),
  };
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

  if (!isDistanceBasedAlert(totalTargetKm)) {
    return { percent: 100, tier: 'none', distanceBased: false };
  }

  const safetyPct = calculateHealthPercentFromRange(latestOdo, baseKm, totalTargetKm);
  const countdown = getDistanceAlertCountdown({
    latestOdo,
    baseKm,
    targetKm: totalTargetKm,
  });

  return {
    percent: safetyPct,
    tier: getHealthBarTier(safetyPct),
    distanceBased: true,
    remainingKm: countdown ? countdown.remainingKm : totalTargetKm - latestOdo,
    absoluteRemainingKm: countdown ? countdown.absoluteRemainingKm : Math.max(0, totalTargetKm - latestOdo),
    overdue: countdown ? countdown.overdue : latestOdo >= totalTargetKm,
  };
}

function getHealthBarTier(safetyPct) {
  if (safetyPct < 20) return 'critical';
  if (safetyPct < 50) return 'warning';
  return 'healthy';
}

/** Previous same-type full-tank fill (oil and gas tracked as separate Fuelio chains). */
function findPreviousSameTypeFullTank(enriched, index) {
  const currentType = enriched[index].fuelType || 'oil';
  for (let j = index - 1; j >= 0; j--) {
    const prev = enriched[j];
    if ((prev.fuelType || 'oil') === currentType && prev.fullTank) {
      return prev;
    }
  }
  return null;
}

/** Fuelio full-tank segments: consecutive full tanks of the same fuel type only. */
function computeFuelLogMetrics(vehicleId, fuelLogs) {
  const logs = (fuelLogs || [])
    .filter((l) => l.vehicleId === vehicleId)
    .sort((a, b) => parseIsoDate(a.date) - parseIsoDate(b.date));

  let totalCostSum = 0;
  let totalLitersSum = 0;
  let efficiencySum = 0;
  let efficiencyCount = 0;

  const enriched = logs.map((log) => ({ ...log, fuelType: log.fuelType || 'oil' }));

  for (let i = 0; i < enriched.length; i++) {
    const current = enriched[i];
    totalCostSum += current.totalCost;
    totalLitersSum += current.liters;

    if (!current.fullTank) continue;
    const prev = findPreviousSameTypeFullTank(enriched, i);
    if (!prev) continue;

    const distance = current.odo - prev.odo;
    if (distance > 0) {
      current.segmentDistance = distance;
      current.calculatedEfficiency = distance / current.liters;
      current.costPerKm = current.totalCost / distance;
      efficiencySum += current.calculatedEfficiency;
      efficiencyCount++;
    }
  }

  let avgEfficiency = null;
  let avgCostPerKm = null;

  if (efficiencyCount > 0) {
    avgEfficiency = efficiencySum / efficiencyCount;
    const withEff = enriched.filter((l) => l.costPerKm != null && l.segmentDistance);
    const totalCalculatedCost = withEff.reduce((sum, l) => sum + l.totalCost, 0);
    const totalCalculatedDistance = withEff.reduce((sum, l) => sum + l.segmentDistance, 0);
    avgCostPerKm =
      totalCalculatedDistance > 0 ? totalCalculatedCost / totalCalculatedDistance : null;
  }

  const lastPricePerLiter = logs.length > 0 ? logs[logs.length - 1].pricePerLiter : null;

  const summarizeType = (type) => {
    const typed = enriched.filter((l) => (l.fuelType || 'oil') === type);
    const withEff = typed.filter((l) => l.calculatedEfficiency != null);
    const effSum = withEff.reduce((sum, l) => sum + l.calculatedEfficiency, 0);
    return {
      count: typed.length,
      totalLiters: typed.reduce((sum, l) => sum + l.liters, 0),
      totalCost: typed.reduce((sum, l) => sum + l.totalCost, 0),
      avgEfficiency: withEff.length ? effSum / withEff.length : null,
      efficiencyCount: withEff.length,
    };
  };

  return {
    logs: enriched,
    totalCostSum,
    totalLitersSum,
    avgEfficiency,
    avgCostPerKm,
    lastPricePerLiter,
    efficiencyCount,
    byType: {
      oil: summarizeType('oil'),
      gas: summarizeType('gas'),
    },
  };
}

/** Recent Fuelio efficiency points for sparkline / bar charts. */
function computeFuelTrendBars(vehicleId, fuelLogs, maxPoints) {
  const limit = maxPoints == null ? 8 : maxPoints;
  const metrics = computeFuelLogMetrics(vehicleId, fuelLogs);
  return metrics.logs
    .filter((l) => l.calculatedEfficiency != null)
    .slice(-limit)
    .map((l) => ({
      id: l.id,
      date: l.date,
      kmPerLiter: l.calculatedEfficiency,
      distance: l.segmentDistance,
      costPerKm: l.costPerKm,
      fuelType: l.fuelType || 'oil',
    }));
}

/** Rank family vehicles by average km/L (null averages sink to bottom). */
function compareFamilyFuelEfficiency(vehicles, fuelLogs) {
  return (vehicles || [])
    .map((v) => {
      const metrics = computeFuelLogMetrics(v.id, fuelLogs);
      return {
        vehicleId: v.id,
        name: v.name,
        license: v.license,
        avgEfficiency: metrics.avgEfficiency,
        avgCostPerKm: metrics.avgCostPerKm,
        fillCount: metrics.logs.length,
        efficiencyCount: metrics.efficiencyCount,
        totalSpend: metrics.totalCostSum,
      };
    })
    .sort((a, b) => (b.avgEfficiency || -1) - (a.avgEfficiency || -1));
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

function coerceToLocalDate(value) {
  if (value instanceof Date) return value;
  if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}/.test(value)) {
    return parseIsoDate(value);
  }
  return new Date(value);
}

function toLocalIsoDate(date) {
  const d = date instanceof Date ? date : coerceToLocalDate(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function addMonthsToIsoDate(isoStr, months) {
  const d = parseIsoDate(isoStr);
  d.setMonth(d.getMonth() + months);
  return toLocalIsoDate(d);
}

function evaluateAlert(alert, vehicle, currentOdo, today) {
  if (alert.status !== 'Active' || !vehicle) {
    return null;
  }

  const targetDate = coerceToLocalDate(alert.targetDate);
  const todayDate = coerceToLocalDate(today);
  const isKmReached = currentOdo >= alert.targetKm;
  const isTimeReached = todayDate >= targetDate;

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
  const nowDate = coerceToLocalDate(now);
  nowDate.setHours(0, 0, 0, 0);
  const target = coerceToLocalDate(targetDate);

  const kmRemaining = targetKm - currentOdo;
  const daysRemaining = daysUntilDate(toLocalIsoDate(target), nowDate);

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
  const date =
    dateStr instanceof Date
      ? dateStr
      : typeof dateStr === 'string' && /^\d{4}-\d{2}-\d{2}/.test(dateStr)
        ? parseIsoDate(dateStr)
        : new Date(dateStr);
  if (isNaN(date.getTime())) {
    return '-';
  }
  return `${date.getDate()} ${THAI_MONTHS_SHORT[date.getMonth()]} ${date.getFullYear() + 543}`;
}

function isValidIsoDateParts(year, month, day) {
  if (month < 1 || month > 12 || day < 1) return false;
  return day <= new Date(year, month, 0).getDate();
}

function parseIsoDate(dateStr) {
  const parts = String(dateStr).split('-');
  if (parts.length !== 3) {
    return new Date(dateStr);
  }
  const year = Number(parts[0]);
  const month = Number(parts[1]);
  const day = Number(parts[2]);
  if (!isValidIsoDateParts(year, month, day)) {
    return new Date(NaN);
  }
  return new Date(year, month - 1, day);
}

/** Parse ISO date year without timezone drift (YYYY-MM-DD). */
function daysUntilDate(dateStr, now) {
  if (!dateStr) return null;
  const parts = String(dateStr).split('-');
  if (parts.length !== 3) return null;
  const target = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  const today = now instanceof Date ? new Date(now) : new Date(now);
  today.setHours(0, 0, 0, 0);
  const days = Math.ceil((target.getTime() - today.getTime()) / MS_PER_DAY);
  return days === 0 ? 0 : days;
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
  DISTANCE_ALERT_SENTINEL_KM,
  getLatestOdometer,
  getLatestOdometerAtDate,
  validateFuelOdometer,
  validateOdometerOnly,
  getFirstOdometer,
  computeMaintenanceCostPerKm,
  isDistanceBasedAlert,
  getDistanceAlertCountdown,
  calculateHealthPercent,
  calculateHealthPercentFromRange,
  getHealthBarTier,
  computeFuelLogMetrics,
  findPreviousSameTypeFullTank,
  computeFuelTrendBars,
  compareFamilyFuelEfficiency,
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
  coerceToLocalDate,
  toLocalIsoDate,
  addMonthsToIsoDate,
  getLogYear,
  getMaintenanceYearsForVehicle,
  pickDefaultReportYear,
  computeAnnualReportStats,
  daysUntilDate,
  isExpiryUrgent,
  getVehicleExpiryWarnings,
};
