from fastapi import APIRouter, Depends, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
import uuid
import time
import hashlib
import json
import random
# import shortuuid
from typing import Optional
from pydantic import BaseModel


router = APIRouter()
RECORDS = 50
# 获取租户ID下所有的云主机(详细)
@router.get('/v2.1/{tenant_id}/servers/detail')
def vhosts_detail(*, tenant_id: str):
    hosts = []
    host_status = "ACTIVE, BUILD,DELETED,ERROR,HARD_REBOOT,MIGRATING,REBOOT,RESIZE,REVERT_RESIZE,SHELVED,SHELVED_OFFLOADED,SHUTOFF,UNKNOWN,VERIFY_RESIZE".split(",")
    for i in range(10, RECORDS):
        id = f"b3a7db10-38c8-407c-9ee9-8f4d078f3c{i}"
        host = {
            "addresses" : {
            f"68269e6e-4a27-441b-8029-35373ad50b{i}" : [ {
                "addr" : f"192.168.0.{i}",
                "version" : 4,
                "OS-EXT-IPS-MAC:mac_addr":f"a111:b111:c111:dd{i}",
                "OS-EXT-IPS:type":"dhcp"
            }]
            },
            "created" : "2012-09-07T16:56:37Z",
            "flavor" : {
            "id" : f"{i}",
            "links" : [ {
                "href" : f"http://openstack.example.com/openstack/flavors/{i}",
                "rel" : "bookmark"
            } ]
            },
            "hostId" : "16d193736a5cfdb60c697ca27ad071d6126fa13baeb670fc9d10645e",
            "host_status": "OK",
            "id" : id,
            "image" : {
                    "id" : f"17a1890b-0fa4-485e-8505-14e2940179{i}"
                    },
            "links" : [ {
            "href" : f"http://openstack.example.com/v2/openstack/servers/{id}",
            "rel" : "self"
            }, {
            "href" : f"http://openstack.example.com/openstack/servers/{id}",
            "rel" : "bookmark"
            } ],
            "metadata" : { },
            "security_groups":[{"name":f"sec_{i}"}],
            "name" : f"new-server-test{i}",
            "description": "description",
            "progress" : 100 if i * 5 > 100 else i *5 ,
            "status" : host_status[i % len(host_status)],
            "tenant_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{i}",
            "updated" : "2012-09-07T16:56:37Z",
            "user_id" : "fake",
            "os-extended-volumes:volumes_attached": [{
                "id": f"b104b8db-170d-441b-897a-3c8ba9c5a2{i}",
                "delete_on_termination": "false",
            }],
            "key_name": "SSH密钥名称",
            "config_drive": "云服务器是否使用配置磁盘",
            "OS-DCF:diskConfig":"AUTO",
            "OS-EXT-AZ:availability_zone":"xxxxxx", #
            "OS-EXT-SRV-ATTR:host":"云服务器宿主名称",
            "OS-EXT-SRV-ATTR:hostname":"云服务器hostname",
            "OS-EXT-SRV-ATTR:hypervisor_hostname":"hypervisor主机名。",
            "OS-EXT-SRV-ATTR:instance_name":"云服务器实例ID",
            "OS-EXT-SRV-ATTR:root_device_name":"/dev/sda1", # 云服务器系统盘盘符。
            "OS-EXT-SRV-ATTR:user_data":"云服务器用户数据信息",
            "OS-EXT-STS:task_state":"云服务器任务状",
            "OS-EXT-STS:power_state":"云服务器电源状态",
            "OS-EXT-STS:vm_state":"云服务器状态",
            "OS-SRV-USG:launched_at":"2012-09-09T12:56:37Z", # 云服务器启动时间
            "OS-SRV-USG:terminated_at": "",
            "OS-EXT-SRV-ATTR:reservation_id": "xxxxxxxxxxxx", # 虚拟机预留ID，批量创建虚拟机时可以用来识别虚拟机。
            "OS-EXT-SRV-ATTR:launch_index": "1" #批量创建虚拟机时，虚拟机的创建顺序。
        }
        hosts.append(host)
    data = {"servers" : hosts}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@router.post('/v2.1/{tenant_id}/servers/{host_id}/action')
