// Alert thresholds (km/time) mirrored in lib/car-logic.js checkAlertStatus (npm tests).
function getAlerts_() {
  return getAllRowsAsObjects_(SHEET_NAMES.ALERTS).map(function (r) {
    return {
      alertId: String(r.alertId),
      vehicleId: String(r.vehicleId),
      targetKm: num_(r.targetKm),
      targetDate: formatDateCell_(r.targetDate),
      status: String(r.status || 'Active'),
      lastUpdated: formatDateCell_(r.lastUpdated)
    };
  });
}

function checkLineAlerts(manual, includeState) {
  try {
    appendLineLog_('⚡ สแกนระยะซ่อมบำรุง...');
    var alerts = getAlerts_();
    var vehicles = getVehicles_();
    var notificationTriggered = false;
    var messages = [];
    var today = new Date();

    alerts.forEach(function (alert) {
      if (alert.status !== 'Active') return;

      var vehicle = vehicles.find(function (v) { return v.id === alert.vehicleId; });
      if (!vehicle) return;

      var currentOdo = getLatestOdometer_(alert.vehicleId);
      var targetDate = new Date(alert.targetDate);
      var isKmReached = currentOdo >= alert.targetKm;
      var isTimeReached = today >= targetDate;

      if (isKmReached || isTimeReached) {
        var reason = isKmReached && isTimeReached
          ? 'ครบกำหนดทั้งระยะทางและเวลา'
          : isKmReached
            ? 'ระยะไมล์สะสมถึงกำหนด (' + currentOdo.toLocaleString() + ' กม.)'
            : 'ถึงกำหนดครบเวลาบำรุงรักษาแล้ว (' + alert.targetDate + ')';

        var msg = '🚗 ' + vehicle.name + ': ' + reason;
        messages.push(msg);

        if (isLineNotifyConfigured_()) {
          sendLineNotify_(buildLineAlertMessage_(vehicle, reason));
          appendLineLog_('📢 LINE NOTIFY API: แจ้งเตือนครอบครัวรถ "' + vehicle.name + '" ครบระยะซ่อมเนื่องจาก ' + reason);
        } else {
          appendLineLog_('📢 LINE NOTIFY (จำลอง): แจ้งเตือนครอบครัวรถ "' + vehicle.name + '" ครบระยะซ่อมเนื่องจาก ' + reason);
        }

        upsertRow_(SHEET_NAMES.ALERTS, 'alertId', alert.alertId, {
          alertId: alert.alertId,
          vehicleId: alert.vehicleId,
          targetKm: alert.targetKm,
          targetDate: alert.targetDate,
          status: 'Notified',
          lastUpdated: getBangkokToday_()
        });

        notificationTriggered = true;
      }
    });

    var result = {
      success: true,
      notificationTriggered: notificationTriggered,
      messages: messages,
      manual: !!manual,
      lineNotifyConfigured: isLineNotifyConfigured_()
    };
    if (includeState !== false) {
      result.state = getAppState(null, { skipCache: true });
    }
    return result;
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function buildLineAlertMessage_(vehicle, reason) {
  return '\n🔧 MyHome CarCare แจ้งเตือนบำรุงรักษา\n' +
    'รถ: ' + vehicle.name + ' (' + vehicle.license + ')\n' +
    'สาเหตุ: ' + reason + '\n' +
    'วันที่: ' + getBangkokNow_() + '\n' +
    'กรุณาตรวจสอบและนัดหมายซ่อมบำรุง';
}

function dailyCheckAlerts() {
  var result = checkLineAlerts(false);
  Logger.log(JSON.stringify(result));
  return result;
}

function setupTriggers() {
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function (trigger) {
    if (trigger.getHandlerFunction() === 'dailyCheckAlerts') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger('dailyCheckAlerts')
    .timeBased()
    .everyDays(1)
    .atHour(8)
    .inTimezone(CONFIG.TIMEZONE)
    .create();

  return {
    success: true,
    message: 'สร้าง daily trigger สำเร็จ (ทุกวัน 08:00 น. Asia/Bangkok)'
  };
}
