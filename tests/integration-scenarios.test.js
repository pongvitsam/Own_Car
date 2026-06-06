'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  getLatestOdometer,
  getLatestOdometerAtDate,
  validateFuelOdometer,
  validateOdometerOnly,
  computeMaintenanceCostPerKm,
  calculateHealthPercent,
  computeFuelLogMetrics,
  calculateFuelEfficiency,
  calculateCostPerKm,
  evaluateAlert,
  checkAlerts,
  checkAlertStatus,
  getVehicleStatusLevel,
  formatThaiDate,
  getLogYear,
  getMaintenanceYearsForVehicle,
  pickDefaultReportYear,
  computeAnnualReportStats,
  daysUntilDate,
  isExpiryUrgent,
  getVehicleExpiryWarnings,
  addMonthsToIsoDate,
  toLocalIsoDate,
  parseIsoDate,
  resolveAlertServiceLabel,
} = require('../lib/car-logic');

const V = 'V-INT';

function maintenanceEntry({ year, odo, cost, month = 6, day = 15, category = 'CAT-001' }) {
  const date = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  return {
    id: `LOG-${year}-${odo}`,
    vehicleId: V,
    odo,
    shop: 'Test Shop',
    category,
    cost,
    date,
    type: 'Maintenance',
  };
}

function fuelEntry({ year, odo, liters = 40, fullTank = true }) {
  return {
    id: `FUEL-${year}-${odo}`,
    vehicleId: V,
    date: `${year}-08-01`,
    odo,
    liters,
    totalCost: liters * 40,
    pricePerLiter: 40,
    fullTank,
  };
}

describe('integration: multi-decade vehicle lifecycle', () => {
  let maintenanceLogs;
  let fuelLogs;
  let alerts;
  const vehicle = { id: V, name: 'Lifecycle SUV', license: 'LC 2026' };

  it('year 2024 — initial purchase and first service', () => {
    maintenanceLogs = [maintenanceEntry({ year: 2024, odo: 10000, cost: 5000 })];
    fuelLogs = [fuelEntry({ year: 2024, odo: 10500 })];
    alerts = [];

    assert.equal(getLatestOdometer(V, maintenanceLogs, fuelLogs), 10500);
    assert.equal(computeMaintenanceCostPerKm(V, maintenanceLogs, 10500), 10);
    const { years } = getMaintenanceYearsForVehicle(maintenanceLogs, V);
    assert.deepEqual(years, [2024]);
  });

  it('year 2025 — alert set with 6-month offset', () => {
    maintenanceLogs.push(maintenanceEntry({ year: 2025, odo: 25000, cost: 8000 }));
    const repairDate = '2025-06-15';
    const targetDate = addMonthsToIsoDate(repairDate, 6);
    assert.equal(targetDate, '2025-12-15');

    alerts = [{
      vehicleId: V,
      targetKm: 35000,
      targetDate,
      status: 'Active',
      lastUpdated: repairDate,
      serviceLabel: 'เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว',
      categoryId: 'CAT-001',
    }];

    const health = calculateHealthPercent({
      vehicleId: V,
      latestOdo: 25000,
      alert: alerts[0],
      maintenanceLogs,
    });
    assert.equal(health.percent, 100);
    assert.equal(formatThaiDate(targetDate), '15 ธ.ค. 2568');
  });

  it('year 2026 — mixed logs, report year defaults, partial urgency', () => {
    maintenanceLogs.push(maintenanceEntry({ year: 2026, odo: 30000, cost: 3500 }));
    fuelLogs.push(fuelEntry({ year: 2026, odo: 32000, fullTank: true }));

    const now = parseIsoDate('2026-06-06');
    const { years, yearCounts } = getMaintenanceYearsForVehicle(maintenanceLogs, V);
    assert.deepEqual(years, [2026, 2025, 2024]);
    assert.equal(pickDefaultReportYear(years, yearCounts, 2026, null), 2026);

    const stats2026 = computeAnnualReportStats(maintenanceLogs, V, 2026);
    assert.equal(stats2026.count, 1);
    assert.equal(stats2026.total, 3500);

    const status = checkAlertStatus(30000, 35000, alerts[0].targetDate, now);
    assert.equal(status.kmRemaining, 5000);
    assert.equal(status.urgent, true);

    const health = calculateHealthPercent({
      vehicleId: V,
      latestOdo: 30000,
      alert: alerts[0],
      maintenanceLogs,
    });
    assert.ok(health.percent < 100);
    assert.equal(getVehicleStatusLevel(alerts[0], 30000, now), 'urgent');
  });

  it('year 2027 — alert triggers on km, fuel efficiency computed', () => {
    fuelLogs.push(fuelEntry({ year: 2027, odo: 36000, liters: 35, fullTank: true }));
    const now = parseIsoDate('2027-03-01');

    const result = evaluateAlert(alerts[0], vehicle, 36000, now);
    assert.ok(result);
    assert.equal(result.isKmReached, true);

    const scan = checkAlerts(alerts, [vehicle], () => 36000, now);
    assert.equal(scan.notificationTriggered, true);

    const fuel = calculateFuelEfficiency(fuelLogs, V);
    assert.ok(fuel.averageKmPerLiter > 0);
    assert.equal(calculateCostPerKm(maintenanceLogs, V, fuelLogs), computeMaintenanceCostPerKm(V, maintenanceLogs, 36000));
  });

  it('year 2100 — century boundary logs and report filter', () => {
    maintenanceLogs.push(maintenanceEntry({ year: 2100, odo: 150000, cost: 12000, month: 2, day: 28 }));
    assert.equal(getLogYear('2100-02-28'), 2100);
    assert.equal(formatThaiDate('2100-02-28'), '28 ก.พ. 2643');

    const stats = computeAnnualReportStats(maintenanceLogs, V, 2100);
    assert.equal(stats.count, 1);
    assert.equal(getLatestOdometerAtDate(V, '2100-02-28', maintenanceLogs), 150000);
  });

  it('year 2200 — far-future alert remains inactive in 2026', () => {
    const farAlert = {
      vehicleId: V,
      targetKm: 500000,
      targetDate: '2200-01-01',
      status: 'Active',
      lastUpdated: '2100-02-28',
    };
    const now = parseIsoDate('2026-06-06');
    assert.equal(evaluateAlert(farAlert, vehicle, 150000, now), null);
    assert.equal(getVehicleStatusLevel(farAlert, 150000, now), 'normal');
  });

  it('year 2300 — insurance expiry simulation', () => {
    const futureVehicle = {
      ...vehicle,
      prbExpiryDate: '2300-01-15',
      insuranceExpiryDate: '2300-06-30',
    };
    const nearExpiry = parseIsoDate('2300-06-10');
    assert.equal(isExpiryUrgent(futureVehicle.insuranceExpiryDate, 30, nearExpiry), true);
    const warnings = getVehicleExpiryWarnings(futureVehicle, nearExpiry);
    assert.equal(warnings.length, 2);
    assert.ok(warnings.some((w) => w.type === 'insurance'));
    assert.ok(warnings.some((w) => w.type === 'prb'));
    assert.equal(daysUntilDate('2300-06-30', nearExpiry), 20);
  });
});