def ecs_action(tenant_id:str, host_id:str):
    # payload = Body(..., embed=True)
    # if payload and payload.get('os-getVNCConsole'):
    #     pass
    # elif payload and payload.get('asd'):
    #     pass
    data = {"console" : {
        "type": "novnc",
        "url": "https://www.baidu.com"
    }}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


# 获取租户ID下所有的云主机(详细)
@router.get('/v2.1/{tenant_id}/servers')
def vhosts_simple(*, tenant_id: str):
    hosts = []
    for i in range(10,RECORDS):
        id = f"b3a7db10-38c8-407c-9ee9-8f4d078f3c{i}"
        host = {
                "id" : id,
                "links" : [ {
                "href" : f"https://compute.localdomain.com:8001/v2.1/servers/{id}",
                "rel" : "self"
                }, {
                "href" : "https://compute.localdomain.com:8001/servers/{id}",
                "rel" : "bookmark"
                } ],
                "name" : f"fake{i}"
        }
        hosts.append(host)
    data = {"servers" :hosts}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/v2.1/{tenant_id}/flavors')
def flavors_simple(*,tenant_id:str):
    flavors = []
    for i in range(10,RECORDS):
        flavor = {
            "id" : f"{i}",
            "links" : [ {
            "href" : f"http://192.168.82.222:8774/v2/9c53a566cb3443ab910cf0daebca90c4/flavors/{i}",
            "rel" : "self"
            }, {
            "href" : f"http://192.168.82.222:8774/9c53a566cb3443ab910cf0daebca90c4/flavors/{i}",
            "rel" : "bookmark"
            } ],
            "name" : f"m{i}.large"
        }
        flavors.append(flavor)
    data = {  "flavors" : flavors}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/v2/{tenant_id}/os-availability-zone')
def availability_zone_list(*,tenant_id:str):
    availabilityZoneInfo = []
    for i in range(1,4):
        az = {
			"zoneState": {
				"available": True
			},
			"zoneName": f"az{i}.dc{i}"
		}
        availabilityZoneInfo.append(az)
    data = {  "availabilityZoneInfo" : availabilityZoneInfo}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/v2.1/{tenant_id}/flavors/detail')
def flavors_simple(*,tenant_id:str):
    flavors = []
    for i in range(10,RECORDS):
        flavor = mock_flavor(str(i))
        flavors.append(flavor)
    data = {  "flavors" : flavors}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)
# v2/{rpoject_id}/flavors/{flavors_id}
@router.get('/v2/{tenant_id}/flavors/{flavors_id}')
def flavors_simple(*,tenant_id:str,flavors_id:str):
    flavor = mock_flavor(flavors_id)
    data = {  "flavor" : flavor}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v2/{tenant_id}/volumes/detail
@router.get('/v2/{tenant_id}/volumes/detail')
def volumes_detail_list(*,tenant_id:str):
    volumes = []
    for i in range(10,RECORDS):
        volume = mock_volumes(str(i))
        volumes.append(volume)
    data = {  "volumes" : volumes,"volumes_links":[]}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v2/{tenant_id}/snapshots/detail
@router.get('/v2/{tenant_id}/snapshots/detail')
def snapshots_detail_list(*, tenant_id: str):
    snapshots = []
    for i in range(10,RECORDS):
        snapshot = mock_snapshot(i)
        snapshots.append(snapshot)
    data = {"snapshots" : snapshots}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v1/{tenant_id}/security-groups
@router.get('/v2.0/security-groups')
def security_groups_list():
    groups = []
    for i in range(10,RECORDS):
        group = mock_security_groups(i)
        groups.append(group)
    data = {"security_groups" : groups}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v2/cloudimages
