function getVehicles_() {
  return getAllRowsAsObjects_(SHEET_NAMES.VEHICLES).map(function (r) {
    return {
      id: String(r.vehicleId),
      name: String(r['ชื่อ'] || ''),
      license: String(r['ทะเบียน'] || ''),
      createdDate: formatDateCell_(r['สร้างเมื่อ'])
    };
  });
}

function addVehicle(data) {
  try {
    var id = data.id || generateId_('V');
    upsertRow_(SHEET_NAMES.VEHICLES, 'vehicleId', id, {
      vehicleId: id,
      'ชื่อ': data.name,
      'ทะเบียน': data.license,
      'สร้างเมื่อ': data.createdDate || getBangkokToday_()
    });

    // Seed initial odometer log
    var logId = generateId_('LOG');
    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', logId, {
      logId: logId,
      vehicleId: id,
      'วันที่': getBangkokToday_(),
      categoryId: '-',
      'ร้าน': '-',
      'ราคา': 0,
      'ไมล์': 0,
      type: 'Odometer_Update',
      alertKm: 0,
      alertMonth: 0,
      driveFileId: '',
      driveUrl: '',
      receiptName: ''
    });

    return { success: true, state: getAppState(id, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function deleteVehicle(vehicleId) {
  try {
    var vehicles = getVehicles_();
    if (vehicles.length <= 1) {
      return { success: false, error: 'ไม่สามารถลบรถคันสุดท้ายในระบบได้' };
    }
    deleteRowById_(SHEET_NAMES.VEHICLES, 'vehicleId', vehicleId);

    getAllRowsAsObjects_(SHEET_NAMES.MAINTENANCE).forEach(function (r) {
      if (String(r.vehicleId) === String(vehicleId)) {
        deleteRowById_(SHEET_NAMES.MAINTENANCE, 'logId', r.logId);
      }
    });
    getAllRowsAsObjects_(SHEET_NAMES.FUEL).forEach(function (r) {
      if (String(r.vehicleId) === String(vehicleId)) {
        deleteRowById_(SHEET_NAMES.FUEL, 'logId', r.logId);
      }
    });
    getAllRowsAsObjects_(SHEET_NAMES.ALERTS).forEach(function (r) {
      if (String(r.vehicleId) === String(vehicleId)) {
        deleteRowById_(SHEET_NAMES.ALERTS, 'alertId', r.alertId);
      }
    });

    var remaining = getVehicles_();
    var selectedId = remaining.length ? remaining[0].id : '';
    return { success: true, state: getAppState(selectedId, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function formatDateCell_(val) {
  if (!val) return '';
  if (val instanceof Date) {
    return Utilities.formatDate(val, CONFIG.TIMEZONE, 'yyyy-MM-dd');
  }
  return String(val).substring(0, 10);
}
