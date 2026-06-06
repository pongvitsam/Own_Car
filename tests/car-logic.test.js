'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
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
} = require('../lib/car-logic');

const V1 = 'V001';
const maintenanceLogs = [
  { vehicleId: V1, odo: 10000, date: '2024-01-01', type: 'Maintenance', cost: 5000 },
  { vehicleId: V1, odo: 15000, date: '2024-06-01', type: 'Maintenance', cost: 3000 },
  { vehicleId: V1, odo: 12000, date: '2024-03-15', type: 'Odometer_Update', cost: 0 },
];

const fuelLogs = [
  {
    id: 'F1',
    vehicleId: V1,
    date: '2024-02-01',
    odo: 11000,
    liters: 40,
    totalCost: 1600,
    pricePerLiter: 40,
    fullTank: true,
  },
  {
    id: 'F2',
    vehicleId: V1,
    date: '2024-03-01',
    odo: 11500,
    liters: 20,
    totalCost: 800,
    pricePerLiter: 40,
    fullTank: false,
  },
  {
    id: 'F3',
    vehicleId: V1,
    date: '2024-04-01',
    odo: 12000,
    liters: 35,
    totalCost: 1400,
    pricePerLiter: 40,
    fullTank: true,
  },
  {
    id: 'F4',
    vehicleId: V1,
    date: '2024-05-01',
    odo: 13000,
    liters: 40,
    totalCost: 1680,
    pricePerLiter: 42,
    fullTank: true,
  },
];

describe('odometer', () => {
  it('getLatestOdometer returns max of maintenance and fuel readings', () => {
    assert.equal(getLatestOdometer(V1, maintenanceLogs, fuelLogs), 15000);
  });

  it('getLatestOdometer returns 0 when no logs exist', () => {
    assert.equal(getLatestOdometer('NONE', [], []), 0);
  });

  it('getLatestOdometerAtDate returns highest odo on or before date', () => {
    assert.equal(getLatestOdometerAtDate(V1, '2024-03-01', maintenanceLogs), 10000);
    assert.equal(getLatestOdometerAtDate(V1, '2024-03-15', maintenanceLogs), 12000);
    assert.equal(getLatestOdometerAtDate(V1, '2024-07-01', maintenanceLogs), 15000);
  });

  it('getLatestOdometerAtDate returns 0 when no logs before date', () => {
    assert.equal(getLatestOdometerAtDate(V1, '2023-01-01', maintenanceLogs), 0);
  });

  it('validateFuelOdometer rejects decreasing mileage', () => {
    const result = validateFuelOdometer(14000, 15000);
    assert.equal(result.valid, false);
    assert.match(result.error, /ระยะไมล์ปัจจุบันน้อยกว่าระยะล่าสุด/);
  });

  it('validateFuelOdometer accepts equal or higher mileage', () => {
    assert.deepEqual(validateFuelOdometer(15000, 15000), { valid: true });
    assert.deepEqual(validateFuelOdometer(16000, 15000), { valid: true });
  });

  it('validateOdometerOnly uses odometer-specific error message', () => {
    const result = validateOdometerOnly(14000, 15000);
    assert.equal(result.valid, false);
    assert.match(result.error, /กิโลเมตรปัจจุบันน้อยกว่าครั้งล่าสุด/);
  });
});

describe('health bar', () => {
  it('getFirstOdometer picks lowest positive maintenance odo', () => {
    assert.equal(getFirstOdometer(V1, maintenanceLogs), 10000);
  });

  it('calculateHealthPercent returns 100% when no active alert', () => {
    const result = calculateHealthPercent({
      vehicleId: V1,
      latestOdo: 15000,
      alert: null,
      maintenanceLogs,
    });
    assert.equal(result.percent, 100);
    assert.equal(result.tier, 'none');
  });

  it('calculateHealthPercent computes safety percentage from alert range', () => {
    const alert = {
      status: 'Active',
      targetKm: 20000,
      lastUpdated: null,
    };
    const result = calculateHealthPercent({
      vehicleId: V1,
      latestOdo: 15000,
      alert,
      maintenanceLogs,
    });
    // range = 20000 - 10000 = 10000, run = 15000 - 10000 = 5000 => 50%
    assert.equal(result.percent, 50);
    assert.equal(result.tier, 'healthy');
  });

  it('calculateHealthPercent uses lastUpdated odo as base when set', () => {
    const alert = {
      status: 'Active',
      targetKm: 20000,
      lastUpdated: '2024-03-01',
    };
    const result = calculateHealthPercent({
      vehicleId: V1,
      latestOdo: 15000,
      alert,
      maintenanceLogs,
    });
    // baseKm = 10000 (latest at 2024-03-01), range = 10000, run = 5000 => 50%
    assert.equal(result.percent, 50);
  });

  it('getHealthBarTier maps thresholds from Scripts.html', () => {
    assert.equal(getHealthBarTier(19), 'critical');
    assert.equal(getHealthBarTier(49), 'warning');
    assert.equal(getHealthBarTier(50), 'healthy');
  });
});

