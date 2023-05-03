import service from '@/utils/request'

// @Tags TExamType
// @Summary 创建TExamType
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data body model.TExamType true "创建TExamType"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"获取成功"}"
// @Router /tExamType/createTExamType [post]
export const createTExamType = (data) => {
  return service({
    url: '/tExamType/createTExamType',
    method: 'post',
    data
  })
}

// @Tags TExamType
// @Summary 删除TExamType
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data body model.TExamType true "删除TExamType"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"删除成功"}"
// @Router /tExamType/deleteTExamType [delete]
export const deleteTExamType = (data) => {
  return service({
    url: '/tExamType/deleteTExamType',
    method: 'delete',
    data
  })
}

// @Tags TExamType
// @Summary 删除TExamType
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data body request.IdsReq true "批量删除TExamType"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"删除成功"}"
// @Router /tExamType/deleteTExamType [delete]
export const deleteTExamTypeByIds = (data) => {
  return service({
    url: '/tExamType/deleteTExamTypeByIds',
    method: 'delete',
    data
  })
}

// @Tags TExamType
// @Summary 更新TExamType
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data body model.TExamType true "更新TExamType"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"更新成功"}"
// @Router /tExamType/updateTExamType [put]
export const updateTExamType = (data) => {
  return service({
    url: '/tExamType/updateTExamType',
    method: 'put',
    data
  })
}

// @Tags TExamType
// @Summary 用id查询TExamType
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data query model.TExamType true "用id查询TExamType"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"查询成功"}"
// @Router /tExamType/findTExamType [get]
export const findTExamType = (params) => {
  return service({
    url: '/tExamType/findTExamType',
    method: 'get',
    params
  })
}

// @Tags TExamType
// @Summary 分页获取TExamType列表
// @Security ApiKeyAuth
// @accept application/json
// @Produce application/json
// @Param data query request.PageInfo true "分页获取TExamType列表"
// @Success 200 {string} string "{"success":true,"data":{},"msg":"获取成功"}"
// @Router /tExamType/getTExamTypeList [get]
export const getTExamTypeList = (params) => {
  return service({
    url: '/tExamType/getTExamTypeList',
    method: 'get',
    params
  })
}
