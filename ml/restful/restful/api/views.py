import json
import os

import boto3
import botocore
import logging
import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from restful.analytics.data_processing import *
from restful.api.serializers import UserSerializer, GroupSerializer

from .models import *

logger = logging.getLogger(__name__)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class WebhookViewSet(APIView):
    """
    Webhook for uploaded file
    """

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        filename = f"{request.GET.get('filename')}.json"

        df = pd.DataFrame.from_records(Cluster.objects.all().values())
        # logger.info(type(df))
        # logger.info(df.info())

        try:
            s3 = boto3.Session(aws_access_key_id=settings.REACT_APP_AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.REACT_APP_AWS_SECRET_ACCESS_KEY).resource("s3")
            downfile = f"restful/analytics/{filename}"
            s3.meta.client.download_file(settings.REACT_APP_S3_BUCKET, filename, downfile)

            # analytics
            # print(f"Processing {downfile} ...")
            # place_visit_df, activity_segment_df = parse_google_takeout_semantic_location_history(downfile)
            #
            # filename1 = downfile.split(".json")[0] + "_place_visit.csv"
            # place_visit_df.to_csv(filename1, index=False)
            # filename2 = downfile.split(".json")[0] + "_activity_segment.csv"
            # activity_segment_df.to_csv(filename2, index=False)
            # print(f"Data exported:\n\t- {filename1}\n\t- {filename2}")
            # print("Data import and processing completed. Program terminated ...")
            #
            # try:
            #     os.remove(downfile)
            # except OSError:
            #     pass

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        # return Response(f"Success. {json.dumps(activity_segment_df[['startLocationlatitudeE7']].to_dict('records'))}")
        return Response(df.to_json(orient='records'))
