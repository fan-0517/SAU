# YouTube平台支持实现计划

## 1. 后端实现

### 1.1 添加YouTube平台常量
- **文件**: `sau_backend/utils/base_social_media.py`
- **内容**: 添加YouTube平台常量定义，并将其加入到支持的社交媒体列表中

### 1.2 添加YouTube平台配置
- **文件**: `sau_backend/newFileUpload/platform_configs.py`
- **内容**: 添加YouTube平台的完整配置，包括：
  - 平台类型编号（type: 10）
  - 平台名称和URLs
  - 选择器配置（上传按钮、发布按钮、标题编辑器等）
  - 功能支持配置

## 2. 前端实现

### 2.1 添加YouTube平台选项
- **文件**: `sau_frontend/src/views/PublishCenter.vue`
- **内容**: 在平台列表中添加YouTube选项

### 2.2 更新平台类型映射
- **文件**: `sau_frontend/src/views/PublishCenter.vue`
- **内容**: 在平台类型到平台名称的映射中添加YouTube

### 2.3 添加YouTube图标资源
- **文件**: 确保 `sau_frontend/src/assets/` 目录下有YouTube图标

## 3. 数据库和账号支持

### 3.1 确保账号系统支持YouTube
- **检查**: 账号管理相关代码是否需要修改以支持YouTube平台
- **内容**: 确保账号类型和文件路径处理正确

## 4. 测试和验证

### 4.1 测试平台选择功能
- **验证**: YouTube平台能在发布中心被正确选择

### 4.2 测试账号关联功能
- **验证**: YouTube账号能被正确关联和管理

### 4.3 测试发布流程
- **验证**: 能成功构建YouTube发布请求

## 实现步骤

1. 首先修改后端文件，添加YouTube常量和配置
2. 然后修改前端文件，添加YouTube平台选项
3. 确保图标资源存在
4. 测试功能完整性

这个计划将确保YouTube平台能够被正确集成到现有系统中，支持账号管理和内容发布功能。