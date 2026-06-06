function uploadReceipt_(fileName, base64Data, mimeType) {
  try {
    var folder = DriveApp.getFolderById(CONFIG.DRIVE_FOLDER_ID);
    var contentType = mimeType || guessMimeType_(fileName);
    var bytes = Utilities.base64Decode(stripBase64Prefix_(base64Data));
    var blob = Utilities.newBlob(bytes, contentType, fileName);
    var file = folder.createFile(blob);
    return {
      success: true,
      fileId: file.getId(),
      url: file.getUrl(),
      name: file.getName()
    };
  } catch (e) {
    appendLineLog_('❌ อัปโหลด Drive ล้มเหลว: ' + e.message);
    return { success: false, error: e.message };
  }
}

function stripBase64Prefix_(data) {
  var str = String(data || '');
  var idx = str.indexOf('base64,');
  if (idx >= 0) {
    return str.substring(idx + 7);
  }
  return str;
}

function guessMimeType_(fileName) {
  var lower = String(fileName).toLowerCase();
  if (lower.endsWith('.pdf')) return 'application/pdf';
  if (lower.endsWith('.png')) return 'image/png';
  if (lower.endsWith('.jpg') || lower.endsWith('.jpeg')) return 'image/jpeg';
  if (lower.endsWith('.webp')) return 'image/webp';
  return 'application/octet-stream';
}

/** On-demand receipt thumbnail — keeps base64 out of getAppState payload. */
function getReceiptThumbnail(driveFileId) {
  if (!driveFileId) {
    return { success: false, error: 'ไม่มีไฟล์แนบ' };
  }
  try {
    var file = DriveApp.getFileById(String(driveFileId));
    var blob = file.getBlob();
    var mime = blob.getContentType() || guessMimeType_(file.getName());
    if (mime.indexOf('image/') !== 0) {
      return { success: true, isImage: false, mimeType: mime, name: file.getName() };
    }
    return {
      success: true,
      isImage: true,
      mimeType: mime,
      name: file.getName(),
      base64: Utilities.base64Encode(blob.getBytes())
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