@router.get('/v2/cloudimages')
def iamge_list():
    images = []
    for i in range(10,RECORDS):
        iamge = mock_image(i)
        images.append(iamge)
    data = {"images" : images}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

#GET /v2/images/{image_id}
@router.get('/v2/images/{image_id}')
def image_detail(*,image_id:str):
    id = image_id[-2:]
    return mock_image(id)

@router.post('/v3/auth/tokens')
def get_token():
    data = { 
            "token" : { 
                "methods" : ["password"], 
                "expires_at" : "2015-11-09T01:42:57.527363Z", 
                "issued_at" : "2015-11-09T00:42:57.527404Z", 
                "user" : { 
                    "domain" : { 
                        "id" : "ded485def148s4e7d2se41d5se...", 
                        "name" : "domain A" 
                    }, 
                    "id" : "ee4dfb6e5540447cb37419051...", 
                    "name" : "user A", 
                    "password_expires_at":"2016-11-06T15:32:17.000000", 
                }, 
                "domain" : { 
                    "name" : "domain A", 
                    "id" : "dod4ed5e8d4e8d2e8e8d5d2d..." 
                }, 
                "catalog": [{ 
                    "type": "identity", 
                    "id": "1331e5cff2a74d76b03da12259...", 
                    "name": "iam", 
                    "endpoints": [{ 
                        "url": "www.example.com/v3", 
                        "region": "*", 
                        "region_id": "*", 
                    "interface": "public", 
                        "id": "089d4a381d574308a703122d3a..." 
                }] 
                }],  
                "roles" : [{ 
                    "name" : "role1", 
                    "id" : "roleid1" 
                    }, { 
                    "name" : "role2", 
                    "id" : "roleid2" 
                    } 
                ],
                "project" : {
                    "id": '666666677777777777'
                } 
            } 
            }

    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_201_CREATED)

@router.put('/rest/plat/smapp/v1/oauth/token')
def get_monitor_token():
    data = { 
            "accessSession": "x-urhd5eo79jvvc9ddsbhcurinthfvvt442ldjpcnyup44vv1irshi7silph7z5h3ysbk7im9jfzo5o7gafwqntfbuhdqn85tcg7bvru2l6p9ielk63so9ipmnemdffv3t",
            "roaRand": "2ce2d56bcb4ead59bb11b4b2dd1a9052bdc379a17a408547",
            "expires": 1800,
            "additionalInfo": None 
            }

    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_201_CREATED)

@router.get('/v3/auth/projects')
def get_projects():
    data = {
        "projects": [
            {
                "id": "b3a7db10-38c8-407c-9ee9-8f4d078f3p11",
                "name": "SC_PROJECT_11",
                "domain_id": "b3a7db10-38c8-407c-9ee9-8f4d078f3d1",
                "description": "test1",
                "enabled": True,
                "parent_id":"b3a7db10-38c8-407c-9ee9-8f4d078f3p0",
                "id_domain": False,
                "links": {
                    "self":"http://www.1111.222.com"
                }
            },
            {
                "id": "b3a7db10-38c8-407c-9ee9-8f4d078f3p12",
                "name": "SC_PROJECT_12",
                "domain_id": "b3a7db10-38c8-407c-9ee9-8f4d078f3d2",
                "description": "test2",
                "enabled": True,
                "parent_id":"b3a7db10-38c8-407c-9ee9-8f4d078f3p0",
                "id_domain": False,
                "links": {
                    "self":"http://www.1111.222.com"
                }
            },
            {
                "id": "b3a7db10-38c8-407c-9ee9-8f4d078f3p13",
                "name": "SC_PROJECT_13",
                "domain_id": "b3a7db10-38c8-407c-9ee9-8f4d078f3d3",
                "description": "test3",
                "enabled": True,
                "parent_id":"b3a7db10-38c8-407c-9ee9-8f4d078f3p0",
                "id_domain": False,
                "links": {
                    "self":"http://www.1111.222.com"
                }
            },
            {
                "id": "b3a7db10-38c8-407c-9ee9-8f4d078f3p14",
                "name": "SC_PROJECT_14",
                "domain_id": "b3a7db10-38c8-407c-9ee9-8f4d078f3d4",
                "description": "test4",
                "enabled": False,
                "parent_id":"b3a7db10-38c8-407c-9ee9-8f4d078f3p0",
                "id_domain": True,
                "links": {
                    "self":"http://www.1111.222.com"
                }
            },
            {
                "id": "666666677777777777",
                "name": "SC_PROJECT_15",
                "domain_id": "b3a7db10-38c8-407c-9ee9-8f4d078f3d15",
                "description": "test5",
                "enabled": True,
                "parent_id":"b3a7db10-38c8-407c-9ee9-8f4d078f3p0",
                "id_domain": False,
                "links": {
                    "self":"http://www.1111.222.com"
                }
        
            }
        ]
    }
    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_201_CREATED)