describe('Fuelio metrics', () => {
  it('computeFuelLogMetrics calculates efficiency between consecutive full tanks', () => {
    const metrics = computeFuelLogMetrics(V1, fuelLogs);
    const withEfficiency = metrics.logs.filter((l) => l.calculatedEfficiency != null);
    assert.equal(withEfficiency.length, 1);
    assert.equal(withEfficiency[0].id, 'F4');
    // F3 (full) -> F4 (full): distance 13000 - 12000 = 1000, liters 40 => 25 km/L
    assert.equal(withEfficiency[0].calculatedEfficiency, 25);
    assert.equal(withEfficiency[0].costPerKm, 1680 / 1000);
  });

  it('computeFuelLogMetrics skips non-full-tank pairs', () => {
    const metrics = computeFuelLogMetrics(V1, fuelLogs);
    const f2 = metrics.logs.find((l) => l.id === 'F2');
    const f3 = metrics.logs.find((l) => l.id === 'F3');
    assert.equal(f2.calculatedEfficiency, undefined);
    assert.equal(f3.calculatedEfficiency, undefined);
  });

  it('computeFuelLogMetrics aggregates summary totals', () => {
    const metrics = computeFuelLogMetrics(V1, fuelLogs);
    assert.equal(metrics.totalCostSum, 1600 + 800 + 1400 + 1680);
    assert.equal(metrics.totalLitersSum, 40 + 20 + 35 + 40);
    assert.equal(metrics.avgEfficiency, 25);
    assert.equal(metrics.lastPricePerLiter, 42);
    assert.equal(metrics.efficiencyCount, 1);
  });

  it('getEfficiencyTier classifies consumption bands', () => {
    assert.equal(getEfficiencyTier(16), 'good');
    assert.equal(getEfficiencyTier(12), 'medium');
    assert.equal(getEfficiencyTier(10), 'poor');
  });
});

describe('maintenance cost per km', () => {
  it('computeMaintenanceCostPerKm divides maintenance cost by distance', () => {
    const costPerKm = computeMaintenanceCostPerKm(V1, maintenanceLogs, 15000);
    // total cost 8000, distance 5000
    assert.equal(costPerKm, 1.6);
  });
});

