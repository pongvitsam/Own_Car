/**
 * HTTP + Bridge API for GitHub Pages ↔ Google Sheets sync.
 * Pages cannot use google.script.run directly — use Bridge.html (iframe postMessage)
 * or ?action= JSON/JSONP endpoints.
 */

function doPost(e) {
  return handleHttpApi_(e);
}

function jsonOutput_(obj, callback) {
  var text = JSON.stringify(obj);
  if (callback) {
    var safeCb = String(callback).replace(/[^\w.$]/g, '');
    return ContentService.createTextOutput(safeCb + '(' + text + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(text)
    .setMimeType(ContentService.MimeType.JSON);
}

function handleHttpApi_(e) {
  e = e || {};
  var callback = e.parameter && e.parameter.callback;
  try {
    var action = '';
    var payload = {};

    if (e.postData && e.postData.contents) {
      var body = JSON.parse(e.postData.contents);
      action = body.action || '';
      payload = body.payload || body.data || {};
    } else if (e.parameter) {
      action = e.parameter.action || '';
      if (e.parameter.payload) {
        payload = JSON.parse(e.parameter.payload);
      } else {
        payload = e.parameter;
      }
    }

    if (!action) {
      return jsonOutput_({ success: false, error: 'missing action' }, callback);
    }

    var result = dispatchApiAction_(action, payload);
    return jsonOutput_(result, callback);
  } catch (err) {
    return jsonOutput_({ success: false, error: String(err.message || err) }, callback);
  }
}

/**
 * Public Bridge / google.script.run entry — Pages iframe calls this only.
 * Underscored helpers are private and not callable from the client.
 */
function apiCall(action, payload) {
  try {
    return dispatchApiAction_(action, payload || {});
  } catch (err) {
    return { success: false, error: String(err.message || err) };
  }
}

/** Full state for Pages (all vehicles' fuel + maintenance). */
function getFullSyncState(selectedVehicleId) {
  try {
    return { success: true, state: getFullSyncState_(selectedVehicleId) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function getFullSyncState_(selectedVehicleId) {
  var ss = getSpreadsheet_();
  ensureSheetsOnce_(ss);
  preloadAllSheets_();

  var vehicles = getVehicles_();
  var selectedId = selectedVehicleId || (vehicles.length ? vehicles[0].id : '');

  return {
    vehicles: vehicles,
    categories: getCategories_(),
    maintenanceLogs: getMaintenanceLogs_(),
    fuelLogs: getFuelLogs_(),
    alerts: getAlerts_(),
    selectedVehicleId: selectedId,
    adminAuthenticated: false,
    lineLogs: getLineLogs_(),
    lineNotifyConfigured: isLineNotifyConfigured_(),
    driveFolderId: CONFIG.DRIVE_FOLDER_ID,
    spreadsheetId: getScriptProp_(CONFIG.SPREADSHEET_PROP) || '',
    syncSource: 'gas',
    syncedAt: getBangkokNow_()
  };
}

function withFullState_(result, selectedVehicleId) {
  if (!result || result.success === false) return result;
  var sid = selectedVehicleId
    || (result.state && result.state.selectedVehicleId)
    || null;
  result.state = getFullSyncState_(sid);
  return result;
}

function dispatchApiAction_(action, payload) {
  payload = payload || {};
  var selectedId = payload.selectedVehicleId || payload.vehicleId || null;

  switch (String(action)) {
    case 'ping':
      return {
        success: true,
        message: 'MyHome CarCare GAS API OK',
        version: '3.2-gas',
        lineNotifyConfigured: isLineNotifyConfigured_(),
        spreadsheetId: getScriptProp_(CONFIG.SPREADSHEET_PROP) || ''
      };

    case 'getFullSyncState':
      return getFullSyncState(selectedId);

    case 'getAppState':
      return {
        success: true,
        state: getAppState(selectedId, payload.opts || { includeFuel: true, skipCache: true })
      };

    case 'saveFuelLog':
      return withFullState_(saveFuelLog(payload), payload.vehicleId);

    case 'deleteFuelLog':
      return withFullState_(deleteFuelLog(payload.id || payload.logId), selectedId);

    case 'saveMaintenanceLog':
      return withFullState_(saveMaintenanceLog(payload), payload.vehicleId);

    case 'saveEditedLog':
      return withFullState_(saveEditedLog(payload), selectedId);

    case 'deleteMaintenanceLog':
      return withFullState_(deleteMaintenanceLog(payload.id || payload.logId), selectedId);

    case 'saveOdometerOnly':
      return withFullState_(saveOdometerOnly(payload), payload.vehicleId);

    case 'addVehicle':
      return withFullState_(addVehicle(payload), null);

    case 'updateVehicle':
    case 'updateVehicleAdmin':
      return updateVehicle(payload);

    case 'deleteVehicle':
      return withFullState_(deleteVehicle(payload.id || payload.vehicleId), null);

    case 'addCategory':
      return withFullState_(addCategory(payload), selectedId);

    case 'deleteCategory':
      return withFullState_(deleteCategory(payload.id || payload.categoryId), selectedId);

    case 'verifyAdmin':
      return verifyAdmin(payload);

    case 'checkLineAlerts':
      return withFullState_(checkLineAlerts(!!payload.manual, true), selectedId);

    case 'setupTriggers':
      return setupTriggers();

    case 'ownerBootstrapOnce':
      return ownerBootstrapOnce();

    case 'importFamilySeedData':
      return importFamilySeedData();

    case 'exportReportPdf':
      return exportReportPdf(payload.vehicleId, payload.year);

    case 'getFuelLogs':
      return getFuelLogs(payload.vehicleId);

    case 'getMaintenanceLogs':
      return getMaintenanceLogs(payload.vehicleId);

    case 'getReceiptThumbnail':
      return getReceiptThumbnail(payload.driveFileId);

    default:
      return { success: false, error: 'Unknown action: ' + action };
  }
}
