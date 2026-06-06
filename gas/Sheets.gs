/**
 * Spreadsheet bootstrap, row-based CRUD (update-not-duplicate)
 * Execution-scoped caches + ScriptCache for getAppState (TTL 45s).
 */

var SHEET_HEADERS_ = {};
var APP_STATE_CACHE_PREFIX_ = 'appState_v3_';
var APP_STATE_CACHE_TTL_ = 45;

var _execCache_ = {
  spreadsheet: null,
  sheetsEnsured: false,
  sheetData: {},
  props: {}
};

function invalidateExecCache_(sheetName) {
  if (sheetName) {
    delete _execCache_.sheetData[sheetName];
  } else {
    _execCache_.sheetData = {};
  }
  invalidateAppStateCache_();
}

function invalidateAppStateCache_() {
  try {
    CacheService.getScriptCache().removeAll(
      CacheService.getScriptCache().getKeys().filter(function (k) {
        return k.indexOf(APP_STATE_CACHE_PREFIX_) === 0;
      })
    );
  } catch (e) {
    CacheService.getScriptCache().remove(APP_STATE_CACHE_PREFIX_ + 'default');
  }
}

function getScriptPropCached_(key) {
  if (_execCache_.props.hasOwnProperty(key)) {
    return _execCache_.props[key];
  }
  var val = PropertiesService.getScriptProperties().getProperty(key);
  _execCache_.props[key] = val;
  return val;
}

function clearScriptPropCache_(key) {
  delete _execCache_.props[key];
}

function initSheetHeaders_() {
  SHEET_HEADERS_[SHEET_NAMES.VEHICLES] = [
    'vehicleId', 'ชื่อ', 'ทะเบียน', 'สร้างเมื่อ', 'prbExpiryDate', 'insuranceExpiryDate'
  ];
  SHEET_HEADERS_[SHEET_NAMES.CATEGORIES] = ['categoryId', 'ชื่อ'];
  SHEET_HEADERS_[SHEET_NAMES.MAINTENANCE] = [
    'logId', 'vehicleId', 'วันที่', 'categoryId', 'ร้าน', 'ราคา', 'ไมล์',
    'type', 'alertKm', 'alertMonth', 'driveFileId', 'driveUrl', 'receiptName'
  ];
  SHEET_HEADERS_[SHEET_NAMES.FUEL] = [
    'logId', 'vehicleId', 'วันที่', 'fuelType', 'ไมล์', 'ลิตร',
    'ราคา/ลิตร', 'ราคารวม', 'เต็มถัง', 'สถานี'
  ];
  SHEET_HEADERS_[SHEET_NAMES.ALERTS] = [
    'alertId', 'vehicleId', 'targetKm', 'targetDate', 'status', 'lastUpdated', 'serviceLabel', 'categoryId'
  ];
  SHEET_HEADERS_[SHEET_NAMES.SETTINGS] = ['key', 'value'];
}

function isSpreadsheetPermissionError_(msg) {
  var lower = String(msg || '').toLowerCase();
  return lower.indexOf('permission') >= 0 ||
    lower.indexOf('do not have access') >= 0 ||
    lower.indexOf('requested document') >= 0 ||
    String(msg).indexOf('สิทธิ์') >= 0;
}

function throwSpreadsheetPermissionError_(ssId) {
  throw new Error(
    'ไม่สามารถเปิดสเปรดชีตได้ (ID: ' + ssId + ') — ' +
    'ตรวจสอบว่า Deploy ตั้งค่า "Execute as: Me" และ "Who has access: Anyone" แล้ว ' +
    'และเจ้าของสคริปต์ต้องรัน getAppState ใน Apps Script Editor ครั้งแรกเพื่ออนุมัติสิทธิ์ Google Sheets'
  );
}

function createAndSaveSpreadsheet_() {
  var ss = SpreadsheetApp.create('MyHome CarCare Database');
  var id = ss.getId();
  setScriptProp_(CONFIG.SPREADSHEET_PROP, id);
  ensureSheets_(ss);
  Logger.log('Created MyHome CarCare spreadsheet: ' + id);
  return ss;
}

