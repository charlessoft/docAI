<template>
  <div>
    <!--    <div class="gva-search-box">-->
    <!--      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">-->
    <!--        <el-form-item label="创建时间">-->
    <!--          <el-date-picker v-model="searchInfo.startCreatedAt" type="datetime" placeholder="开始时间" />-->
    <!--          —-->
    <!--          <el-date-picker v-model="searchInfo.endCreatedAt" type="datetime" placeholder="结束时间" />-->
    <!--        </el-form-item>-->
    <!--        <el-form-item>-->
    <!--          <el-button size="small" type="primary" icon="search" @click="onSubmit">查询</el-button>-->
    <!--          <el-button size="small" icon="refresh" @click="onReset">重置</el-button>-->
    <!--        </el-form-item>-->
    <!--      </el-form>-->
    <!--    </div>-->
    <div class="gva-table-box">
      <!--      <div class="gva-btn-list">-->
      <!--        <el-button size="small" type="primary" icon="plus" @click="openDialog">新增</el-button>-->
      <!--        <el-popover v-model:visible="deleteVisible" placement="top" width="160">-->
      <!--          <p>确定要删除吗？</p>-->
      <!--          <div style="text-align: right; margin-top: 8px;">-->
      <!--            <el-button size="small" type="primary" link @click="deleteVisible = false">取消</el-button>-->
      <!--            <el-button size="small" type="primary" @click="onDelete">确定</el-button>-->
      <!--          </div>-->
      <!--          <template #reference>-->
      <!--            <el-button icon="delete" size="small" style="margin-left: 10px;" :disabled="!multipleSelection.length" @click="deleteVisible = true">删除</el-button>-->
      <!--          </template>-->
      <!--        </el-popover>-->
      <!--      </div>-->
      <el-form ref="elFormRef" :model="formData" label-position="right" :rules="rule" label-width="80px">
        <el-form-item label="Prompt:" prop="system">
          <el-input v-model="formData.system" />
        </el-form-item>

        <el-form-item label="Question:" prop="title">

              <el-input v-model="formData.question" >
                <template #append>
                  <el-button :loading="loading" @click="btnSubmit" :icon="Position" />
                </template>
              </el-input>

<!--            <el-col :span="4">-->
<!--              <el-button style="margin: auto;" type="primary" loading="loading" @click="btnSubmit">提交</el-button>-->

<!--            </el-col>-->



        </el-form-item>

        <el-form-item label="Answer:" prop="title">
          <el-input
                     type="textarea"
                     :rows="20"
                     v-model="formData.answer" ></el-input>
        </el-form-item>


      </el-form>
<!--      <el-row justify="center">-->
<!--        <el-col :span="24">-->
<!--        </el-col>-->
<!--      </el-row>-->

      <warning-bar title="log" />
      <el-row :gutter="10">
        <el-col :span="8">
          gpt_原始请求:
          <el-input
              v-model="formData.raw_message"
              type="textarea"
              :rows="30"
          />
        </el-col>
        <el-col :span="8">
          gpt_原始返回数据:
          <el-input
            v-model="formData.raw_gpt_response"
            type="textarea"
            :rows="30"
          />
        </el-col>
        <el-col :span="8">
          文档相关性:
          <el-input
            v-model="formData.similarity"
            type="textarea"
            :rows="30"
          />
        </el-col>
      </el-row>

      <!--      <el-table-->
      <!--        ref="multipleTable"-->
      <!--        style="width: 100%"-->
      <!--        tooltip-effect="dark"-->
      <!--        :data="tableData"-->
      <!--        row-key="ID"-->
      <!--        @selection-change="handleSelectionChange"-->
      <!--      >-->
      <!--        <el-table-column type="selection" width="55" />-->
      <!--        &lt;!&ndash;        <el-table-column align="left" label="日期" width="180">&ndash;&gt;-->
      <!--        &lt;!&ndash;            <template #default="scope">{{ formatDate(scope.row.CreatedAt) }}</template>&ndash;&gt;-->
      <!--        &lt;!&ndash;        </el-table-column>&ndash;&gt;-->
      <!--        <el-table-column align="left" label="考试标题" prop="title" width="120" />-->
      <!--        <el-table-column align="left" label="登分权限" prop="recordScorePowerInfo.title" width="120" />-->
      <!--        <el-table-column align="left" label="按钮组">-->
      <!--          <template #default="scope">-->
      <!--            <el-button type="primary" link icon="edit" size="small" class="table-button" @click="updateTExamTypeFunc(scope.row)">变更</el-button>-->
      <!--            <el-button type="primary" link icon="delete" size="small" @click="deleteRow(scope.row)">删除</el-button>-->
      <!--          </template>-->
      <!--        </el-table-column>-->
      <!--      </el-table>-->
<!--      <div class="gva-pagination">-->
<!--        <el-pagination-->
<!--          layout="total, sizes, prev, pager, next, jumper"-->
<!--          :current-page="page"-->
<!--          :page-size="pageSize"-->
<!--          :page-sizes="[10, 30, 50, 100]"-->
<!--          :total="total"-->
<!--          @current-change="handleCurrentChange"-->
<!--          @size-change="handleSizeChange"-->
<!--        />-->
<!--      </div>-->
    </div>

  </div>
</template>

<script>
export default {
  name: 'TExamType'
}
</script>

<script setup>