describe('integration: validation and service labels across years', () => {
  it('odometer validation rejects rollback regardless of log year', () => {
    assert.equal(validateFuelOdometer(50000, 60000).valid, false);
    assert.equal(validateOdometerOnly(50000, 60000).valid, false);
    assert.equal(validateFuelOdometer(60000, 60000).valid, true);
  });

  it('resolveAlertServiceLabel resolves from log dated in 2326', () => {
    const categories = [{ id: 'CAT-FUTURE', name: 'ระบบไฟฟ้ารถยนต์' }];
    const logs = [{
      vehicleId: V,
      date: '2326-12-31',
      category: 'CAT-FUTURE',
      alertKm: 5000,
      alertMonth: 12,
    }];
    const label = resolveAlertServiceLabel(
      { vehicleId: V, lastUpdated: '2326-12-31' },
      categories,
      logs
    );
    assert.equal(label, 'ระบบไฟฟ้ารถยนต์');
  });

  it('simulate saveMaintenanceLog date chain: repair + alert months', () => {
    const repairDate = '2026-06-06';
    const alertMonths = 18;
    const targetDate = addMonthsToIsoDate(repairDate, alertMonths);
    assert.equal(targetDate, '2027-12-06');
    assert.equal(toLocalIsoDate(parseIsoDate(repairDate)), repairDate);
  });
});

describe('integration: chronological fuel segments over decades', () => {
  it('Fuelio metrics across sparse multi-year fill history', () => {
    const logs = [
      fuelEntry({ year: 2000, odo: 10000 }),
      fuelEntry({ year: 2010, odo: 20000 }),
      fuelEntry({ year: 2020, odo: 30000 }),
      fuelEntry({ year: 2030, odo: 40000 }),
    ];
    const metrics = computeFuelLogMetrics(V, logs);
    assert.equal(metrics.efficiencyCount, 3);
    assert.equal(metrics.avgEfficiency, 250);
    metrics.logs.slice(1).forEach((log) => {
      assert.equal(log.calculatedEfficiency, 250);
    });
  });
});
