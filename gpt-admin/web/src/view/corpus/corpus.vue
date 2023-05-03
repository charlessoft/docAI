<template>
  <div>
    <div class="gva-search-box">
      <el-form :inline="true" :model="searchInfo" class="demo-form-inline">
<!--        <el-form-item label="创建时间">-->
<!--          <el-date-picker v-model="searchInfo.startCreatedAt" type="datetime" placeholder="开始时间" />-->
<!--          —-->
<!--          <el-date-picker v-model="searchInfo.endCreatedAt" type="datetime" placeholder="结束时间" />-->
<!--        </el-form-item>-->
        <el-form-item>
          <el-button size="small" type="primary" icon="search" @click="onSubmit">查询</el-button>
          <el-button size="small" icon="refresh" @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="gva-table-box">
      <div class="gva-btn-list">
        <el-button size="small" type="primary" icon="plus" @click="openDialog" >新增</el-button>
        <el-popover v-model:visible="deleteVisible" placement="top" width="160">
          <p>确定要删除吗？</p>
          <div style="text-align: right; margin-top: 8px;">
            <el-button size="small" type="primary" link @click="deleteVisible = false">取消</el-button>
            <el-button size="small" type="primary" @click="onDelete">确定</el-button>
          </div>
          <template #reference>
            <el-button icon="delete" size="small" style="margin-left: 10px;" :disabled="!multipleSelection.length" @click="deleteVisible = true">删除</el-button>
          </template>
        </el-popover>
      </div>
      <el-table
        ref="multipleTable"
        style="width: 100%"
        tooltip-effect="dark"
        :data="tableData"
        row-key="ID"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <!--        <el-table-column align="left" label="日期" width="180">-->
        <!--            <template #default="scope">{{ formatDate(scope.row.CreatedAt) }}</template>-->
        <!--        </el-table-column>-->
        <el-table-column align="left" label="id" prop="id" width="120" />
        <el-table-column align="left" label="content" prop="content" />
<!--        <el-table-column align="left" label="按钮组">-->
<!--          <template #default="scope">-->
<!--            <el-button type="primary" link icon="edit" size="small" class="table-button" @click="updateTExamTypeFunc(scope.row)">变更</el-button>-->
<!--            <el-button type="primary" link icon="delete" size="small" @click="deleteRow(scope.row)">删除</el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
      </el-table>
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
    <el-dialog v-model="dialogFormVisible" :before-close="closeDialog" title="弹窗操作">
      <el-form ref="elFormRef" :model="formData" label-position="right" :rules="rule" label-width="80px">
        <el-upload
            ref="uploadRef"
            v-model:file-list="fileList"
            style="width: 100%"
            type="drag"
            drag
            class="upload-demo"
            :action="`${domain_url}/gpt/addcorpus?sheetName=test`"
            :headers="{'x-token':userStore.token}"
            :before-upload="beforeUpload"
            :on-success="handleSuccess"
            :on-error="handleError"
            :auto-upload="false"
        >
          <el-icon class="el-icon--upload">
            <upload-filled />
          </el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>

        </el-upload>
<!--        <el-form-item label="考试标题:" prop="title">-->
<!--          <el-input v-model="formData.title" :clearable="true" placeholder="请输入" />-->
<!--        </el-form-item>-->
<!--        <el-form-item label="登分权限:">-->
<!--          <el-select v-model="formData.recordScorePowerId" filterable placeholder="登分权限">-->
<!--            <el-option-->
<!--              v-for="item in tableRecordScorePowerData"-->
<!--              :key="item.ID"-->
<!--              :label="item.title"-->
<!--              :value="item.ID"-->
<!--            />-->
<!--          </el-select>-->
<!--        </el-form-item>-->

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="small" @click="closeDialog">取 消</el-button>
          <el-button size="small" type="primary" @click="submitUpload">确 定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'TExamType'
}
</script>

<script setup>
// import {
//   createTExamType,
//   deleteTExamType,
//   deleteTExamTypeByIds,
//   updateTExamType,
//   findTExamType,
//   getTExamTypeList
// } from '@/api/tExamType'

