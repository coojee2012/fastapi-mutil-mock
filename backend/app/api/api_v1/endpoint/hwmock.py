from typing import Any
from datetime import timedelta
from sqlalchemy.orm import Session
import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter()
# 获取租户ID下所有的云主机(详细)
@router.get('/v2.1/{tenant_id}/servers/detail')
def vhosts_detail(*, tenant_id: str):
    hosts = []
    host_status = "ACTIVE, BUILD,DELETED,ERROR,HARD_REBOOT,MIGRATING,REBOOT,RESIZE,REVERT_RESIZE,SHELVED,SHELVED_OFFLOADED,SHUTOFF,UNKNOWN,VERIFY_RESIZE".split(",")
    for i in range(10,100):
        id = f"b3a7db10-38c8-407c-9ee9-8f4d078f3c{i}"
        host = {
            "addresses" : {
            f"68269e6e-4a27-441b-8029-35373ad50b{i}" : [ {
                "addr" : f"192.168.0.{i}",
                "version" : 4,
                "mac":f"a111:b111:c111:dd{i}",
                "type":"fixed"
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
            "security_groups":[{"name":f"security_groups_test{i}"}],
            "name" : f"new-server-test{i}",
            "progress" : 100 if i * 5 > 100 else i *5 ,
            "status" : host_status[i % len(host_status)],
            "tenant_id" : "openstack",
            "updated" : "2012-09-07T16:56:37Z",
            "user_id" : "fake"
        }
        hosts.append(host)
    data = {"servers" : hosts}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# 获取租户ID下所有的云主机(详细)
@router.get('/v2.1/{tenant_id}/servers')
def vhosts_simple(*, tenant_id: str):
    hosts = []
    for i in range(10,100):
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
    for i in range(10,100):
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

@router.get('/v2.1/{tenant_id}/flavors/detail')
def flavors_simple(*,tenant_id:str):
    flavors = []
    for i in range(10,100):
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
    for i in range(10,100):
        volume = mock_volumes(str(i))
        volumes.append(volume)
    data = {  "volumes" : volumes,"volumes_links":[]}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v2/{tenant_id}/snapshots/detail
@router.get('/v2/{tenant_id}/snapshots/detail')
def snapshots_detail_list(*, tenant_id: str):
    snapshots = []
    for i in range(10,100):
        snapshot = mock_snapshot(i)
        snapshots.append(snapshot)
    data = {"snapshots" : snapshots}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v1/{tenant_id}/security-groups
@router.get('/v2.0/security-groups')
def security_groups_list():
    groups = []
    for i in range(33,55):
        group = mock_security_groups(i)
        groups.append(group)
    data = {"security_groups" : groups}
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)

# GET /v2/images
@router.get('/v2/images')
def iamge_list():
    images = []
    for i in range(10,99):
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
    data = {"message":"ok"}
    return JSONResponse(
        headers={"X-Subject-Token":"123-123-123-123-123"},
        content=jsonable_encoder(data), 
        status_code=status.HTTP_201_CREATED)

@router.get('/v2.1/{tenant_id}/servers/{server_id}/os-volume_attachments')
def get_volume_attachments(*, tenant_id:str, server_id:str ):
    attachs = []
    for i in range(10,100):
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
        "os-vol-tenant-attr:tenant_id" : "dd14c6ac581f40059e27f5320b60bf2f",
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
        "size" : 1,
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
        "project_id" : "fba0be97e6bc4bb1b34bdc98c6bec946",
        "description" : "472b1047-8f40-4bcd-a80c-89bbd561c884",
        "security_group_rules" : [ {
                "direction" : "ingress",
                "ethertype" : "IPv4",
                "id" : f"e36847a0-e469-41cb-8202-324bd19cd3{id}",
                "remote_group_id" : "07d53c6f-a5c2-4ac4-a7c3-e1df90b7a8f5",
                "security_group_id" : group_id,
                "action" : None,
                "priority" : None,
                "protocol" : None,
                "description" : None,
                "remote_ip_prefix" : None,
                "tenant_id" : "e76643bc71784ce0808e962b8a6c6257",
                "port_range_max" : None,
                "port_range_min" : None,
                "created_at" : "2021-06-27T14:46:10",
                "updated_at" : "2021-06-27T14:46:10",
                "project_id" : "e76643bc71784ce0808e962b8a6c6257"
                }, {
                "direction" : "egress",
                "ethertype" : "IPv4",
                "id" : f"22baf104-85ef-4f75-8f70-50458d433c{id}",
                "security_group_id" : group_id,
                "action" : None,
                "priority" : None,
                "protocol" : None,
                "description" : "",
                "remote_group_id" : "00e1590a-bf3c-443f-b29f-1633b7cd9303",
                "remote_ip_prefix" : None,
                "tenant_id" : "e76643bc71784ce0808e962b8a6c6257",
                "port_range_max" : None,
                "port_range_min" : None,
                "created_at" : "2021-06-27T14:46:10",
                "updated_at" : "2021-06-27T14:46:10",
                "project_id" : "e76643bc71784ce0808e962b8a6c6257"
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
    network_id = f"00ed6888-6aee-40c1-90b9-6d1dbcd24d{i}",
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
    "tenant_id" : "94e05b0bb4cf4ec99a42af4cb4e5b630",
    "provider:network_type" : "local",
    "router:external" : True,
    "created_at" : "2019-01-23T06:20:13",
    "updated_at" : "2019-01-23T06:20:13",
    "project_id" : "94e05b0bb4cf4ec99a42af4cb4e5b630"
  }
    
def mock():
    pass