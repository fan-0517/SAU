<template>
  <div class="website-container">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>网站管理</span>
        </div>
      </template>
      
      <div class="website-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="功能说明">
            网站管理模块用于配置和管理各个平台的网站设置。
          </el-descriptions-item>
        </el-descriptions>
        
        <el-divider>平台配置</el-divider>
        
        <el-table :data="websiteData" style="width: 100%">
          <el-table-column prop="platform" label="平台" width="120" />
          <el-table-column prop="url" label="网站地址" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                {{ scope.row.status === 'active' ? '活跃' : '未激活' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="editWebsite(scope.row)">编辑</el-button>
              <el-button size="small" :type="scope.row.status === 'active' ? 'danger' : 'success'" 
                @click="toggleStatus(scope.row)">
                {{ scope.row.status === 'active' ? '停用' : '启用' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 网站数据
const websiteData = ref([
  {
    platform: '抖音',
    url: 'https://www.douyin.com',
    status: 'active'
  },
  {
    platform: '快手',
    url: 'https://www.kuaishou.com',
    status: 'active'
  },
  {
    platform: '视频号',
    url: 'https://channels.weixin.qq.com',
    status: 'active'
  },
  {
    platform: '小红书',
    url: 'https://www.xiaohongshu.com',
    status: 'active'
  },
  {
    platform: 'TikTok',
    url: 'https://www.tiktok.com',
    status: 'active'
  }
])

// 编辑网站配置
const editWebsite = (row) => {
  console.log('编辑网站配置:', row)
}

// 切换状态
const toggleStatus = (row) => {
  row.status = row.status === 'active' ? 'inactive' : 'active'
}
</script>

<style scoped>
.website-container {
  padding: 20px;
}

.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.website-content {
  margin-top: 20px;
}
</style>