describe('alerts', () => {
  const vehicle = { id: V1, name: 'Family SUV', license: '1กก 1234' };
  const today = new Date('2024-06-15');

  it('resolveAlertServiceLabel prefers serviceLabel then categoryId then log', () => {
    const categories = [
      { id: 'CAT-001', name: 'เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว' },
      { id: 'CAT-005', name: 'แก๊ส/LPG' },
    ];
    assert.equal(
      resolveAlertServiceLabel({ serviceLabel: 'ตรวจแก๊ส LPG' }, categories, []),
      'ตรวจแก๊ส LPG'
    );
    assert.equal(
      resolveAlertServiceLabel({ categoryId: 'CAT-005' }, categories, []),
      'แก๊ส/LPG'
    );
    const logs = [
      {
        vehicleId: V1,
        date: '2025-06-06',
        category: 'CAT-001',
        alertKm: 3000,
        alertMonth: 0,
      },
    ];
    assert.equal(
      resolveAlertServiceLabel({ vehicleId: V1, lastUpdated: '2025-06-06' }, categories, logs),
      'เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว'
    );
    assert.equal(resolveAlertServiceLabel(null, categories, logs), 'บำรุงรักษาตามกำหนด');
  });

  it('buildAlertReason covers km, time, and both triggers', () => {
    assert.equal(
      buildAlertReason(true, false, 20000, '2024-12-01'),
      'ระยะไมล์สะสมถึงกำหนด (20,000 กม.)'
    );
    assert.equal(
      buildAlertReason(false, true, 10000, '2024-06-01'),
      'ถึงกำหนดครบเวลาบำรุงรักษาแล้ว (2024-06-01)'
    );
    assert.equal(buildAlertReason(true, true, 20000, '2024-06-01'), 'ครบกำหนดทั้งระยะทางและเวลา');
  });

  it('evaluateAlert returns null when thresholds not met', () => {
    const alert = {
      alertId: 'A1',
      vehicleId: V1,
      targetKm: 30000,
      targetDate: '2025-01-01',
      status: 'Active',
    };
    assert.equal(evaluateAlert(alert, vehicle, 15000, today), null);
  });

  it('evaluateAlert triggers on km threshold', () => {
    const alert = {
      alertId: 'A1',
      vehicleId: V1,
      targetKm: 15000,
      targetDate: '2025-01-01',
      status: 'Active',
    };
    const result = evaluateAlert(alert, vehicle, 15000, today);
    assert.ok(result);
    assert.equal(result.isKmReached, true);
    assert.equal(result.isTimeReached, false);
    assert.match(result.message, /Family SUV/);
  });

  it('evaluateAlert triggers on date threshold', () => {
    const alert = {
      alertId: 'A1',
      vehicleId: V1,
      targetKm: 30000,
      targetDate: '2024-06-01',
      status: 'Active',
    };
    const result = evaluateAlert(alert, vehicle, 10000, today);
    assert.ok(result);
    assert.equal(result.isKmReached, false);
    assert.equal(result.isTimeReached, true);
  });

  it('checkAlerts scans all active alerts', () => {
    const alerts = [
      {
        alertId: 'A1',
        vehicleId: V1,
        targetKm: 15000,
        targetDate: '2025-01-01',
        status: 'Active',
      },
      {
        alertId: 'A2',
        vehicleId: 'V999',
        targetKm: 1000,
        targetDate: '2025-01-01',
        status: 'Active',
      },
    ];
    const vehicles = [vehicle];
    const result = checkAlerts(alerts, vehicles, () => 15000, today);
    assert.equal(result.notificationTriggered, true);
    assert.equal(result.triggered.length, 1);
    assert.equal(result.messages.length, 1);
  });

  it('buildLineAlertMessage formats LINE notify body', () => {
    const msg = buildLineAlertMessage(vehicle, 'ครบกำหนดทั้งระยะทางและเวลา', '2024-06-15 08:00');
    assert.match(msg, /MyHome CarCare/);
    assert.match(msg, /Family SUV \(1กก 1234\)/);
    assert.match(msg, /ครบกำหนดทั้งระยะทางและเวลา/);
  });

  it('getVehicleStatusLevel flags urgent when km or days threshold hit', () => {
    const alert = {
      status: 'Active',
      targetKm: 16000,
      targetDate: '2024-07-01',
    };
    assert.equal(getVehicleStatusLevel(alert, 15000, today), 'urgent');

    const farAlert = {
      status: 'Active',
      targetKm: 30000,
      targetDate: '2024-07-01',
    };
    assert.equal(getVehicleStatusLevel(farAlert, 15000, today), 'normal');
    assert.equal(getVehicleStatusLevel(null, 15000, today), 'none');
  });
});

describe('public API wrappers', () => {
  it('calculateFuelEfficiency exposes Fuelio km/L for two full tanks', () => {
    const result = calculateFuelEfficiency(
      [
        { id: 'A', vehicleId: V1, date: '2024-01-01', odo: 10000, liters: 40, totalCost: 1600, fullTank: true },
        { id: 'B', vehicleId: V1, date: '2024-02-01', odo: 11000, liters: 20, totalCost: 800, fullTank: true },
      ],
      V1
    );
    assert.equal(result.efficiencyCount, 1);
    assert.equal(result.averageKmPerLiter, 50);
  });

  it('calculateHealthPercentFromRange starts at 100% and decreases toward target', () => {
    assert.equal(calculateHealthPercentFromRange(10000, 10000, 20000), 100);
    assert.equal(calculateHealthPercentFromRange(15000, 10000, 20000), 50);
    assert.equal(calculateHealthPercentFromRange(20000, 10000, 20000), 0);
  });

  it('checkAlertStatus triggers urgent at km <= 1000 or days <= 15', () => {
    const now = parseIsoDate('2026-06-01');
    assert.equal(checkAlertStatus(49000, 50000, parseIsoDate('2026-12-01'), now).urgent, true);
    assert.equal(checkAlertStatus(10000, 50000, parseIsoDate('2026-06-10'), now).urgent, true);
    assert.equal(checkAlertStatus(10000, 50000, parseIsoDate('2026-12-31'), now).urgent, false);
  });

  it('calculateCostPerKm uses latest odometer from maintenance and fuel logs', () => {
    assert.equal(calculateCostPerKm(maintenanceLogs, V1, fuelLogs), 1.6);
  });

  it('formatThaiDate renders Buddhist era date', () => {
    assert.equal(formatThaiDate('2026-01-15'), '15 ม.ค. 2569');
    assert.equal(formatThaiDate('invalid'), '-');
  });
});

