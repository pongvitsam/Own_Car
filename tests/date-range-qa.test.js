'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const {
  parseIsoDate,
  daysUntilDate,
  formatThaiDate,
  getLogYear,
  getLatestOdometerAtDate,
  evaluateAlert,
  checkAlertStatus,
  isExpiryUrgent,
  computeFuelLogMetrics,
  getMaintenanceYearsForVehicle,
  computeAnnualReportStats,
  pickDefaultReportYear,
  getVehicleExpiryWarnings,
  calculateHealthPercent,
  getFirstOdometer,
} = require('../lib/car-logic');

const START_YEAR = 1726;
const END_YEAR = 2026;
const SPAN = END_YEAR - START_YEAR + 1;

function isoDate(y, m, d) {
  return `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

function localMidnight(y, m, d) {
  return new Date(y, m - 1, d);
}

describe(`300-year date range QA (${START_YEAR}–${END_YEAR})`, () => {
  it(`parseIsoDate round-trips ${SPAN} calendar days without drift`, () => {
    for (let y = START_YEAR; y <= END_YEAR; y++) {
      for (let m = 1; m <= 12; m++) {
        const daysInMonth = new Date(y, m, 0).getDate();
        for (let d = 1; d <= daysInMonth; d++) {
          const str = isoDate(y, m, d);
          const parsed = parseIsoDate(str);
          assert.equal(parsed.getFullYear(), y, `year drift: ${str}`);
          assert.equal(parsed.getMonth(), m - 1, `month drift: ${str}`);
          assert.equal(parsed.getDate(), d, `day drift: ${str}`);
        }
      }
    }
  });

  it('daysUntilDate is symmetric: forward N days then back yields 0', () => {
    for (let y = START_YEAR; y <= END_YEAR; y += 17) {
      for (let m = 1; m <= 12; m += 3) {
        const d = Math.min(15, new Date(y, m, 0).getDate());
        const base = isoDate(y, m, d);
        const now = localMidnight(y, m, d);
        for (const offset of [0, 1, 7, 30, 365, 1000]) {
          const targetDate = new Date(now);
          targetDate.setDate(targetDate.getDate() + offset);
          const targetStr = isoDate(
            targetDate.getFullYear(),
            targetDate.getMonth() + 1,
            targetDate.getDate()
          );
          assert.equal(daysUntilDate(targetStr, now), offset, `${base} +${offset}`);
          const backward = daysUntilDate(base, targetDate);
          assert.equal(backward, offset === 0 ? 0 : -offset, `${targetStr} -${offset}`);
        }
      }
    }
  });

  it('formatThaiDate Buddhist era matches parseIsoDate calendar fields', () => {
    for (let y = START_YEAR; y <= END_YEAR; y += 11) {
      for (let m = 1; m <= 12; m++) {
        const d = Math.min(28, new Date(y, m, 0).getDate());
        const str = isoDate(y, m, d);
        const formatted = formatThaiDate(str);
        assert.match(formatted, new RegExp(`^${d} `), `${str} => ${formatted}`);
        assert.match(formatted, new RegExp(`${y + 543}$`), `${str} => ${formatted}`);
      }
    }
  });

  it('getLogYear extracts year from ISO strings across range', () => {
    for (let y = START_YEAR; y <= END_YEAR; y++) {
      assert.equal(getLogYear(isoDate(y, 6, 15)), y);
      assert.equal(getLogYear(`${y}`), y);
    }
  });

  it('getLatestOdometerAtDate respects ISO lexicographic order over 300 years', () => {
    const logs = [];
    for (let y = START_YEAR; y <= END_YEAR; y += 50) {
      logs.push({ vehicleId: 'V1', odo: y - START_YEAR + 1000, date: isoDate(y, 6, 1) });
    }
    for (let y = START_YEAR; y <= END_YEAR; y += 50) {
      const expected = y - START_YEAR + 1000;
      assert.equal(getLatestOdometerAtDate('V1', isoDate(y, 12, 31), logs), expected, y);
    }
  });

  it('evaluateAlert time trigger is consistent with parseIsoDate at local midnight', () => {
    const vehicle = { id: 'V1', name: 'Test', license: 'X' };
    for (let y = START_YEAR; y <= END_YEAR; y += 13) {
      const targetStr = isoDate(y, 3, 15);
      const alert = {
        alertId: 'A1',
        vehicleId: 'V1',
        targetKm: 999999,
        targetDate: targetStr,
        status: 'Active',
      };
      const before = evaluateAlert(alert, vehicle, 0, localMidnight(y, 3, 14));
      const onDay = evaluateAlert(alert, vehicle, 0, localMidnight(y, 3, 15));
      const after = evaluateAlert(alert, vehicle, 0, localMidnight(y, 3, 16));
      assert.equal(before, null, `should not trigger before ${targetStr}`);
      assert.ok(onDay, `should trigger on ${targetStr}`);
      assert.equal(onDay.isTimeReached, true);
      assert.ok(after, `should trigger after ${targetStr}`);
    }
  });

  it('checkAlertStatus daysRemaining matches daysUntilDate for ISO targets', () => {
    for (let y = START_YEAR; y <= END_YEAR; y += 19) {
      const now = localMidnight(y, 7, 1);
      const targetStr = isoDate(y, 8, 1);
      const status = checkAlertStatus(0, 50000, targetStr, now);
      assert.equal(status.daysRemaining, daysUntilDate(targetStr, now));
    }
  });

  it('isExpiryUrgent boundary: exactly threshold days is urgent', () => {
    for (let y = START_YEAR; y <= END_YEAR; y += 23) {
      const now = localMidnight(y, 5, 1);
      const withinStr = isoDate(y, 5, 31);
      assert.equal(isExpiryUrgent(withinStr, 30, now), true, withinStr);
      const outsideStr = isoDate(y, 6, 1);
      assert.equal(isExpiryUrgent(outsideStr, 30, now), false, outsideStr);
    }
  });

  it('computeFuelLogMetrics preserves chronological order across centuries', () => {
    for (let y = START_YEAR; y <= END_YEAR; y += 37) {
      const logs = [
        { id: 'A', vehicleId: 'V1', date: isoDate(y, 1, 1), odo: 1000, liters: 40, totalCost: 1600, fullTank: true },
        { id: 'B', vehicleId: 'V1', date: isoDate(y, 2, 1), odo: 2000, liters: 40, totalCost: 1600, fullTank: true },
      ];
      const metrics = computeFuelLogMetrics('V1', logs.slice().reverse());
      assert.equal(metrics.logs[0].id, 'A');
      assert.equal(metrics.logs[1].id, 'B');
      assert.equal(metrics.logs[1].calculatedEfficiency, 25);
    }
  });

  it('annual report stats aggregate correctly per year in range', () => {
    const logs = [];
    for (let y = START_YEAR; y <= END_YEAR; y += 100) {
      logs.push({
        vehicleId: 'V1',
        type: 'Maintenance',
        date: isoDate(y, 4, 10),
        cost: y,
        odo: 1000,
      });
    }
    const { years, yearCounts } = getMaintenanceYearsForVehicle(logs, 'V1');
    assert.equal(years.length, logs.length);
    for (const entry of logs) {
      const y = getLogYear(entry.date);
      const stats = computeAnnualReportStats(logs, 'V1', y);
      assert.equal(stats.count, 1);
      assert.equal(stats.total, y);
    }
    assert.equal(pickDefaultReportYear(years, yearCounts, END_YEAR, null), END_YEAR);
  });

  it('calculateHealthPercent lastUpdated lookup works across date range', () => {
    const logs = [
      { vehicleId: 'V1', odo: 5000, date: isoDate(1900, 1, 1), type: 'Maintenance', cost: 0 },
      { vehicleId: 'V1', odo: 8000, date: isoDate(1950, 6, 1), type: 'Maintenance', cost: 0 },
    ];
    const alert = { status: 'Active', targetKm: 10000, lastUpdated: isoDate(1950, 6, 1) };
    const result = calculateHealthPercent({
      vehicleId: 'V1',
      latestOdo: 9000,
      alert,
      maintenanceLogs: logs,
    });
    assert.equal(result.percent, 50);
  });

  it('leap-day Feb 29 handled in parseIsoDate and daysUntilDate', () => {
    const leapYears = [];
    for (let y = START_YEAR; y <= END_YEAR; y++) {
      if ((y % 4 === 0 && y % 100 !== 0) || y % 400 === 0) leapYears.push(y);
    }
    assert.ok(leapYears.length > 0);
    for (const y of leapYears) {
      const feb29 = isoDate(y, 2, 29);
      const parsed = parseIsoDate(feb29);
      assert.equal(parsed.getMonth(), 1);
      assert.equal(parsed.getDate(), 29);
      assert.equal(daysUntilDate(isoDate(y, 3, 1), localMidnight(y, 2, 29)), 1);
      assert.equal(formatThaiDate(feb29), `29 ก.พ. ${y + 543}`);
    }
  });

  it('getVehicleExpiryWarnings returns sorted warnings with correct day counts', () => {
    const vehicle = {
      prbExpiryDate: isoDate(2000, 6, 10),
      insuranceExpiryDate: isoDate(2000, 6, 15),
    };
    const now = localMidnight(2000, 5, 20);
    const warnings = getVehicleExpiryWarnings(vehicle, now, 30);
    assert.equal(warnings.length, 2);
    assert.equal(warnings[0].days, daysUntilDate(vehicle.prbExpiryDate, now));
    assert.equal(warnings[1].days, daysUntilDate(vehicle.insuranceExpiryDate, now));
  });
});
