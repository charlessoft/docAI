package system

import (
	"bytes"
	"fmt"
	"github.com/flipped-aurora/gin-vue-admin/server/global"
	"github.com/flipped-aurora/gin-vue-admin/server/model/common/request"
	"github.com/flipped-aurora/gin-vue-admin/server/model/common/response"
	"github.com/flipped-aurora/gin-vue-admin/server/model/system"
	systemReq "github.com/flipped-aurora/gin-vue-admin/server/model/system/request"
	systemRes "github.com/flipped-aurora/gin-vue-admin/server/model/system/response"
	"github.com/flipped-aurora/gin-vue-admin/server/utils"
	"io"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

type GPTApiApi struct{}

// CreateApi
// @Tags      SysApi
// @Summary   创建基础api
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      system.SysApi                  true  "api路径, api中文描述, api组, 方法"
// @Success   200   {object}  response.Response{msg=string}  "创建基础api"
// @Router    /api/createApi [post]
func (s *GPTApiApi) CreateApi(c *gin.Context) {
	var api system.SysApi
	err := c.ShouldBindJSON(&api)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = utils.Verify(api, utils.ApiVerify)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = apiService.CreateApi(api)
	if err != nil {
		global.GVA_LOG.Error("创建失败!", zap.Error(err))
		response.FailWithMessage("创建失败", c)
		return
	}
	response.OkWithMessage("创建成功", c)
}

// DeleteApi
// @Tags      SysApi
// @Summary   删除api
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      system.SysApi                  true  "ID"
// @Success   200   {object}  response.Response{msg=string}  "删除api"
// @Router    /api/deleteApi [post]
func (s *GPTApiApi) DeleteApi(c *gin.Context) {
	var api system.SysApi
	err := c.ShouldBindJSON(&api)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = utils.Verify(api.GVA_MODEL, utils.IdVerify)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = apiService.DeleteApi(api)
	if err != nil {
		global.GVA_LOG.Error("删除失败!", zap.Error(err))
		response.FailWithMessage("删除失败", c)
		return
	}
	response.OkWithMessage("删除成功", c)
}

// GetApiList
// @Tags      SysApi
// @Summary   分页获取API列表
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      systemReq.SearchApiParams                               true  "分页获取API列表"
// @Success   200   {object}  response.Response{data=response.PageResult,msg=string}  "分页获取API列表,返回包括列表,总数,页码,每页数量"
// @Router    /api/getApiList [post]
func (s *GPTApiApi) GetApiList(c *gin.Context) {
	var pageInfo systemReq.SearchApiParams
	err := c.ShouldBindJSON(&pageInfo)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = utils.Verify(pageInfo.PageInfo, utils.PageInfoVerify)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	list, total, err := apiService.GetAPIInfoList(pageInfo.SysApi, pageInfo.PageInfo, pageInfo.OrderKey, pageInfo.Desc)
	if err != nil {
		global.GVA_LOG.Error("获取失败!", zap.Error(err))
		response.FailWithMessage("获取失败", c)
		return
	}
	response.OkWithDetailed(response.PageResult{
		List:     list,
		Total:    total,
		Page:     pageInfo.Page,
		PageSize: pageInfo.PageSize,
	}, "获取成功", c)
}

// GetApiById
// @Tags      SysApi
// @Summary   根据id获取api
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      request.GetById                                   true  "根据id获取api"
// @Success   200   {object}  response.Response{data=systemRes.SysAPIResponse}  "根据id获取api,返回包括api详情"
// @Router    /api/getApiById [post]
func (s *GPTApiApi) GetApiById(c *gin.Context) {
	var idInfo request.GetById
	err := c.ShouldBindJSON(&idInfo)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = utils.Verify(idInfo, utils.IdVerify)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	api, err := apiService.GetApiById(idInfo.ID)
	if err != nil {
		global.GVA_LOG.Error("获取失败!", zap.Error(err))
		response.FailWithMessage("获取失败", c)
		return
	}
	response.OkWithDetailed(systemRes.SysAPIResponse{Api: api}, "获取成功", c)
}

// UpdateApi
// @Tags      SysApi
// @Summary   修改基础api
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      system.SysApi                  true  "api路径, api中文描述, api组, 方法"
// @Success   200   {object}  response.Response{msg=string}  "修改基础api"
// @Router    /api/updateApi [post]
func (s *GPTApiApi) UpdateApi(c *gin.Context) {
	var api system.SysApi
	err := c.ShouldBindJSON(&api)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = utils.Verify(api, utils.ApiVerify)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = apiService.UpdateApi(api)
	if err != nil {
		global.GVA_LOG.Error("修改失败!", zap.Error(err))
		response.FailWithMessage("修改失败", c)
		return
	}
	response.OkWithMessage("修改成功", c)
}

// GetAllApis
// @Tags      SysApi
// @Summary   获取所有的Api 不分页
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Success   200  {object}  response.Response{data=systemRes.SysAPIListResponse,msg=string}  "获取所有的Api 不分页,返回包括api列表"
// @Router    /api/getAllApis [post]
func (s *GPTApiApi) GetAllApis(c *gin.Context) {
	apis, err := apiService.GetAllApis()
	if err != nil {
		global.GVA_LOG.Error("获取失败!", zap.Error(err))
		response.FailWithMessage("获取失败", c)
		return
	}
	response.OkWithDetailed(systemRes.SysAPIListResponse{Apis: apis}, "获取成功", c)
}
func WrapperProxy(targeturl string, c *gin.Context) {

	target, _ := url.Parse(targeturl)

	director := func(req *http.Request) {
		req.Method = c.Request.Method
		//req.Body = c.Request.Body
		//req.Form = c.Request.Form
		req.URL = target
		req.Host = target.Host // 必须显示修改Host，否则转发可能失败
		req.URL.Path = target.Path
		req.Header = c.Request.Header

		if c.Request.Header.Get("Content-Type") == "multipart/form-data" {
			// 将文件编码为multipart/form-data格式，并将其包含在请求体中
			if c.Request.Method == http.MethodPost {
				file, header, err := c.Request.FormFile("file")
				if err != nil {
					log.Println("failed to get form file:", err)
					http.Error(c.Writer, "failed to get form file", http.StatusBadRequest)
					return
				}
				defer file.Close()

				body := &bytes.Buffer{}
				writer := multipart.NewWriter(body)

				part, err := writer.CreateFormFile("file", header.Filename)
				if err != nil {
					log.Println("failed to create form file:", err)
					http.Error(c.Writer, "failed to create form file", http.StatusBadRequest)
					return
				}

				if _, err := io.Copy(part, file); err != nil {
					log.Println("failed to copy file data:", err)
					http.Error(c.Writer, "failed to copy file data", http.StatusInternalServerError)
					return
				}

				contentType := writer.FormDataContentType()
				if err := writer.Close(); err != nil {
					log.Println("failed to close multipart writer:", err)
					http.Error(c.Writer, "failed to close multipart writer", http.StatusInternalServerError)
					return
				}

				req.Body = ioutil.NopCloser(body)
				req.Header.Set("Content-Type", contentType)
				req.ContentLength = int64(body.Len())
			} else {
				req.Header = c.Request.Header
			}
		} else {
			req.Body = c.Request.Body
		}

	}
	transport := &http.Transport{
		Proxy: http.ProxyFromEnvironment,
		DialContext: (&net.Dialer{
			Timeout:   9000 * time.Second, // 设置超时时间
			KeepAlive: 9000 * time.Second,
			DualStack: true,
		}).DialContext,
		MaxIdleConns:          9000,
		IdleConnTimeout:       9000 * time.Second,
		TLSHandshakeTimeout:   9000 * time.Second,
		ExpectContinueTimeout: 1 * time.Second,
	}

	client := &http.Client{
		Timeout:   time.Second * 9000, // 设置超时时间
		Transport: transport,
	}
	modifyResponse := func(resp *http.Response) error {
		log.Println("resp status:", resp.Status)
		log.Println("resp headers:")
		for hk, hv := range resp.Header {
			log.Println(hk, ":", strings.Join(hv, ","))
		}
		cont, _ := ioutil.ReadAll(resp.Body)
		resp.Body = ioutil.NopCloser(bytes.NewReader(cont))
		return nil
	}

	errorHandler := func(w http.ResponseWriter, r *http.Request, err error) {
		if err != nil {
			log.Println("ErrorHandler catch err:", err)

			w.WriteHeader(http.StatusBadGateway)
			_, _ = fmt.Fprintf(w, err.Error())
		}
	}

	proxy := &httputil.ReverseProxy{Director: director, Transport: client.Transport, ModifyResponse: modifyResponse, ErrorHandler: errorHandler}
	proxy.ServeHTTP(c.Writer, c.Request)

}

func (s *GPTApiApi) Tokenlizer(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/tokenlizer"
	WrapperProxy(url, c)
}

func (s *GPTApiApi) Tokenlizer_role(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/tokenlizer_role"
	WrapperProxy(url, c)
}

func (s *GPTApiApi) Memerychat_raw(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/memerychat_raw"
	WrapperProxy(url, c)
}
func (s *GPTApiApi) DelCorpusIds(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/delcorpusIds"
	WrapperProxy(url, c)
}

func (s *GPTApiApi) DelCorpus(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/delcorpus"
	WrapperProxy(url, c)
}

func (s *GPTApiApi) AddCorpus(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/addcorpus"
	WrapperProxy(url, c)
}

func (s *GPTApiApi) GetCorpusList(c *gin.Context) {
	url := "http://127.0.0.1:18883/api/v1/getcorpuslist"
	WrapperProxy(url, c)
}
func (s *GPTApiApi) QuerySimilarity(c *gin.Context) {
	//response.OkWithMessage("sss", c)
	url1 := "http://127.0.0.1:18883/api/v1/querysimilarity"
	WrapperProxy(url1, c)
	return
	//response.OkWithMessage("xxx", c)
	client := &http.Client{}

	//key, _ := beego.AppConfig.String("TX_LOCATION_KEY")
	//url := fmt.Sprintf("https://apis.map.qq.com/ws/location/v1/ip?ip=%s&key=%s", ipaddr, key)
	url := fmt.Sprintf("http://127.0.0.1:18883/api/v1/querysimilarity")

	// 构建 请求 url
	//UrlAddress = fmt.Sprintf("%s&timestamp=%d&sign=%s", UrlAddress, timeStampNow, urlEncode)

	//var dd []byte
	//c.Request.Body.Read(dd)
	var bodyBytes []byte // 我们需要的body内容

	// 从原有Request.Body读取
	bodyBytes, err := ioutil.ReadAll(c.Request.Body)
	//if err != nil {
	//	return 0, nil, fmt.Errorf("Invalid request body")
	//}
	// 构建 请求体
	request, _ := http.NewRequest("POST", url, strings.NewReader(string(bodyBytes)))

	// 设置库端口

	// 请求头添加内容
	request.Header.Set("Content-Type", "application/json")

	// 发送请求
	response1, err := client.Do(request)
	if err != nil {
		//logs.Error("发送请求失败")
		return
	}
	fmt.Println("response: ", response1)

	// 关闭 读取 reader
	defer response1.Body.Close()

	// 读取内容
	//all, _ := ioutil.ReadAll(response1.Body)
	//fmt.Println("all: ", string(all))
	//cont, _ := ioutil.ReadAll(resp.Body)
	//c.Request.Response.Body = ioutil.NopCloser(bytes.NewReader(all))

	response.OkWithData(gin.H{"name": "xiaoming"}, c)
}
func (s *GPTApiApi) TestRole(c *gin.Context) {
	//response.OkWithMessage("xxx", c)
	client := &http.Client{}

	//key, _ := beego.AppConfig.String("TX_LOCATION_KEY")
	//url := fmt.Sprintf("https://apis.map.qq.com/ws/location/v1/ip?ip=%s&key=%s", ipaddr, key)
	url := fmt.Sprintf("http://127.0.0.1:18883/api/v1/testrole")

	// 构建 请求 url
	//UrlAddress = fmt.Sprintf("%s&timestamp=%d&sign=%s", UrlAddress, timeStampNow, urlEncode)

	//var dd []byte
	//c.Request.Body.Read(dd)
	var bodyBytes []byte // 我们需要的body内容

	// 从原有Request.Body读取
	bodyBytes, err := ioutil.ReadAll(c.Request.Body)
	//if err != nil {
	//	return 0, nil, fmt.Errorf("Invalid request body")
	//}
	// 构建 请求体
	request, _ := http.NewRequest("POST", url, strings.NewReader(string(bodyBytes)))

	// 设置库端口

	// 请求头添加内容
	request.Header.Set("Content-Type", "application/json")

	// 发送请求
	response, err := client.Do(request)
	if err != nil {
		//logs.Error("发送请求失败")
		return
	}
	fmt.Println("response: ", response)

	// 关闭 读取 reader
	defer response.Body.Close()

	// 读取内容
	all, _ := ioutil.ReadAll(response.Body)
	fmt.Println("all: ", string(all))

}

// DeleteApisByIds
// @Tags      SysApi
// @Summary   删除选中Api
// @Security  ApiKeyAuth
// @accept    application/json
// @Produce   application/json
// @Param     data  body      request.IdsReq                 true  "ID"
// @Success   200   {object}  response.Response{msg=string}  "删除选中Api"
// @Router    /api/deleteApisByIds [delete]
func (s *GPTApiApi) DeleteApisByIds(c *gin.Context) {
	var ids request.IdsReq
	err := c.ShouldBindJSON(&ids)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	err = apiService.DeleteApisByIds(ids)
	if err != nil {
		global.GVA_LOG.Error("删除失败!", zap.Error(err))
		response.FailWithMessage("删除失败", c)
		return
	}
	response.OkWithMessage("删除成功", c)
}