@router.post('/v2/{tenant_id}/volumes')
def create_volumes(*, tenant_id: str):
    # b104b8db-170d-441b-897a-3c8ba9c5a2{id}
    payload = Body(..., embed=True)
    if payload:
        pass
    data = {
        "volume" : {
            "status" : "creating",
            "user_id" : "9c158a8fa85b47cfa820e25fab9af47b",
            "attachments" : [ ],
            "links" : [ {
            "href" : "http://172.30.101.201:8776/v2/3dab0aaf682849678a94ec7b5a3af2ce/volumes/70b14513-faad-4646-b7ab-a065cef282b4",
            "rel" : "self"
            }, {
            "href" : "http://172.30.101.201:8776/3dab0aaf682849678a94ec7b5a3af2ce/volumes/70b14513-faad-4646-b7ab-a065cef282b4",
            "rel" : "bookmark"
            } ],
            "availability_zone" : "nova",
            "bootable" : "false",
            "encrypted" : False,
            "created_at" : "2014-12-18T15:57:56.299000",
            "description" : '',
            "volume_type" : '',
            "name" : "test",
            "replication_status" : "disabled",
            "consistencygroup_id" : '',
            "source_volid" : '',
            "snapshot_id" : '',
            "shareable" : False,
            "metadata" : { },
            "id" : "b104b8db-170d-441b-897a-3c8ba9c5a211",
            "size" : 10,
            "multiattach" : False
        }

    }
    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_202_ACCEPTED)
# class CreateVMItem(BaseModel):
#     name: str
#     desc: Optional[str] = None
#     price: float

@router.post('/v2.1/{tenant_id}/servers')
def create_VM(*, tenant_id: str):
    data = {
            "server" : {
                "security_groups" : [ {
                "name" : "name_xx5_sg"
                } ],
                "OS-DCF:diskConfig" : " MANUAL",
                "id" : "b3a7db10-38c8-407c-9ee9-8f4d078f3c14",
                "links" : [ {
                "href" : "http://192.168.82.230:8774/v2/dc4059e8e7994f2498b514ca04cdaf44/servers/567c1557-0eca-422c-bfce-149d6b8f1bb8",
                "rel" : "self"
                }, {
                "href" : "http://192.168.82.230:8774/dc4059e8e7994f2498b514ca04cdaf44/servers/567c1557-0eca-422c-bfce-149d6b8f1bb8",
                "rel" : "bookmark"
                } ],
                "adminPass" : "name_xx1"
            }
        }
    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_202_ACCEPTED)

@router.get('/v2.1/{tenant_id}/servers/{server_id}/os-volume_attachments')
def get_volume_attachments(*, tenant_id:str, server_id:str ):
    attachs = []
    for i in range(10,RECORDS):
        attach = mock_volume_attachments(i)
        attachs.append(attach)
    data = {  "volumeAttachments" : attachs}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/v2.0/networks')
def get_networks():
    networks = []
    for i in range(10,100):
        network = mock_networks(i)
        networks.append(network)
    data = {  "networks" : networks}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/{code}/openid')
