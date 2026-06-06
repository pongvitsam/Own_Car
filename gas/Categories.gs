function getCategories_() {
  return getAllRowsAsObjects_(SHEET_NAMES.CATEGORIES).map(function (r) {
    return {
      id: String(r.categoryId),
      name: String(r['ชื่อ'] || '')
    };
  });
}

function addCategory(data) {
  try {
    var id = data.id || generateId_('CAT');
    var existing = getCategories_().find(function (c) {
      return c.name.toLowerCase() === String(data.name).toLowerCase();
    });
    if (existing) {
      return { success: true, categoryId: existing.id, state: getAppState(null, { skipCache: true }) };
    }
    upsertRow_(SHEET_NAMES.CATEGORIES, 'categoryId', id, {
      categoryId: id,
      'ชื่อ': data.name
    });
    return { success: true, categoryId: id, state: getAppState(null, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function deleteCategory(categoryId) {
  try {
    var cats = getCategories_();
    if (cats.length <= 1) {
      return { success: false, error: 'จำเป็นต้องเหลือหมวดหมู่อย่างน้อย 1 ประเภท' };
    }
    deleteRowById_(SHEET_NAMES.CATEGORIES, 'categoryId', categoryId);
    return { success: true, state: getAppState(null, { skipCache: true }) };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function findOrCreateCategory_(name) {
  var cats = getCategories_();
  var matched = cats.find(function (c) {
    return c.name.toLowerCase() === String(name).toLowerCase();
  });
  if (matched) return matched.id;
  var id = generateId_('CAT');
  upsertRow_(SHEET_NAMES.CATEGORIES, 'categoryId', id, {
    categoryId: id,
    'ชื่อ': name
  });
  return id;
}
