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
      <div style="text-align: center;">
        用于计算gpt-3.5-turbo-0301模型需要的token.
      </div>
      <el-form ref="elFormRef" :model="formData" label-position="right" :rules="rule" label-width="100px">


        <el-form-item label="文本:" prop="title">
          <el-input
              type="textarea"
              :rows="20"
              v-model.lazy="formData.content"
              @change="handlerContent"
          ></el-input>


          <el-icon v-if="loading===true">
            <Loading/>
          </el-icon>
          <span style="color:#606266">消耗token:{{ formData.content_token }}</span>
        </el-form-item>

        <el-form-item label="消息结构体:" prop="title">
          <el-input
              type="textarea"
              :rows="20"
              v-model.lazy="formData.messages"
              @change="handlerMessage"
          ></el-input>
          <el-icon v-if="loading===true">
            <Loading/>
          </el-icon>
          <span style="color:#606266">消耗token:{{ formData.messages_token }}</span>
        </el-form-item>

        <el-form-item label="openAI 在线token计算">
          https://platform.openai.com/tokenizer
        </el-form-item>


      </el-form>
    </div>

  </div>
</template>

<script>
export default {
  name: 'TExamType',
}
</script>

<script setup>

import { ElMessage, ElMessageBox } from 'element-plus'
import { ref, reactive } from 'vue'

import { tonenlizer, tonenlizer_role } from '../../../api/tokenlizer'

// 自动化生成的字典（可能为空）以及字段
const formData = ref({
  // system: 'You are a helpful assistant that, when given context, can answer questions using only that information and generate relevant code.',
  content: '你好,chatsdk',
  content_token: null,
  messages: JSON.stringify([
    {
      'role': 'system',
      'content': 'You are an AI assistant that helps people find information.',
    },
    {
      'role': 'user',
      'content': '你是谁?',
    },
  ], null, 2),
  messages_token: null,
  engine: 'ChatGPT-0301',
})

// 验证规则
const rule = reactive({})

const elFormRef = ref()

// =========== 表格控制部分 ===========
const page = ref(1)
const total = ref(0)
const pageSize = ref(10)
const tableData = ref([])
const tableRecordScorePowerData = ref([])
const searchInfo = ref({})
const loading = ref(false)


const handlerContent = async() => {
  console.log('1111')
  loading.value = true
  let ret = await tonenlizer({ 'content': formData.value.content, 'model': 'gpt-3.5-turbo-0301' })
  loading.value = false
  formData.value.content_token = ret.data.num

}

const handlerMessage = async() => {
  loading.value = true
  let ret = await tonenlizer_role({ 'content': formData.value.messages, 'model': 'gpt-3.5-turbo-0301' })
  loading.value = false
  formData.value.messages_token = ret.data.num
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
    type: 'warning',
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
      message: '请选择要删除的数据',
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
      message: '删除成功',
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
      message: '删除成功',
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
    recordScorePowerId: null,
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
        message: '创建/更改成功',
      })
      closeDialog()
      getTableData()
    }
  })
}
</script>

<style>
</style>
