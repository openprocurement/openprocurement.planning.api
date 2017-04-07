# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openprocurement.api.events import ErrorDesctiptorEvent


@subscriber(ErrorDesctiptorEvent)
def plan_error_handler(event):
    if 'plan' in event.request.validated:
        event.params['PLAN_REV'] = event.request.validated['plan'].rev
        event.params['PLANID'] = event.request.validated['plan'].planID
