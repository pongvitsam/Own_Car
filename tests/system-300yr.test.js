'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  formatThaiDate,
  parseIsoDate,
  toLocalIsoDate,
  addMonthsToIsoDate,
  coerceToLocalDate,
  getLogYear,
  getMaintenanceYearsForVehicle,
  pickDefaultReportYear,
  computeAnnualReportStats,
  checkAlertStatus,
  evaluateAlert,
  checkAlerts,
  getVehicleStatusLevel,
  daysUntilDate,
  isExpiryUrgent,
  getVehicleExpiryWarnings,
  calculateHealthPercent,
  calculateHealthPercentFromRange,
  computeFuelLogMetrics,
  calculateFuelEfficiency,
  THAI_MONTHS_SHORT,
} = require('../lib/car-logic');

const SAMPLE_CE_YEARS = [1726, 1900, 2000, 2024, 2026, 2100, 2200, 2300, 2326];
const V = 'V-STRESS';

function iso(year, month, day) {
  return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

describe('300-year formatThaiDate (CE 1726–2326 / BE 2269–2869)', () => {
  for (const ceYear of SAMPLE_CE_YEARS) {
    it(`formats ${ceYear}-06-06 as 6 มิ.ย. ${ceYear + 543}`, () => {
      assert.equal(formatThaiDate(iso(ceYear, 6, 6)), `6 มิ.ย. ${ceYear + 543}`);
    });
  }

  it('uses local calendar day for ISO strings (no UTC drift)', () => {
    assert.equal(formatThaiDate('2026-01-15'), '15 ม.ค. 2569');
    assert.equal(formatThaiDate('2300-12-31'), '31 ธ.ค. 2843');
  });

  it('handles month boundaries across centuries', () => {
    assert.equal(formatThaiDate(iso(2000, 1, 1)), `1 ${THAI_MONTHS_SHORT[0]} 2543`);
    assert.equal(formatThaiDate(iso(2000, 12, 31)), `31 ${THAI_MONTHS_SHORT[11]} 2543`);
    assert.equal(formatThaiDate(iso(2100, 3, 1)), `1 ${THAI_MONTHS_SHORT[2]} 2643`);
  });

  it('handles leap-day 2000-02-29', () => {
    assert.equal(formatThaiDate('2000-02-29'), '29 ก.พ. 2543');
  });

  it('returns dash for invalid dates', () => {
    assert.equal(formatThaiDate('invalid'), '-');
    assert.equal(formatThaiDate(''), '-');
    assert.equal(formatThaiDate('2300-13-40'), '-');
  });

  it('accepts Date instances', () => {
    const d = parseIsoDate('2026-06-06');
    assert.equal(formatThaiDate(d), '6 มิ.ย. 2569');
  });
});

describe('300-year getLogYear and report filtering', () => {
  const logs = SAMPLE_CE_YEARS.flatMap((year, idx) => [
    {
      vehicleId: V,
      type: 'Maintenance',
      date: iso(year, 3, 15),
      cost: 100 + idx,
      odo: 1000 + idx,
    },
  ]);

  for (const year of SAMPLE_CE_YEARS) {
    it(`getLogYear extracts ${year} from ISO date`, () => {
      assert.equal(getLogYear(iso(year, 7, 1)), year);
    });
  }

  it('getMaintenanceYearsForVehicle lists all sample centuries', () => {
    const { years } = getMaintenanceYearsForVehicle(logs, V);
    for (const year of SAMPLE_CE_YEARS) {
      assert.ok(years.includes(year), `missing year ${year}`);
    }
  });

  it('computeAnnualReportStats filters per year across 300-year span', () => {
    for (let i = 0; i < SAMPLE_CE_YEARS.length; i++) {
      const year = SAMPLE_CE_YEARS[i];
      const stats = computeAnnualReportStats(logs, V, year);
      assert.equal(stats.count, 1);
      assert.equal(stats.total, 100 + i);
    }
  });

  it('pickDefaultReportYear prefers current year when data exists', () => {
    const { years, yearCounts } = getMaintenanceYearsForVehicle(logs, V);
    assert.equal(pickDefaultReportYear(years, yearCounts, 2026, null), 2026);
  });

  it('BE display year equals CE + 543 for report labels', () => {
    const be2026 = 2026 + 543;
    const be2326 = 2326 + 543;
    assert.equal(be2026, 2569);
    assert.equal(be2326, 2869);
    const stats = computeAnnualReportStats(logs, V, 2026);
    assert.equal(stats.yearLogs[0].date, iso(2026, 3, 15));
  });
});

describe('300-year alert status (km + date)', () => {
  const vehicle = { id: V, name: 'Stress Test Car', license: 'ST 9999' };
  const now2026 = parseIsoDate('2026-06-06');

  it('does not trigger time alert when target is year 2300 and today is 2026', () => {
    const alert = {
      alertId: 'A-FAR',
      vehicleId: V,
      targetKm: 999999,
      targetDate: '2300-01-01',
      status: 'Active',
    };
    const result = evaluateAlert(alert, vehicle, 50000, now2026);
    assert.equal(result, null);

    const status = checkAlertStatus(50000, 999999, '2300-01-01', now2026);
    assert.equal(status.timeReached, false);
    assert.equal(status.kmReached, false);
    assert.equal(status.shouldNotify, false);
    assert.ok(status.daysRemaining > 90000);
  });

  it('triggers time alert for far-past targetDate (1726)', () => {
    const alert = {
      alertId: 'A-PAST',
      vehicleId: V,
      targetKm: 999999,
      targetDate: '1726-01-01',
      status: 'Active',
    };
    const result = evaluateAlert(alert, vehicle, 1000, now2026);
    assert.ok(result);
    assert.equal(result.isTimeReached, true);
    assert.equal(result.isKmReached, false);
  });

  it('km threshold is date-independent at year 2326', () => {
    const farFuture = parseIsoDate('2326-12-31');
    const status = checkAlertStatus(50000, 50000, '2326-01-01', farFuture);
    assert.equal(status.kmReached, true);
    assert.equal(status.shouldNotify, true);
  });

  it('urgent window uses days not centuries', () => {
    const status = checkAlertStatus(10000, 50000, '2026-06-20', now2026);
    assert.equal(status.urgent, true);
    assert.equal(status.daysRemaining, 14);
  });

  it('getVehicleStatusLevel normal for far-future maintenance date', () => {
    const alert = { status: 'Active', targetKm: 200000, targetDate: '2300-06-01' };
    assert.equal(getVehicleStatusLevel(alert, 50000, now2026), 'normal');
  });

  it('checkAlerts scans mixed near and far alerts', () => {
    const alerts = [
      { alertId: '1', vehicleId: V, targetKm: 999999, targetDate: '2300-01-01', status: 'Active' },
      { alertId: '2', vehicleId: V, targetKm: 10000, targetDate: '2300-01-01', status: 'Active' },
    ];
    const result = checkAlerts(alerts, [vehicle], () => 15000, now2026);
    assert.equal(result.triggered.length, 1);
    assert.equal(result.triggered[0].isKmReached, true);
  });
});

describe('300-year Thai calendar helpers (BE ↔ CE +543)', () => {
  it('toLocalIsoDate round-trips parseIsoDate across sample years', () => {
    for (const year of SAMPLE_CE_YEARS) {
      const isoStr = iso(year, 6, 6);
      assert.equal(toLocalIsoDate(parseIsoDate(isoStr)), isoStr);
    }
  });

  it('addMonthsToIsoDate advances across year boundaries', () => {
    assert.equal(addMonthsToIsoDate('2026-11-15', 2), '2027-01-15');
    assert.equal(addMonthsToIsoDate('2299-12-01', 1), '2300-01-01');
  });

  it('daysUntilDate spans centuries correctly', () => {
    const days = daysUntilDate('2300-01-01', parseIsoDate('2026-06-06'));
    assert.ok(days > 99000);
    assert.equal(daysUntilDate('2026-06-06', parseIsoDate('2026-06-06')), 0);
    assert.equal(daysUntilDate('2026-06-07', parseIsoDate('2026-06-06')), 1);
  });

  it('coerceToLocalDate handles ISO strings and Date objects', () => {
    assert.equal(coerceToLocalDate('2100-03-01').getFullYear(), 2100);
    assert.equal(coerceToLocalDate(parseIsoDate('2100-03-01')).getMonth(), 2);
  });
});

describe('300-year insurance/PRB expiry warnings', () => {
  const vehicle = {
    id: V,
    prbExpiryDate: '2300-06-01',
    insuranceExpiryDate: '1726-12-31',
  };

  it('flags past insurance expiry in 2026', () => {
    const warnings = getVehicleExpiryWarnings(vehicle, parseIsoDate('2026-06-06'));
    assert.ok(warnings.some((w) => w.type === 'insurance'));
    assert.ok(!warnings.some((w) => w.type === 'prb'));
  });

  it('flags far-future PRB within 30 days of 2300', () => {
    const near = parseIsoDate('2300-05-15');
    assert.equal(isExpiryUrgent('2300-06-01', 30, near), true);
    const warnings = getVehicleExpiryWarnings(vehicle, near);
    assert.ok(warnings.some((w) => w.type === 'prb'));
  });
});

describe('300-year fuel efficiency (date-independent math)', () => {
  const fuelLogs = [
    { id: 'A', vehicleId: V, date: '1900-01-01', odo: 1000, liters: 40, totalCost: 1600, fullTank: true },
    { id: 'B', vehicleId: V, date: '2300-12-31', odo: 2000, liters: 20, totalCost: 800, fullTank: true },
  ];

  it('computes km/L regardless of 400-year gap between fills', () => {
    const metrics = computeFuelLogMetrics(V, fuelLogs);
    const eff = metrics.logs.find((l) => l.id === 'B');
    assert.equal(eff.calculatedEfficiency, 50);
    assert.equal(metrics.avgEfficiency, 50);
  });

  it('calculateFuelEfficiency average unchanged by extreme dates', () => {
    const result = calculateFuelEfficiency(fuelLogs, V);
    assert.equal(result.averageKmPerLiter, 50);
    assert.equal(result.efficiencyCount, 1);
  });
});

describe('300-year health percent (odo-only, dates inert)', () => {
  it('calculateHealthPercentFromRange stable across any calendar year context', () => {
    for (const year of [1726, 2026, 2326]) {
      assert.equal(calculateHealthPercentFromRange(15000, 10000, 20000), 50, `year ${year}`);
    }
  });

  it('calculateHealthPercent uses lastUpdated from distant past/future logs', () => {
    const logs = [
      { vehicleId: V, odo: 5000, date: '1726-01-01', type: 'Maintenance', cost: 100 },
      { vehicleId: V, odo: 10000, date: '2026-01-01', type: 'Maintenance', cost: 100 },
      { vehicleId: V, odo: 12000, date: '2300-01-01', type: 'Odometer_Update', cost: 0 },
    ];
    const alert = { status: 'Active', targetKm: 20000, lastUpdated: '2026-01-01' };
    const result = calculateHealthPercent({
      vehicleId: V,
      latestOdo: 15000,
      alert,
      maintenanceLogs: logs,
    });
    assert.equal(result.percent, 50);
  });
});
