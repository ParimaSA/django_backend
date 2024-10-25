from typing import List
import json
from django.shortcuts import get_object_or_404
from ninja import Router

import helpers

from .forms import *
from .models import *
from .schemas import *

router = Router()


@router.get("queue/", response=List[QueueDetailSchema], auth=helpers.api_auth_user_required)
def list_business_queue(request):
    # return Queue.objects.all()
    business = Business.objects.get(user=request.user)
    queue_list = Queue.objects.filter(business=business)
    return queue_list


@router.get("get_entry/{queue_id}", response=List[EntryDetailSchema], auth=helpers.api_auth_user_required)
def list_waiting_entry_in_queue(request, queue_id:int):
    today = timezone.now().date()
    queue = get_object_or_404(Queue, business__user=request.user, pk=queue_id)
    entry = Entry.objects.filter(queue=queue, status='waiting', time_in__date=today).order_by("time_in")
    return entry


@router.post("queue/", response=QueueDetailSchema, auth=helpers.api_auth_user_required)
def create_business_queue(request, data:QueueCreateSchema):
    data_dict = data.dict()
    obj = Queue.objects.create(business=request.user, **data_dict)
    obj.save()
    return obj


@router.put("{entry_id}/", response=QueueDetailSchema, auth=helpers.api_auth_user_required)
def update_queue(request,
    queue_id:int,
    payload:QueueUpdateSchema
    ):
    obj = get_object_or_404(
        Queue,
        id=queue_id,
        user=request.user)
    payload_dict = payload.dict()
    for k,v in payload_dict.items():
        setattr(obj, k, v)
    obj.save()
    return obj


@router.delete("{queue_id}/delete/", response=QueueDetailSchema, auth=helpers.api_auth_user_required)
def delete_queue(request, queue_id:int):
    obj = get_object_or_404(
        Queue,
        id=queue_id,
        user=request.user)
    obj.delete()
    return obj


@router.post("add_customer/", response=EntryDetailSchema, auth=helpers.api_auth_user_required)
def create_customer_entry(request, data:EntryCreateSchema):
    data_dict = data.dict()
    obj = Entry.objects.create(business=request.user, **data_dict)
    obj.save()
    return obj
