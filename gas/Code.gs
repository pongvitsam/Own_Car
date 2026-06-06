/**
 * MyHome CarCare - Web App entry & API facade
 */

function doGet(e) {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('MyHome CarCare')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Include HTML fragments (Scripts.html). Do NOT use for CSS — GAS strips
 * <style> tags from included files, leaving raw CSS as visible page text.
 * Custom styles must live inline in Index.html <head>.
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * Owner-only bootstrap: run once in Apps Script Editor to create spreadsheet,
 * authorize OAuth scopes, and seed default data.
 */
function ownerBootstrapOnce() {
  var ss = getSpreadsheet_();
  ensureSheets_(ss);
  _execCache_.sheetsEnsured = true;
  return {
    success: true,
    spreadsheetId: ss.getId(),
    spreadsheetUrl: ss.getUrl(),
    message: 'สร้าง/เปิดสเปรดชีตสำเร็จ — พร้อมใช้งานเว็บแอปแล้ว'
  };
}

function getAppStateCacheKey_(selectedVehicleId, opts) {
  opts = opts || {};
  return APP_STATE_CACHE_PREFIX_ + String(selectedVehicleId || '_') +
    (opts.includeFuel ? '_f' + String(opts.fuelVehicleId || selectedVehicleId || '') : '');
}

function buildAppState_(selectedVehicleId, opts) {
  opts = opts || {};
  var includeFuel = !!opts.includeFuel;
  var fuelVehicleId = opts.fuelVehicleId || selectedVehicleId;

  var ss = getSpreadsheet_();
  ensureSheetsOnce_(ss);
  preloadAllSheets_();

  var vehicles = getVehicles_();
  var selectedId = selectedVehicleId || (vehicles.length ? vehicles[0].id : '');

  return {
    vehicles: vehicles,
    categories: getCategories_(),
    vehicleOdometers: getVehicleOdometers_(),
    maintenanceLogs: selectedId ? getMaintenanceLogsForVehicle_(selectedId, 50) : [],
    fuelLogs: includeFuel && fuelVehicleId ? getFuelLogsForVehicle_(fuelVehicleId) : [],
    fuelLogsLoaded: includeFuel,
    alerts: getAlerts_().map(function (a) {
      return {
        vehicleId: a.vehicleId,
        targetKm: a.targetKm,
        targetDate: a.targetDate,
        status: a.status,
        lastUpdated: a.lastUpdated
      };
    }),
    selectedVehicleId: selectedId,
    adminAuthenticated: false,
    lineLogs: getLineLogs_(),
    lineNotifyConfigured: isLineNotifyConfigured_(),
    driveFolderId: CONFIG.DRIVE_FOLDER_ID,
    spreadsheetId: getScriptProp_(CONFIG.SPREADSHEET_PROP) || ''
  };
}

function getAppState(selectedVehicleId, opts) {
  opts = opts || {};
  try {
    getSpreadsheet_();
    ensureSheetsOnce_(getSpreadsheet_());
  } catch (e) {
    throw new Error(
      String(e.message || e) ||
      'ไม่สามารถโหลดข้อมูลจาก Google Sheets ได้ — กรุณาให้เจ้าของสคริปต์รัน ownerBootstrapOnce ใน Editor'
    );
  }

  if (opts.skipCache) {
    return buildAppState_(selectedVehicleId, opts);
  }

  var cacheKey = getAppStateCacheKey_(selectedVehicleId, opts);
  try {
    var cached = CacheService.getScriptCache().get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }
  } catch (e) { /* cache miss */ }

  var state = buildAppState_(selectedVehicleId, opts);
  try {
    CacheService.getScriptCache().put(cacheKey, JSON.stringify(state), APP_STATE_CACHE_TTL_);
  } catch (e) { /* payload too large for cache */ }
  return state;
}

/** Lazy-load fuel logs when user opens Fuelio tab */
function getFuelLogs(vehicleId) {
  try {
    ensureSheetsOnce_(getSpreadsheet_());
    loadSheetValues_(SHEET_NAMES.FUEL);
    loadSheetValues_(SHEET_NAMES.MAINTENANCE);
    return {
      success: true,
      vehicleId: vehicleId,
      fuelLogs: getFuelLogsForVehicle_(vehicleId),
      vehicleOdometers: getVehicleOdometers_()
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/** Load maintenance history when switching vehicles */
function getMaintenanceLogs(vehicleId) {
  try {
    ensureSheetsOnce_(getSpreadsheet_());
    loadSheetValues_(SHEET_NAMES.MAINTENANCE);
    loadSheetValues_(SHEET_NAMES.FUEL);
    return {
      success: true,
      vehicleId: vehicleId,
      maintenanceLogs: getMaintenanceLogsForVehicle_(vehicleId, 50),
      vehicleOdometers: getVehicleOdometers_()
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/** On-demand receipt thumbnail (avoids huge getAppState payload) */
function getReceiptThumbnail(driveFileId) {
  try {
    if (!driveFileId) {
      return { success: false, error: 'ไม่มีไฟล์แนบ' };
    }
    var file = DriveApp.getFileById(String(driveFileId));
    var blob = file.getBlob();
    var mime = blob.getContentType() || '';
    if (mime.indexOf('image/') !== 0) {
      return { success: false, error: 'ไม่ใช่ไฟล์รูปภาพ' };
    }
    var bytes = blob.getBytes();
    if (bytes.length > 500000) {
      return { success: false, error: 'ไฟล์ใหญ่เกินไป — เปิดจาก Drive แทน' };
    }
    return {
      success: true,
      mimeType: mime,
      base64: 'data:' + mime + ';base64,' + Utilities.base64Encode(bytes),
      name: file.getName()
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
