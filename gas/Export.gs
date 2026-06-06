function formatNum_(n) {
  return Number(n || 0).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function formatMoney_(n) {
  return Number(n || 0).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function exportReportPdf(vehicleId, year) {
  try {
    var vehicles = getVehicles_();
    var vehicle = vehicles.find(function (v) { return v.id === vehicleId; });
    if (!vehicle) {
      return { success: false, error: 'ไม่พบรถ' };
    }

    var targetYear = String(year || new Date().getFullYear());
    var logs = getMaintenanceLogs_().filter(function (l) {
      if (l.type !== 'Maintenance' || l.vehicleId !== vehicleId) return false;
      return String(new Date(l.date).getFullYear()) === targetYear;
    });

    var categories = getCategories_();
    var total = logs.reduce(function (sum, l) { return sum + l.cost; }, 0);
    var categorySums = {};

    logs.forEach(function (l) {
      var cat = categories.find(function (c) { return c.id === l.category; });
      var name = cat ? cat.name : 'อื่นๆ';
      categorySums[name] = (categorySums[name] || 0) + l.cost;
    });

    var html = buildReportHtml_(vehicle, targetYear, logs, total, categorySums);
    var pdfBlob = HtmlService.createHtmlOutput(html)
      .getBlob()
      .getAs('application/pdf')
      .setName('MyHome-CarCare-' + vehicle.license + '-' + targetYear + '.pdf');

    return {
      success: true,
      base64: Utilities.base64Encode(pdfBlob.getBytes()),
      filename: pdfBlob.getName(),
      mimeType: 'application/pdf'
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function buildReportHtml_(vehicle, year, logs, total, categorySums) {
  var buddhistYear = parseInt(year, 10) + 543;
  var rowsHtml = logs.map(function (l) {
    return '<tr>' +
      '<td>' + l.date + '</td>' +
      '<td>' + l.shop + '</td>' +
      '<td>' + formatNum_(l.odo) + '</td>' +
      '<td style="text-align:right">฿' + l.cost.toFixed(2) + '</td>' +
      '</tr>';
  }).join('');

  var catHtml = Object.keys(categorySums).map(function (name) {
    var sum = categorySums[name];
    var pct = total > 0 ? ((sum / total) * 100).toFixed(0) : 0;
    return '<li>' + name + ': ฿' + formatNum_(sum) + ' (' + pct + '%)</li>';
  }).join('');

  return '<!DOCTYPE html><html><head><meta charset="UTF-8">' +
    '<style>body{font-family:Sarabun,Arial,sans-serif;padding:24px;color:#1e293b}' +
    'h1{font-size:20px;margin-bottom:4px}table{width:100%;border-collapse:collapse;margin-top:16px}' +
    'th,td{border:1px solid #cbd5e1;padding:8px;font-size:12px}th{background:#eef2ff}' +
    '.summary{background:#f8fafc;padding:12px;border-radius:8px;margin-top:12px}' +
    '</style></head><body>' +
    '<h1>MyHome CarCare - รายงานค่าบำรุงรักษา</h1>' +
    '<p>รถ: <strong>' + vehicle.name + '</strong> (' + vehicle.license + ')</p>' +
    '<p>ปี พ.ศ. ' + buddhistYear + ' (ค.ศ. ' + year + ')</p>' +
    '<div class="summary">' +
    '<p>ยอดรวม: <strong>฿' + formatMoney_(total) + '</strong></p>' +
    '<p>จำนวนรายการ: ' + logs.length + '</p>' +
    '<ul>' + catHtml + '</ul></div>' +
    '<table><thead><tr><th>วันที่</th><th>ร้าน/ศูนย์</th><th>ไมล์</th><th>ค่าใช้จ่าย</th></tr></thead>' +
    '<tbody>' + (rowsHtml || '<tr><td colspan="4">ไม่มีข้อมูลในปีนี้</td></tr>') + '</tbody></table>' +
    '<p style="font-size:10px;color:#64748b;margin-top:24px">สร้างเมื่อ ' + getBangkokNow_() + ' (Asia/Bangkok)</p>' +
    '</body></html>';
}
