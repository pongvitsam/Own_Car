// Fuelio consumption formulas: mirrored in lib/car-logic.js (npm test source of truth).
function getFuelLogs_() {
  return getAllRowsAsObjects_(SHEET_NAMES.FUEL).map(function (r) {
    return {
      id: String(r.logId),
      vehicleId: String(r.vehicleId),
      date: formatDateCell_(r['วันที่']),
      fuelType: String(r.fuelType || 'oil'),
      odo: num_(r['ไมล์']),
      liters: num_(r['ลิตร']),
      pricePerLiter: num_(r['ราคา/ลิตร']),
      totalCost: num_(r['ราคารวม']),
      fullTank: bool_(r['เต็มถัง']),
      station: String(r['สถานี'] || '')
    };
  });
}

function getFuelLogsForVehicle_(vehicleId) {
  return getFuelLogs_().filter(function (l) {
    return l.vehicleId === String(vehicleId);
  });
}

function saveFuelLog(data) {
  try {
    var vehicleId = data.vehicleId;
    var odo = parseInt(data.odo, 10);
    var lastOdo = getLatestOdometer_(vehicleId);
    if (odo < lastOdo) {
      return { success: false, error: 'ระยะไมล์ปัจจุบันน้อยกว่าระยะล่าสุดของรถ!' };
    }

    var logId = data.id || generateId_('FUEL');
    upsertRow_(SHEET_NAMES.FUEL, 'logId', logId, {
      logId: logId,
      vehicleId: vehicleId,
      'วันที่': data.date || getBangkokToday_(),
      fuelType: data.fuelType || 'oil',
      'ไมล์': odo,
      'ลิตร': num_(data.liters),
      'ราคา/ลิตร': num_(data.pricePerLiter),
      'ราคารวม': num_(data.totalCost),
      'เต็มถัง': data.fullTank ? 'TRUE' : 'FALSE',
      'สถานี': data.station || ''
    });

    return { success: true, state: getAppState(vehicleId, { includeFuel: true, skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function deleteFuelLog(logId) {
  try {
    var rows = getAllRowsAsObjects_(SHEET_NAMES.FUEL);
    var existing = rows.find(function (r) { return String(r.logId) === String(logId); });
    if (!existing) {
      return { success: false, error: 'ไม่พบรายการ' };
    }
    deleteRowById_(SHEET_NAMES.FUEL, 'logId', logId);
    return { success: true, state: getAppState(String(existing.vehicleId), { includeFuel: true, skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