// import {
//   getTRecordScorePowerList
// } from '@/api/tRecordScorePower'

// 全量引入格式化工具 请按需保留
// import { getDictFunc, formatDate, formatBoolean, filterDict } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import { nextTick, ref, reactive, onMounted } from 'vue'

import { delcorpus, delcorpusIds, getcopuslist } from '../../api/copus'
import { useUserStore } from '../../pinia/modules/user'
const userStore = useUserStore()

// 自动化生成的字典（可能为空）以及字段
const formData = ref({
  title: '',
  recordScorePowerId: null
})

// 验证规则
const rule = reactive({
})
const fileList = ref([])

const elFormRef = ref()
const uploadRef = ref(null)

// =========== 表格控制部分 ===========
const page = ref(1)
const total = ref(0)
const pageSize = ref(10)
const tableData = ref([])
const tableRecordScorePowerData = ref([])
const searchInfo = ref({})
const loading = ref(false)
const path = ref(import.meta.env.VITE_BASE_API)

const domain_url = ref('')
// 重置
const onReset = () => {
  searchInfo.value = {}
}

// 搜索
const onSubmit = () => {
  page.value = 1
  pageSize.value = 10
  getTableData()

}

onMounted(() => {
  domain_url.value = document.URL.split('/#')[0]
});

const submitUpload = () => {
  if (fileList.value.length === 0) {
    ElMessage('请先上传文件')
    return
  }
  loading.value = true
  uploadRef.value.submit()


}

const beforeUpload = (ss) => {
  console.log(ss)
  return true
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

const handleError = (ret) => {
  ElMessage({
    message: '导入失败!! 如果连续导入失败,请联系管理员',
    type: 'error',
  })
  loading.value = false
  console.log(ret)
}

const handleSuccess = (ret) => {
  // console.log(ret.data.stdout.data.list)
  // tableData.value = ret.data.stdout.data.list
  // headers.value = ret.data.stdout.data.headers
  // importCount.value = ret.data.stdout.data.count // 要导入的个数
  // totalCount.value = ret.data.stdout.data.total // 总共处理个数

  loading.value = false
  // const ret1 = JSON.stringify(tableData.value)
  //
  // if (ret1.indexOf('old') >= 0 && ret1.indexOf('new') >= 0) {
  //   disableImport.value = true
  // } else {
  //   disableImport.value = false
  // }
  nextTick(() => {
    uploadRef.value.clearFiles()

    ElMessage({
      type: 'success',
      message: '上传成功'
    })
    closeDialog()
    getTableData()
  })
}

// 查询
const getTableData = async() => {
  const table = await getcopuslist({ page: page.value, pageSize: pageSize.value, ...searchInfo.value })
  const lst = []
  if (table.code === 200) {
    // for (let i = 0; i < table.data.length; i++) {
    //   const obj = table.data[i];
    //   debugger
    for (const key in table.data) {
      lst.push(
          Object.assign(
        {
          'id': key
        }, table.data[key]
      ))
      console.log(key)
    }
    // }
    // table.data.list.data.map(item=>{
    //
    // })
    // tableData.value = table.data.list
    // total.value = table.data.total
    // page.value = table.data.page
    // pageSize.value = table.data.pageSize
    tableData.value = lst
    console.log(table)
  }
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
          ids.push(item.id)
        })
  const res = await delcorpusIds({ ids })
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
     // elFormRef.value?.validate(async(valid) => {
     //   if (!valid) return
     //   let res
     //   switch (type.value) {
     //     case 'create':
     //       res = await createTExamType(formData.value)
     //       break
     //     case 'update':
     //       res = await updateTExamType(formData.value)
     //       break
     //     default:
     //       res = await createTExamType(formData.value)
     //       break
     //   }
     //   if (res.code === 0) {
     //     ElMessage({
     //       type: 'success',
     //       message: '创建/更改成功'
     //     })
     //     closeDialog()
     //     getTableData()
     //   }
     // })
}
</script>

<style>
</style>