def get_openid(*, code:str):
    GetOpenId = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&grant_type=authorization_code&js_code={code}"
    url = GetOpenId.format(appid="wx62cbda4346701cd6",secret="b6bd0c5a14ac076669c93cf647314950",code=code)
    res = requests.get(url)
    print(res)
    data = '{ "success":false }'
    print(res.json())
    if res.status_code == 200:
        data = res.text
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

@router.get('/{code}/openid2')
def get_openid(*, code:str):
    GetOpenId ='https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
    url = GetOpenId.format(appid="wx40656143d5db06f9",secret="7aa48615c82e3002929dd517660c60ad",code=code)
    res = requests.get(url)
    print(res)
    data = '{ "success":false }'
    print(res.json())
    access_token=''
    openid=''
    if res.status_code == 200:
        resultStr = res.text
        dict_var2 = json.loads(resultStr)
        access_token = dict_var2['access_token']
        openid = dict_var2['openid']
    userinfoUrl = 'https://api.weixin.qq.com/sns/userinfo?access_token={token}&openid={openid}&lang=zh_CN'
    url = userinfoUrl.format(token=access_token,openid=openid)
    data = {
        "access_token":access_token,
        "openid": openid
    }
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


class MonitorItem(BaseModel):
    obj_type_id: str
    indicator_ids: list
    range: str
    begin_time: str
    end_time: str
    obj_ids: list

@router.post('/rest/performance/v1/data-svc/history-data/action/query')
def get_monitor_disk(data: MonitorItem):
    redata = {
        "data": {
            
        }
    }
    for resource in data.obj_ids:
        redata["data"][resource] = {}
        for indicator in data.indicator_ids:
            avg = random.uniform(0,80)
            redata["data"][resource][indicator] = {"avg":{data.begin_time:"{:.2f}".format(avg)}}
            #avg = {resource:{indicator:{data.begin_time:"5.72"}}}
            #redata["data"] = avg
    return JSONResponse(content=jsonable_encoder(redata), status_code=status.HTTP_200_OK)

@router.get('/goods/wx/wx_jsapi_ticket')
def wx_jsapi_ticket(*, url: str = ""):
    APPID = "wx40656143d5db06f9"
    SECRET = "7aa48615c82e3002929dd517660c60ad"
    AccessTokenUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    requestUrl = AccessTokenUrl.format(APPID=APPID,SECRET=SECRET)
    res = requests.get(requestUrl)
    # print(res)
    access_token=""
    if res.status_code == 200:
        resultStr = res.text
        dict_var2 = json.loads(resultStr)
        access_token = dict_var2['access_token']
        
    
    AccessTokenUrl = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={ACCESS_TOKEN}&type=jsapi"
    requestUrl = AccessTokenUrl.format(ACCESS_TOKEN=access_token)
    res = requests.get(requestUrl)
    # print(res)
    ticket = ""
    errcode = ""
    errmsg = ""
    expires_in = ""
    if res.status_code == 200:
        resultStr = res.text
        dict_var2 = json.loads(resultStr)
        ticket = dict_var2['ticket']
        errcode = dict_var2['errcode']
        errmsg = dict_var2['errmsg']
        expires_in = dict_var2['expires_in']
    print("ticket:{},errcode:{},errmsg:{},expires_in:{}".format(ticket,errcode,errmsg,expires_in))

    noncestr = '111111111111' # this.randomUUID();//随机字符串
    timestamp = time.time() # String.valueOf(System.currentTimeMillis());//时间戳

    str = "jsapi_ticket={}&noncestr={}&timestamp={}&url={}".format(ticket,noncestr,timestamp,url)
    print(str)
    # 6、将字符串进行sha1加密
    # hashlib.sha1(str.encode("utf-8")).hexdigest()
    signature = hashlib.sha1(str.encode('utf-8')).hexdigest()
    data = {
        "signature": signature,
        "noncestr": noncestr,
        "timestamp": timestamp,
        "appId": APPID,
        "ticket": ticket
    }
    print(data)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