describe('vehicle expiry dates', () => {
  const { execSync } = require('node:child_process');
  const seedVehicles = JSON.parse(
    execSync('python -c "import json; from tools.seed_data import VEHICLES; print(json.dumps(VEHICLES))"', {
      cwd: require('path').join(__dirname, '..'),
      encoding: 'utf8',
    })
  );
  const today = new Date('2026-06-06');

  it('seed vehicles include PRB/insurance expiry from spreadsheet', () => {
    const mazda = seedVehicles.find((v) => v.id === 'V-001');
    const click = seedVehicles.find((v) => v.id === 'V-002');
    const altis = seedVehicles.find((v) => v.id === 'V-003');
    assert.equal(mazda.insuranceExpiryDate, '2026-08-25');
    assert.equal(mazda.prbExpiryDate, '2026-09-04');
    assert.equal(click.prbExpiryDate, '2026-10-04');
    assert.equal(altis.insuranceExpiryDate, '2026-11-22');
  });

  it('isExpiryUrgent flags dates within 30 days', () => {
    assert.equal(isExpiryUrgent('2026-06-20', 30, today), true);
    assert.equal(isExpiryUrgent('2026-08-25', 30, today), false);
    assert.equal(isExpiryUrgent(null, 30, today), false);
  });

  it('getVehicleExpiryWarnings lists urgent PRB/insurance for Mazda in June 2026', () => {
    const mazda = seedVehicles.find((v) => v.id === 'V-001');
    const warnings = getVehicleExpiryWarnings(mazda, today);
    assert.equal(warnings.length, 0);
  });

  it('getVehicleExpiryWarnings flags Mazda insurance near August 2026', () => {
    const mazda = seedVehicles.find((v) => v.id === 'V-001');
    const near = new Date('2026-08-01');
    const warnings = getVehicleExpiryWarnings(mazda, near);
    assert.ok(warnings.some((w) => w.type === 'insurance'));
  });
});

describe('annual report stats', () => {
  const { execSync } = require('node:child_process');
  const seedJson = execSync('python -c "import json; from tools.seed_data import build_maintenance_logs; print(json.dumps(build_maintenance_logs()))"', {
    cwd: require('path').join(__dirname, '..'),
    encoding: 'utf8',
  });
  const seedLogs = JSON.parse(seedJson);

  it('getLogYear parses ISO year without timezone issues', () => {
    assert.equal(getLogYear('2025-11-24'), 2025);
    assert.equal(getLogYear('2024-07-30'), 2024);
    assert.equal(getLogYear('invalid'), null);
  });

  it('Mazda defaults to 2025 (most recent year with data in 2026)', () => {
    const { years, yearCounts } = getMaintenanceYearsForVehicle(seedLogs, 'V-001');
    assert.deepEqual(years, [2025, 2024]);
    assert.equal(pickDefaultReportYear(years, yearCounts, 2026, null), 2025);
  });

  it('Mazda 2025 totals match seed data', () => {
    const stats = computeAnnualReportStats(seedLogs, 'V-001', 2025);
    assert.equal(stats.count, 8);
    assert.equal(Math.round(stats.total * 100) / 100, 38978.61);
  });

  it('Mazda 2024 totals match seed data', () => {
    const stats = computeAnnualReportStats(seedLogs, 'V-001', 2024);
    assert.equal(stats.count, 4);
    assert.equal(stats.total, 43320);
  });

  it('Click 2026 totals match seed data', () => {
    const stats = computeAnnualReportStats(seedLogs, 'V-002', 2026);
    assert.equal(stats.count, 5);
    assert.equal(stats.total, 3301);
  });

  it('Altis 2025 totals match seed data', () => {
    const stats = computeAnnualReportStats(seedLogs, 'V-003', 2025);
    assert.equal(stats.count, 65);
    assert.equal(Math.round(stats.total * 100) / 100, 119158.08);
  });

  it('Altis 2026 has one maintenance log', () => {
    const stats = computeAnnualReportStats(seedLogs, 'V-003', 2026);
    assert.equal(stats.count, 1);
    assert.equal(stats.total, 1839);
  });

  it('pickDefaultReportYear resets when previous year is from another vehicle', () => {
    const click = getMaintenanceYearsForVehicle(seedLogs, 'V-002');
    assert.equal(pickDefaultReportYear(click.years, click.yearCounts, 2026, null), 2026);
    assert.equal(pickDefaultReportYear(click.years, click.yearCounts, 2026, '2025'), 2025);

    const mazda2025 = computeAnnualReportStats(seedLogs, 'V-001', 2025);
    const altis2025 = computeAnnualReportStats(seedLogs, 'V-003', 2025);
    assert.notEqual(Math.round(mazda2025.total), Math.round(altis2025.total));
    assert.equal(mazda2025.count, 8);
    assert.equal(altis2025.count, 65);
  });

  it('Click and Mazda 2025 totals differ per vehicle', () => {
    const mazda = computeAnnualReportStats(seedLogs, 'V-001', 2025);
    const click = computeAnnualReportStats(seedLogs, 'V-002', 2025);
    assert.equal(mazda.count, 8);
    assert.equal(click.count, 2);
    assert.notEqual(Math.round(mazda.total), Math.round(click.total));
  });
});