// import {
//   getTRecordScorePowerList
// } from '@/api/tRecordScorePower'
import WarningBar from '@/components/warningBar/warningBar.vue'
import { Position } from '@element-plus/icons-vue'
// 全量引入格式化工具 请按需保留
// import { getDictFunc, formatDate, formatBoolean, filterDict } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ref, reactive } from 'vue'
import { testRole, querySimilarity } from '@/api/qa'
import { deleteAuthority } from '@/api/authority'
import error from '@/view/error/index.vue'

// 自动化生成的字典（可能为空）以及字段
const formData = ref({
  // system: 'You are a helpful assistant that, when given context, can answer questions using only that information and generate relevant code.',
  system:'You are Foxiter, working on Foxit as a senior C++ developer, when given context, can answer questions using only that information and generate relevant code.',
  question: '',
  similarity: '',
  answer: '',
  engine: 'ChatGPT-0301',
  raw_message:'',
  raw_gpt_response: '',
})

// 验证规则
const rule = reactive({
})

const elFormRef = ref()

// =========== 表格控制部分 ===========
const page = ref(1)
const total = ref(0)
const pageSize = ref(10)
const tableData = ref([])
const tableRecordScorePowerData = ref([])
const searchInfo = ref({})
const loading = ref(false)

// 重置
const onReset = () => {
  searchInfo.value = {}
}

const btnSubmit = async() => {
  formData.value.raw_gpt_response = ''
  formData.value.answer = ''
  formData.value.similarity = ''
  formData.value.raw_message = ''

  loading.value = true
  const ret = await querySimilarity(formData.value)
  loading.value = false
  formData.value.raw_gpt_response = JSON.stringify(ret.data.raw_gpt_response)
  formData.value.answer = ret.data.answer
  formData.value.similarity = ret.data.similarity
  formData.value.raw_message = JSON.stringify(ret.data.raw_message)
  console.log(ret)
}

// 搜索
const onSubmit = () => {
  page.value = 1
  pageSize.value = 10
  getTableData()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  getTableData()
}

// 修改页面容量
const handleCurrentChange = (val) => {
  page.value = val
  getTableData()
}

// 查询
const getTableData = async() => {
  // const table = await getTExamTypeList({ page: page.value, pageSize: pageSize.value, ...searchInfo.value })
  // if (table.code === 0) {
  //   tableData.value = table.data.list
  //   total.value = table.data.total
  //   page.value = table.data.page
  //   pageSize.value = table.data.pageSize
  // }
}

const getTableRecordScorePowerData = async() => {
  const table = await getTRecordScorePowerList({ page: page.value })
  if (table.code === 0) {
    tableRecordScorePowerData.value = table.data.list
    // total.value = table.data.total
    // page.value = table.data.page
    // pageSize.value = table.data.pageSize
  }
}

getTableData()

// getTableRecordScorePowerData()

// ============== 表格控制部分结束 ===============

// 获取需要的字典 可能为空 按需保留
const setOptions = async() => {
}

// 获取需要的字典 可能为空 按需保留
setOptions()

// 多选数据
const multipleSelection = ref([])
// 多选
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}

// 删除行
const deleteRow = (row) => {
  ElMessageBox.confirm('确定要删除吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    deleteTExamTypeFunc(row)
  })
}

// 批量删除控制标记
const deleteVisible = ref(false)

// 多选删除
const onDelete = async() => {
  const ids = []
  if (multipleSelection.value.length === 0) {
    ElMessage({
      type: 'warning',
      message: '请选择要删除的数据'
    })
    return
  }
  multipleSelection.value &&
        multipleSelection.value.map(item => {
          ids.push(item.ID)
        })
  const res = await deleteTExamTypeByIds({ ids })
  if (res.code === 0) {
    ElMessage({
      type: 'success',
      message: '删除成功'
    })
    if (tableData.value.length === ids.length && page.value > 1) {
      page.value--
    }
    deleteVisible.value = false
    getTableData()
  }
}

// 行为控制标记（弹窗内部需要增还是改）
const type = ref('')

// 更新行
const updateTExamTypeFunc = async(row) => {
  const res = await findTExamType({ ID: row.ID })
  type.value = 'update'
  if (res.code === 0) {
    formData.value = res.data.retExamType
    dialogFormVisible.value = true
  }
}

// 删除行
const deleteTExamTypeFunc = async(row) => {
  const res = await deleteTExamType({ ID: row.ID })
  if (res.code === 0) {
    ElMessage({
      type: 'success',
      message: '删除成功'
    })
    if (tableData.value.length === 1 && page.value > 1) {
      page.value--
    }
    getTableData()
  }
}

// 弹窗控制标记
const dialogFormVisible = ref(false)

// 打开弹窗
const openDialog = () => {
  type.value = 'create'
  dialogFormVisible.value = true
}

// 关闭弹窗
const closeDialog = () => {
  dialogFormVisible.value = false
  formData.value = {
    title: '',
    recordScorePowerId: null
  }
}
// 弹窗确定
const enterDialog = async() => {
     elFormRef.value?.validate(async(valid) => {
       if (!valid) return
       let res
       switch (type.value) {
         case 'create':
           res = await createTExamType(formData.value)
           break
         case 'update':
           res = await updateTExamType(formData.value)
           break
         default:
           res = await createTExamType(formData.value)
           break
       }
       if (res.code === 0) {
         ElMessage({
           type: 'success',
           message: '创建/更改成功'
         })
         closeDialog()
         getTableData()
       }
     })
}
</script>

<style>
</style>