def mock_image(id):
    #
 
    #镜像状态。取值如下：queued：表示镜像元数据已经创建成功，等待上传镜像文件。saving：表示镜像正在上传文件到后端存储。deleted：表示镜像已经删除。killed：表示镜像上传错误。active：表示镜像可以正常使用。
 
    image = {
            "id" : f"17a1890b-0fa4-485e-8505-14e2940179{id}",
            "status" : "active",
            "updated_at" : "2015-12-27T02:52:25Z",
            "name" : f"cirror{id}",
            "architecture":"x86_64",#镜像CPU架构类型，取值为x86_64或aarch64。
            "file":"",#镜像文件下载和上传链接。
            "tags":{},#镜像标签列表。
            "created_at" : "2015-12-27T02:52:24Z",
            "visibility":"public",#是否被其他租户可见，取值为public或private。
            "owner" : "zhangsan", #镜像属于哪个租户。
            "size":"",#目前暂时不使用。
            "schema":"镜像视图",
            "checksum":"",#目前暂时不使用。
            "protected":True,#是否是受保护的，受保护的镜像不允许删除。取值为true或false。
            "container_format":"",#容器类型
            "min_ram":1024,#镜像运行需要的最小内存，单位为MB。参数取值依据弹性云服务器的 规格限制，默认设置为0。
            "updated_at":"2016-12-27T02:52:24Z",
            "__os_version":"CentOS 4.4 32bit",#操作系统版本。使用上传至OBS桶中的外部镜像文件制作镜像时生效，具体取值见相关参数取值列表。
            "__os_bit":"32", #操作系统位数，一般取值为“32”或者“64”。
            "__description":"镜像描述信息。",
            "disk_format":"vhd", #镜像的格式，目前支持vhd，zvhd、raw，qcow2。默认值是vhd。
            "__isregistered": "true", #是否是注册过的镜像，取值为“true”或者“false”。
            "__platform":"Ubuntu", #镜像平台分类，取值为Windows，Ubuntu，RedHat，SUSE，CentOS，Debian，OpenSUSE, Oracle Linux，Fedora，Other，CoreOS和EulerOS。
            "__os_type" : "Linux",
            "min_disk":100,#GB
            "virtual_env_type":"FusionCompute", #镜像使用环境类型：FusionCompute，Ironic，DataImage。如果弹性云服务器镜像，则取值为FusionCompute，如果是数据卷镜像则取值是DataImage，如果是裸金属服务器镜像，则取值是Ironic。
            "__image_source_type": "镜像后端存储类型，目前只支持uds",
            "__imagetype":"gold", #镜像类型，目前支持：公共镜像（gold）,私有镜像（private）,共享镜像（shared）。
            "created_at":"2015-12-27T02:52:24Z",
            "virtual_size":0, #目前暂时不使用。
            "deleted_at":"",
            "__originalimagename":"",#父镜像ID。公共镜像或通过文件创建的私有镜像，取值为空。
            "__backup_id":"" ,#备份ID。如果是备份创建的镜像，则填写为备份的ID，否则为空。
            "__productcode":"1111-1111-1111",#市场镜像的产品ID。
            "__image_size":"1231231" ,#镜像文件的大小，单位为字节。必须大于0。
            "__data_origin":"",#"镜像来源。公共镜像为空。" ,
            "__is_config_init":"true", #是否完成了初始化配置
            "__sequence_num":"3123123",#序列号信息。
            "__support_kvm": "",#如果镜像支持KVM，取值为true，否则无需增加该属性。
            "__support_xen":"",#如果镜像支持XEN，取值为true，否则无需增加该属性。
            "__support_largememory":"",#表示该镜像支持超大内存。如果镜像支持超大内存，取值为true，否则无需增加该属性。
            "__support_diskintensive":"",#表示该镜像支持密集存储。如果镜像支持密集存储性能，则值为true，否则无需增加该属性。
            "__support_highperformance":"",#表示该镜像支持高计算性能。如果镜像支持高计算性能，则值为true，否则无需增加该属性。
            "__support_kvm_gpu_type":"",#表示该镜像是支持KVM虚拟化平台下的GPU类型，如果不支持KVM虚拟机下GPU类型，无需添加该属性。该属性与“__support_xen”和“__support_kvm”属性不共存。
            "__support_xen_hana":"",#如果镜像支持XEN虚拟化下HANA类型，取值为true。否则，无需添加该属性。该属性与“__support_xen”和__support_kvm属性不共存。
            "__support_kvm_infiniband":""#如果镜像支持KVM虚拟化下Infiniband网卡类型，取值为true。否则，无需添加该属性。该属性与“__suport_xen”属性不共存。
 

    }
    return image

