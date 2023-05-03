package system

import (
	v1 "github.com/flipped-aurora/gin-vue-admin/server/api/v1"
	"github.com/gin-gonic/gin"
)

type GPTApiRouter struct{}

func (s *GPTApiRouter) InitGPTRouter(Router *gin.RouterGroup) {
	//apiRouter := Router.Group("gpt").Use(middleware.OperationRecord())
	apiRouterWithoutRecord := Router.Group("gpt")
	apiRouterApi := v1.ApiGroupApp.SystemApiGroup.GPTApiApi
	//{
	//	apiRouter.POST("createApi", apiRouterApi.CreateApi)               // 创建Api
	//	apiRouter.POST("deleteApi", apiRouterApi.DeleteApi)               // 删除Api
	//	apiRouter.POST("getApiById", apiRouterApi.GetApiById)             // 获取单条Api消息
	//	apiRouter.POST("updateApi", apiRouterApi.UpdateApi)               // 更新api
	//	apiRouter.DELETE("deleteApisByIds", apiRouterApi.DeleteApisByIds) // 删除选中api
	//}
	{
		apiRouterWithoutRecord.POST("testrole", apiRouterApi.TestRole)               // 获取所有api
		apiRouterWithoutRecord.POST("querysimilarity", apiRouterApi.QuerySimilarity) // 获取所有api
		apiRouterWithoutRecord.GET("getcorpuslist", apiRouterApi.GetCorpusList)      // 获取所有api
		apiRouterWithoutRecord.POST("addcorpus", apiRouterApi.AddCorpus)             // 获取所有api
		apiRouterWithoutRecord.POST("delcorpus", apiRouterApi.DelCorpus)             // 获取所有api
		apiRouterWithoutRecord.POST("delcorpusIds", apiRouterApi.DelCorpusIds)       // 获取所有api
		apiRouterWithoutRecord.POST("memerychat_raw", apiRouterApi.Memerychat_raw)   // 获取所有api
		apiRouterWithoutRecord.POST("tokenlizer", apiRouterApi.Tokenlizer)           // 获取Tokenlizer
		apiRouterWithoutRecord.POST("tonenlizer_role", apiRouterApi.Tokenlizer_role) // 获取Tokenlizer 按照消息计算

	}
}
