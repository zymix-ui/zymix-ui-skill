# 一键删除旧变量/样式(zz_Archive)

> 执行时机建议:阶段③组件重建完成后。删除后残留绑定的节点**视觉不变**(值保留),
> 但失去变量联动(不随 Light/Dark 切换)。对 Claude 说"执行删除归档"即可运行。

```javascript
// use_figma 运行
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const removed = [];
for (const c of cols) {
  if (c.name.startsWith('zz_Archive/')) { removed.push(c.name + ' (' + c.variableIds.length + ' 变量)'); c.remove(); }
}
// 废弃样式
for (const s of await figma.getLocalTextStylesAsync()) {
  if (s.name === 'Link/Sm Hover') { removed.push('样式 Link/Sm Hover'); s.remove(); }
}
// 清理迁移用临时数据
figma.root.setSharedPluginData('zymix.migrate', 'idmap', '');
figma.root.setSharedPluginData('zymix.migrate', 'done_pages', '');
return JSON.stringify(removed);
```

删除范围:zz_Archive/01_Base(158)、02_Theme(151)、03_Typography(40)、04_Docs(7)、Link/Sm Hover 样式、迁移映射数据。
注意:04_Docs 删除会影响旧文档站页面的变量联动(值保留)。
