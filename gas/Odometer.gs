// Odometer max logic mirrored in lib/car-logic.js getLatestOdometer (npm tests).
function getVehicleOdometers_() {
  preloadAllSheets_();
  var odometers = {};
  getAllRowsAsObjects_(SHEET_NAMES.MAINTENANCE).forEach(function (r) {
    var vid = String(r.vehicleId);
    var odo = num_(r['ไมล์']);
    odometers[vid] = Math.max(odometers[vid] || 0, odo);
  });
  getAllRowsAsObjects_(SHEET_NAMES.FUEL).forEach(function (r) {
    var vid = String(r.vehicleId);
    var odo = num_(r['ไมล์']);
    odometers[vid] = Math.max(odometers[vid] || 0, odo);
  });
  return odometers;
}

function getLatestOdometer_(vehicleId) {
  var odometers = getVehicleOdometers_();
  return odometers[String(vehicleId)] || 0;
}

function saveOdometerOnly(data) {
  try {
    var vehicleId = data.vehicleId;
    var odoVal = parseInt(data.odo, 10);
    var lastOdo = getLatestOdometer_(vehicleId);
    if (odoVal < lastOdo) {
      return { success: false, error: 'กิโลเมตรปัจจุบันน้อยกว่าครั้งล่าสุด!' };
    }

    var logId = data.id || generateId_('LOG');
    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', logId, {
      logId: logId,
      vehicleId: vehicleId,
      'วันที่': getBangkokToday_(),
      categoryId: '-',
      'ร้าน': '-',
      'ราคา': 0,
      'ไมล์': odoVal,
      type: 'Odometer_Update',
      alertKm: 0,
      alertMonth: 0,
      driveFileId: '',
      driveUrl: '',
      receiptName: ''
    });

    var alertResult = checkLineAlerts(false, true);
    return {
      success: true,
      state: alertResult.state || getAppState(vehicleId, { skipCache: true }),
      alertCheck: alertResult
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