def mock_flavor(flavors_id:str):
    flavor = {
            "id" : flavors_id,
            "name" : f"m{flavors_id}.large",
            "vcpus" : (int(flavors_id) % 2) + 2 ,
            "ram" : 8192 * (int(flavors_id) % 5 + 1),
            "disk" : 20 * (int(flavors_id) % 3 + 1),
            "swap" : "",
            "links" : [ {
            "rel" : "self",
            "href" : f"https://compute.Region.dc1.domainname.com/v2/a1d8bff5d3d240adab0665cf6843c770/flavors/{flavors_id}"
            }, {
            "rel" : "bookmark",
            "href" : f"https://compute.Region.dc1.domainname.com/a1d8bff5d3d240adab0665cf6843c770/flavors/{flavors_id}"
            } ],
            "OS-FLV-EXT-DATA:ephemeral" : 0,
            "rxtx_factor" : None,
            "OS-FLV-DISABLED:disabled" : None,
            "rxtx_quota" : None,
            "rxtx_cap" : None,
            "os-flavor-access:is_public" : None
        }
    return flavor

# 模拟返回云硬盘详细信息
def mock_volumes(id:int):
    vol_id = f"b104b8db-170d-441b-897a-3c8ba9c5a2{id}"
    volume = {
        "attachments" : [ ],
        "availability_zone" : "xxx",
        "bootable" : "false",
        "consistencygroup_id" : None,
        "created_at" : "2016-05-25T02:42:10.856332",
        "description" : None,
        "encrypted" : False,
        "id" : f"b104b8db-170d-441b-897a-3c8ba9c5a2{id}",
        "links" : [ {
        "href" : f"https://volume.localdomain.com:8776/v2/dd14c6ac581f40059e27f5320b60bf2f/volumes/{vol_id}",
        "rel" : "self"
        }, {
        "href" : f"https://volume.localdomain.com:8776/dd14c6ac581f40059e27f5320b60bf2f/volumes/{vol_id}",
        "rel" : "bookmark"
        } ],
        "metadata" : {
        "__openstack_region_name" : "pod01.xxx",
        "a" : "b",
        "quantityGB" : "1",
        "volInfoUrl" : "fusionstorage://172.30.64.10/0/FEFEEB07D3924CDEA93C612D4E16882D"
        },
        "name" : f"zjb_u25_test_{id}",
        "os-vol-host-attr:host" : "pod01.xxx#SATA",
        "volume_image_metadata" : { },
        "os-vol-mig-status-attr:migstat" : None,
        "os-vol-mig-status-attr:name_id" : None,
        "os-vol-tenant-attr:tenant_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
        "os-volume-replication:driver_data" : None,
        "os-volume-replication:extended_status" : None,
        "replication_status" : "disabled",
        "shareable" : False,
        "multiattach" : False,
        "size" : 1,
        "snapshot_id" : None,
        "source_volid" : None,
        "status" : "available",
        "updated_at" : "2016-05-25T02:42:22.341984",
        "user_id" : "b0524e8342084ef5b74f158f78fc3049",
        "volume_type" : "SATA"
    } 
    return volume