function getSpreadsheet_() {
  if (_execCache_.spreadsheet) {
    return _execCache_.spreadsheet;
  }
  initSheetHeaders_();
  var ssId = getScriptProp_(CONFIG.SPREADSHEET_PROP);
  if (ssId) {
    try {
      _execCache_.spreadsheet = SpreadsheetApp.openById(ssId);
      return _execCache_.spreadsheet;
    } catch (e) {
      var errMsg = String(e.message || e);
      if (isSpreadsheetPermissionError_(errMsg)) {
        throwSpreadsheetPermissionError_(ssId);
      }
      Logger.log('openById failed for ' + ssId + ': ' + errMsg + ' — creating new spreadsheet');
    }
  }
  _execCache_.spreadsheet = createAndSaveSpreadsheet_();
  return _execCache_.spreadsheet;
}

function ensureSheetsOnce_(ss) {
  if (_execCache_.sheetsEnsured) {
    return;
  }
  ensureSheets_(ss || getSpreadsheet_());
  _execCache_.sheetsEnsured = true;
}

function preloadAllSheets_() {
  initSheetHeaders_();
  Object.keys(SHEET_HEADERS_).forEach(function (name) {
    loadSheetValues_(name);
  });
}

function loadSheetValues_(sheetName) {
  if (_execCache_.sheetData[sheetName]) {
    return _execCache_.sheetData[sheetName];
  }
  initSheetHeaders_();
  var sheet = getSpreadsheet_().getSheetByName(sheetName);
  var headers = SHEET_HEADERS_[sheetName];
  if (!sheet) {
    _execCache_.sheetData[sheetName] = { headers: headers, rows: [] };
    return _execCache_.sheetData[sheetName];
  }
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) {
    _execCache_.sheetData[sheetName] = { headers: headers, rows: [] };
    return _execCache_.sheetData[sheetName];
  }
  var values = sheet.getRange(2, 1, lastRow, headers.length).getValues();
  _execCache_.sheetData[sheetName] = { headers: headers, rows: values };
  return _execCache_.sheetData[sheetName];
}

function getSheet_(name) {
  return getSpreadsheet_().getSheetByName(name);
}

function ensureSheets_(ss) {
  initSheetHeaders_();
  Object.keys(SHEET_HEADERS_).forEach(function (name) {
    var sheet = ss.getSheetByName(name);
    if (!sheet) {
      sheet = ss.insertSheet(name);
    }
    var headers = SHEET_HEADERS_[name];
    if (sheet.getLastRow() === 0) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    } else {
      var existing = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
      var mismatch = headers.some(function (h, i) {
        return String(existing[i] || '') !== h;
      });
      if (mismatch) {
        sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      }
    }
  });

  seedDefaultSettings_(ss);
  seedSampleDataIfEmpty_(ss);
  invalidateExecCache_();
}

function seedDefaultSettings_(ss) {
  var sheet = ss.getSheetByName(SHEET_NAMES.SETTINGS);
  var defaults = {
    driveFolderId: CONFIG.DRIVE_FOLDER_ID,
    adminPass: CONFIG.DEFAULT_ADMIN_PASS,
    lineNotifyToken: ''
  };
  Object.keys(defaults).forEach(function (key) {
    if (!findRowById_(sheet, 0, key)) {
      sheet.appendRow([key, defaults[key]]);
    }
  });
}

