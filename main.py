import datetime
import json
import time
import traceback

import aliyunsdkcore
from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest, DeleteVideoRequest, GetVideoListRequest, \
    DeleteMezzaninesRequest, DeleteStreamRequest, GetVideoInfosRequest, SubmitSnapshotJobRequest

"""  Start transcoding process   """
from aliyunsdkvod.request.v20170321 import SubmitTranscodeJobsRequest


def init_vod_client(accessKeyId, accessKeySecret):
    regionId = 'ap-south-1'
    connectTimeout = 3  # Connection timeout in seconds.
    return AcsClient(accessKeyId, accessKeySecret, regionId, auto_retry=True, max_retry_time=3, timeout=connectTimeout)


def get_play_info(clt, videoId):
    request = GetPlayInfoRequest.GetPlayInfoRequest()
    request.set_accept_format('JSON')
    request.set_VideoId(videoId)
    request.set_AuthTimeout(3600 * 5)
    try:
        response = json.loads(clt.do_action_with_exception(request))
    except aliyunsdkcore.acs_exception.exceptions.ServerException:
        pass
        return False
    return response


def delete_videos(clt):
    request = DeleteVideoRequest.DeleteVideoRequest()
    videoIds = ['233b9b47c62b45b5ac40acb0bd6eaa6b']
    request.set_VideoIds(
        ','.join(videoIds))  # You can delete multiple videos. Separate multiple videos with commas (,).

    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


def get_video_list(clt, page):
    request = GetVideoListRequest.GetVideoListRequest()
    # Take querying the video list in the last 30 days as an example.
    utcNow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    utcMonthAgo = datetime.datetime.utcfromtimestamp(time.time() - 500 * 86400).strftime("%Y-%m-%dT%H:%M:%SZ")
    request.set_StartTime(utcMonthAgo)  # The start time for video creation, in UTC.
    request.set_EndTime(utcNow)  # The end time for video creation, in UTC.
    # request.set_Status('Uploading,Normal,Transcoding')  # The Video Status. Videos in all statuses are queried by default Separate multiple videos with commas (,).
    # request.set_CateId (0) # Filter by category.
    request.set_PageNo(page)
    request.set_PageSize(20)

    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


def delete_mezzanines(clt):
    request = DeleteMezzaninesRequest.DeleteMezzaninesRequest()

    videoIds = ['a03e7aee37c04b2dbbcf65ba0f2aff66']
    request.set_VideoIds(','.join(videoIds))

    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


def delete_stream(clt, videoId, jobIds):
    request = DeleteStreamRequest.DeleteStreamRequest()
    request.set_VideoId(videoId)
    # Specify the IDs of media stream transcoding jobs. Separate multiple job IDs with commas (,). You can query the JobId by using the GetPlayInfo operation.
    # jobIds = ['ee8d02a40e234f52917e8332e8110046','4dc1330059a54cc4a056ef9a7ec4d580','1ce6099d45aa49ea9984ea783e27d906', '71d78e82095f45afb7246899c98254cd']
    request.set_JobIds(','.join(jobIds))
    request.set_accept_format('JSON')

    response = json.loads(clt.do_action_with_exception(request))
    return response


def get_video_infos(clt, video_id):
    request = GetVideoInfosRequest.GetVideoInfosRequest()
    videoIds = [video_id]
    request.set_VideoIds(','.join(videoIds))

    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


def normal_submit_transcode_jobs(clt, videoId):
    request = SubmitTranscodeJobsRequest.SubmitTranscodeJobsRequest()

    # Specify the ID of the video to be transcoded.
    request.set_VideoId(videoId)

    # Specify the transcoding template group.
    request.set_TemplateGroupId('1946a18a488f1509d112202da03385d5')

    """
    # Set optional overriding parameters, such as parameters related to watermark information overriding.
    overrideParams = build_override_params()
    request.set_OverrideParams(json.dumps(overrideParams))
    """

    request.set_accept_format('JSON')
    try:
        response = json.loads(clt.do_action_with_exception(request))
    except aliyunsdkcore.acs_exception.exceptions.ServerException:
        return False
    return response


def submit_snapshot_job(clt, videoId):
    request = SubmitSnapshotJobRequest.SubmitSnapshotJobRequest()

    # The ID of the video for which you want to create a snapshot.
    request.set_VideoId(videoId)

    # The ID of the snapshot template.
    request.set_SnapshotTemplateId('bce6480b56bdfbfc97585895c4660b42')

    # snapshotIf you specify the ID of the snapshot template parameter, the following parameters are ignored:
    # request.set_Count(50L)
    # request.set_SpecifiedOffsetTime(0L)
    # request.set_Interval(1L)
    # request.set_Width(200)
    # request.set_Height(200)

    # Image sprite-related parameters, which are optional.
    # spriteSnapshotConfig = {'CellWidth': 120, 'CellHeight': 68, 'Columns': 3,
    #                         'Lines': 10, 'Padding': 20, 'Margin': 50}
    # Whether to retain the source image after an image sprite is generated.
    # spriteSnapshotConfig['KeepCellPic'] = 'keep'
    # spriteSnapshotConfig['Color'] = 'tomato'
    # request.set_SpriteSnapshotConfig(json.dumps(spriteSnapshotConfig))

    request.set_accept_format('JSON')
    response = json.loads(clt.do_action_with_exception(request))
    return response


if __name__ == '__main__':

    try:
        clt = init_vod_client('key', 'secret key')
        for i in range(300):
            if i>79:
                videos = get_video_list(clt, i + 1)
                videos = dict(videos)
                videos = videos['VideoList']['Video']
                # print(videos)
                for video in videos:
                    res = normal_submit_transcode_jobs(clt, video['VideoId'])
                    if res:
                        print(i, video['Title'], video['VideoId'], '✅')
                    else:
                        pass

                    # time.sleep(1)
                    # playInfo = get_play_info(clt, video['VideoId'])
                    # if playInfo:
                    #     playInfo = dict(playInfo)['PlayInfoList']['PlayInfo']
                    #     job_ids = []
                    #     for play_i in playInfo:
                    #         job_ids.append(play_i['JobId'])
                    #         # print(play_i['JobId'])
                    #     delete_stream(clt, video['VideoId'], job_ids)
                    #     print('✅')
                    #     # print('-----')
                    #     # print(playInfo)
                    # else:
                    #     pass

            # print(json.dumps(videos, ensure_ascii=False, indent=4))
        # playInfo = get_play_info(clt, '792177f7202646319c471b16b91a3629')
        # playInfo = get_video_infos(clt, '4287da9435344a0abfa969a3b20d6225')
        # print(json.dumps(playInfo, ensure_ascii=False, indent=4))
        # delete_mezzanines(clt)

        # delete_stream(clt)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
