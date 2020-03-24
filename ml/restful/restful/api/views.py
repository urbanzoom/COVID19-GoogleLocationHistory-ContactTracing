import logging
import os

import boto3
import botocore
import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from restful.analytics.data_matching import *
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

    def get(self, request, format=None):
        filename = request.GET.get('filename')

        cluster_df = pd.DataFrame.from_records(Cluster.objects.all().values())
        logger.info('Fetched cluster from database.')

        try:
            s3 = boto3.Session(aws_access_key_id=settings.REACT_APP_AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.REACT_APP_AWS_SECRET_ACCESS_KEY).resource("s3")
            downfile = f"restful/analytics/{filename}"
            s3.meta.client.download_file(settings.REACT_APP_S3_BUCKET, filename, downfile)
            logger.info('Downloaded S3 file ...')

            matched_cluster_df = intersections(downfile, cluster_df)
            logger.info('Matching completed.')

            try:
                os.remove(downfile)
            except OSError:
                pass

            s3.Object(settings.REACT_APP_S3_BUCKET, filename).delete()

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('The object does not exist.')
            else:
                raise

        return Response(matched_cluster_df.to_dict(orient='records'))