def mock_snapshot(id:int):
    snapshot_id =  f"b1323cda-8e4b-41c1-afc5-2fc791809c{id}",
    vol_id = f"b104b8db-170d-441b-897a-3c8ba9c5a2{id}"
    snapshot = {
        "status" : "available",
        "metadata" : {
        "name" : "test"
        },
        "os-extended-snapshot-attributes:progress" : "100%",
        "name" : f"test-volume-snapshot_{id}",
        "volume_id" : vol_id,
        "os-extended-snapshot-attributes:project_id" : "bab7d5c60cd041a0a36f7c4b6e1dd978",
        "created_at" : "2015-11-29T02:25:51.000000",
        "updated_at" : "2015-11-29T02:26:28.000000",
        "size" : 11,
        "id" : snapshot_id,
        "description" : "volume snapshot"
    } 
    return snapshot

def mock_security_groups(id:int):
    group_id = f"534fcfed-9f7e-4ba6-b251-7ead02184f{id}"
    group = {
        "id" : group_id,
        "name" : f"sec_{id}",
        "vpc_id" : "472b1047-8f40-4bcd-a80c-89bbd561c884",
        "project_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
        "description" : "472b1047-8f40-4bcd-a80c-89bbd561c884",
        "security_group_rules" : [ {
                "direction" : "ingress",
                "ethertype" : "IPv4",
                "id" : f"e36847a0-e469-41cb-8202-324bd19c{id}",
                "remote_group_id" : "07d53c6f-a5c2-4ac4-a7c3-e1df90b7a8f5",
                "security_group_id" : group_id,
                "parent_group_id": "",
                "action" : None,
                "priority" : None,
                "protocol" : "TCP",
                "description" : f"description{id}",
                "remote_ip_prefix" : None,
                "tenant_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
                "port_range_max" : 255,
                "port_range_min" : id,
                "created_at" : "2021-06-27T14:46:10",
                "updated_at" : "2021-06-27T14:46:10",
                "project_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
                }, {
                "direction" : "egress",
                "ethertype" : "IPv4",
                "id" : f"22baf104-85ef-4f75-8f70-50458d433{id}",
                "security_group_id" : group_id,
                "parent_group_id": "",
                "action" : None,
                "priority" : None,
                "protocol" : "UDP",
                "description" : f"description _ {id}",
                "remote_group_id" : "00e1590a-bf3c-443f-b29f-1633b7cd9303",
                "remote_ip_prefix" : None,
                "tenant_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
                "port_range_max" : 3000,
                "port_range_min" : id + 10,
                "created_at" : "2021-06-27T14:46:10",
                "updated_at" : "2021-06-27T14:46:10",
                "project_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
                } ]
    }
    return group
def mock_volume_attachments(id: int):
    host_id = f"b3a7db10-38c8-407c-9ee9-8f4d078f3c{id}"
    vol_id = f"b104b8db-170d-441b-897a-3c8ba9c5a2{id}"
    attach = {
            "device" : "/dev/vda",
            "serverId" : host_id,
            "id" : f"6135be32-3fba-4400-bfb5-35454a2ff8{id}",
            "volumeId" : vol_id
        }
    return attach

def mock_networks(id: int):
    network_id = f"00ed6888-6aee-40c1-90b9-6d1dbcd24d{id}",
    return {
    "id" : network_id,
    "name" : f"vpn_external_network_{id}",
    "status" : "ACTIVE",
    "shared" : True,
    "subnets" : [ "5c1d18c0-2eb7-4ffe-aa50-4afb51f48009" ],
    "description" : "",
    "mtu" : 1500,
    "availability_zone_hints" : [ ],
    "availability_zones" : [ "az1.dc1" ],
    "admin_state_up" : True,
    "tenant_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
    "provider:network_type" : "local",
    "router:external" : True,
    "created_at" : "2019-01-23T06:20:13",
    "updated_at" : "2019-01-23T06:20:13",
    "project_id" : f"b3a7db10-38c8-407c-9ee9-8f4d078f3p{id}",
    "port_security_enabled": True
  }
    
def mock():
    pass