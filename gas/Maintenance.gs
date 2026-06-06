function getMaintenanceLogs_() {
  var folderUrl = 'https://drive.google.com/drive/folders/' + CONFIG.DRIVE_FOLDER_ID;
  return getAllRowsAsObjects_(SHEET_NAMES.MAINTENANCE).map(function (r) {
    var driveUrl = String(r.driveUrl || '');
    if (!driveUrl && r.driveFileId) {
      driveUrl = 'https://drive.google.com/file/d/' + r.driveFileId + '/view';
    }
    return {
      id: String(r.logId),
      vehicleId: String(r.vehicleId),
      date: formatDateCell_(r['วันที่']),
      category: String(r.categoryId || '-'),
      shop: String(r['ร้าน'] || '-'),
      cost: num_(r['ราคา']),
      odo: num_(r['ไมล์']),
      type: String(r.type || 'Maintenance'),
      alertKm: num_(r.alertKm),
      alertMonth: num_(r.alertMonth),
      receipt: String(r.receiptName || ''),
      fileLink: driveUrl || folderUrl,
      driveFileId: String(r.driveFileId || '')
    };
  });
}

function getMaintenanceLogsForVehicle_(vehicleId, limit) {
  var logs = getMaintenanceLogs_().filter(function (l) {
    return l.vehicleId === String(vehicleId);
  });
  logs.sort(function (a, b) {
    return new Date(b.date) - new Date(a.date);
  });
  if (limit && logs.length > limit) {
    return logs.slice(0, limit);
  }
  return logs;
}

function saveMaintenanceLog(data) {
  try {
    var vehicleId = data.vehicleId;
    var odoVal = parseInt(data.odo, 10);
    var lastOdo = getLatestOdometer_(vehicleId);
    if (odoVal < lastOdo) {
      return { success: false, error: 'เลขไมล์ปัจจุบันต่ำกว่าครั้งล่าสุด!' };
    }

    var categoryId = data.category;
    if (categoryId === 'OTHER' && data.otherCategoryName) {
      categoryId = findOrCreateCategory_(data.otherCategoryName);
    }

    var logId = data.id || generateId_('LOG');
    var driveFileId = '';
    var driveUrl = '';
    var receiptName = data.receiptName || '';

    if (data.receiptBase64 && data.receiptName) {
      var upload = uploadReceipt_(data.receiptName, data.receiptBase64, data.receiptMimeType);
      if (upload.success) {
        driveFileId = upload.fileId;
        driveUrl = upload.url;
        receiptName = upload.name;
        appendLineLog_('📁 สำเร็จ: ส่งภาพหลักฐาน "' + receiptName + '" เข้าโฟลเดอร์ Google Drive');
      }
    }

    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', logId, {
      logId: logId,
      vehicleId: vehicleId,
      'วันที่': data.date || getBangkokToday_(),
      categoryId: categoryId,
      'ร้าน': data.shop || '-',
      'ราคา': num_(data.cost),
      'ไมล์': odoVal,
      type: 'Maintenance',
      alertKm: num_(data.alertKm),
      alertMonth: num_(data.alertMonth),
      driveFileId: driveFileId,
      driveUrl: driveUrl,
      receiptName: receiptName
    });

    if (data.alertKm > 0 || data.alertMonth > 0) {
      upsertAlertForVehicle_(vehicleId, odoVal, data.date, data.alertKm, data.alertMonth);
    }

    return { success: true, state: getAppState(vehicleId, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function saveEditedLog(data) {
  try {
    var logId = data.id;
    var rows = getAllRowsAsObjects_(SHEET_NAMES.MAINTENANCE);
    var existing = rows.find(function (r) { return String(r.logId) === String(logId); });
    if (!existing) {
      return { success: false, error: 'ไม่พบรายการ' };
    }

    var vehicleId = String(existing.vehicleId);
    var odoVal = parseInt(data.odo, 10);

    upsertRow_(SHEET_NAMES.MAINTENANCE, 'logId', logId, {
      logId: logId,
      vehicleId: vehicleId,
      'วันที่': formatDateCell_(existing['วันที่']),
      categoryId: existing.categoryId,
      'ร้าน': data.shop || '-',
      'ราคา': num_(data.cost),
      'ไมล์': odoVal,
      type: existing.type,
      alertKm: existing.alertKm,
      alertMonth: existing.alertMonth,
      driveFileId: existing.driveFileId,
      driveUrl: existing.driveUrl,
      receiptName: existing.receiptName
    });

    return { success: true, state: getAppState(vehicleId, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function deleteMaintenanceLog(logId) {
  try {
    var rows = getAllRowsAsObjects_(SHEET_NAMES.MAINTENANCE);
    var existing = rows.find(function (r) { return String(r.logId) === String(logId); });
    if (!existing) {
      return { success: false, error: 'ไม่พบรายการ' };
    }
    deleteRowById_(SHEET_NAMES.MAINTENANCE, 'logId', logId);
    return { success: true, state: getAppState(String(existing.vehicleId), { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function upsertAlertForVehicle_(vehicleId, odoVal, repairDate, alertKm, alertMonth) {
  var targetKm = alertKm > 0 ? (odoVal + alertKm) : 99999999;
  var targetDateStr = '2099-12-31';
  if (alertMonth > 0) {
    var d = new Date(repairDate);
    d.setMonth(d.getMonth() + alertMonth);
    targetDateStr = Utilities.formatDate(d, CONFIG.TIMEZONE, 'yyyy-MM-dd');
  }

  var alerts = getAllRowsAsObjects_(SHEET_NAMES.ALERTS);
  var existing = alerts.find(function (a) {
    return String(a.vehicleId) === String(vehicleId) && String(a.status) === 'Active';
  });
  var alertId = existing ? String(existing.alertId) : generateId_('ALERT');

  upsertRow_(SHEET_NAMES.ALERTS, 'alertId', alertId, {
    alertId: alertId,
    vehicleId: vehicleId,
    targetKm: targetKm,
    targetDate: targetDateStr,
    status: 'Active',
    lastUpdated: repairDate || getBangkokToday_()
  });

  appendLineLog_('⏰ ตั้งค่ารอบตรวจสอบของคัน ' + vehicleId + ': เป้าหมาย ' + targetKm + ' กม. หรือ ' + targetDateStr);
}