function seedSampleDataIfEmpty_(ss) {
  var vehicles = getSheet_(SHEET_NAMES.VEHICLES);
  if (vehicles.getLastRow() > 1) return;

  var today = getBangkokToday_();
  var rows = [
    ['V-001', 'Toyota Camry Hybrid', 'กข 555 กรุงเทพ', '2025-01-10'],
    ['V-002', 'Tesla Model Y', 'ชภ 9999 นนทบุรี', '2025-03-15']
  ];
  rows.forEach(function (r) { vehicles.appendRow(r); });

  var cats = getSheet_(SHEET_NAMES.CATEGORIES);
  [
    ['CAT-001', 'เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว'],
    ['CAT-002', 'ระบบห้ามล้อและเบรก'],
    ['CAT-003', 'เปลี่ยนยางและถ่วงล้อ'],
    ['CAT-004', 'แบตเตอรี่และระบบขับเคลื่อน']
  ].forEach(function (r) { cats.appendRow(r); });

  var maint = getSheet_(SHEET_NAMES.MAINTENANCE);
  var folderUrl = 'https://drive.google.com/drive/folders/' + CONFIG.DRIVE_FOLDER_ID;
  [
    ['LOG-001', 'V-001', today, '-', '-', 0, 148000, 'Odometer_Update', 0, 0, '', '', ''],
    ['LOG-002', 'V-001', '2026-03-01', 'CAT-001', 'ศูนย์โตโยต้า พระราม 9', 3800, 152000, 'Maintenance', 10000, 6, '', folderUrl, 'receipt_camry_oil.jpg'],
    ['LOG-003', 'V-002', '2025-11-20', 'CAT-003', 'ศูนย์เทสลา รามคำแหง', 32000, 24500, 'Maintenance', 20000, 12, '', folderUrl, 'tesla_invoice.pdf'],
    ['LOG-004', 'V-001', '2025-08-14', 'CAT-002', 'บี-ควิก ติวานนท์', 5400, 135000, 'Maintenance', 15000, 12, '', folderUrl, 'bq_invoice.jpg']
  ].forEach(function (r) { maint.appendRow(r); });

  var fuel = getSheet_(SHEET_NAMES.FUEL);
  [
    ['FUEL-001', 'V-001', '2026-01-10', 'oil', 148500, 45, 38.5, 1732.5, true, ''],
    ['FUEL-002', 'V-001', '2026-02-15', 'oil', 149200, 42, 39.2, 1646.4, true, ''],
    ['FUEL-003', 'V-001', '2026-04-10', 'oil', 150050, 44.5, 40.1, 1784.45, true, '']
  ].forEach(function (r) { fuel.appendRow(r); });

  var alerts = getSheet_(SHEET_NAMES.ALERTS);
  [
    ['ALERT-001', 'V-001', 162000, '2026-09-01', 'Active', '2026-03-01', 'เปลี่ยนถ่ายน้ำมันเครื่อง/ของเหลว', 'CAT-001'],
    ['ALERT-002', 'V-002', 44500, '2026-11-20', 'Active', '2025-11-20', 'เปลี่ยนยางและถ่วงล้อ', 'CAT-003']
  ].forEach(function (r) { alerts.appendRow(r); });
}

function findRowById_(sheet, idColIndex, id) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return 0;
  var ids = sheet.getRange(2, idColIndex + 1, lastRow - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === String(id)) {
      return i + 2;
    }
  }
  return 0;
}

function upsertRow_(sheetName, idColName, id, rowObj) {
  var sheet = getSheet_(sheetName);
  var headers = SHEET_HEADERS_[sheetName];
  var idColIndex = headers.indexOf(idColName);
  if (idColIndex < 0) throw new Error('Invalid id column: ' + idColName);

  var row = headers.map(function (h) {
    var val = rowObj[h];
    if (val === undefined || val === null) return '';
    if (typeof val === 'boolean') return val ? 'TRUE' : 'FALSE';
    return val;
  });

  var existingRow = findRowById_(sheet, idColIndex, id);
  if (existingRow > 0) {
    sheet.getRange(existingRow, 1, 1, headers.length).setValues([row]);
    invalidateExecCache_(sheetName);
    return { updated: true, row: existingRow };
  }
  sheet.appendRow(row);
  invalidateExecCache_(sheetName);
  return { updated: false, row: sheet.getLastRow() };
}

function deleteRowById_(sheetName, idColName, id) {
  var sheet = getSheet_(sheetName);
  var headers = SHEET_HEADERS_[sheetName];
  var idColIndex = headers.indexOf(idColName);
  var row = findRowById_(sheet, idColIndex, id);
  if (row > 0) {
    sheet.deleteRow(row);
    invalidateExecCache_(sheetName);
    return true;
  }
  return false;
}

function getAllRowsAsObjects_(sheetName) {
  var cached = loadSheetValues_(sheetName);
  var headers = cached.headers;
  return cached.rows.map(function (row) {
    var obj = {};
    headers.forEach(function (h, i) {
      obj[h] = row[i];
    });
    return obj;
  });
}

function num_(val, fallback) {
  var n = parseFloat(val);
  return isNaN(n) ? (fallback || 0) : n;
}

function bool_(val) {
  return val === true || val === 'TRUE' || val === 'true' || val === 1 || val === '1';
}
